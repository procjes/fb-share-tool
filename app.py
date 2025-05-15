import streamlit as st
import aiohttp
import asyncio
import re
import time
import requests
import json
import uuid
import random
import httpx
import string
from bs4 import BeautifulSoup
from rich import print as rp

# Page config with custom theme
st.set_page_config(
    page_title="FB Share Tool",
    page_icon="🌀",
    layout="wide"
)

# Custom CSS for unique aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300;400;500;600;700&family=Roboto:wght@300;400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif !important;
        letter-spacing: 0.5px;
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        font-family: 'Roboto', monospace !important;
        font-size: 14px !important;
        background-color: rgba(0, 0, 0, 0.1) !important;
        color: #e0e0e0 !important;
        border-radius: 6px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stTextInput>label, .stTextArea>label, .stSlider>label {
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #e0e0e0 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    
    .main-header {
        background: linear-gradient(90deg, #8A2387 0%, #E94057 50%, #F27121 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3.5rem;
        margin-bottom: 0;
        text-align: center;
        font-family: 'Montserrat', sans-serif !important;
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #a0a0a0;
        margin-top: 0;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 300;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .input-container {
        background: rgba(30, 30, 30, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
        margin-bottom: 30px;
    }
    
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 20px;
        letter-spacing: 1px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
    }
    
    .section-title:after {
        content: "";
        flex-grow: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(233, 64, 87, 0.5) 0%, rgba(255, 255, 255, 0) 100%);
        margin-left: 10px;
    }
    
    .stat-box {
        background: linear-gradient(135deg, rgba(138, 35, 135, 0.9) 0%, rgba(233, 64, 87, 0.9) 100%);
        color: white;
        padding: 20px 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        margin: 10px 0;
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stat-box h3 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600;
        letter-spacing: 1px;
        font-size: 14px;
        margin-bottom: 10px;
        text-transform: uppercase;
        opacity: 0.9;
    }
    
    .footer {
        text-align: center;
        color: #a0a0a0;
        font-size: 0.8rem;
        margin-top: 40px;
        font-weight: 300;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #8A2387 0%, #E94057 50%, #F27121 100%);
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        font-size: 14px !important;
        margin-top: 15px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    .stButton>button:active {
        transform: translateY(1px) !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #8A2387 0%, #E94057 50%, #F27121 100%) !important;
        height: 8px !important;
        border-radius: 4px !important;
    }
    
    .stProgress > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        height: 8px !important;
        border-radius: 4px !important;
    }
    
    .success-msg {
        color: #38ef7d;
        font-weight: 500;
        font-family: 'Roboto', monospace !important;
        font-size: 14px;
        letter-spacing: 0.5px;
        padding: 5px 10px;
        border-radius: 4px;
        background-color: rgba(56, 239, 125, 0.1);
        border-left: 3px solid #38ef7d;
        margin: 5px 0;
    }
    
    .error-msg {
        color: #ff6b6b;
        font-weight: 500;
        font-family: 'Roboto', monospace !important;
        font-size: 14px;
        letter-spacing: 0.5px;
        padding: 5px 10px;
        border-radius: 4px;
        background-color: rgba(255, 107, 107, 0.1);
        border-left: 3px solid #ff6b6b;
        margin: 5px 0;
    }
    
    /* Custom expander styling */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 15px !important;
        color: #e0e0e0 !important;
        letter-spacing: 1px !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
    }
    
    .streamlit-expanderContent {
        background-color: rgba(0, 0, 0, 0.2) !important;
        border-radius: 0 0 8px 8px !important;
        padding: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Remove default Streamlit margins and paddings */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# App header with custom gradient style
st.markdown("<div style='margin-bottom: 40px;'><h1 class='main-header'>FB SHARE</h1></div>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>sharing automation</p>", unsafe_allow_html=True)

# Store sharing state in session
if 'sharing_active' not in st.session_state:
    st.session_state.sharing_active = False
if 'share_count' not in st.session_state:
    st.session_state.share_count = 0
if 'target_count' not in st.session_state:
    st.session_state.target_count = 0
if 'share_logs' not in st.session_state:
    st.session_state.share_logs = []
if 'current_post' not in st.session_state:
    st.session_state.current_post = None
if 'current_token' not in st.session_state:
    st.session_state.current_token = None
if 'current_cookie' not in st.session_state:
    st.session_state.current_cookie = None
if 'share_success_rate' not in st.session_state:
    st.session_state.share_success_rate = 0
if 'sharing_complete' not in st.session_state:
    st.session_state.sharing_complete = False

# Main function to execute the share operation
def Execute(cookie, post, share_count, delay):
    # Update session state
    st.session_state.sharing_active = True
    st.session_state.target_count = share_count
    st.session_state.current_post = post
    st.session_state.current_cookie = cookie
    st.session_state.share_logs = []
    st.session_state.share_count = 0
    st.session_state.share_success_rate = 0
    st.session_state.sharing_complete = False
    
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }
    
    class Share:
        async def get_token(self, session):
            try:
                head['cookie'] = cookie
                async with session.get('https://business.facebook.com/content_management', headers=head) as response:
                    data = await response.text()
                    token_match = re.search('EAAG(.*?)","', data)
                    if token_match:
                        access_token = 'EAAG' + token_match.group(1)
                        st.session_state.current_token = access_token
                        return access_token, head['cookie']
                    else:
                        log_error("Could not extract access token. Please verify your cookie.")
                        return None, None
            except Exception as er:
                log_error(f"Authentication failed: {str(er)}")
                return None, None
                
        async def share(self, session, token, cookie):
            ji = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Windows",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "cookie": cookie,
                "accept-encoding": "gzip, deflate",
                "host": "b-graph.facebook.com"
            }
            
            count = st.session_state.share_count
            target = st.session_state.target_count
            
            while count < target and st.session_state.sharing_active:
                time.sleep(delay)
                # Use URL with appropriate parameters
                endpoint = "https://b-graph.facebook.com/v13.0/me/feed"
                share_url = f'{endpoint}?link={post}&published=0&access_token={token}'
                
                try:
                    async with session.post(share_url, headers=ji) as response:
                        data = await response.json()
                        if 'id' in data:
                            count += 1
                            st.session_state.share_count = count
                            st.session_state.share_success_rate = int((count / target) * 100)
                            
                            # Add log entry with timestamp
                            current_time = time.strftime("%H:%M:%S", time.localtime())
                            post_id_preview = data['id'][:8] if len(data['id']) > 8 else data['id']
                            log_msg = f"[{current_time}] Share #{count} successful! Post ID: {post_id_preview}..."
                            st.session_state.share_logs.append({"type": "success", "message": log_msg})
                            
                            # Force a rerun every 5 shares to update UI
                            if count % 5 == 0:
                                st.rerun()
                        else:
                            error_msg = data.get('error', {}).get('message', 'Unknown error')
                            log_error(f"Sharing blocked. Reason: {error_msg}. Total successful: {count}")
                            st.session_state.sharing_active = False
                            st.session_state.sharing_complete = True
                            st.rerun()
                            return
                except Exception as e:
                    log_error(f"Error during sharing process: {str(e)}")
                    st.session_state.sharing_active = False
                    st.session_state.sharing_complete = True
                    st.rerun()
                    return
            
            st.session_state.sharing_active = False
            st.session_state.sharing_complete = True
            st.rerun()
    
    # Function to log errors
    def log_error(message):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        st.session_state.share_logs.append({"type": "error", "message": f"[{current_time}] {message}"})
    
    async def main(num_tasks): 
        async with aiohttp.ClientSession() as session:
            share = Share()
            token_result = await share.get_token(session)
            
            if token_result[0] is None:
                st.session_state.sharing_active = False
                return
                
            token, cookie = token_result
            tasks = []
            for i in range(num_tasks):
                task = asyncio.create_task(share.share(session, token, cookie))
                tasks.append(task)
            await asyncio.gather(*tasks)
    
    # Run the sharing process asynchronously
    asyncio.run(main(1))

# Function to check if cookie is valid
def cCheck(cookie):
    try:
        # Check if cookie format appears valid
        if 'c_user' in cookie and len(cookie) > 50:
            return True
        return False
    except:
        return False

# Main content in a sleek container
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

# Display section title with gradient line
st.markdown("<h2 class='section-title'>🔧 CONFIGURATION</h2>", unsafe_allow_html=True)

# Create a cleaner 2-column layout
left_col, right_col = st.columns([2, 1])

with left_col:
    # Cookie input with monospace styling
    COOKIE = st.text_area("FACEBOOK COOKIE", 
                          help="Enter your Facebook cookie with c_user value",
                          placeholder="Paste your cookie string here...",
                          key='cookie_input')
    
    POST = st.text_input("POST URL", 
                         help="Facebook post URL to share",
                         placeholder="https://www.facebook.com/username/posts/123456789",
                         key='post_input')

with right_col:
    st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
    
    COUNT = st.slider("SHARES", 
                      min_value=1, max_value=1000, 
                      value=50,
                      help="How many times to share the post",
                      key='count_input')
    
    DELAY = st.slider("DELAY", 
                     min_value=0, max_value=30, 
                     value=2,
                     help="Time between shares in seconds",
                     key='delay_input')

st.markdown("</div>", unsafe_allow_html=True)

# Function to get cookie from credentials
def get_cookie(user, passw):
    accessToken = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
    data = {
        'adid': str(uuid.uuid4()),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'cpl': 'true',
        'family_device_id': str(uuid.uuid4()),
        'credentials_type': 'device_based_login_password',
        'error_detail_type': 'button_with_disabled',
        'source': 'device_based_login',
        'email': user,
        'password': passw,
        'access_token': accessToken,
        'generate_session_cookies': '1',
        'meta_inf_fbmeta': '',
        'advertiser_id': str(uuid.uuid4()),
        'currently_logged_in_userid': '0',
        'locale': 'en_US',
        'client_country_code': 'US',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
        'api_key': '62f8ce9f74b12f84c123cc23437a4a32'
    }
    headers = {
        'User-Agent': "[FBAN/FB4A;FBAV/196.0.0.29.99;FBPN/com.facebook.katana;FBLC/en_US;FBBV/135374479;FBCR/SMART;FBMF/samsung;FBBD/samsung;FBDV/SM-A720F;FBSV/8.0.0;FBCA/armeabi-v7a:armeabi;FBDM={density=3.0,width=1080,height=1920};FB_FW/1;]",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'graph.facebook.com',
        'X-FB-Net-HNI': str(random.randint(10000, 99999)),
        'X-FB-SIM-HNI': str(random.randint(10000, 99999)),
        'X-FB-Connection-Type': 'MOBILE.LTE',
        'X-Tigon-Is-Retry': 'False',
        'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;nc=1;fc=0;bc=0;cid=62f8ce9f74b12f84c123cc23437a4a32',
        'x-fb-device-group': str(random.randint(1000, 9999)),
        'X-FB-Friendly-Name': 'ViewerReactionsMutation',
        'X-FB-Request-Analytics-Tags': 'graphservice',
        'X-FB-HTTP-Engine': 'Liger',
        'X-FB-Client-IP': 'True',
        'X-FB-Connection-Bandwidth': str(random.randint(20000000, 30000000)),
        'X-FB-Server-Cluster': 'True',
        'x-fb-connection-token': '62f8ce9f74b12f84c123cc23437a4a32'
    }
    
    try:
        # Make the request to get the cookie
        response = httpx.post("https://b-graph.facebook.com/auth/login", headers=headers, data=data, follow_redirects=False).json()
        
        if "session_key" in response:
            # Format the cookie from the response
            sb_value = ''.join(random.choices(string.ascii_letters+string.digits+'_', k=24))
            cookie_string = f"sb={sb_value};" + ';'.join(i['name']+'='+i['value'] for i in response['session_cookies'])
            token = response['access_token']
            
            return {
                "status": True,
                "cookie": cookie_string,
                "access_token": token
            }
        else:
            return {
                "status": False,
                "message": "Invalid credentials or account checkpoint"
            }
    except Exception as e:
        return {
            "status": False,
            "message": f"Error: {str(e)}"
        }

# Usage tips in a styled expander
with st.expander("⚡ TIPS", expanded=False):
    st.markdown("""
    <ul style="list-style-type: none; padding-left: 0;">
        <li style="margin-bottom: 12px; font-size: 14px; letter-spacing: 0.3px; color: #d0d0d0;">
            <span style="color: #E94057; font-weight: 600;">►</span> 
            Use dummy accounts to avoid triggering Facebook's anti-spam systems
        </li>
        <li style="margin-bottom: 12px; font-size: 14px; letter-spacing: 0.3px; color: #d0d0d0;">
            <span style="color: #E94057; font-weight: 600;">►</span> 
            Verify your cookie contains the essential 'c_user' parameter
        </li>
        <li style="margin-bottom: 12px; font-size: 14px; letter-spacing: 0.3px; color: #d0d0d0;">
            <span style="color: #E94057; font-weight: 600;">►</span> 
            Increase delay time between shares to reduce detection chance
        </li>
    </ul>
    """, unsafe_allow_html=True)

# Cookie getter tab
with st.expander("🔑 GET COOKIE", expanded=False):
    st.markdown("<p style='font-size: 14px; color: #d0d0d0; margin-bottom: 15px;'>Generate cookie from your credentials</p>", unsafe_allow_html=True)
    
    user_col, pass_col = st.columns(2)
    with user_col:
        username = st.text_input("USERNAME/EMAIL", key="cookie_username", placeholder="Enter email or username")
    with pass_col:
        password = st.text_input("PASSWORD", key="cookie_password", type="password", placeholder="Enter password")
    
    if st.button("GENERATE COOKIE", key="generate_cookie_btn"):
        with st.spinner("Authenticating..."):
            result = get_cookie(username, password)
            
            if result["status"]:
                st.success("Authentication successful!")
                st.code(result["cookie"], language=None)
                
                # Create columns for copy buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("COPY COOKIE", key="copy_cookie_btn"):
                        st.write("Cookie copied to clipboard!")
                with col2:
                    if st.button("USE THIS COOKIE", key="use_cookie_btn"):
                        st.session_state.cookie_input = result["cookie"]
                        st.success("Cookie added to the share tool!")
            else:
                st.error(f"Failed: {result['message']}")

# Submit button with custom styling and icon
submit_button = st.button("▶︎ START ENGINE", 
                         use_container_width=True,
                         key="submit_button")

# Display sharing progress if active
if st.session_state.sharing_active or st.session_state.sharing_complete:
    # Create a stylish results container with custom header
    st.markdown("""
    <div style='background: rgba(20, 20, 20, 0.7); 
               border-radius: 12px; 
               padding: 25px; 
               margin-top: 25px;
               border: 1px solid rgba(233, 64, 87, 0.3);
               box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);'>
    """, unsafe_allow_html=True)
    
    # Custom operation title
    st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <div style='background: linear-gradient(135deg, #8A2387 0%, #E94057 100%); 
                    width: 30px; 
                    height: 30px; 
                    border-radius: 15px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    margin-right: 10px;
                    box-shadow: 0 4px 10px rgba(233, 64, 87, 0.3);'>
            <span style='color: white; font-weight: bold; font-size: 16px;'>⚡</span>
        </div>
        <h2 style='margin: 0; 
                  font-size: 20px; 
                  font-weight: 600; 
                  color: white;
                  letter-spacing: 1px;
                  text-transform: uppercase;'>OPERATION STATUS</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Display stats
    stats_cols = st.columns([1, 1, 1])
    with stats_cols[0]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(138, 35, 135, 0.9) 0%, rgba(233, 64, 87, 0.9) 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
                    margin: 10px 0;">
            <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; margin-bottom: 5px;">TARGET</div>
            <div style="font-size: 24px; font-weight: 700;">{st.session_state.target_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[1]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(138, 35, 135, 0.9) 0%, rgba(233, 64, 87, 0.9) 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
                    margin: 10px 0;">
            <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; margin-bottom: 5px;">COMPLETED</div>
            <div style="font-size: 24px; font-weight: 700;">{st.session_state.share_count}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with stats_cols[2]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(138, 35, 135, 0.9) 0%, rgba(233, 64, 87, 0.9) 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
                    margin: 10px 0;">
            <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; margin-bottom: 5px;">SUCCESS RATE</div>
            <div style="font-size: 24px; font-weight: 700;">{st.session_state.share_success_rate}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    st.markdown('<div style="margin: 25px 0 15px;"><div style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; color: #a0a0a0;">PROGRESS</div></div>', unsafe_allow_html=True)
    
    if st.session_state.target_count > 0:
        progress = st.session_state.share_count / st.session_state.target_count
        st.progress(progress)
    
    # Activity log
    st.markdown('<div style="margin: 25px 0 15px;"><div style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; color: #a0a0a0;">ACTIVITY LOG</div></div>', unsafe_allow_html=True)
    
    # Display logs
    for log in st.session_state.share_logs[-10:]:  # Show last 10 logs only
        if log["type"] == "success":
            st.markdown(f"<p class='success-msg'>{log['message']}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='error-msg'>{log['message']}</p>", unsafe_allow_html=True)
    
    # Status message
    if st.session_state.sharing_complete:
        if st.session_state.share_count == st.session_state.target_count:
            st.markdown(f"<h2 style='text-align:center; color:#38ef7d; margin-top: 20px;'>🎉 All {st.session_state.share_count} shares completed successfully!</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h3 style='text-align:center; color:#ff6b6b; margin-top: 20px;'>Process stopped. Completed {st.session_state.share_count} of {st.session_state.target_count} shares.</h3>", unsafe_allow_html=True)
        
        # Reset button
        if st.button("START NEW OPERATION", key="reset_btn"):
            st.session_state.sharing_active = False
            st.session_state.sharing_complete = False
            st.session_state.share_count = 0
            st.session_state.target_count = 0
            st.session_state.share_logs = []
            st.session_state.current_post = None
            st.session_state.current_token = None
            st.session_state.current_cookie = None
            st.rerun()
    
    # Stop button if sharing is active
    if st.session_state.sharing_active and not st.session_state.sharing_complete:
        if st.button("STOP OPERATION", key="stop_btn"):
            st.session_state.sharing_active = False
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

# Validation and execution
if submit_button and not st.session_state.sharing_active and not st.session_state.sharing_complete:
    if not COOKIE or not POST:
        st.error("MISSING DATA: All fields must be completed")
    elif 'c_user' not in COOKIE:
        st.error("INVALID COOKIE: Must contain 'c_user' parameter")
    elif not POST.startswith('https://www.facebook.com/'):
        st.error("INVALID URL: Must be a Facebook post URL")
    elif not cCheck(COOKIE):
        st.error("AUTHENTICATION FAILED: Please verify your cookie")
    else:
        # Execute sharing operation
        Execute(COOKIE, POST, int(COUNT), int(DELAY))

# Custom footer with gradient separator and sleek design
st.markdown("""
<div style='margin-top: 60px;'>
    <div style='height: 1px; 
               background: linear-gradient(90deg, 
                           rgba(138, 35, 135, 0), 
                           rgba(233, 64, 87, 0.5), 
                           rgba(242, 113, 33, 0)); 
               margin-bottom: 20px;'></div>
    <div class='footer'>FB SHARE · STEALTH MODE · VERSION 2.5</div>
</div>
""", unsafe_allow_html=True)
