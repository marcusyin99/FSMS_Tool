import streamlit as st
import os
import json
import shutil

st.set_page_config(page_title="Company Toolbelt", layout="wide")

CONFIG_PATH = os.path.join(os.getcwd(), "config.json")
DEFAULT_CONFIG = {
    "display_name": "",
    "employee_id": "",
    "conn_timeout": 10,
    "heartbeat": True,
    "accent_color": "Neon Cyan",
    "is_online": False
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

            /* Status Dots */
            .status-dot {
                height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 8px;
            }
            .dot-online { 
                background-color: #00ff00; box-shadow: 0 0 10px #00ff00; 
            }
            .dot-offline { 
                background-color: #888888; 
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

if "is_online" not in st.session_state:
    st.session_state.is_online = st.session_state.config.get("is_online", False)

if "last_presence_sync" not in st.session_state:
    st.session_state.last_presence_sync = 0

from fsms_logic import TeamPresence
# Clean stale records once per session startup
if "already_cleaned" not in st.session_state:
    TeamPresence.clean_stale_records()
    st.session_state.already_cleaned = True

def navigate_to(page_name):
    st.session_state.current_page = page_name
    # Sync the sidebar dropdown so it doesn't fight with the dashboard buttons
    tools = [
        "📄 Jobsheet Generator",
        "💻 Multi-Brand Warranty Checker",
        "🔍 Serial Number Grabber (Dell OPP)",
        "📑 Bulk eFSR downloader",
        "📂 Bulk PDF Merger"
    ]
    if page_name in tools:
        st.session_state.tool_select = page_name

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
    
    # 1. High-Level Navigation (Home)
    is_home = (st.session_state.current_page == "🏠 Home / Dashboard")
    if st.sidebar.button("🏠 Home / Dashboard", use_container_width=True, key="home_btn", 
                         type="primary" if is_home else "secondary"):
        st.session_state.current_page = "🏠 Home / Dashboard"
        st.rerun()

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Tools Section
    st.sidebar.markdown("### 🛠️ Core Utilities")
    tools = [
        "📄 Jobsheet Generator",
        "💻 Multi-Brand Warranty Checker",
        "🔍 Serial Number Grabber (Dell OPP)",
        "📑 Bulk eFSR downloader",
        "📂 Bulk PDF Merger"
    ]
    
    # Check if currently on a tool page
    current_tool_index = 0
    if st.session_state.current_page in tools:
        current_tool_index = tools.index(st.session_state.current_page)
    
    def on_tool_change():
        st.session_state.current_page = st.session_state.tool_select
        
    selected_tool = st.sidebar.selectbox(
        "Select a Tool",
        options=tools,
        index=current_tool_index,
        key="tool_select",
        label_visibility="collapsed",
        on_change=on_tool_change
    )

    st.sidebar.divider()
    
    # 3. Team Presence Section (Middle)
    st.sidebar.subheader("Team Status Board")
    team_data = TeamPresence.fetch_team()
    
    if team_data is None:
        st.sidebar.error("⚠️ Team Board Unavailable")
    elif not team_data:
        st.sidebar.info("No one else is online.")
    else:
        from datetime import datetime
        processed_team = []
        for member in team_data:
            m_last_seen = datetime.fromisoformat(member['last_seen'])
            is_active = (datetime.now() - m_last_seen).total_seconds() < 900
            is_online = member['is_visible'] and is_active
            processed_team.append({**member, "online": is_online})
            
        sorted_team = sorted(processed_team, key=lambda x: x['online'], reverse=True)
            
        for member in sorted_team:
            m_name = member['name']
            m_status = member['current_status'] or "Active"
            m_emp_id = member['emp_id']
            is_online = member['online']
            is_self = m_emp_id == st.session_state.config.get('employee_id')
            label = f"**{m_name}** {'(You)' if is_self else ''}"
            dot_class = "dot-online" if is_online else "dot-offline"
            display_status = m_status if is_online else "Currently Offline"
            
            with st.sidebar.container(height=250):
                for member in sorted_team:
                    m_name = member['name']
                    m_status = member['current_status'] or "Active"
                    m_emp_id = member['emp_id']
                    is_online = member['online']
                    is_self = m_emp_id == st.session_state.config.get('employee_id')
                    label = f"**{m_name}** {'(You)' if is_self else ''}"
                    dot_class = "dot-online" if is_online else "dot-offline"
                    display_status = m_status if is_online else "Currently Offline"
                    
                    st.markdown(f"""
                        <div style="padding: 6px 10px; background: rgba(255, 255, 255, 0.03); border-radius: 6px; margin-bottom: 6px; border: 1px solid rgba(255,255,255,0.04);">
                            <div style="display: flex; align-items: center; margin-bottom: 2px;">
                                <span class="status-dot {dot_class}"></span>
                                <div style="font-size: 0.85rem; color: #e6f1ff;">{label}</div>
                            </div>
                            <div style="font-size: 0.7rem; opacity: 0.5; margin-left: 18px;">{display_status}</div>
                        </div>
                    """, unsafe_allow_html=True)
            break # Exit outer loop once container is built

    st.sidebar.divider()

    # 4. System Navigation (Settings) at the bottom
    is_settings = (st.session_state.current_page == "⚙️ Global Settings / Profile")
    if st.sidebar.button("⚙️ Settings & Profile", use_container_width=True, key="settings_btn",
                         type="primary" if is_settings else "secondary"):
        st.session_state.current_page = "⚙️ Global Settings / Profile"
        st.rerun()

    # Auth Status (Existing)
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
           DEVELOPED BY MARCUS ENG<br>v1.2.0
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
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    
    with col1:
        st.markdown("#### 📄 Jobsheet Generator")
        st.write("Bulk-print jobsheets and auto-fill spare parts requests.")
        st.button("Open Jobsheet Generator", use_container_width=True, on_click=navigate_to, args=("📄 Jobsheet Generator",))

    with col2:
        st.markdown("#### 💻 Multi-Brand Warranty Checker")
        st.write("Automated bulk model & warranty checker for HP, Lenovo & Dell.")
        st.button("Open Warranty Tool", use_container_width=True, on_click=navigate_to, args=("💻 Multi-Brand Warranty Checker",))

    with col3:
        st.markdown("#### 🔍 S/N Grabber (Dell OPP)")
        st.write("Extract Serial Numbers dynamically from Customer Reference IDs.")
        st.button("Open Grabber", use_container_width=True, on_click=navigate_to, args=("🔍 Serial Number Grabber (Dell OPP)",))
            
    with col4:
        st.markdown("#### 📑 Bulk eFSR downloader")
        st.write("Batch-download eFSR documents directly from ticket IDs.")
        st.button("Open eFSR Grabber", use_container_width=True, on_click=navigate_to, args=("📑 Bulk eFSR downloader",))

    with col5:
        st.markdown("#### 📂 Bulk PDF Merger")
        st.write("Combine multiple PDF files into a single document instantly.")
        st.button("Open PDF Merger", use_container_width=True, on_click=navigate_to, args=("📂 Bulk PDF Merger",))

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
    st.title("💻 Multi-Brand Warranty Checker")
    st.write("Bulk-check warranty status for HP, Lenovo & Dell devices.")
    
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
            info = check_warranty(sn)
            
            full_url = info.get('url') if info.get('url') else "None"
            timestamp = datetime.now().strftime("%H:%M:%S")
            results.append({
                "Time": timestamp, 
                "Brand": info.get('brand', 'Unknown'),
                "S/N": info.get('sn', sn).upper(), 
                "Product Name": info.get('name', 'Unknown'), 
                "Start": info.get('start', 'N/A'),
                "End": info.get('end', 'N/A'),
                "Status": info.get('status', 'N/A'),
                "Official Site": full_url
            })
            
            progress_bar.progress((i + 1) / len(serial_numbers))
            time.sleep(0.3) 
            
        status_text.success(f"✅ {len(serial_numbers)} warranties checked!")
        
        # Enhanced Display with Deep Links and Multi-Brand Data
        st.dataframe(
            results, 
            use_container_width=True,
            column_config={
                "Official Site": st.column_config.LinkColumn(
                    "Official Site",
                    help="Manufacturer Support Page",
                    validate="^https://.*",
                    display_text="View on Official Site ↗"
                ),
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Warranty Status from Manufacturer"
                )
            },
            hide_index=True
        )
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["Time", "Brand", "S/N", "Product Name", "Start", "End", "Status", "Official Site"])
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

def render_pdf_merger():
    st.title("📂 Bulk PDF Merger")
    st.write("Upload multiple PDF files to combine them into a single document. Files will be merged in the order they appear below.")
    
    uploaded_files = st.file_uploader(
        "Select PDF files", 
        type="pdf", 
        accept_multiple_files=True,
        help="You can drag and drop multiple files here."
    )
    
    if uploaded_files:
        st.subheader("Files to Merge")
        # Display list of filenames for verification
        for idx, f in enumerate(uploaded_files):
            st.write(f"{idx + 1}. {f.name} ({(f.size/1024):.1f} KB)")
        
        st.divider()
        
        if st.button("🚀 Merge PDFs", type="primary", use_container_width=True):
            with st.spinner("Merging documents..."):
                try:
                    from fsms_logic import merge_pdfs
                    merged_buffer = merge_pdfs(uploaded_files)
                    
                    st.success("✅ PDFs successfully merged!")
                    st.download_button(
                        label="⬇️ Download Merged PDF",
                        data=merged_buffer,
                        file_name="Merged_Documents.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Failed to merge PDFs. One or more files might be corrupted or protected. Error: {e}")
    else:
        st.info("Please upload at least one PDF file to begin.")

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
    config = st.session_state.config
    
    # Trigger onboarding if fields are blank or just whitespace
    name_val = str(config.get('display_name', '')).strip()
    id_val = str(config.get('employee_id', '')).strip()
    
    if not name_val or not id_val:
        st.title("🚀 Welcome to the Company Toolbelt")
        st.markdown("It looks like your profile is incomplete. Please enter your identity to unlock Toolbelt access.")
        with st.form("setup_form"):
            user = st.text_input("Display Name (e.g. Marcus)", value=name_val)
            emp_id = st.text_input("Employee ID (e.g. 95878)", value=id_val)
            submit = st.form_submit_button("Complete Setup")
            if submit:
                if user.strip() and emp_id.strip():
                    new_conf = config.copy()
                    new_conf['display_name'] = user
                    new_conf['employee_id'] = emp_id
                    save_config(new_conf)
                    st.session_state.config = new_conf
                    st.rerun()
                else:
                    st.error("Please fill in both fields.")
        return

    # Header with visibility toggle
    head_col1, head_col2 = st.columns([5, 1])
    with head_col2:
        is_online = st.toggle("Go Online", value=st.session_state.is_online, key="online_toggle")
        if is_online != st.session_state.is_online:
            st.session_state.is_online = is_online
            # Persist to config.json
            st.session_state.config["is_online"] = is_online
            save_config(st.session_state.config)
            
            # Immediate sync upon toggle change
            TeamPresence.sync_presence(
                st.session_state.config.get('employee_id'),
                st.session_state.config.get('display_name'),
                "Browsing Toolbelt",
                "",
                is_online
            )
            st.rerun()

    # Automatic background presence sync every 5 mins if online
    import time
    if st.session_state.is_online and (time.time() - st.session_state.last_presence_sync > 300):
        TeamPresence.sync_presence(
            st.session_state.config.get('employee_id'),
            st.session_state.config.get('display_name'),
            "Active",
            "",
            True
        )
        st.session_state.last_presence_sync = time.time()

    render_sidebar()
    
    page = st.session_state.current_page
    
    if page == "🏠 Home / Dashboard":
        render_home()
    elif page == "📄 Jobsheet Generator":
        render_fsms_tool()
    elif page == "💻 Multi-Brand Warranty Checker":
        render_warranty_tool()
    elif page == "🔍 Serial Number Grabber (Dell OPP)":
        render_serial_grabber()
    elif page == "📑 Bulk eFSR downloader":
        from efsr_grabber import render_efsr_tool
        render_efsr_tool()
    elif page == "📂 Bulk PDF Merger":
        render_pdf_merger()
    elif page == "⚙️ Global Settings / Profile":
        render_settings()

if __name__ == "__main__":
    main()
