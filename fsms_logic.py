import requests
from bs4 import BeautifulSoup
import logging
import sys
import os
from fpdf import FPDF
import textwrap
import re

logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

class FSMSFetcher:
    def __init__(self, cookie_string=None, session_id=None):
        self.session = requests.Session()
        if cookie_string:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Cookie': cookie_string
            })
        self.session_id = session_id
   
    def fetch_job_sheet(self, ticket_id, session_id, log_cb=print):
        url = f"https://intranetapp.ctc-g.com.my/fsms/fs_trx_showjs.pl?encrypted={session_id}&ticket_id={ticket_id}"
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            pre_tag = soup.find('pre')
            if pre_tag:
                return pre_tag.get_text(), response.text
            else:
                log_cb(f"[ERROR] Ticket {ticket_id}: Authentication Failed. Check cookie expiration.")
                return "", response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"[Job Sheet] Failed to load Ticket {ticket_id}: {e}")
            return "", ""

    def fetch_spare_data(self, ticket_id, session_id, log_cb=print):
        url = f"https://intranetapp.ctc-g.com.my/fsms/fs_trx_spare_req_bback.pl?encrypted={session_id}&ticket_id={ticket_id}"
        num_rows = 0
        raw_html = ""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            raw_html = response.text
            soup = BeautifulSoup(raw_html, 'html.parser')
            trs = soup.find_all('tr')
            num_rows = len(trs)
            item_name = ""
            serial_no = ""
            part_no = ""
            if len(trs) > 2:
                row_found = False
                for row_idx in range(2, len(trs)):
                    tds = trs[row_idx].find_all(['td', 'th'])
                    if len(tds) >= 8:
                        first_cell_text = tds[0].get_text(strip=True)
                        if first_cell_text.startswith("1."):
                            item_name = tds[5].get_text(strip=True).replace('\xa0', ' ')
                            serial_no = tds[6].get_text(strip=True).replace('\xa0', ' ')
                            part_no = tds[7].get_text(strip=True).replace('\xa0', ' ')
                            log_cb(f"MATCH FOUND: [Item: {item_name}] [S/N: {serial_no}] [P/N: {part_no}]")
                            row_found = True
                            break
                if not row_found:
                    log_cb(" [FAILSAFE] No row starting with '1.' was found beginning from index 2.")
            else:
                log_cb(f" [FAILSAFE] Only {num_rows} <tr> tags found. Table structure might be missing.")
            
            if not item_name and len(trs) > 2:
                first_target_row = trs[2].get_text(strip=True, separator=' | ')[:150]
                log_cb(f" [FAILSAFE] 'Item Name' empty! Expected row 2: {first_target_row}...")
                if "HP Pro Mini" in raw_html:
                    log_cb(" [FAILSAFE] 'HP Pro Mini' exists. HTML Index layout shifted!")
                else:
                    log_cb(" [FAILSAFE] 'HP Pro Mini' NOT found. Page may be empty or access-denied.")
                debug_file = f"debug_spare_{ticket_id}.html"
                try:
                    with open(debug_file, "w", encoding="utf-8") as f:
                        f.write(raw_html)
                    log_cb(f" [FAILSAFE] Auto-Dumped RAW HTML to '{debug_file}'.")
                except Exception as eval_err:
                    log_cb(f" [FAILSAFE] Could not dump file: {eval_err}")
            return {"item_name": item_name, "serial_no": serial_no, "part_no": part_no}, num_rows, raw_html
        except requests.exceptions.RequestException as e:
            logging.error(f"[Spare Data] Failed to load Ticket {ticket_id}: {e}")
            return {"item_name": "", "serial_no": "", "part_no": ""}, num_rows, raw_html

    def bulk_fetch(self, ticket_ids_str, session_id, log_cb=print, progress_cb=None):
        if isinstance(ticket_ids_str, str):
            ticket_ids = [t.strip() for t in ticket_ids_str.replace('\n', ',').split(',') if t.strip()]
        else:
            ticket_ids = ticket_ids_str
           
        pdf = FPDF()
        any_pdf_generated = False
        total = len(ticket_ids)
        if total == 0:
            log_cb("No tickets to process.")
            if progress_cb: progress_cb(1.0)
            return None
       
        for idx, ticket_id in enumerate(ticket_ids):
            if progress_cb:
                progress_cb(idx / total)
            log_cb(f"\n--- Processing Ticket: {ticket_id} ---")
           
            js_text, js_raw_html = self.fetch_job_sheet(ticket_id, session_id, log_cb)
            if not js_text:
                continue
               
            spare_data, num_rows, spare_raw_html = self.fetch_spare_data(ticket_id, session_id, log_cb)
           
            item_n = str(spare_data.get('item_name', '')).strip()
            part_n = str(spare_data.get('part_no', '')).strip()
            ser_n = str(spare_data.get('serial_no', '')).strip()
           
            log_cb(f"--- DIAGNOSTIC START: Ticket {ticket_id} ---")
            log_cb(f"JOB SHEET HTML LENGTH: {len(js_raw_html)} chars, SPARE TABLE ROWS FOUND: {num_rows}")
            log_cb(f"EXTRACTED: Item '{item_n}', P/N '{part_n}', S/N '{ser_n}'")
           
            if not item_n and not part_n and not ser_n:
                log_cb(f" [CLEANUP] Ticket {ticket_id} yielded no spare data.")
                continue
               
            any_pdf_generated = True

            pdf.add_page()
            pdf.set_auto_page_break(auto=False)
            MAX_Y_LIMIT = 275.0
           
            lines = js_text.splitlines()
           
            injected_rows = 0
            if item_n or part_n or ser_n:
                i_mock = textwrap.wrap(item_n, width=25) if item_n else []
                p_mock = textwrap.wrap(part_n, width=15) if part_n else []
                s_mock = textwrap.wrap(ser_n, width=20) if ser_n else []
                injected_rows = max(len(i_mock), len(p_mock), len(s_mock))
               
            total_lines = len(lines) + injected_rows + 1
           
            available_height = 275.0
            if total_lines * 5.0 <= available_height:
                line_height = 5.0
                base_font_size = 9.0
                data_font_size = 8.0
                scale_factor = 1.0
            else:
                line_height = available_height / total_lines
                scale_factor = line_height / 5.0
                base_font_size = 9.0 * scale_factor
                data_font_size = 8.0 * scale_factor
           
            spare_request_found = False
            spare_return_found = False
           
            for line in lines:
                current_y = pdf.get_y()
                upper_line = line.upper()
                if "SPARE REQUEST" in upper_line:
                    spare_request_found = True
                    spare_return_found = False
                elif "SPARE RETURN" in upper_line:
                    spare_request_found = False
                    spare_return_found = True

                if (spare_request_found or spare_return_found) and line.strip().startswith("1.") and "___" in line:
                    if spare_request_found:
                        i_val, p_val, s_val = item_n, part_n, ser_n
                        spare_request_found = False
                    else:
                        i_val, p_val, s_val = "", "", ""
                        spare_return_found = False
                       
                    if i_val or p_val or s_val:
                        pdf.set_font("Courier", style="B", size=data_font_size)
                        pdf.set_text_color(0, 0, 0)
                       
                        i_val = str(i_val).strip()
                        p_val = str(p_val).strip()
                        s_val = str(s_val).strip()
                       
                        i_lines = textwrap.wrap(i_val, width=25) if i_val else []
                        p_lines = textwrap.wrap(p_val, width=15) if p_val else []
                        s_lines = textwrap.wrap(s_val, width=20) if s_val else []
                       
                        max_lines = max(len(i_lines), len(p_lines), len(s_lines))
                       
                        for i in range(max_lines):
                            y_pos = pdf.get_y() + (line_height * 0.7)
                           
                            x_item = 10 + (5 * scale_factor)
                            x_part = 10 + (55 * scale_factor)
                            x_serial = 10 + (82 * scale_factor)
                           
                            if i < len(i_lines):
                                pdf.text(x=x_item, y=y_pos, text=i_lines[i])
                            if i < len(p_lines):
                                pdf.text(x=x_part, y=y_pos, text=p_lines[i])
                            if i < len(s_lines):
                                pdf.text(x=x_serial, y=y_pos, text=s_lines[i])
                               
                            pdf.cell(0, line_height * 0.8, text="", new_x="LMARGIN", new_y="NEXT")
                           
                        pdf.set_y(pdf.get_y() + (line_height * 0.2))
                       
                pdf.set_font("Courier", size=base_font_size)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, line_height, text=line, new_x="LMARGIN", new_y="NEXT")

        if progress_cb:
            progress_cb(1.0)
                       
        if any_pdf_generated and pdf.page_no() > 0:
            output_filename = "FSMS_JobSheets_Export.pdf"
            output_path = os.path.join(os.getcwd(), output_filename)
            pdf.output(output_path)
            log_cb(f"\n[INFO] PDF generated securely: {output_path}")
            return output_path
        else:
            log_cb("\n[WARNING] PDF Blocked: None of the input tickets possessed printable spare part data.")
            return None

    def grab_serials(self, cust_refs_str, session_id, log_cb=print, progress_cb=None):
        if isinstance(cust_refs_str, str):
            cust_refs = [r.strip() for r in cust_refs_str.replace('\n', ',').split(',') if r.strip()]
        else:
            cust_refs = cust_refs_str
            
        results = []
        total = len(cust_refs)
        if total == 0:
            log_cb("No references to process.")
            if progress_cb: progress_cb(1.0)
            return results
            
        statuses = [
            'Open: New', 'Open: Acknowledged', 'Open: EUC Acknowledged Part Not Available',
            'Open: EUC Acknowledged Preventive Maintenance', 'Open: EUC Acknowledged Projects',
            'Open: EUC Acknowledged Resouces', 'Open: EUC Acknowledged User Schedule',
            'Open: Re-open', 'Open: Customer Rescheduled', 'Open: Assigned',
            'Pending: Quotation In Progress', 'Pending: Quotation Approved and Waiting for Part',
            'Pending: Customer Rescheduled', 'Pending: Follow Up', 'Pending: Customer Problem Solving',
            'Pending: DELL Cancelled', 'Pending: Ordering Spare', 'Pending: Preventive Maintenance',
            'Pending: Projects', 'Pending: Quotation Initiate', 'Pending: Repair',
            'Pending: Quotation Rejected', 'Pending: Customer ID & Password',
            'Pending: Approval on Cancellation of Installation', 'Closed',
            'Closed: Call Cancelled', 'Closed: Completed', 'Pending: Customer',
            'Closed: Closed First Call', 'Closed: Quotation Rejected',
            'Closed: Without Test File', 'Closed: Installation Cancelled',
            'MAS - APPOINTMENT SET'
        ]
            
        for idx, ref in enumerate(cust_refs):
            if progress_cb: progress_cb(idx / total)
            log_cb(f"Processing Request for Ref: {ref}")
            
            params = {
                'encrypted': session_id,
                'post_action': 'S',
                'srh_status': statuses,
                'fr_date': '', 'to_date': '', 'cust_name': '', 'branch_id': '',
                'region_name': '', 'cust_ref': ref,
                'cust_subset': '', 'helpdesk': '', 'priority': '', 'rpt_by': '',
                'rpt_phone': '', 'rpt_by_mobile': '', 'site_contact': '',
                'site_phone': '', 'site_mobile': '', 'call_src': '', 'misc_ref': '',
                'serial_no': '', 'make': '', 'sv_dept': '', 'ass_se': '',
                'rcv_by': '', 'ticket_type': '', 'proj_name': '', 'fsr_no': '',
                'urg_id': '', 'etes_id': ''
            }
            
            try:
                resp_a = self.session.get('https://intranetapp.ctc-g.com.my/fsms/fs_trx_srhticket.pl', params=params, timeout=15)
                resp_a.raise_for_status()
                
                match_id = re.search(r'javascript:runShow\((\d+)\)', resp_a.text)
                if match_id:
                    ticket_id = match_id.group(1)
                    log_cb(f"Found Ticket ID: {ticket_id}")
                    
                    url_b = f"http://intranetapp.ctc-g.com.my/fsms/fs_trx_editticket.pl?encrypted={session_id}&ticket_id={ticket_id}"
                    resp_b = self.session.get(url_b, timeout=15)
                    resp_b.raise_for_status()
                    
                    match_sn = re.search(r'<input[^>]*name="equip_sn"[^>]*value="([^"]*)"', resp_b.text)
                    if match_sn:
                        sn = match_sn.group(1).strip()
                        log_cb(f"Successfully Extracted S/N: {sn}")
                        results.append({"Customer Ref": ref, "Serial Number": sn})
                    else:
                        log_cb(f"Could not find S/N element for Ticket {ticket_id}")
                        results.append({"Customer Ref": ref, "Serial Number": "Not Found"})
                else:
                    log_cb(f"No Ticket ID matched for Ref: {ref}")
                    results.append({"Customer Ref": ref, "Serial Number": "No Ticket ID"})
                    
            except Exception as e:
                log_cb(f"Error evaluating Ref {ref}: {e}")
                results.append({"Customer Ref": ref, "Serial Number": f"Error: {e}"})
                
        if progress_cb: progress_cb(1.0)
        return results

    def grab_efsr_pdfs(self, ticket_ids_str, session_id, log_cb=print, progress_cb=None):
        if isinstance(ticket_ids_str, str):
            ticket_ids = [t.strip() for t in ticket_ids_str.replace('\n', ',').split(',') if t.strip()]
        else:
            ticket_ids = ticket_ids_str
            
        results = []
        total = len(ticket_ids)
        if total == 0:
            log_cb("No tickets to process.")
            if progress_cb: progress_cb(1.0)
            return results
            
        for idx, t_id in enumerate(ticket_ids):
            if progress_cb: progress_cb(idx / total)
            log_cb(f"Processing Ticket ID: {t_id}")
            
            url = f"https://intranetapp.ctc-g.com.my/fsms/fs_trx_close.pl?encrypted={session_id}&ticket_id={t_id}"
            try:
                resp = self.session.get(url, timeout=15)
                resp.raise_for_status()
                
                matches = re.findall(r'(eFSA\d+-\d+\.pdf)', resp.text)
                unique_matches = list(set(matches))
                if unique_matches:
                    pdf_urls = [f"https://drtu.ctc-g.com.my/eucFSA/efsrpdf/{m}" for m in unique_matches]
                    log_cb(f"  -> Found {len(unique_matches)} unique PDF(s)")
                    results.append({"Ticket ID": t_id, "PDF Link": pdf_urls})
                else:
                    log_cb(f"  -> No eFSR PDF found for Ticket {t_id}")
                    results.append({"Ticket ID": t_id, "PDF Link": []})
                    
            except Exception as e:
                log_cb(f"  -> Error evaluating Ticket {t_id}: {e}")
                results.append({"Ticket ID": t_id, "PDF Link": []})
                
        if progress_cb: progress_cb(1.0)
        return results
