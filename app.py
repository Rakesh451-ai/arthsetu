import streamlit as st
from ai_helper import get_response
from calculators import (
    sip_calculator, 
    lumpsum_calculator, 
    emi_calculator, 
    fd_calculator,
    goal_planner,
    tax_calculator,
    compare_investments,
    health_score
)

# Page Configuration
st.set_page_config(
    page_title="Arthsetu - Financial Bridge",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    
    .main-header h1 {
        color: #FF9933;
        font-size: 56px;
        margin-bottom: 0;
        font-weight: 700;
        letter-spacing: -1px;
    }
    
    .main-header p {
        color: #138808;
        font-size: 18px;
        margin-top: 5px;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #138808 0%, #0a5c0a 100%);
    }
    
    /* Sidebar text color */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    
    /* Sidebar title */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #FF9933 !important;
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
    }
    
    /* User message */
    [data-testid="stChatMessage"][data-testid="user"] {
        background: linear-gradient(135deg, #FF9933 0%, #FFB347 100%);
        color: white;
    }
    
    /* Assistant message */
    [data-testid="stChatMessage"][data-testid="assistant"] {
        background: linear-gradient(135deg, #138808 0%, #2ecc71 100%);
        color: white;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #FF9933 0%, #FFB347 100%);
        color: white;
        border-radius: 25px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        width: 100%;
        font-size: 14px;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #138808 0%, #2ecc71 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #FF9933 0%, #FFB347 100%);
        padding: 18px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
    }
    
    [data-testid="stMetric"] label {
        color: white !important;
        font-weight: 600;
        font-size: 14px !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 32px !important;
        font-weight: bold;
    }
    
    /* Success/info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid #FF9933;
    }
    
    /* Number input styling */
    .stNumberInput input {
        border-radius: 12px;
        border: 2px solid #FF9933;
        padding: 8px 12px;
    }
    
    .stNumberInput input:focus {
        border-color: #138808;
        box-shadow: 0 0 0 2px rgba(19,136,8,0.2);
    }
    
    /* Selectbox styling */
    .stSelectbox select {
        border-radius: 12px;
        border: 2px solid #138808;
        padding: 8px 12px;
    }
    
    /* Title animation */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-title {
        animation: fadeInDown 0.6s ease-out;
    }
    
    /* Card styling for calculators */
    .calculator-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin: 10px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #FF9933 0%, #138808 100%);
        border-radius: 15px;
        color: white;
        margin-top: 30px;
    }
    
    .footer p {
        margin: 5px 0;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #FF9933 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #FF9933 0%, #FFB347 100%);
        color: white;
        border-radius: 12px;
        font-weight: 600;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #FF9933 0%, #FFB347 100%);
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Modern Header - Clean and Simple
st.markdown("""
<div class="main-header animate-title">
    <h1>🌉 Arthsetu</h1>
    <p>Your AI-Powered Financial Guide</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "💬 Chat"
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = True
    welcome_msg = {
        "role": "assistant",
        "content": "🌟 **Namaste! Welcome to Arthsetu!** 🌟\n\nI'm your AI-powered financial guide, here to help you understand money in your language.\n\n**I can help you with:**\n\n• 💰 **Financial Education** - Learn about FD, SIP, PPF, Mutual Funds, and more\n• 📊 **Investment Planning** - Calculate your future wealth with interactive calculators\n• 💵 **Tax Saving** - Discover smart ways to save tax under Section 80C\n• 🏠 **Loan Planning** - Understand your EMI and repayment schedule\n• 🎯 **Goal Planning** - Plan for weddings, homes, education\n• 💪 **Health Score** - Check your financial wellness\n\n**Try asking me:**\n- \"What is SIP?\"\n- \"FD kya hai?\"\n- \"How to save tax?\"\n- \"PPF vs Mutual Fund kaunsa better hai?\"\n\n**Or try our calculators in the sidebar!** 📈\n\nLet's build your financial bridge to a brighter future! 🌉"
    }
    st.session_state.messages.append(welcome_msg)

# Sidebar
with st.sidebar:
    # Logo and title
    st.markdown("""
    <div style='text-align: center; padding: 15px;'>
        <h1 style='color: #FF9933; font-size: 36px; margin-bottom: 5px;'>🌉 Arthsetu</h1>
        <p style='color: white; font-size: 13px; opacity: 0.9;'>Your Financial Guide</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "",
        ["💬 Chat", 
         "📊 SIP Calculator", 
         "💰 Lumpsum Calculator", 
         "🏠 EMI Calculator", 
         "🏦 FD Calculator",
         "🎯 Goal Planner",
         "💰 Tax Calculator",
         "📊 Compare Investments",
         "💪 Health Score"],
        label_visibility="collapsed"
    )
    st.session_state.page = page
    
    st.markdown("---")
    
    # Language Selection (only show in Chat mode)
    if page == "💬 Chat":
        st.markdown("### 🌐 Language")
        language = st.selectbox(
            "Choose your preferred language",
            ["English", "Hindi", "Hinglish"],
            key="language"
        )
    
    st.markdown("---")
    
    # Features info
    st.markdown("### ✨ Features")
    st.info("""
    **📚 Learn Finance**
    • Ask anything about money
    • Simple explanations
    • Indian context
    
    **🧮 Calculators**
    • SIP Calculator
    • Lumpsum Calculator
    • EMI Calculator
    • FD Calculator
    • Goal Planner
    • Tax Calculator
    • Compare Investments
    • Health Score
    
    **🌐 Languages**
    • English
    • Hindi
    • Hinglish
    """)
    
    st.markdown("---")
    
    # Clear chat button (only in chat mode)
    if page == "💬 Chat":
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            # Re-add welcome message
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🌟 **Chat cleared!** 🌟\n\nI'm still here to help with all your financial questions. What would you like to know today?"
            })
            st.rerun()
    
    st.markdown("---")
    
    # Footer in sidebar
    st.markdown("""
    <div style='text-align: center; color: white; font-size: 11px; margin-top: 20px;'>
        Made with ❤️ for India<br>
        🇮🇳 Financial Freedom for All
    </div>
    """, unsafe_allow_html=True)

# Main Content
if st.session_state.page == "💬 Chat":
    st.markdown("### 💬 Chat with Arthsetu")
    st.markdown("Ask me anything about money, investments, savings, or taxes...")
    st.markdown("---")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    user_question = st.chat_input("Type your question in Hindi, English, or Hinglish...")
    
    if user_question:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🧠 Arthsetu is thinking..."):
                response = get_response(user_question, language)
                st.markdown(response)
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Quick Questions Section
    st.markdown("---")
    st.markdown("### 📝 Quick Questions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 What is FD?", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "What is FD?"})
            response = get_response("What is FD?", language)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("📈 What is SIP?", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "What is SIP?"})
            response = get_response("What is SIP?", language)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("💵 How to save tax?", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "How to save tax?"})
            response = get_response("How to save tax?", language)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col4:
        if st.button("🏦 What is PPF?", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "What is PPF?"})
            response = get_response("What is PPF?", language)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Additional quick questions in expander
    with st.expander("📚 More Questions"):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Home Loan vs Car Loan", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Home loan vs car loan difference"})
                response = get_response("Home loan vs car loan difference", language)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
            
            if st.button("📊 Mutual Fund vs FD", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Mutual fund vs FD which is better"})
                response = get_response("Mutual fund vs FD which is better", language)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        with col2:
            if st.button("💳 Credit Card Benefits", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Credit card benefits and risks"})
                response = get_response("Credit card benefits and risks", language)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
            
            if st.button("💰 Emergency Fund", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "What is emergency fund and how much needed"})
                response = get_response("What is emergency fund and how much needed", language)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

elif st.session_state.page == "📊 SIP Calculator":
    st.markdown("### 📊 SIP Calculator")
    st.markdown("See how your monthly investments grow over time")
    st.markdown("---")
    sip_calculator()

elif st.session_state.page == "💰 Lumpsum Calculator":
    st.markdown("### 💰 Lumpsum Calculator")
    st.markdown("Calculate the future value of your one-time investment")
    st.markdown("---")
    lumpsum_calculator()

elif st.session_state.page == "🏠 EMI Calculator":
    st.markdown("### 🏠 EMI Calculator")
    st.markdown("Plan your monthly loan payments with ease")
    st.markdown("---")
    emi_calculator()

elif st.session_state.page == "🏦 FD Calculator":
    st.markdown("### 🏦 FD Calculator")
    st.markdown("Calculate your fixed deposit maturity amount")
    st.markdown("---")
    fd_calculator()

elif st.session_state.page == "🎯 Goal Planner":
    st.markdown("### 🎯 Goal Planner")
    st.markdown("Plan your path to financial goals")
    st.markdown("---")
    goal_planner()

elif st.session_state.page == "💰 Tax Calculator":
    st.markdown("### 💰 Tax Calculator")
    st.markdown("Calculate your tax liability with Section 80C benefits")
    st.markdown("---")
    tax_calculator()

elif st.session_state.page == "📊 Compare Investments":
    st.markdown("### 📊 Compare Investments")
    st.markdown("Compare returns across different investment options")
    st.markdown("---")
    compare_investments()

elif st.session_state.page == "💪 Health Score":
    st.markdown("### 💪 Financial Health Score")
    st.markdown("Check your financial wellness and get recommendations")
    st.markdown("---")
    health_score()

# Modern Footer
st.markdown("""
<div class="footer">
    <p style='font-size: 14px; margin: 0;'>🌉 Arthsetu - Your Trusted Financial Guide 🇮🇳</p>
    <p style='font-size: 12px; margin: 5px 0 0 0; opacity: 0.9;'>Learn • Calculate • Grow</p>
</div>
""", unsafe_allow_html=True)

# Display current page indicator
if st.session_state.page != "💬 Chat":
    st.sidebar.success(f"📍 {st.session_state.page}")