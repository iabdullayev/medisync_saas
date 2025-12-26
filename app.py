import streamlit as st
import os
import tempfile
from src.pipeline import MediSyncPipeline

from src.auth import login_form, check_subscription, create_portal_session



st.set_page_config(page_title="MediSync SaaS", page_icon="🏥", layout="wide")

# --- CSS for Production Polish (INJECTED FIRST TO PREVENT FLASH) ---
# --- CSS for Production Polish (DISABLED FOR DEBUGGING) ---
# st.markdown("""
#     <link rel="preconnect" href="https://fonts.googleapis.com">
#     ...
# """, unsafe_allow_html=True)

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
    # 1. API Key
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
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
    # st.warning("⚠️ Authentication Required. Please enter your API credentials in the sidebar.")
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