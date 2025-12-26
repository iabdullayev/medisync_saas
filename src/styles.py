"""Shared CSS styles for MediSync SaaS application."""


def get_base_styles() -> str:
    """Returns base CSS styles used across the application.
    
    Returns:
        str: HTML string containing base CSS styles.
    """
    return """
    <style>
    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide Streamlit Deploy Button */
    .stDeployButton {display: none;}
    
    /* Hide "Manage app" button */
    button[kind="header"] {display: none;}
    
    /* Base Button Styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
    }
    </style>
    """


def get_landing_page_styles() -> str:
    """Returns landing page specific styles.
    
    Returns:
        str: HTML string containing landing page CSS styles.
    """
    return """
    <style>
    /* Lighter, Dreamy Purple Gradient */
    .stApp {
        background: linear-gradient(135deg, #4c1d95 0%, #8b5cf6 40%, #ddd6fe 100%);
        background-attachment: fixed;
    }
    
    /* Typography - White with correct weights */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* White text ONLY on main landing page, NOT in dialogs */
    .stApp > div:not([role="dialog"]) {
        color: #ffffff;
    }
    
    /* Ensure main page markdown is white */
    .stMarkdown:not(div[role="dialog"] *) {
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
    
    /* ============================================ */
    /* DIALOG FIXES - Ensure dark text visibility  */
    /* ============================================ */
    
    /* Dialog container - force dark text */
    div[role="dialog"] {
        color: #1f2937 !important;
    }
    
    /* All dialog text elements - dark and readable */
    div[role="dialog"] p, 
    div[role="dialog"] span, 
    div[role="dialog"] div:not(.stButton),
    div[role="dialog"] h1,
    div[role="dialog"] h2,
    div[role="dialog"] h3,
    div[role="dialog"] label {
        color: #1f2937 !important;
    }
    
    /* Dialog markdown content - dark text */
    div[role="dialog"] .stMarkdown,
    div[role="dialog"] .stMarkdown *,
    div[role="dialog"] .stMarkdown p {
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

    /* 2. Primary Buttons (Login / Signup) -> Darker Blue for Better Contrast */
    div[data-testid="column"] .stButton > button[kind="primary"],
    button[kind="primary"] {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important; 
        color: #ffffff !important; 
        border: none !important;
        padding: 0.6rem 1.2rem;
        border-radius: 9999px !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.5) !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Primary button text - force white and bold */
    button[kind="primary"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="column"] .stButton > button[kind="primary"]:hover,
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 8px 15px rgba(37, 99, 235, 0.4) !important;
        transform: translateY(-2px);
    }
    
    /* Hide Decorations */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """


def get_app_styles() -> str:
    """Returns main application specific styles.
    
    Returns:
        str: HTML string containing main app CSS styles.
    """
    return """
    <style>
    /* File Uploader Styling */
    .stFileUploader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 16px;
        padding: 2rem;
        border: 2px dashed #cbd5e1;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #2563eb;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    }
    
    /* Success/Warning Messages */
    .stSuccess, .stWarning {
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-weight: 500;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.4);
        transform: translateY(-2px);
    }
    </style>
    """
