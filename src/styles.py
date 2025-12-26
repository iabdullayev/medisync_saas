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

    /* Hero Section */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 400;
        color: #e0e7ff;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    /* CTA Button */
    .cta-button {
        background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
        color: #4c1d95 !important;
        padding: 1rem 2.5rem;
        border-radius: 16px;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        display: inline-block;
        text-decoration: none;
    }

    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }

    /* Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: #ffffff;
    }

    .feature-description {
        font-size: 1rem;
        color: #e0e7ff;
        line-height: 1.6;
    }

    /* Modal Styling */
    div[data-testid="stModal"] {
        background: rgba(76, 29, 149, 0.95) !important;
        backdrop-filter: blur(20px);
    }

    div[data-testid="stModal"] > div {
        background: linear-gradient(135deg, #4c1d95 0%, #6d28d9 100%);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    }

    /* Input Fields in Modal */
    div[data-testid="stModal"] input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 0.75rem 1rem !important;
    }

    div[data-testid="stModal"] input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }

    div[data-testid="stModal"] input:focus {
        border-color: rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
    }

    /* Modal Buttons */
    div[data-testid="stModal"] button {
        background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%) !important;
        color: #4c1d95 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stModal"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Glass Card Feature Boxes */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        min-height: 180px;
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }
    
    .glass-card h3 {
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    .glass-card p {
        color: #e0e7ff;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Landing Page Bottom Buttons (Light Purple/Lavender - Almost Transparent) */
    /* Target buttons in the footer section specifically */
    .stButton > button {
        background: rgba(167, 139, 250, 0.15) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stButton > button:hover {
        background: rgba(167, 139, 250, 0.25) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Hide hyperlink icons next to headings */
    .glass-card h3 a {
        display: none !important;
    }
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
