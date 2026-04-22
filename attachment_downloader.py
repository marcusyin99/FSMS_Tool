import requests
import re
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import zipfile
import io
import time
from datetime import datetime

def get_ticket_data(ticket_id, session_id, cookie_string=None):
    """
    Scrapes ticket metadata and attachment links from FSMS.
    
    Args:
        ticket_id (str): The ID of the ticket.
        session_id (str): The encrypted session ID.
        cookie_string (str): The authenticated cookie string.
        
    Returns:
        list of dict: A list where each dict contains ticket metadata and attachment details.
    """
    base_url = "https://intranetapp.ctc-g.com.my/fsms/"

    # Initialize a session
    session = requests.Session()
    if cookie_string:
        session.headers.update({"Cookie": cookie_string})
    # It might be necessary to ignore SSL verification depending on the intranet site setup.
    # session.verify = False 

    # --- Request 1: Metadata Extraction ---
    metadata_url = f"{base_url}fs_trx_editticket.pl?encrypted={session_id}&ticket_id={ticket_id}&dis=Y"
    
    try:
        response1 = session.get(metadata_url)
        response1.raise_for_status()
    except Exception as e:
        print(f"Error fetching metadata for ticket {ticket_id}: {e}")
        return []

    soup1 = BeautifulSoup(response1.text, "html.parser")
    
    # Extract cust_ref with fallback to cust_cost_ctr
    cust_ref_tag = soup1.find("input", {"name": "cust_ref"})
    cust_ref = cust_ref_tag.get("value", "").strip() if cust_ref_tag else ""
    
    if not cust_ref:
        cust_cost_ctr_tag = soup1.find("input", {"name": "cust_cost_ctr"})
        cust_ref = cust_cost_ctr_tag.get("value", "").strip() if cust_cost_ctr_tag else ""
        
    if not cust_ref:
        cust_ref = "Ref No Not Found"
    
    # Extract rpt_by_address
    rpt_by_address_tag = soup1.find("input", {"name": "rpt_by_address"})
    full_address = rpt_by_address_tag.get("value", "").strip() if rpt_by_address_tag else ""
    

    # --- Request 2: File Link Discovery ---
    attachment_url = f"{base_url}fs_trx_attachfile.pl?encrypted={session_id}&ticket_id={ticket_id}&dis=Y"
    
    try:
        response2 = session.get(attachment_url)
        response2.raise_for_status()
    except Exception as e:
        print(f"Error fetching attachments for ticket {ticket_id}: {e}")
        return []

    soup2 = BeautifulSoup(response2.text, "html.parser")
    
    # Find all <a> tags (assuming they might be located within a document table as per context)
    links = soup2.find_all("a")
    
    results = []
    
    if not links:
        # Scenario 3: Empty / No file found
        results.append({
            "ticket_id": ticket_id,
            "cust_ref": cust_ref,
            "full_address": full_address,
            "final_url": None,
            "scenario": "No File"
        })
    else:
        # Identify links based on scenarios
        valid_links_found = False
        for link in links:
            href = link.get("href")
            if not href:
                continue
                
            final_url = None
            scenario = None
            
            if href.startswith("http"):
                # Scenario 1 (Absolute Link)
                final_url = href
                scenario = "Absolute Link"
                
            elif href.startswith("doc/"):
                # Scenario 2 (Relative Link)
                final_url = f"{base_url}{href}"
                scenario = "Relative Link"
                
            if final_url:
                valid_links_found = True
                results.append({
                    "ticket_id": ticket_id,
                    "cust_ref": cust_ref,
                    "full_address": full_address,
                    "final_url": final_url,
                    "scenario": scenario
                })
                
        if not valid_links_found:
             # Handle case where 'a' tags exist but none match our criteria
             results.append({
                "ticket_id": ticket_id,
                "cust_ref": cust_ref,
                "full_address": full_address,
                "final_url": None,
                "scenario": "No File"
            })
            
    return results

def clean_site_name(address):
    """
    Scans left-to-right to find the first address anchor and cuts the string.
    Removes trailing colons, commas, hyphens, and extra spaces.
    """
    anchors = [r"LOT\b", r"NO\.", r"LEVEL\b", r"LG-", r"BLOCK\b", r"BT\b", r"MILE\b", r"GROUND\b", r"JALAN\b", r"SITE ID\b"]
    pattern = re.compile(r"(?i)\s*(" + "|".join(anchors) + r")\s*")
    
    match = pattern.search(address)
    if match:
        site_name = address[:match.start()]
    else:
        site_name = address
        
    # Replace internal colons and commas, then standardize spaces
    site_name = site_name.replace(":", " ").replace(",", " ")
    site_name = re.sub(r'\s+', ' ', site_name)
    
    # Clean any trailing colons, commas, hyphens, and spaces
    return site_name.strip(" :,-")

def to_roman(num):
    """Helper to convert integer to a Roman Numeral string."""
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

def generate_filenames(data_list):
    """
    Adds 'new_filename' key to each dictionary in data_list.
    Handles multiple identical ticket_ids by appending roman numerals.
    """
    # Count occurrences to determine if roman numerals are needed
    ticket_counts = {}
    for item in data_list:
        tid = item.get("ticket_id", "UNKNOWN")
        ticket_counts[tid] = ticket_counts.get(tid, 0) + 1
        
    current_index = {}
    
    for item in data_list:
        tid = item.get("ticket_id", "UNKNOWN")
        cust_ref = item.get("cust_ref", "")
        full_address = item.get("full_address", "")
        
        cleaned_site_name = clean_site_name(full_address)
        base_name = f"{tid}_{cleaned_site_name}_{cust_ref}"
        
        if ticket_counts[tid] > 1:
            idx = current_index.get(tid, 0) + 1
            current_index[tid] = idx
            roman_suffix = f"_{to_roman(idx)}"
            item["roman_suffix"] = roman_suffix
            item["new_filename"] = base_name
        else:
            item["roman_suffix"] = ""
            item["new_filename"] = base_name
            
    return data_list

def render_attachment_downloader():
    st.title("📥 FSMS Attachment Downloader")
    st.write("Scrape metadata and automatically download and rename attachments.")
    
    text_input = st.text_area("Ticket IDs (one per line)", height=150)
    
    if "attachment_data" not in st.session_state:
        st.session_state.attachment_data = []

    if st.button("Process Tickets", use_container_width=True):
        if not text_input.strip():
            st.warning("Please enter at least one Ticket ID.")
            return
            
        ticket_ids = [line.strip() for line in text_input.splitlines() if line.strip()]
        
        # Hardcoded session ID for simplicity in testing as per current app standard
        hardcoded_session_id = "155aa70338de898c5a16b6b45c9399fa"
        hardcoded_cookie = "_ga=GA1.3.301266867.1748954739; _ga_3JE4R8NPJQ=GS2.1.s1765772355$o9$g1$t1765772575$j60$l0$h0; 155aa70338de898c5a16b6b45c9399fa=95878; 95878=7145996093"
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        all_data = []
        for i, tid in enumerate(ticket_ids):
            status_text.write(f"Scraping Ticket: **{tid}**...")
            data = get_ticket_data(tid, hardcoded_session_id, hardcoded_cookie)
            all_data.extend(data)
            progress_bar.progress((i + 1) / len(ticket_ids))
            time.sleep(0.1)
            
        all_data = generate_filenames(all_data)
        st.session_state.attachment_data = all_data
        status_text.success("✅ Extraction complete.")
        
    if st.session_state.attachment_data:
        st.divider()
        st.subheader("Results")
        
        data = st.session_state.attachment_data
        
        df_list = []
        for d in data:
            link_val = d['final_url'] if d['scenario'] != 'No File' else 'No File Found'
                
            df_list.append({
                "Ticket ID": d['ticket_id'],
                "Customer Ref": d['cust_ref'],
                "Full Address": d['full_address'],
                "File Link": link_val,
                "New Filename": d['new_filename'],
                "Roman Suffix": d.get('roman_suffix', ''),
                "Original URL": d['final_url']
            })
            
        df = pd.DataFrame(df_list)
        
        edited_df = st.data_editor(
            df,
            column_config={
                "Ticket ID": st.column_config.TextColumn("Ticket ID", disabled=True),
                "Customer Ref": st.column_config.TextColumn("Customer Ref", disabled=True),
                "Full Address": st.column_config.TextColumn("Full Address", disabled=True),
                "File Link": st.column_config.LinkColumn("File Link", disabled=True) if not df['File Link'].eq('No File Found').all() else st.column_config.TextColumn("File Link", disabled=True),
                "New Filename": st.column_config.TextColumn("New Filename", disabled=False),
                "Roman Suffix": None,
                "Original URL": None
            },
            hide_index=True,
            use_container_width=True
        )
        
        no_file_tickets = edited_df[edited_df['File Link'] == 'No File Found']['Ticket ID'].tolist()
        if no_file_tickets:
             st.warning(f"⚠️ The following tickets have no valid files and will be skipped: {', '.join(list(set(no_file_tickets)))}")
            
        st.divider()
        if st.button("🚀 Download All Files", type="primary", use_container_width=True):
            with st.spinner("Downloading and Zipping..."):
                zip_buffer = io.BytesIO()
                dl_session = requests.Session()
                hardcoded_cookie = "_ga=GA1.3.301266867.1748954739; _ga_3JE4R8NPJQ=GS2.1.s1765772355$o9$g1$t1765772575$j60$l0$h0; 155aa70338de898c5a16b6b45c9399fa=95878; 95878=7145996093"
                dl_session.headers.update({"Cookie": hardcoded_cookie})
                
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for index, row in edited_df.iterrows():
                        if row["File Link"] == 'No File Found':
                            continue
                            
                        url = row["Original URL"]
                        if not url:
                            continue
                            
                        try:
                            response = dl_session.get(url)
                            response.raise_for_status()
                            
                            ext = ""
                            if "." in url.split("/")[-1]:
                                possible_ext = "." + url.split("/")[-1].split(".")[-1].split("?")[0]
                                if len(possible_ext) <= 5: 
                                    ext = possible_ext
                            if not ext:
                                ext = ".pdf" 
                                
                            final_name = f"{row['New Filename']}{row['Roman Suffix']}{ext}"
                            final_name = re.sub(r'[/\\?%*:|"<>]', '-', final_name)
                            
                            zip_file.writestr(final_name, response.content)
                        except Exception as e:
                            st.error(f"Failed to download from {url}: {e}")
                
                date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                zip_filename = f"FSMS_Attachments_{date_str}.zip"
                
                st.success("✅ ZIP archive created!")
                st.download_button(
                    label="📦 Download ZIP Archive",
                    data=zip_buffer.getvalue(),
                    file_name=zip_filename,
                    mime="application/zip",
                    use_container_width=True
                )

if __name__ == "__main__":
    pass
