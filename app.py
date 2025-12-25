import streamlit as st
import os
import tempfile
from src.pipeline import MediSyncPipeline

from src.auth import login_form, check_subscription, create_portal_session



st.set_page_config(page_title="MediSync SaaS", page_icon="🏥", layout="wide")

# --- CSS for Production Polish (INJECTED FIRST TO PREVENT FLASH) ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main {
        background-color: #f8f9fc;
    }

    /* HIDE STREAMLIT BRANDING & UI ELEMENTS */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* Hide Fullscreen Button on Images/Plots */
    button[title="View fullscreen"], 
    [data-testid="StyledFullScreenButton"],
    [data-testid="stImage"] button {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Hide the top-right decoration/deploy button if visible */
    .stDeployButton, [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide the Status Widget (top right running man) */
    .stStatusWidget {
        visibility: hidden !important;
    }
    
    /* Hide Streamlit Toolbar */
    [data-testid="stToolbar"] {
        display: none !important;
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0f172a; /* Slate 900 */
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    p, label, .stMarkdown {
        color: #334155; /* Slate 700 */
    }
    
    /* Modern Input Fields */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Fluid 'Squicle' Button Style (Brightened) */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); 
        color: #ffffff !important; 
        border: none;
        padding: 0.8rem 1.5rem;
        font-size: 16px;
        font-weight: 600;
        letter-spacing: 0.3px;
        border-radius: 12px; 
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2), 0 2px 4px -1px rgba(37, 99, 235, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stButton > button p, .stButton > button * {
        color: #ffffff !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3), 0 4px 6px -2px rgba(37, 99, 235, 0.15);
        color: #ffffff !important;
    }
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
    }
    
    /* Sidebar Modernization */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        box-shadow: 4px 0 24px rgba(0,0,0,0.02);
        border-right: 1px solid #f1f5f9;
        padding-top: 2rem;
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 2rem;
    }
    
    /* Alerts */
    .stAlert {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e40af;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION GATE ---
# This must run before anything else to protect the app
user = login_form()
if not user:
    st.stop()

# COMPATIBILITY FIX: Ensure user is an object, not a dict (handles legacy session state)
import types
if isinstance(user, dict):
    user = types.SimpleNamespace(**user)

# Check Subscription
is_subscribed = check_subscription(user.email)
if not is_subscribed:
    payment_link = st.secrets.get("STRIPE_PAYMENT_LINK", "https://stripe.com")
    
    st.warning("💳 Subscription Required")
    st.markdown("Your 7-day free trial has expired or you do not have an active subscription.")
    st.markdown(f"[Manage Subscription]({payment_link})") 
    st.stop()



# Initialize Page State
if "page" not in st.session_state:
    st.session_state.page = "generator"

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/policy-document.png", width=60)
    st.markdown("### **MediSync** | Enterprise")
    st.caption("v1.2.0 • HIPAA Compliant Environment")
    
    # 3. User Info in Sidebar
    st.markdown(f"**Logged in as:** `{user.email}`")
    if st.sidebar.button("Logout", type="primary"):
        st.session_state.user = None
        st.rerun()

    # Manage Subscription Button (Only if logged in)
    if st.sidebar.button("💳 Manage Billing"):
        portal_url = create_portal_session(user.email)
        if portal_url:
            st.markdown(f'<meta http-equiv="refresh" content="0;url={portal_url}">', unsafe_allow_html=True)
        else:
            st.sidebar.error("Could not create billing portal.")
            
    st.markdown("---")
    
    # 1. API Key
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        # Removed "Secure Connection Active" alert to prevent flash
    else:
        api_key = st.text_input("Enter API Key", type="password", help="Enter your Groq API Key for secure processing.")

    st.markdown("---")
    st.subheader("👤 Advocate Profile")
    
    with st.expander("Edit Advocate Details", expanded=True):
        # 2. Advocate Inputs (To fill placeholders)
        advocate_name = st.text_input("Full Name", value="Your Name")
        advocate_title = st.text_input("Title", value="Medical Billing Advocate")
        advocate_address = st.text_area("Facility / Address", value="Mailing Address")

# --- Main Generator Logic ---
st.title("📑 Insurance Appeal Generator")
st.markdown("""
    **Securely process denial letters.** Upload the insurance denial PDF to generate a formal, evidence-based appeal letter automatically drafted by our secure HIPAA-compliant engine.
""")
st.markdown("---")

if not api_key:
    st.warning("⚠️ Authentication Required. Please enter your API credentials in the sidebar.")
    st.stop()

# Initialize Cached Pipeline (Lazy Load)
@st.cache_resource
def get_pipeline(api_key):
    if not api_key:
        return None
    return MediSyncPipeline(api_key)

# Initialize Session State to hold data across re-runs
if "appeal_result" not in st.session_state:
    st.session_state["appeal_result"] = None

uploaded_file = st.file_uploader("Upload Denial Letter", type=["pdf"])

# If a new file is uploaded, clear previous results
if uploaded_file and st.session_state["appeal_result"] and st.session_state["appeal_result"]["filename"] != uploaded_file.name:
    st.session_state["appeal_result"] = None

if uploaded_file:
    # We use a button to trigger processing
    if st.button("Draft Appeal"):
        with st.spinner("Analyzing Medical Policy & Drafting..."):
            try:
                # 1. Save to Temp File
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                # 2. Run Pipeline (PASSING THE SIDEBAR DATA NOW)
                pipeline = get_pipeline(api_key)
                result = pipeline.process_file(tmp_path, advocate_details={
                    "name": advocate_name,
                    "title": advocate_title,
                    "address": advocate_address
                })
                
                # 3. SAVE TO SESSION STATE
                st.session_state["appeal_result"] = {
                    "draft": result['draft'],
                    "context": result['context'],
                    "filename": uploaded_file.name
                }
                
                # Cleanup
                os.unlink(tmp_path)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Display Result (If it exists in memory)
    if st.session_state["appeal_result"]:
        res = st.session_state["appeal_result"]
        
        st.success("✅ Appeal Generated!")
        st.balloons()
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.text_area("Original Context", value=res['context'], height=300, disabled=True)
        with col2:
            # We let the user edit this text area, but we don't save the edits back to state yet for simplicity
            final_draft = st.text_area("Appeal Draft", value=res['draft'], height=500)
            
            st.download_button(
                label="Download Text File",
                data=final_draft,
                file_name=f"{res['filename']}_APPEAL.txt",
                mime="text/plain"
            )