import streamlit as st
import os
from dotenv import load_dotenv
from smolagents import CodeAgent, HfApiModel, tool
import json
from PIL import Image

# 1. Load the API Key
load_dotenv()
token = os.getenv("HF_TOKEN")

if not token:
    st.error("Missing Hugging Face Token! Please check your .env file.")
    st.stop()

# 2. Page Setup
icon = Image.open("pageicon.png")
st.set_page_config(
    page_title="GovScheme AI - Find Your Benefits",
    page_icon="icon",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Requestly Integration
query_params = st.query_params  # Gets the ?mode=admin from the URL
mode = query_params.get("mode", "")

# If Requestly injected "admin", show the secret debug menu
if mode == "admin":
    st.error("🔧 REQUESTLY DEBUG MODE ACTIVE: Admin Access Granted")
    with st.sidebar:
        st.markdown("### 🔒 Admin Controls")
        st.write("Server Status: ✅ Online")
        st.write("Model: HuggingFace-Zephyr")
        st.write("Latency: 43ms")

# Custom CSS with Tailwind CDN and warm, human-centered design
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<style>
    /* Import warm, friendly fonts */
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=Work+Sans:wght@300;400;500;600&display=swap');
    
    /* Tailwind config */
    @layer base {
        :root {
            --color-primary: #d97706;
            --color-secondary: #0c4a6e;
            --color-accent: #059669;
        }
    }
    
    /* Global resets */
    .main {
        background: #fefcf9;
        font-family: 'Work Sans', sans-serif;
    }
    
    .main > div {
        padding-top: 2rem;
    }
    
    /* Header - warm and welcoming */
    .hero-section {
        background: linear-gradient(to bottom, #fff7ed, #fefcf9);
        border-left: 6px solid #d97706;
        padding: clamp(1.5rem, 4vw, 2.5rem) clamp(1rem, 3vw, 2rem);
        margin-bottom: 2rem;
        border-radius: 2px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .main-title {
        font-family: 'Crimson Pro', serif;
        font-size: clamp(1.75rem, 4vw, 2.75rem);
        font-weight: 700;
        color: #1f2937 !important;
        margin-bottom: 0.75rem;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-size: clamp(0.95rem, 2vw, 1.15rem);
        color: #6b7280 !important;
        line-height: 1.6;
        max-width: 680px;
        font-weight: 400;
    }
    
    .trust-indicators {
        margin-top: 1.5rem;
        display: flex;
        gap: clamp(0.75rem, 2vw, 1.5rem);
        flex-wrap: wrap;
    }
    
    .trust-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #059669 !important;
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
        font-weight: 500;
    }
    
    /* Sidebar - friendly and informative */
    [data-testid="stSidebar"] {
        background: #0c4a6e;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.02) 10px, rgba(255,255,255,0.02) 20px);
    }
    
    /* Make sidebar toggle button more visible - native Streamlit arrow */
    [data-testid="collapsedControl"] {
        color: #0c4a6e !important;
        background: rgba(12, 74, 110, 0.1) !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 0.5rem !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: rgba(12, 74, 110, 0.2) !important;
    }
    
    [data-testid="collapsedControl"] svg {
        color: #0c4a6e !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    /* Sidebar collapse button when sidebar is open */
    button[kind="header"] {
        color: white !important;
    }
    
    button[kind="header"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .sidebar-header {
        font-family: 'Crimson Pro', serif;
        font-size: clamp(1.25rem, 3vw, 1.5rem);
        font-weight: 700;
        padding: 1.5rem 1rem 1rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-card {
        background: rgba(255, 255, 255, 0.08);
        border-left: 3px solid #d97706;
        padding: clamp(1rem, 2vw, 1.25rem);
        margin: 1rem 0;
        border-radius: 2px;
        line-height: 1.7;
    }
    
    .sidebar-card h3 {
        font-family: 'Work Sans', sans-serif;
        font-size: clamp(0.9rem, 2vw, 1rem);
        font-weight: 600;
        margin-bottom: 0.75rem;
        letter-spacing: 0.02em;
    }
    
    .sidebar-card ul {
        list-style: none;
        padding-left: 0;
    }
    
    .sidebar-card li {
        padding-left: 1.25rem;
        position: relative;
        margin-bottom: 0.5rem;
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
    }
    
    .sidebar-card li:before {
        content: "→";
        position: absolute;
        left: 0;
        color: #fbbf24;
    }
    
    .sidebar-card p {
        color: white !important;
    }
    
    /* Chat container - clean and spacious */
    .chat-section {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: clamp(1rem, 3vw, 2rem);
        min-height: 400px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
    }
    
    /* Example prompts - helpful suggestions */
    .examples-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
        gap: 1rem;
        margin: 1.5rem 0 2rem;
    }
    
    .example-card {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        padding: clamp(1rem, 2vw, 1.25rem);
        border-radius: 2px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .example-card:hover {
        background: #fef3c7;
        border-left-width: 6px;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .example-card .label {
        font-weight: 600;
        color: #92400e !important;
        font-size: clamp(0.75rem, 1.5vw, 0.85rem);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .example-card .text {
        color: #1f2937 !important;
        font-size: clamp(0.85rem, 1.5vw, 0.95rem);
        line-height: 1.5;
    }
    
    /* Chat messages - natural conversation feel */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        padding: 1rem 0 !important;
    }
    
    [data-testid="stChatMessageContent"] {
        background: white !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 4px !important;
        padding: clamp(0.75rem, 2vw, 1rem) clamp(1rem, 2vw, 1.25rem) !important;
        max-width: 100% !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* User messages */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
        background: #dbeafe !important;
        border-color: #3b82f6 !important;
    }
    
    /* Assistant messages */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {
        background: #f0fdf4 !important;
        border-color: #22c55e !important;
    }
    
    /* Make chat message text responsive and visible */
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] h3,
    [data-testid="stChatMessageContent"] strong,
    [data-testid="stChatMessageContent"] em {
        color: #1f2937 !important;
        font-size: clamp(0.9rem, 1.5vw, 1rem) !important;
        line-height: 1.6 !important;
    }
    
    [data-testid="stChatMessageContent"] hr {
        border-color: #e5e7eb !important;
        margin: 0.75rem 0 !important;
    }
    
    /* Input area - welcoming */
    .stChatInputContainer {
        border-top: 2px solid #e5e7eb !important;
        padding-top: 1.5rem !important;
        background: white !important;
        margin-top: 1rem !important;
    }
    
    textarea[data-testid="stChatInputTextArea"] {
        border: 2px solid #d1d5db !important;
        border-radius: 8px !important;
        font-family: 'Work Sans', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        background: white !important;
        color: #1f2937 !important;
    }
    
    textarea[data-testid="stChatInputTextArea"]::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }
    
    textarea[data-testid="stChatInputTextArea"]:focus {
        border-color: #d97706 !important;
        box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.1) !important;
        outline: none !important;
    }
    
    /* Buttons - clear and functional */
    .stButton > button {
        background: #0c4a6e !important;
        color: white !important;
        border: none !important;
        border-radius: 2px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 500 !important;
        font-family: 'Work Sans', sans-serif !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em !important;
    }
    
    .stButton > button:hover {
        background: #075985 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Stats box - understated */
    .stat-box {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
        padding: clamp(1rem, 3vw, 1.5rem);
        text-align: center;
        margin: 1rem 0;
        border-radius: 2px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stat-number {
        font-family: 'Crimson Pro', serif;
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 700;
        line-height: 1;
        color: white !important;
    }
    
    .stat-label {
        font-size: clamp(0.85rem, 1.5vw, 0.95rem);
        margin-top: 0.5rem;
        opacity: 0.95;
        font-weight: 400;
        color: white !important;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Crimson Pro', serif;
        font-size: clamp(1.25rem, 3vw, 1.5rem);
        font-weight: 600;
        color: #1f2937 !important;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f3f4f6;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Spinner */
    .stSpinner > div {
        border-color: #d97706 !important;
    }
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        .main > div {
            padding-top: 1rem;
        }
        
        .hero-section {
            border-left-width: 4px;
        }
        
        .examples-grid {
            grid-template-columns: 1fr;
        }
        
        .trust-indicators {
            flex-direction: column;
            gap: 0.75rem;
        }
        
        [data-testid="stSidebar"] {
            font-size: 0.9rem;
        }
    }
    
    /* Tablet adjustments */
    @media (min-width: 769px) and (max-width: 1024px) {
        .examples-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    /* Container width adjustments */
    .block-container {
        max-width: 100% !important;
        padding-left: clamp(1rem, 3vw, 2rem) !important;
        padding-right: clamp(1rem, 3vw, 2rem) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Define the Tool
@tool
def find_schemes(age: int, gender: str, income: int, state: str, occupation: str, disability_percent: int) -> str:
    """
    Searches schemes.json for government schemes based on the user's profile.
    
    Args:
        age: User's age in years.
        gender: User's gender ('male', 'female', 'other').
        income: Annual family income in Rupees.
        state: User's home state (e.g., 'Uttar Pradesh', 'Telangana').
        occupation: User's job (e.g., 'student', 'farmer', 'street_vendor', 'unemployed').
        disability_percent: Percentage of disability (0 if none).
    """
    try:
        with open('schemes.json', 'r', encoding='utf-8') as f:
            schemes = json.load(f)
    except FileNotFoundError:
        return "Error: schemes.json file not found."

    eligible = []
    
    # Simple logic to filter schemes
    for scheme in schemes:
        cond = scheme.get('conditions', {})
        
        # Age
        if 'min_age' in cond and age < cond['min_age']: continue
        if 'max_age' in cond and age > cond['max_age']: continue
        # Income
        if 'max_income' in cond and income > cond['max_income']: continue
        # Gender
        if 'gender' in cond and cond['gender'].lower() != gender.lower(): continue
        # State
        if 'state' in cond and cond['state'].lower() != state.lower(): continue
        # Disability
        if 'min_disability' in cond and disability_percent < cond['min_disability']: continue
        # Occupation
        if 'occupation' in cond:
            req_occ = cond['occupation']
            if isinstance(req_occ, list):
                if occupation.lower() not in [o.lower() for o in req_occ]: continue
            elif req_occ.lower() != occupation.lower(): continue

        scheme_text = f"""
**{scheme['name']}**

💰 **Benefits:** {scheme['benefits']}

📄 **Required Documents:** {', '.join(scheme.get('documents', []))}

---
"""
        eligible.append(scheme_text)

    if not eligible:
        return "❌ No schemes found matching this exact profile. Try adjusting your details or check back later for new schemes."
    
    header = f"✅ **Found {len(eligible)} scheme(s) you may be eligible for:**\n\n"
    return header + "\n".join(eligible)

# 4. Initialize Agent
@st.cache_resource
def get_agent():
    model = HfApiModel(token=token) 
    return CodeAgent(tools=[find_schemes], model=model)

agent = get_agent()

# 5. Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-header">🇮🇳 GovScheme Finder</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-card">
        <h3>How to Use</h3>
        <ul>
            <li>Share your basic details</li>
            <li>Get personalized scheme matches</li>
            <li>Apply with the right documents</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-card">
        <h3>What We Need</h3>
        <ul>
            <li>Your age and gender</li>
            <li>Annual family income</li>
            <li>Home state</li>
            <li>Current occupation</li>
            <li>Disability status (if any)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">500+</div>
        <div class="stat-label">Schemes in Database</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("""
    <div class="sidebar-card">
        <p style="font-size: 0.85rem; opacity: 0.9; line-height: 1.6;">
        We help you discover government benefits. Information is updated regularly but always verify with official sources.
        </p>
    </div>
    """, unsafe_allow_html=True)

# 6. Main Content
st.markdown("""
<div class="hero-section">
    <h1 class="main-title">Find Government Schemes You Qualify For</h1>
    <p class="subtitle">
        Tell us a bit about yourself, and we'll help you discover financial assistance, 
        subsidies, and support programs from central and state governments.
    </p>
    <div class="trust-indicators">
        <div class="trust-item">
            <span>✓</span>
            <span>Free to use</span>
        </div>
        <div class="trust-item">
            <span>✓</span>
            <span>No registration required</span>
        </div>
        <div class="trust-item">
            <span>✓</span>
            <span>Updated regularly</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Example prompts (shown only if no messages)
if not st.session_state.get("messages", []):
    st.markdown('<h2 class="section-header">Start with an Example</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="examples-grid">
        <div class="example-card">
            <div class="label">Student</div>
            <div class="text">
                I'm a 22-year-old female student from Delhi. My family earns about ₹2 lakh annually.
            </div>
        </div>
        <div class="example-card">
            <div class="label">Farmer</div>
            <div class="text">
                I'm a 48-year-old male farmer in Madhya Pradesh with yearly income around ₹1.5 lakh.
            </div>
        </div>
        <div class="example-card">
            <div class="label">With Disability</div>
            <div class="text">
                I'm 32 years old from Gujarat with 45% disability. Family income is ₹3 lakh per year.
            </div>
        </div>
        <div class="example-card">
            <div class="label">Small Business</div>
            <div class="text">
                I'm a 38-year-old street vendor in Karnataka. My annual income is around ₹2.8 lakh.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 7. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history with wrapper if messages exist
if st.session_state.messages:
    st.markdown('<div class="chat-section">', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.messages:
    st.markdown('</div>', unsafe_allow_html=True)

# Handle User Input
if prompt := st.chat_input("Describe yourself: age, income, state, occupation..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Checking your eligibility..."):
            try:
                # The agent runs here!
                response = agent.run(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Footer
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem; text-align: center; color: #6b7280; border-top: 1px solid #e5e7eb;">
    <p style="font-size: 0.9rem; line-height: 1.6;">
        This tool helps you discover schemes, but always verify details on official government websites.<br>
        Made to help Indian citizens access their benefits.
    </p>
</div>
""", unsafe_allow_html=True)