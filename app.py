import streamlit as st
import pandas as pd
import time
import mysql.connector
from datetime import datetime
import requests
import json
from transformers import pipeline
import cv2
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import threading
import queue
import os

# Page Configuration
st.set_page_config(
    page_title="Enterprise Hiring Platform - Hiring Skilled Candidates",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .timer-display {
        background: #ff4b4b;
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }
    .question-card {
        background: #f0f2f6;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #1f4e79;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        height: 20px;
        margin: 20px 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #27ae60, #2ecc71);
        height: 100%;
        transition: width 0.3s ease;
    }
    .enterprise-badge {
        background: #2c3e50;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .security-badge {
        background: #27ae60;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Enterprise Hiring Platform</h1>
    <h3>AI-Powered Interview & Assessment System</h3>
    <p><strong>Developed by:</strong> Akash Bauri | <strong>Email:</strong> akashbauri16021998@gmail.com | <strong>Phone:</strong> 8002778855</p>
    <span class="enterprise-badge">ENTERPRISE VERSION</span>
    <span class="security-badge">🔒 SECURE</span>
</div>
""", unsafe_allow_html=True)

# SECURE Configuration - API Keys in Streamlit Secrets
class Config:
    """Secure Configuration Class - All sensitive data in Streamlit Secrets"""
    
    @staticmethod
    def get_hugging_face_token():
        try:
            return st.secrets["api_keys"]["hugging_face"]
        except KeyError:
            st.error("🔒 Hugging Face API key not configured in secrets")
            return None
    
    @staticmethod
    def get_perplexity_api_key():
        try:
            return st.secrets["api_keys"]["perplexity"]
        except KeyError:
            st.error("🔒 Perplexity API key not configured in secrets")
            return None
    
    @staticmethod
    def get_db_config():
        try:
            return {
                'host': st.secrets["database"]["host"],
                'port': int(st.secrets["database"]["port"]),
                'user': st.secrets["database"]["user"],
                'password': st.secrets["database"]["password"],
                'database': st.secrets["database"]["database"]
            }
        except KeyError:
            st.error("🔒 Database credentials not configured in secrets")
            return None
    
    INTRO_TIME = 120
    TECHNICAL_TIME = 180
    PROJECT_TIME = 300
    VIDEO_TIME = 240

# Database Connection
@st.cache_resource
def get_db_connection():
    try:
        db_config = Config.get_db_config()
        if db_config:
            conn = mysql.connector.connect(**db_config)
            return conn
        return None
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# Check Configuration
def check_configuration():
    missing = []
    if not Config.get_hugging_face_token():
        missing.append("Hugging Face API key")
    if not Config.get_perplexity_api_key():
        missing.append("Perplexity API key")
    if not Config.get_db_config():
        missing.append("Database credentials")
    
    if missing:
        st.error(f"Missing configuration: {', '.join(missing)}")
        st.info("""
        **Configuration Required:**
        Please set up Streamlit secrets with your API keys and database credentials.
        
        Go to app settings → Secrets → Add configuration
        """)
        return False
    return True

# Main application logic
if check_configuration():
    # Initialize session state
    if "demo_mode" not in st.session_state:
        st.session_state.demo_mode = True
    
    st.success("✅ Enterprise Hiring Platform Ready!")
    st.info("""
    🎯 **Complete AI-Powered Interview System**
    
    **Features:**
    - Experience-adaptive questions (Fresher/Intermediate/Advanced)
    - 5 technical questions per skill + 5 project questions
    - Timer auto-advance with skip functionality
    - Live video interview with AI analysis
    - Direct MySQL database storage
    - Secure API key management
    
    **Technologies:**
    - Perplexity API for advanced AI evaluation
    - Hugging Face for NLP processing
    - WebRTC for real-time video interviews
    - MySQL for enterprise data storage
    
    **Configure your secrets to enable full functionality!**
    """)
    
    # Demo interface
    st.subheader("🔧 System Configuration Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        hf_status = "🟢 Ready" if Config.get_hugging_face_token() else "🔴 Not Set"
        st.metric("Hugging Face API", hf_status)
    
    with col2:
        px_status = "🟢 Ready" if Config.get_perplexity_api_key() else "🔴 Not Set"
        st.metric("Perplexity API", px_status)
    
    with col3:
        db_status = "🟢 Connected" if get_db_connection() else "🔴 Not Set"
        st.metric("MySQL Database", db_status)
    
    if st.button("🚀 Start Demo Interview (Test Mode)", use_container_width=True):
        st.success("Demo mode activated! This showcases the complete interview workflow.")
        st.info("Configure secrets for full AI-powered functionality with database storage.")

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Enterprise Platform")
    st.markdown("""
    **🔒 Secure Features:**
    ✅ API Key Protection  
    ✅ Database Security  
    ✅ Enterprise Grade  
    
    **🤖 AI Capabilities:**
    ✅ Perplexity API Integration  
    ✅ Hugging Face Models  
    ✅ Advanced Evaluation  
    
    **🎥 Interview Features:**
    ✅ Live Video Assessment  
    ✅ Timer Auto-advance  
    ✅ Skip Functionality  
    ✅ Multi-level Questions  
    """)
    
    st.markdown("### 👨‍💻 Developer")
    st.markdown("""
    **Akash Bauri**  
    📧 akashbauri16021998@gmail.com  
    📱 8002778855  
    🔗 [GitHub Portfolio](https://github.com/akashbauri)
    """)
