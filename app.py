import streamlit as st
import pandas as pd
import time
import sqlite3
from datetime import datetime
import requests
import json
import os
import re
import io

# Page Configuration
st.set_page_config(
    page_title="Hiring Skilled Candidates - AI Interview Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as before)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2c3e50 0%, #3498db 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    .hr-dashboard {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3);
    }
    .data-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .export-button {
        background: #3498db;
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        margin: 5px;
    }
    .candidate-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3498db;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# Professional Header - Updated Project Name
st.markdown("""
<div class="main-header">
    <h1>🎯 Hiring Skilled Candidates</h1>
    <h2>AI-Powered Technical Interview & Assessment Platform</h2>
    <p><strong>Developed by:</strong> Akash Bauri | <strong>Email:</strong> akashbauri16021998@gmail.com | <strong>Phone:</strong> 8002778855</p>
    <div>
        <span style="background: #e74c3c; color: white; padding: 8px 20px; border-radius: 25px; font-size: 14px; font-weight: bold; margin: 5px;">🧠 PERPLEXITY AI</span>
        <span style="background: #e74c3c; color: white; padding: 8px 20px; border-radius: 25px; font-size: 14px; font-weight: bold; margin: 5px;">🤗 HUGGING FACE</span>
        <span style="background: #e74c3c; color: white; padding: 8px 20px; border-radius: 25px; font-size: 14px; font-weight: bold; margin: 5px;">💾 DATA EXPORT</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ALL YOUR EXISTING CODE HERE (Configuration, AI functions, etc.)
# ... (keeping all previous functions exactly as they were)

# ADD THIS NEW HR DASHBOARD SECTION
def render_hr_dashboard():
    """Comprehensive HR Dashboard with all user data access"""
    
    st.markdown("""
    <div class="hr-dashboard">
        <h2>👥 HR DASHBOARD - Hiring Skilled Candidates</h2>
        <p><strong>Access all candidate data, interviews, and comprehensive analytics</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    conn = setup_database()
    if not conn:
        st.error("❌ Database connection failed!")
        return
    
    try:
        # Get all candidates data
        candidates_df = pd.read_sql_query("""
            SELECT 
                id,
                name,
                email,
                phone_no,
                position,
                experience,
                skills,
                final_score,
                speaking_quality,
                result_status,
                interview_duration,
                created_at
            FROM candidates 
            ORDER BY created_at DESC
        """, conn)
        
        # Get detailed responses data
        responses_df = pd.read_sql_query("""
            SELECT 
                r.*,
                c.name as candidate_name,
                c.email as candidate_email
            FROM interview_responses r
            JOIN candidates c ON r.candidate_id = c.id
            ORDER BY r.created_at DESC
        """, conn)
        
        if len(candidates_df) == 0:
            st.info("📝 No interview data available yet. Candidates will appear here after completing interviews.")
            return
        
        # Dashboard Metrics
        st.subheader("📊 Interview Analytics Dashboard")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("👥 Total Candidates", len(candidates_df))
        
        with col2:
            hired_count = len(candidates_df[candidates_df['result_status'].str.contains('HIRED', na=False)])
            st.metric("✅ Hired", hired_count)
        
        with col3:
            pending_count = len(candidates_df[candidates_df['result_status'].str.contains('REVIEW', na=False)])
            st.metric("⏳ Under Review", pending_count)
        
        with col4:
            avg_score = candidates_df['final_score'].mean() if len(candidates_df) > 0 else 0
            st.metric("📈 Average Score", f"{avg_score:.1f}%")
        
        with col5:
            today_count = len(candidates_df[candidates_df['created_at'].str.contains(datetime.now().strftime('%Y-%m-%d'), na=False)])
            st.metric("📅 Today", today_count)
        
        # Data Export Section
        st.subheader("📤 Export Complete Interview Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export All Candidates to Excel", use_container_width=True):
                # Create Excel file with multiple sheets
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    candidates_df.to_excel(writer, sheet_name='Candidates', index=False)
                    if len(responses_df) > 0:
                        responses_df.to_excel(writer, sheet_name='Detailed_Responses', index=False)
                
                output.seek(0)
                
                st.download_button(
                    label="💾 Download Complete Interview Data (Excel)",
                    data=output.getvalue(),
                    file_name=f"hiring_skilled_candidates_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with col2:
            if st.button("📋 Export Candidates CSV", use_container_width=True):
                csv_data = candidates_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download Candidates CSV",
                    data=csv_data,
                    file_name=f"candidates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col3:
            if st.button("📝 Export Responses CSV", use_container_width=True) and len(responses_df) > 0:
                responses_csv = responses_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download All Responses CSV",
                    data=responses_csv,
                    file_name=f"interview_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        # Filter Options
        st.subheader("🔍 Filter & Search Candidates")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            result_filter = st.selectbox(
                "Filter by Result:",
                ["All Results"] + list(candidates_df['result_status'].unique())
            )
        
        with col2:
            experience_filter = st.selectbox(
                "Filter by Experience:",
                ["All Experience Levels"] + list(candidates_df['experience'].unique())
            )
        
        with col3:
            search_term = st.text_input("🔍 Search by name/email/skills:", placeholder="Type to search...")
        
        # Apply filters
        filtered_df = candidates_df.copy()
        
        if result_filter != "All Results":
            filtered_df = filtered_df[filtered_df['result_status'] == result_filter]
        
        if experience_filter != "All Experience Levels":
            filtered_df = filtered_df[filtered_df['experience'] == experience_filter]
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df['name'].str.contains(search_term, case=False, na=False) |
                filtered_df['email'].str.contains(search_term, case=False, na=False) |
                filtered_df['skills'].str.contains(search_term, case=False, na=False)
            ]
        
        # Display Candidates
        st.subheader(f"👥 Candidates List ({len(filtered_df)} candidates)")
        
        if len(filtered_df) > 0:
            for idx, candidate in filtered_df.iterrows():
                # Color coding based on result
                if "HIRED" in str(candidate['result_status']):
                    card_color = "#d5f4e6"  # Light green
                    status_color = "#27ae60"
                elif "REVIEW" in str(candidate['result_status']):
                    card_color = "#fef9e7"  # Light yellow
                    status_color = "#f39c12"
                else:
                    card_color = "#fadbd8"  # Light red
                    status_color = "#e74c3c"
                
                st.markdown(f"""
                <div class="candidate-card" style="background: {card_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin: 0; color: #2c3e50;">👤 {candidate['name']}</h3>
                            <p style="margin: 5px 0; color: #34495e;"><strong>📧 Email:</strong> {candidate['email']}</p>
                            <p style="margin: 5px 0; color: #34495e;"><strong>📱 Phone:</strong> {candidate['phone_no']}</p>
                            <p style="margin: 5px 0; color: #34495e;"><strong>💼 Position:</strong> {candidate['position']}</p>
                            <p style="margin: 5px 0; color: #34495e;"><strong>📊 Experience:</strong> {candidate['experience']}</p>
                            <p style="margin: 5px 0; color: #34495e;"><strong>🛠️ Skills:</strong> {candidate['skills']}</p>
                        </div>
                        <div style="text-align: center;">
                            <div style="background: {status_color}; color: white; padding: 10px 20px; border-radius: 25px; font-weight: bold; margin-bottom: 10px;">
                                {candidate['result_status']}
                            </div>
                            <div style="font-size: 28px; font-weight: bold; color: {status_color};">
                                {candidate['final_score']}%
                            </div>
                            <div style="color: #7f8c8d; font-size: 14px;">
                                🗣️ {candidate['speaking_quality']}
                            </div>
                            <div style="color: #7f8c8d; font-size: 12px; margin-top: 5px;">
                                ⏱️ {candidate['interview_duration']:.1f} min
                            </div>
                        </div>
                    </div>
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #bdc3c7;">
                        <span style="color: #7f8c8d; font-size: 14px;">
                            📅 Interview Date: {candidate['created_at'][:19]}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show detailed responses for this candidate
                with st.expander(f"📝 View Detailed Interview Responses - {candidate['name']}"):
                    candidate_responses = responses_df[responses_df['candidate_id'] == candidate['id']]
                    
                    if len(candidate_responses) > 0:
                        for _, response in candidate_responses.iterrows():
                            st.markdown(f"""
                            **🎯 Skill:** {response['skill']}  
                            **❓ Question:** {response['question']}  
                            **✍️ Answer:** {response['answer'][:200]}{'...' if len(response['answer']) > 200 else ''}  
                            **📊 Score:** {response['score']}%  
                            **💬 AI Feedback:** {response['feedback']}  
                            **⏱️ Response Time:** {response['response_time']:.1f}s  
                            
                            ---
                            """)
                    else:
                        st.info("No detailed responses found for this candidate.")
        else:
            st.info("No candidates match the current filters.")
        
        # Raw Data Tables
        st.subheader("📊 Complete Data Tables")
        
        tab1, tab2 = st.tabs(["👥 Candidates Data", "📝 Interview Responses"])
        
        with tab1:
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
            
            if len(filtered_df) > 0:
                st.info(f"📊 Showing {len(filtered_df)} candidates out of {len(candidates_df)} total")
        
        with tab2:
            if len(responses_df) > 0:
                st.dataframe(
                    responses_df,
                    use_container_width=True,
                    hide_index=True
                )
                st.info(f"📝 Total interview responses: {len(responses_df)}")
            else:
                st.info("No detailed response data available.")
    
    except Exception as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

# MAIN APPLICATION LOGIC
def main():
    # Initialize session state
    initialize_session_state()
    
    # Navigation
    st.sidebar.title("🎯 Hiring Skilled Candidates")
    page = st.sidebar.radio("Navigate:", [
        "🚀 Take Interview",
        "👥 HR Dashboard",
        "📊 System Status"
    ])
    
    if page == "🚀 Take Interview":
        # Your existing interview stages here
        if st.session_state.stage == "registration":
            # Registration code
            pass
        elif st.session_state.stage == "interview":
            # Interview code
            pass
        elif st.session_state.stage == "results":
            # Results code
            pass
    
    elif page == "👥 HR Dashboard":
        render_hr_dashboard()
    
    elif page == "📊 System Status":
        st.header("🔧 System Status")
        
        # System metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            hf_status = "🟢 Active" if os.getenv("HUGGING_FACE_TOKEN") else "🟡 Demo"
            st.metric("🤗 Hugging Face", hf_status)
        
        with col2:
            px_status = "🟢 Active" if os.getenv("PERPLEXITY_API_KEY") else "🟡 Demo"
            st.metric("🧠 Perplexity AI", px_status)
        
        with col3:
            db = setup_database()
            db_status = "🟢 Connected" if db else "🔴 Error"
            st.metric("💾 Database", db_status)
        
        with col4:
            st.metric("🚀 System", "🟢 OPERATIONAL")
        
        # Show database schema
        if st.checkbox("🔍 Show Database Schema"):
            st.code("""
            -- Candidates Table
            CREATE TABLE candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone_no TEXT NOT NULL,
                position TEXT NOT NULL,
                experience TEXT NOT NULL,
                skills TEXT NOT NULL,
                final_score INTEGER NOT NULL,
                speaking_quality TEXT NOT NULL,
                result_status TEXT NOT NULL,
                interview_duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Interview Responses Table
            CREATE TABLE interview_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER,
                skill TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                score INTEGER NOT NULL,
                feedback TEXT,
                response_time REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates (id)
            );
            """)

# Run the application
if __name__ == "__main__":
    main()
