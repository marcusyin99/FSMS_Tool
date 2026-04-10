import streamlit as st
import io
import zipfile
import pandas as pd
from fsms_logic import FSMSFetcher

def render_efsr_tool():
    st.title("📑 eFSR PDF Grabber")
    st.write("Extract and download eFSR PDF links associated with tickets.")

    ticket_input = st.text_area("Ticket IDs (comma-separated or one per line)", height=150)
    
    if st.button("Start eFSR Grabber"):
        if not ticket_input.strip():
            st.warning("Please provide at least one Ticket ID.")
            return

        tickets = [line.strip() for line in ticket_input.replace('\n', ',').split(',') if line.strip()]
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def log_cb(msg):
            status_text.write(f"**Status:** {msg}")
            
        def progress_cb(val):
            progress_bar.progress(val)

        hardcoded_session_id = "155aa70338de898c5a16b6b45c9399fa"
        hardcoded_cookie = "_ga=GA1.3.301266867.1748954739; _ga_3JE4R8NPJQ=GS2.1.s1765772355$o9$g1$t1765772575$j60$l0$h0; 155aa70338de898c5a16b6b45c9399fa=95878; 95878=7145996093"
        fetcher = FSMSFetcher(
            cookie_string=hardcoded_cookie,
            session_id=hardcoded_session_id
        )
        
        results = fetcher.grab_efsr_pdfs(tickets, hardcoded_session_id, log_cb=log_cb, progress_cb=progress_cb)
        
        st.success("✅ eFSR Grabber finished.")
        
        df_list = []
        all_valid_urls = []
        for r in results:
            urls = r['PDF Link']
            if urls:
                all_valid_urls.extend(urls)
                for u in urls:
                    df_list.append({
                        "Ticket ID": r['Ticket ID'],
                        "PDF Link": u
                    })
            else:
                df_list.append({
                    "Ticket ID": r['Ticket ID'],
                    "PDF Link": "No PDF found"
                })
                
        df = pd.DataFrame(df_list)
        st.dataframe(
            df, 
            column_config={
                "PDF Link": st.column_config.LinkColumn("PDF Link")
            },
            hide_index=True, 
            use_container_width=True
        )
        
        # Zip download
        if all_valid_urls:
            st.info(f"Preparing ZIP file containing {len(all_valid_urls)} PDFs...")
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                for url in all_valid_urls:
                    try:
                        resp = fetcher.session.get(url, timeout=10)
                        if resp.status_code == 200:
                            filename = url.split('/')[-1]
                            zf.writestr(filename, resp.content)
                    except Exception as e:
                        pass
            
            st.download_button(
                label="🗜️ Download All (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="eFSR_PDFs.zip",
                mime="application/zip"
            )
