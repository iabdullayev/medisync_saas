import streamlit as st
import time
import re
import string
from supabase import create_client, Client
import stripe

# Initialize specific to this module so it doesn't break if keys are missing initially
def init_services():
    # Load secrets safely
    SUPABASE_URL = st.secrets.get("SUPABASE_URL")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
    STRIPE_KEY = st.secrets.get("STRIPE_API_KEY")
    
    if not SUPABASE_URL or not SUPABASE_KEY or not STRIPE_KEY:
        st.warning("⚠️ Monetization keys missing in secrets.toml. Please configure Supabase & Stripe.")
        return None, None

    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.warning(f"⚠️ Auth Error: Invalid Supabase Credentials. ({str(e)})")
        print(f"Supabase Init Error: {e}")
        return None, None

    stripe.api_key = STRIPE_KEY
    return supabase, stripe

def landing_page_css():
    st.markdown("""
        <style>
        /* Lighter, Dreamy Purple Gradient */
        .stApp {
            background: linear-gradient(135deg, #4c1d95 0%, #8b5cf6 40%, #ddd6fe 100%);
            background-attachment: fixed;
        }
        
        /* Typography - White with correct weights */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
        html, body, [class*="css"], .stMarkdown, .stButton {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #ffffff !important;
        }

        /* Nav Buttons (Top Right) */
        div[data-testid="column"] button {
            backdrop-filter: blur(10px);
            border-radius: 12px;
            transition: all 0.2s;
        }
        div[data-testid="column"] button:hover {
            transform: translateY(-2px);
        }
        
        /* Specific Fix for Dialog Text visibility (Markdown content) */
        div[role="dialog"] p, div[role="dialog"] span, div[role="dialog"] div {
            color: #1f2937 !important;
        }
        
        /* Header Logo Brightness */
        h3 {
            color: white !important;
            text-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        /* Hero Headlines */
        .hero-title {
            font-size: 5rem;
            font-weight: 800;
            line-height: 1.1;
            text-align: center;
            background: linear-gradient(to bottom, #ffffff 40%, #e9d5ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            filter: drop-shadow(0 0 30px rgba(124, 58, 237, 0.5));
        }
        
        /* Glass Cards for Features */
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 2rem;
            height: 100%;
            transition: transform 0.3s ease;
        }
        .glass-card h3 {
             margin-top: 0;
        }
        .glass-card:hover {
             transform: translateY(-5px);
             background: rgba(255, 255, 255, 0.15);
        }

        /* Inputs - Fix Visibility inside Dialogs */
        .stTextInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.9) !important;
            color: #1e1b4b !important;
            border-radius: 10px;
            border: 1px solid #ccc;
            padding: 10px 15px;
        }
        
        /* --- BUTTON STYLES --- */
        
        /* 1. Default Buttons (Footer Links) -> Ghost Style */
        .stButton > button {
            background: transparent !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            color: #ffffff !important;
            box-shadow: none !important;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background: rgba(255, 255, 255, 0.1) !important;
            border-color: #ffffff !important;
            transform: translateY(-2px);
        }
        .stButton > button p {
             color: #ffffff !important;
        }

        /* 2. Primary Buttons (Login / Signup) -> Blue Pill Style */
        /* Target buttons with specific kind or class if possible, or fallback to the specific columns */
        div[data-testid="column"] .stButton > button[kind="primary"],
        button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important; 
            color: #ffffff !important; 
            border: none !important;
            padding: 0.6rem 1.2rem;
            border-radius: 9999px !important;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
        }
        div[data-testid="column"] .stButton > button[kind="primary"]:hover,
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            box-shadow: 0 8px 15px rgba(37, 99, 235, 0.4) !important;
            transform: translateY(-2px);
        }
        
        /* Hide Decorations */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)


# --- SECURITY VALIDATORS ---
def validate_email(email):
    # RFC 5322 compliant regex for email validation
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."
    if not any(char in string.punctuation for char in password):
        return False, "Password must contain at least one special character (!@#$%^&*)."
    return True, ""

# --- HELPER: FRIENDLY ERRORS ---
def format_error_message(e):
    msg = str(e).lower()
    if "invalid login credentials" in msg:
        return "Incorrect email or password."
    if "user already registered" in msg:
        return "This email is already registered. Please log in."
    if "email address" in msg and "invalid" in msg:
        return "Please enter a valid email address."
    if "password" in msg and "character" in msg:
        return "Password does not meet requirements."
    if "rate limit" in msg:
        return "Too many attempts. Please try again later."
    return "Something went wrong. Please try again."

@st.dialog("Log In")
def login_dialog():
    supabase, _ = init_services()
    import types
    
    email = st.text_input("Email", key="login_email").strip()
    password = st.text_input("Password", type="password", key="login_pass").strip()
    
    if st.button("Sign In", type="primary", use_container_width=True):
         # Input Validation
         if not email or not password:
             st.markdown(f"<small style='color: #ef4444; font-weight: 500;'>⚠️ Please enter both email and password.</small>", unsafe_allow_html=True)
             return
             
         if not validate_email(email):
             st.markdown(f"<small style='color: #ef4444; font-weight: 500;'>⚠️ Invalid email format.</small>", unsafe_allow_html=True)
             return

         if not supabase:
             # Dev Fallback
             st.session_state.user = types.SimpleNamespace(email="dev@local.com", id="dev_123")
             st.rerun()
         else:
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                # Friendly Error
                friendly_msg = format_error_message(e)
                st.markdown(f"<small style='color: #ef4444; font-weight: 500;'>⚠️ {friendly_msg}</small>", unsafe_allow_html=True)

@st.dialog("Start Free Trial")
def signup_dialog():
    supabase, _ = init_services()
    
    st.markdown("Create an account to start your **7-day free trial**.")
    new_email = st.text_input("Email Address", key="signup_email").strip()
    
    # Real-time Email Validation
    if new_email and not validate_email(new_email):
        st.markdown(f"<small style='color: #ef4444; font-weight: 500;'>⚠️ Invalid email address</small>", unsafe_allow_html=True)
        
    new_pass = st.text_input("Password", type="password", key="signup_pass").strip()
    
    # Real-time Password Validation Feedback
    if new_pass:
        is_valid_pass, rules_msg = validate_password(new_pass)
        if not is_valid_pass:
            # Subtle text error instead of big box
            st.markdown(f"<small style='color: #ef4444; font-weight: 500;'>⚠️ {rules_msg}</small>", unsafe_allow_html=True)
        else:
             st.markdown(f"<small style='color: #22c55e; font-weight: 500;'>✅ Strong password</small>", unsafe_allow_html=True)
    else:
        st.caption("Requirements: 8+ chars, 1 number, 1 special char (!@#$%^&*)")
    
    if st.button("Create Account & Start Trial", type="primary", use_container_width=True):
         # Input Validation checks (Submit time)
         if not validate_email(new_email):
             return # Already shown

         is_valid_pass, rules_msg = validate_password(new_pass)
         if not is_valid_pass:
             return # Already shown

         if supabase:
            try:
                supabase.auth.sign_up({"email": new_email, "password": new_pass})
                st.success("✅ Confirmation email sent! Please check your inbox.")
            except Exception as e:
                friendly_msg = format_error_message(e)
                st.markdown(f"<small style='color: #ef4444; font-weight: 500;'>⚠️ {friendly_msg}</small>", unsafe_allow_html=True)

# --- MODALS FOR FOOTER LINKS ---
from src.security_content import get_about_content, get_addendum_content, get_compliance_content

@st.dialog("About MediSync")
def about_modal():
    st.markdown(get_about_content(), unsafe_allow_html=True)

@st.dialog("Data Security Addendum")
def addendum_modal():
    st.markdown(get_addendum_content(), unsafe_allow_html=True)

@st.dialog("Security Compliance")
def compliance_modal():
    st.markdown(get_compliance_content(), unsafe_allow_html=True)

def login_form():
    """Draws the Landing Page and triggers Dialogs."""
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        return st.session_state.user

    landing_page_css()

    # --- TOP NAV ---
    nav_col1, nav_col2, nav_col3 = st.columns([0.65, 0.15, 0.2])
    with nav_col1:
         st.markdown("### ⚡ **MediSync** | SaaS")
    
    with nav_col2:
        if st.button("Log In", type="primary", use_container_width=True):
            login_dialog()
            
    with nav_col3:
        if st.button("Start Free Trial", type="primary", use_container_width=True):
             signup_dialog()

    st.markdown("<br><br>", unsafe_allow_html=True) # Spacer

    # --- HERO CONTENT ---
    st.markdown('<div class="hero-title">Turn Denials into<br>Approvals.</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#e9d5ff; margin-bottom:4rem; font-weight:400;'>Generative AI for medical billing advocates.</h3>", unsafe_allow_html=True)
    
    # FEATURE GRID
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        <div class="glass-card">
            <h3>🔒 HIPAA Secure</h3>
            <p style="color:#f3f4f6; font-size:0.9rem;">Enterprise-grade encryption ensures patient data remains protected and compliant at all times.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with f2:
            st.markdown("""
        <div class="glass-card">
            <h3>🧠 AI Reasoning</h3>
            <p style="color:#f3f4f6; font-size:0.9rem;">Our LLM analyzes clinical context to draft arguments that insurance companies actually listen to.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with f3:
            st.markdown("""
        <div class="glass-card">
            <h3>⚡ 10x Faster</h3>
            <p style="color:#f3f4f6; font-size:0.9rem;">Stop spending hours on specific letters. Generate professional appeals in seconds.</p>
        </div>
        """, unsafe_allow_html=True)
        
    # FOOTER LINKS (Badge Removed)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1]) # Centering logic
    
    with c2:
        if st.button("About", use_container_width=True):
            about_modal()
            
    with c3:
        if st.button("Addendum", use_container_width=True):
            addendum_modal()

    with c4:
        if st.button("Security Compliance", use_container_width=True):
             compliance_modal()

    st.markdown("<br><br>", unsafe_allow_html=True)
    return None

def create_portal_session(user_email):
    """Generates a Stripe Customer Portal link for the user."""
    _, stripe_client = init_services()
    if not stripe_client:
        return "https://billing.stripe.com/p/login/example"
        
    try:
        customers = stripe.Customer.list(email=user_email)
        if not customers.data:
            return None
            
        customer_id = customers.data[0].id
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=st.secrets.get("STRIPE_PAYMENT_LINK", "http://localhost:8501") # Fallback
        )
        return session.url
    except Exception as e:
        print(f"Portal Error: {e}")
        return None

def check_subscription(user_email):
    """Checks if the user has an active Stripe subscription."""
    _, stripe_client = init_services()
    
    if not stripe_client:
        return True # Dev mode: allow if no keys
        
    try:
        # Search for customer
        customers = stripe.Customer.list(email=user_email)
        if not customers.data:
            return False # No customer found = No sub

        customer_id = customers.data[0].id
        
        # Check active subscriptions
        subscriptions = stripe.Subscription.list(customer=customer_id, status='active')
        
        # Also check trialing
        trials = stripe.Subscription.list(customer=customer_id, status='trialing')
        
        if subscriptions.data or trials.data:
            return True
            
        return False
        
    except Exception as e:
        st.error(f"Billing Error: {e}")
        return False
