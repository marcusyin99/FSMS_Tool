import streamlit as st

st.set_page_config(page_title="Company Toolbelt", layout="wide")

def inject_custom_css():
    st.markdown(
        """
        <style>
            /* 1. Global Aesthetics */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            
            html, body, [class*="css"]  {
                font-family: 'Inter', sans-serif !important;
            }
            
            /* Neon Outline Buttons */
            .stButton > button {
                background-color: transparent !important;
                border: 1px solid #00d4ff !important;
                color: #00d4ff !important;
                box-shadow: 0 0 5px rgba(0, 212, 255, 0.2), inset 0 0 5px rgba(0, 212, 255, 0.1) !important;
                transition: all 0.3s ease-in-out !important;
                border-radius: 8px !important;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }
            .stButton > button:hover {
                box-shadow: 0 0 15px rgba(0, 212, 255, 0.6), inset 0 0 10px rgba(0, 212, 255, 0.4) !important;
                text-shadow: 0 0 5px rgba(0, 212, 255, 0.8) !important;
                border: 1px solid #00d4ff !important;
                color: #ffffff !important;
            }

            /* Floating Glassmorphism Cards */
            [data-testid="column"] > div {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 1.5rem;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                height: 100%;
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            }
            [data-testid="column"] > div:hover {
                transform: translateY(-6px);
                border: 1px solid rgba(0, 212, 255, 0.6);
                box-shadow: 0 15px 30px rgba(0, 212, 255, 0.25), inset 0 0 12px rgba(0, 212, 255, 0.15);
            }

            /* Sidebar Glass */
            [data-testid="stSidebar"] {
                background-color: rgba(14, 17, 23, 0.6) !important;
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border-right: 1px solid rgba(0, 212, 255, 0.2) !important;
                box-shadow: 4px 0 20px rgba(0, 212, 255, 0.1) !important;
            }

            /* Heartbeat Dot */
            .heartbeat-dot {
                width: 10px;
                height: 10px;
                background-color: #00d4ff;
                border-radius: 50%;
                box-shadow: 0 0 10px #00d4ff;
                animation: heartbeat 1.5s ease-in-out infinite;
                margin-left: -5px;
                margin-top: -30px;
                position: relative;
                z-index: 99;
            }
            @keyframes heartbeat {
                0% { transform: scale(1); filter: brightness(1) drop-shadow(0 0 5px #00d4ff); }
                15% { transform: scale(1.3); filter: brightness(1.5) drop-shadow(0 0 15px #00d4ff); }
                30% { transform: scale(1); filter: brightness(1) drop-shadow(0 0 5px #00d4ff); }
                45% { transform: scale(1.3); filter: brightness(1.5) drop-shadow(0 0 15px #00d4ff); }
                100% { transform: scale(1); filter: brightness(1) drop-shadow(0 0 5px #00d4ff); }
            }

            /* Pulsing Green LED for Auth */
            .pulsing-led {
                display: inline-block;
                width: 12px;
                height: 12px;
                background-color: #00ff00;
                border-radius: 50%;
                box-shadow: 0 0 10px #00ff00;
                animation: pulse 1.5s infinite alternate;
                margin-right: 12px;
            }
            @keyframes pulse {
                from { box-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00; opacity: 0.8; }
                to { box-shadow: 0 0 15px #00ff00, 0 0 20px #00ff00; opacity: 1; }
            }

            /* Terminal News Banner */
            .terminal-banner {
                background-color: #0d1117;
                border-radius: 8px;
                border: 1px solid #30363d;
                font-family: 'Courier New', Courier, monospace;
                overflow: hidden;
                margin-top: 10px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            }
            .terminal-header {
                background-color: #161b22;
                padding: 8px 12px;
                display: flex;
                align-items: center;
                border-bottom: 1px solid #30363d;
            }
            .terminal-header .dot {
                width: 12px; height: 12px; border-radius: 50%; margin-right: 8px;
            }
            .terminal-header .red { background-color: #ff5f56; }
            .terminal-header .yellow { background-color: #ffbd2e; }
            .terminal-header .green { background-color: #27c93f; }
            .terminal-title {
                color: #8b949e; font-size: 0.85rem; margin-left: 10px; font-weight: bold; font-family: 'Inter', sans-serif;
            }
            .terminal-body {
                padding: 16px;
                color: #58a6ff;
                font-size: 0.95rem;
                display: flex;
                align-items: center;
            }
            .prompt {
                color: #3fb950;
                font-weight: bold;
                margin-right: 8px;
            }
            .news-text {
                color: #e6f1ff;
            }
            .blinking-cursor {
                font-weight: bold;
                color: #d2a8ff;
                animation: blink 1s step-end infinite;
                margin-left: 2px;
            }
            @keyframes blink {
                50% { opacity: 0; }
            }

            /* Header Gradient Text */
            .gradient-header {
                background: linear-gradient(90deg, #00d4ff, #ffffff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 800;
                font-size: 3rem;
                margin-bottom: -10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
inject_custom_css()

# Initialize session state variables
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home / Dashboard"
# Session ID is hardcoded
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def navigate_to(page_name):
    st.session_state.current_page = page_name

def render_sidebar():
    try:
        import base64
        with open("CTC-Global-Logo.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        logo_html = f'''
        <div style="display: flex; align-items: start; margin-bottom: 20px;">
            <img src="data:image/png;base64,{encoded_string}" style="width: 85%; border-radius: 8px;">
            <div class="heartbeat-dot"></div>
        </div>
        '''
        st.sidebar.markdown(logo_html, unsafe_allow_html=True)
    except:
        pass # fallback silently if logo missing
    st.sidebar.title("Company Toolbelt")
    
    # Navigation pages
    pages = [
        "🏠 Home / Dashboard",
        "📄 FSMS Job Sheet Tool (Existing logic)",
        "💻 HP Warranty Checker",
        "🔍 Serial Number Grabber (Dell OPP)",
        "📑 eFSR PDF Grabber",
        "⚙️ Global Settings / Profile"
    ]
    
    # Determine the index for the radio button based on session state
    current_index = pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0
    
    selected_page = st.sidebar.radio(
        "Navigation",
        options=pages,
        index=current_index,
        key="nav_radio"
    )
    
    # If the user clicks a different radio option, sync session state and rerun
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()

    st.sidebar.divider()
    
    # Auth Status
    st.sidebar.subheader("Global Auth Status")
    if st.session_state.get('authenticated', False):
        st.sidebar.markdown(
            """<div style="display: flex; align-items: center; padding: 12px; background: rgba(0, 255, 0, 0.05); border: 1px solid rgba(0, 255, 0, 0.4); border-radius: 8px;">
                   <span class="pulsing-led"></span>
                   <span style="color: #00ff00; font-weight: 600; letter-spacing: 0.5px;">System Online</span>
               </div>""", 
            unsafe_allow_html=True
        )
    else:
        st.sidebar.warning("⚠️ Authentication Required")
        
    st.sidebar.markdown(
        """<div style='text-align: center; margin-top: 80px; padding-bottom: 10px; opacity: 0.15; font-size: 0.65rem; font-family: "Inter", sans-serif; letter-spacing: 1px;'>
           DEVELOPED BY MARCUS ENG
           </div>""", 
        unsafe_allow_html=True
    )

def render_home():
    st.markdown('<h1 class="gradient-header">Welcome to the Company Toolbelt</h1>', unsafe_allow_html=True)
    st.caption("Your Central Hub for Internal Tools & Services")
    
    st.markdown("### Available Tools")
    
    # Create Tool Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 📄 FSMS Tool")
        st.write("Process HP warranty serial numbers from job sheets.")
        if st.button("Open FSMS Tool", use_container_width=True):
            navigate_to("📄 FSMS Job Sheet Tool (Existing logic)")
            st.rerun()

    with col2:
        st.markdown("#### 💻 HP Warranty")
        st.write("Automated bulk warranty lookups.")
        if st.button("Open Warranty Tool", use_container_width=True):
            navigate_to("💻 HP Warranty Checker")
            st.rerun()

    with col3:
        st.markdown("#### 🔍 S/N Grabber (Dell OPP)")
        st.write("Extract Serial Numbers dynamically from Customer Reference IDs.")
        if st.button("Open Grabber", use_container_width=True):
            navigate_to("🔍 Serial Number Grabber (Dell OPP)")
            st.rerun()
            
    with col4:
        st.markdown("#### 📑 eFSR PDF")
        st.write("Extract and zip eFSR PDFs assigned to specific tickets.")
        if st.button("Open eFSR Grabber", use_container_width=True):
            navigate_to("📑 eFSR PDF Grabber")
            st.rerun()

    st.divider()
    
    st.markdown("### System News")
    terminal_html = '''
    <div class="terminal-banner">
        <div class="terminal-header">
            <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
            <span class="terminal-title">bash - root@sys-ops</span>
        </div>
        <div class="terminal-body">
            <span class="prompt">$></span><span class="news-text">Latest deployment complete. Toolbelt modules are fully operational.</span><span class="blinking-cursor">_</span>
        </div>
    </div>
    '''
    st.markdown(terminal_html, unsafe_allow_html=True)

def render_fsms_tool():
    st.title("📄 FSMS Job Sheet Tool")
    
    st.write("Enter Ticket IDs (comma-separated or one per line) to process Job Sheets and fetch Spare Data.")
    text_input = st.text_area("Ticket IDs")
    
    if st.button("Start Processing"):
        if not text_input.strip():
            st.warning("Please enter at least one Ticket ID.")
            return

        progress_bar = st.progress(0)
        status_text = st.empty()
        log_expander = st.expander("Processing Logs", expanded=True)
        log_container = log_expander.empty()
        
        log_msgs = []
        def log_cb(msg):
            status_text.write(f"**Status:** {msg}")
            log_msgs.append(msg)
            # Join list into one string separated by double space/newlines for markdown rendering
            log_container.markdown("\n\n".join([f"`{m}`" for m in log_msgs]))
                
        def progress_cb(val):
            progress_bar.progress(val)
        
        from fsms_logic import FSMSFetcher
        # Initialize the unified fetcher using global Auth stored previously
        hardcoded_session_id = "155aa70338de898c5a16b6b45c9399fa"
        hardcoded_cookie = "_ga=GA1.3.301266867.1748954739; _ga_3JE4R8NPJQ=GS2.1.s1765772355$o9$g1$t1765772575$j60$l0$h0; 155aa70338de898c5a16b6b45c9399fa=95878; 95878=7145996093"
        fetcher = FSMSFetcher(
            cookie_string=hardcoded_cookie,
            session_id=hardcoded_session_id
        )
        
        # Pass the input arguments alongside the Streamlit UI callbacks
        pdf_path = fetcher.bulk_fetch(text_input, hardcoded_session_id, log_cb=log_cb, progress_cb=progress_cb)
        
        if pdf_path:
            st.success("✅ Process finalized. Your Job Sheet PDF is ready for download.")
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="⬇️ Download Generated Job Sheets PDF",
                    data=pdf_file.read(),
                    file_name="FSMS_JobSheets_Export.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("⚠️ No printable PDF was generated (Data was likely missing or inaccessible).")

def render_warranty_tool():
    st.title("💻 HP Warranty Checker")
    st.write("Fetch serial numbers from your clipboard to automatically pull HP warranty info.")
    
    if st.button("📋 Fetch from Clipboard"):
        import pyperclip
        try:
            st.session_state.clipboard_serials = pyperclip.paste()
        except Exception as e:
            st.error(f"Clipboard error: {e}")
            
    current_serials = st.session_state.get('clipboard_serials', '')
    serial_input = st.text_area("Serial Numbers (one per line)", value=current_serials, height=200)
    
    if st.button("Confirm & Check Warranties"):
        if not serial_input.strip():
            st.warning("Please provide at least one serial number.")
            return
            
        import time
        import io
        import csv
        from datetime import datetime
        from warranty_checker import check_warranty
        
        serial_numbers = [line.strip() for line in serial_input.splitlines() if line.strip()]
        st.info(f"Checking {len(serial_numbers)} serial numbers...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        for i, sn in enumerate(serial_numbers):
            status_text.write(f"Checking: **{sn}**...")
            product_name = check_warranty(sn)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            results.append({"Timestamp": timestamp, "Serial Number": sn, "Product Name": product_name})
            
            progress_bar.progress((i + 1) / len(serial_numbers))
            time.sleep(0.5)
            
        status_text.success("✅ All warranties checked successfully!")
        st.dataframe(results, use_container_width=True)
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["Timestamp", "Serial Number", "Product Name"])
        writer.writeheader()
        writer.writerows(results)
        
        st.download_button(
            label="⬇️ Download CSV Results",
            data=output.getvalue().encode('utf-8'),
            file_name="warranty_results_bulk.csv",
            mime="text/csv"
        )

def render_serial_grabber():
    st.title("🔍 Serial Number Grabber (Dell OPP)")
    st.write("Extract Serial Numbers directly passing in Customer Reference IDs.")
    
    ref_input = st.text_area("Customer References (comma-separated or one per line)", height=150)
    
    if st.button("Start Grabber"):
        if not ref_input.strip():
            st.warning("Please provide at least one Customer Reference.")
            return
            
        import io
        import csv
        from fsms_logic import FSMSFetcher
        
        refs = [line.strip() for line in ref_input.replace('\n', ',').split(',') if line.strip()]
        
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
        
        results = fetcher.grab_serials(refs, hardcoded_session_id, log_cb=log_cb, progress_cb=progress_cb)
        
        st.success("✅ Grabber finished.")
        st.dataframe(results, use_container_width=True)
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["Customer Ref", "Serial Number"])
        writer.writeheader()
        writer.writerows(results)
        
        st.download_button(
            label="⬇️ Download CSV Results",
            data=output.getvalue().encode('utf-8'),
            file_name="serial_grabber_results.csv",
            mime="text/csv"
        )

def render_settings():
    st.title("⚙️ Global Settings / Profile")
    
    st.markdown("Your active session profile constraints.")
    st.write("Logged in as: **admin123**")
    
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

def main():
    if not st.session_state.get('authenticated', False):
        st.title("🔒 Login Required")
        st.write("Please sign in to access the Company Toolbelt.")
        with st.form("login_form"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                if user == "admin123" and pwd == "CTC123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        return

    render_sidebar()
    
    page = st.session_state.current_page
    
    if page == "🏠 Home / Dashboard":
        render_home()
    elif page == "📄 FSMS Job Sheet Tool (Existing logic)":
        render_fsms_tool()
    elif page == "💻 HP Warranty Checker":
        render_warranty_tool()
    elif page == "🔍 Serial Number Grabber (Dell OPP)":
        render_serial_grabber()
    elif page == "📑 eFSR PDF Grabber":
        from efsr_grabber import render_efsr_tool
        render_efsr_tool()
    elif page == "⚙️ Global Settings / Profile":
        render_settings()

if __name__ == "__main__":
    main()
