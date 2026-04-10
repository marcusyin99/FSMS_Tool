import streamlit as st
import os
import json
import shutil

st.set_page_config(page_title="Company Toolbelt", layout="wide")

CONFIG_PATH = os.path.join(os.getcwd(), "config.json")
DEFAULT_CONFIG = {
    "display_name": "Marcus",
    "employee_id": "",
    "conn_timeout": 10,
    "heartbeat": True,
    "accent_color": "Neon Cyan"
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except: pass
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=4)

def inject_custom_css(accent_color="Neon Cyan"):
    colors = {
        "Neon Cyan": {"hex": "#00d4ff", "rgb": "0, 212, 255"},
        "Electric Purple": {"hex": "#b000ff", "rgb": "176, 0, 255"},
        "CTC Blue": {"hex": "#0050b3", "rgb": "0, 80, 179"}
    }
    selected = colors.get(accent_color, colors["Neon Cyan"])
    hex_code = selected["hex"]
    rgb_code = selected["rgb"]
    
    css = """
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
    """
    css = css.replace("#00d4ff", hex_code)
    css = css.replace("0, 212, 255", rgb_code)
    st.markdown(css, unsafe_allow_html=True)

def cleanup_temp_files():
    import time
    folders = ["temp_processing"]
    now = time.time()
    for folder in folders:
        target_path = os.path.join(os.getcwd(), folder)
        if os.path.exists(target_path):
            for item in os.listdir(target_path):
                item_path = os.path.join(target_path, item)
                try:
                    # 86400 seconds = 24 hours
                    if os.path.isfile(item_path) and os.stat(item_path).st_mtime < now - 86400:
                        os.remove(item_path)
                except Exception:
                    pass

# Call once per application evaluation run
cleanup_temp_files()

# Initialize session state variables
if "config" not in st.session_state:
    st.session_state.config = load_config()

inject_custom_css(st.session_state.config.get("accent_color", "Neon Cyan"))    

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home / Dashboard"
# Session ID is hardcoded

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.session_state.nav_radio = page_name

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
        "📄 Jobsheet Generator",
        "💻 HP Model Checker",
        "🔍 Serial Number Grabber (Dell OPP)",
        "📑 Bulk eFSR downloader",
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
    st.sidebar.subheader("Intranet Status")
    import requests
    vpn_connected = False
    try:
        # Fast 1.5s timeout probing the intranet
        resp = requests.get("http://intranetapp.ctc-g.com.my", timeout=1.5)
        if resp.status_code == 200:
            vpn_connected = True
    except requests.exceptions.Timeout:
        st.toast("Intranet Ping Timeout (Server Busy or Slow Connection)", icon="⏳")
    except:
        pass
    
    if vpn_connected:
        st.sidebar.markdown(
            """<div title="Connected via Office LAN or VPN" style="display: flex; align-items: center; padding: 12px; background: rgba(0, 255, 0, 0.05); border: 1px solid rgba(0, 255, 0, 0.4); border-radius: 8px; cursor: help;">
                   <span class="pulsing-led"></span>
                   <span style="color: #00ff00; font-weight: 600; letter-spacing: 0.5px;">Intranet Connected</span>
               </div>""", 
            unsafe_allow_html=True
        )
    else:
        st.sidebar.markdown(
            """<div title="Please connect to company VPN to use these tools" style="display: flex; align-items: center; padding: 12px; background: rgba(255, 0, 0, 0.05); border: 1px solid rgba(255, 0, 0, 0.4); border-radius: 8px; cursor: help;">
                   <span style="display: inline-block; width: 12px; height: 12px; background-color: #ff0000; border-radius: 50%; box-shadow: 0 0 10px #ff0000; margin-right: 12px;"></span>
                   <span style="color: #ff0000; font-weight: 600; letter-spacing: 0.5px; line-height: 1.2;">Offline / VPN Required</span>
               </div>""", 
            unsafe_allow_html=True
        )
        
    st.sidebar.markdown(
        """<div style='text-align: center; margin-top: 80px; padding-bottom: 10px; opacity: 0.15; font-size: 0.65rem; font-family: "Inter", sans-serif; letter-spacing: 1px;'>
           DEVELOPED BY MARCUS ENG<br>v1.1.0
           </div>""", 
        unsafe_allow_html=True
    )

def render_home():
    display_name = st.session_state.config.get('display_name', '').strip()
    header_str = f"Welcome back, {display_name}" if display_name else "Welcome to the Company Toolbelt"
    st.markdown(f'<h1 class="gradient-header">{header_str}</h1>', unsafe_allow_html=True)
    
    emp_id = st.session_state.config.get('employee_id', '').strip()
    if emp_id:
        st.caption(f"Employee ID: {emp_id} | Your Central Hub for Internal Tools & Services")
    else:
        st.caption("Your Central Hub for Internal Tools & Services")
    
    st.markdown("### Available Tools")
    
    # Create Tool Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 📄 Jobsheet Generator")
        st.write("Bulk-print jobsheets and auto-fill spare parts requests.")
        st.button("Open Jobsheet Generator", use_container_width=True, on_click=navigate_to, args=("📄 Jobsheet Generator",))

    with col2:
        st.markdown("#### 💻 HP Model Checker")
        st.write("Automated bulk model checker through serial numbers.")
        st.button("Open Warranty Tool", use_container_width=True, on_click=navigate_to, args=("💻 HP Model Checker",))

    with col3:
        st.markdown("#### 🔍 S/N Grabber (Dell OPP)")
        st.write("Extract Serial Numbers dynamically from Customer Reference IDs.")
        st.button("Open Grabber", use_container_width=True, on_click=navigate_to, args=("🔍 Serial Number Grabber (Dell OPP)",))
            
    with col4:
        st.markdown("#### 📑 Bulk eFSR downloader")
        st.write("Batch-download eFSR documents directly from ticket IDs.")
        st.button("Open eFSR Grabber", use_container_width=True, on_click=navigate_to, args=("📑 Bulk eFSR downloader",))

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
    st.title("📄 Jobsheet Generator")
    st.write("Bulk print jobsheets and autofilling spare parts request.")
    
    if "fsms_scanned_data" not in st.session_state:
        st.session_state.fsms_scanned_data = None
    if "fsms_selections" not in st.session_state:
        st.session_state.fsms_selections = {}

    text_input = st.text_area("Ticket IDs (one per line or comma-separated)", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Scan & Fetch Data", use_container_width=True):
            if not text_input.strip():
                st.warning("Please enter at least one Ticket ID.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                log_expander = st.expander("Scanning Logs", expanded=True)
                log_container = log_expander.empty()
                
                log_msgs = []
                def log_cb(msg):
                    status_text.write(f"**Status:** {msg}")
                    log_msgs.append(msg)
                    log_container.markdown("\n\n".join([f"`{m}`" for m in log_msgs]))
                        
                def progress_cb(val):
                    progress_bar.progress(val)
                
                from fsms_logic import FSMSFetcher
                hardcoded_session_id = "155aa70338de898c5a16b6b45c9399fa"
                hardcoded_cookie = "_ga=GA1.3.301266867.1748954739; _ga_3JE4R8NPJQ=GS2.1.s1765772355$o9$g1$t1765772575$j60$l0$h0; 155aa70338de898c5a16b6b45c9399fa=95878; 95878=7145996093"
                fetcher = FSMSFetcher(cookie_string=hardcoded_cookie, session_id=hardcoded_session_id)
                
                st.session_state.fsms_scanned_data = fetcher.prepare_bulk_data(text_input, hardcoded_session_id, log_cb=log_cb, progress_cb=progress_cb)
                
                # Pre-populate selections: if only 1 part, auto-select it.
                st.session_state.fsms_selections = {}
                for tid, data in st.session_state.fsms_scanned_data.items():
                    if len(data["parts"]) == 1:
                        st.session_state.fsms_selections[tid] = [data["parts"][0]]
                    else:
                        st.session_state.fsms_selections[tid] = []

    with col2:
        if st.button("🗑️ Reset Tool", use_container_width=True):
            st.session_state.fsms_scanned_data = None
            st.session_state.fsms_selections = {}
            st.rerun()

    if st.session_state.fsms_scanned_data:
        st.divider()
        st.subheader("🛠️ Part Selection Checkpoint")
        st.write("For tickets with multiple parts, please select the ones you want to include (up to 3).")

        for tid, data in st.session_state.fsms_scanned_data.items():
            parts = data["parts"]
            if not parts:
                st.info(f"Ticket **{tid}**: No spare parts found. Jobsheet will be printed blank.")
                continue

            if len(parts) == 1:
                st.success(f"Ticket **{tid}**: Found 1 part. (Auto-selected)")
                # Already selected in pre-populate
            else:
                st.info(f"Ticket **{tid}**: {len(parts)} parts found. Please select:")
                options = [f"Part #{i+1} - {p['item_name']} ({p['part_no']})" for i, p in enumerate(parts)]
                
                # Determine current selections labels
                curr_sel = st.session_state.fsms_selections.get(tid, [])
                default_labels = []
                for p in curr_sel:
                    for i, orig_p in enumerate(parts):
                        if p == orig_p:
                            default_labels.append(f"Part #{i+1} - {orig_p['item_name']} ({orig_p['part_no']})")
                            break

                selected_labels = st.multiselect(
                    f"Select parts for {tid}",
                    options=options,
                    default=default_labels,
                    key=f"sel_{tid}",
                    max_selections=3
                )
                
                # Map labels back to part objects
                new_sel_objs = []
                for label in selected_labels:
                    idx = int(label.split('#')[1].split(' ')[0]) - 1
                    new_sel_objs.append(parts[idx])
                st.session_state.fsms_selections[tid] = new_sel_objs

        st.divider()
        if st.button("🚀 Generate Final Jobsheet PDF", type="primary", use_container_width=True):
            status_text = st.empty()
            def log_cb(msg):
                status_text.write(f"**PDF Engine:** {msg}")

            from fsms_logic import FSMSFetcher
            hardcoded_session_id = "155aa70338de898c5a16b6b45c9399fa"
            hardcoded_cookie = "_ga=GA1.3.301266867.1748954739; _ga_3JE4R8NPJQ=GS2.1.s1765772355$o9$g1$t1765772575$j60$l0$h0; 155aa70338de898c5a16b6b45c9399fa=95878; 95878=7145996093"
            fetcher = FSMSFetcher(cookie_string=hardcoded_cookie, session_id=hardcoded_session_id)

            pdf_path = fetcher.generate_pdf_from_selections(
                st.session_state.fsms_scanned_data, 
                st.session_state.fsms_selections, 
                log_cb=log_cb
            )

            if pdf_path:
                st.success("✅ PDF Built successfully!")
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="⬇️ Download Final PDF",
                        data=pdf_file.read(),
                        file_name="FSMS_JobSheets_Export.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.error("Failed to generate PDF.")

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
    st.markdown("Customize your isolated Toolbelt environment. Changes are saved locally.")
    
    c = st.session_state.config
    
    with st.expander("👤 User Identity", expanded=True):
        new_name = st.text_input("Display Name", value=c.get('display_name', ''))
        new_id = st.text_input("Employee ID", value=c.get('employee_id', ''))
        
    with st.expander("📡 Network Config", expanded=True):
        new_timeout = st.slider("Connection Timeout (Seconds)", min_value=1, max_value=60, value=int(c.get('conn_timeout', 10)))
        new_heartbeat = st.toggle("Auto-Test Heartbeat", value=bool(c.get('heartbeat', True)))
        
    with st.expander("🎨 Appearance", expanded=True):
        themes = ["Neon Cyan", "Electric Purple", "CTC Blue"]
        curr_theme = c.get('accent_color', 'Neon Cyan')
        new_color = st.selectbox("Accent Color", options=themes, index=themes.index(curr_theme) if curr_theme in themes else 0)
        
    with st.expander("🗑️ Storage Initialization", expanded=False):
        st.warning("Warning: This will permanently delete all temporary and generated files tracked locally.")
        del_confirm = st.text_input("Type 'deleteall' to confirm wipe:")
        if st.button("Wipe Local Temp Folder", type="primary"):
            if del_confirm.strip() == "deleteall":
                folders = ["temp_processing"]
                deleted_count = 0
                for folder in folders:
                    target_path = os.path.join(os.getcwd(), folder)
                    if os.path.exists(target_path):
                        for item in os.listdir(target_path):
                            item_path = os.path.join(target_path, item)
                            try:
                                if os.path.isfile(item_path):
                                    os.remove(item_path)
                                elif os.path.isdir(item_path):
                                    shutil.rmtree(item_path)
                                deleted_count += 1
                            except Exception:
                                pass
                st.success(f"Successfully purged {deleted_count} items from system caches.")
            else:
                st.error("Text did not match 'deleteall'. Aborted.")
                
    st.divider()
    
    if st.button("Save Configuration & Reload"):
        c['display_name'] = new_name
        c['employee_id'] = new_id
        c['conn_timeout'] = new_timeout
        c['heartbeat'] = new_heartbeat
        c['accent_color'] = new_color
        
        save_config(c)
        st.session_state.config = c
        st.success("Configuration successfully persisted!")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

def main():
    if not os.path.exists(CONFIG_PATH):
        st.title("🚀 Welcome to the Company Toolbelt")
        st.markdown("It looks like this is your first time launching the tool on this environment. Please initialize your profile constraints.")
        with st.form("setup_form"):
            user = st.text_input("Display Name (e.g. Marcus)")
            emp_id = st.text_input("Employee ID (e.g. CTC-001)")
            submit = st.form_submit_button("Complete Setup")
            if submit:
                if user.strip() and emp_id.strip():
                    new_conf = load_config()
                    new_conf['display_name'] = user
                    new_conf['employee_id'] = emp_id
                    save_config(new_conf)
                    st.session_state.config = new_conf
                    st.rerun()
                else:
                    st.error("Please fill in both fields.")
        return

    render_sidebar()
    
    page = st.session_state.current_page
    
    if page == "🏠 Home / Dashboard":
        render_home()
    elif page == "📄 Jobsheet Generator":
        render_fsms_tool()
    elif page == "💻 HP Model Checker":
        render_warranty_tool()
    elif page == "🔍 Serial Number Grabber (Dell OPP)":
        render_serial_grabber()
    elif page == "📑 Bulk eFSR downloader":
        from efsr_grabber import render_efsr_tool
        render_efsr_tool()
    elif page == "⚙️ Global Settings / Profile":
        render_settings()

if __name__ == "__main__":
    main()
