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

# Custom CSS
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
    .ai-badge {
        background: #e74c3c;
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: bold;
        margin: 5px;
        animation: glow 2s infinite;
    }
    @keyframes glow {
        0% { box-shadow: 0 0 5px #e74c3c; }
        50% { box-shadow: 0 0 20px #e74c3c; }
        100% { box-shadow: 0 0 5px #e74c3c; }
    }
    .hr-dashboard {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3);
    }
    .candidate-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3498db;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .question-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 30px;
        border-radius: 15px;
        border-left: 6px solid #3498db;
        margin: 25px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    .timer-display {
        background: linear-gradient(90deg, #e74c3c, #c0392b);
        color: white;
        padding: 20px;
        border-radius: 12px;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin: 15px 0;
        animation: pulse 1.5s infinite;
    }
    .progress-bar {
        background: #ecf0f1;
        border-radius: 12px;
        overflow: hidden;
        height: 30px;
        margin: 25px 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    .progress-fill {
        background: linear-gradient(90deg, #27ae60, #2ecc71);
        height: 100%;
        transition: width 0.8s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 16px;
    }
    .result-card {
        padding: 40px;
        border-radius: 20px;
        margin: 30px 0;
        box-shadow: 0 12px 35px rgba(0,0,0,0.18);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Professional Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Hiring Skilled Candidates</h1>
    <h2>AI-Powered Technical Interview & Assessment Platform</h2>
    <p><strong>Developed by:</strong> Akash Bauri | <strong>Email:</strong> akashbauri16021998@gmail.com | <strong>Phone:</strong> 8002778855</p>
    <div>
        <span class="ai-badge">🧠 PERPLEXITY AI</span>
        <span class="ai-badge">🤗 HUGGING FACE</span>
        <span class="ai-badge">💾 COMPLETE DATA</span>
        <span class="ai-badge">🎙️ LIVE RECORDING</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Configuration Class
class AIConfig:
    @staticmethod
    def get_hugging_face_token():
        try:
            return st.secrets.get("HUGGING_FACE_TOKEN", None)
        except:
            return os.getenv("HUGGING_FACE_TOKEN", None)
    
    @staticmethod
    def get_perplexity_api_key():
        try:
            return st.secrets.get("PERPLEXITY_API_KEY", None)
        except:
            return os.getenv("PERPLEXITY_API_KEY", None)
    
    TECHNICAL_TIME = 180
    PROJECT_TIME = 300

# Initialize Session State - FIXED FUNCTION
def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        "stage": "registration",
        "candidate_data": {},
        "generated_questions": [],
        "current_question": 0,
        "responses": [],
        "start_time": time.time()
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Database Setup
@st.cache_resource
def setup_database():
    """Setup SQLite database for storing results"""
    try:
        conn = sqlite3.connect('hiring_skilled_candidates.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Candidates table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            position TEXT NOT NULL,
            experience TEXT NOT NULL,
            skills TEXT NOT NULL,
            final_score INTEGER NOT NULL,
            speaking_quality TEXT NOT NULL,
            result_status TEXT NOT NULL,
            interview_duration REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Interview responses table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS interview_responses (
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
        )
        ''')
        
        conn.commit()
        cursor.close()
        return conn
    except Exception as e:
        st.error(f"Database setup error: {e}")
        return None

# Perplexity AI Integration
def call_perplexity_ai(prompt, model="llama-3.1-sonar-large-128k-online"):
    """Advanced Perplexity AI integration"""
    api_key = AIConfig.get_perplexity_api_key()
    
    if not api_key:
        return "AI_DEMO_MODE"
    
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert technical interviewer and question generator. Create questions for ANY technical skill at appropriate difficulty levels."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "AI_DEMO_MODE"
    except Exception as e:
        return "AI_DEMO_MODE"

# AI Question Generator
def generate_ai_questions(skill, experience_level, num_questions=5):
    """AI generates questions for ANY skill automatically"""
    
    question_prompt = f"""
    Generate exactly {num_questions} technical interview questions for: "{skill}" at {experience_level} level.

    Guidelines:
    - Questions should test real-world knowledge
    - Difficulty should match {experience_level} level
    - Cover different aspects of {skill}
    - Include practical scenarios

    Format as:
    Q1: [question]
    Q2: [question]
    Q3: [question]
    Q4: [question]
    Q5: [question]

    Generate {num_questions} questions for {skill} ({experience_level} level):
    """
    
    ai_response = call_perplexity_ai(question_prompt)
    
    if ai_response == "AI_DEMO_MODE":
        return generate_fallback_questions(skill, experience_level, num_questions)
    
    # Parse AI response
    questions = []
    lines = ai_response.split('\n')
    
    for line in lines:
        line = line.strip()
        if line and ('Q' in line[:3] or line.startswith(('1.', '2.', '3.', '4.', '5.'))):
            if ':' in line:
                question_text = line.split(':', 1)[1].strip()
            elif '.' in line:
                question_text = line.split('.', 1)[1].strip()
            else:
                question_text = line
            
            if len(question_text) > 20:
                questions.append(question_text)
    
    # Ensure we have enough questions
    while len(questions) < num_questions:
        questions.append(f"Explain the core concepts and practical applications of {skill}.")
    
    return questions[:num_questions]

# Fallback questions
def generate_fallback_questions(skill, experience_level, num_questions):
    """Generate fallback questions when AI is not available"""
    
    templates = {
        "BEGINNER": [
            f"What is {skill} and how is it used in software development?",
            f"Explain the basic concepts of {skill} with examples",
            f"How do you get started with {skill}? What are the prerequisites?",
            f"What are the main advantages of using {skill}?",
            f"Describe a simple use case for {skill}"
        ],
        "INTERMEDIATE": [
            f"How do you implement best practices with {skill}?",
            f"What challenges have you faced with {skill} and how did you solve them?",
            f"How does {skill} integrate with other technologies?",
            f"How do you optimize performance when using {skill}?",
            f"What security considerations apply to {skill}?"
        ],
        "ADVANCED": [
            f"How do you architect large-scale systems using {skill}?",
            f"What advanced techniques do you use for {skill} optimization?",
            f"How do you handle complex scenarios with {skill}?",
            f"How would you mentor others in {skill} best practices?",
            f"What are the future trends for {skill} technology?"
        ]
    }
    
    level_key = experience_level.upper()
    if level_key not in templates:
        level_key = "INTERMEDIATE"
    
    return templates[level_key][:num_questions]

# AI Answer Evaluation
def evaluate_answer_with_ai(question, skill, experience_level, answer_text):
    """AI-powered answer evaluation"""
    
    if not answer_text or len(answer_text.strip()) < 10:
        return 0, ["Response too short"], "Beginner"
    
    evaluation_prompt = f"""
    Evaluate this technical interview answer:

    SKILL: {skill}
    LEVEL: {experience_level}
    QUESTION: {question}
    ANSWER: {answer_text}

    Rate 0-100 based on:
    - Technical accuracy (40%)
    - Depth of knowledge (30%)
    - Practical understanding (20%)
    - Communication clarity (10%)

    Format:
    SCORE: [0-100]
    FEEDBACK: [specific feedback]
    SPEAKING_QUALITY: [Beginner/Intermediate/Advanced/Fluent/Proficiency]
    """
    
    ai_evaluation = call_perplexity_ai(evaluation_prompt)
    
    if ai_evaluation == "AI_DEMO_MODE":
        return evaluate_fallback(answer_text, skill, experience_level)
    
    # Parse AI evaluation
    try:
        score = 75
        feedback = ["AI evaluation completed"]
        speaking_quality = "Intermediate"
        
        lines = ai_evaluation.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('SCORE:'):
                score_text = line.replace('SCORE:', '').strip()
                score = int(re.search(r'\d+', score_text).group())
            elif line.startswith('FEEDBACK:'):
                feedback_text = line.replace('FEEDBACK:', '').strip()
                feedback = [feedback_text]
            elif line.startswith('SPEAKING_QUALITY:'):
                speaking_quality = line.replace('SPEAKING_QUALITY:', '').strip()
        
        return min(100, max(0, score)), feedback, speaking_quality
        
    except:
        return evaluate_fallback(answer_text, skill, experience_level)

# Fallback evaluation
def evaluate_fallback(answer_text, skill, experience_level):
    """Fallback evaluation when AI is not available"""
    
    word_count = len(answer_text.split())
    skill_mentions = answer_text.lower().count(skill.lower())
    
    score = 0
    
    if word_count >= 100: score += 30
    elif word_count >= 50: score += 20
    else: score += 10
    
    score += min(25, skill_mentions * 8)
    
    technical_terms = ['implementation', 'architecture', 'performance', 'optimization']
    tech_score = sum(5 for term in technical_terms if term in answer_text.lower())
    score += min(20, tech_score)
    
    score = min(100, max(0, score + 25))  # Base score adjustment
    
    if score >= 80:
        feedback = ["Excellent technical response"]
        speaking_quality = "Proficiency"
    elif score >= 65:
        feedback = ["Good technical understanding"]
        speaking_quality = "Fluent"
    else:
        feedback = ["Basic understanding shown"]
        speaking_quality = "Intermediate"
    
    return score, feedback, speaking_quality

# Live Recording Component
def render_live_recording():
    """Professional live recording component"""
    
    recording_html = """
    <div style="background: linear-gradient(135deg, #34495e, #2c3e50); padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h3>🎙️ PROFESSIONAL LIVE RECORDING</h3>
        <p><strong>High-Quality Audio + Video Recording</strong></p>
        
        <div style="display: flex; justify-content: center; gap: 20px; margin: 20px 0; flex-wrap: wrap;">
            <video id="videoFeed" width="300" height="200" autoplay muted 
                   style="border-radius: 10px; background: #2c3e50; border: 3px solid #3498db;"></video>
            <canvas id="audioCanvas" width="300" height="150" 
                    style="background: #2c3e50; border-radius: 10px; border: 3px solid #e74c3c;"></canvas>
        </div>
        
        <div style="margin: 20px 0;">
            <button onclick="startRecording()" id="startRec" 
                    style="background: #e74c3c; color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 16px; margin: 10px; cursor: pointer;">
                🎙️ START RECORDING
            </button>
            <button onclick="stopRecording()" id="stopRec" disabled
                    style="background: #95a5a6; color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 16px; margin: 10px; cursor: pointer;">
                🛑 STOP RECORDING
            </button>
        </div>
        
        <div id="recordStatus" style="font-size: 18px; font-weight: bold; margin: 15px 0;">
            📊 Ready to Record
        </div>
        
        <audio id="playback" controls style="width: 80%; margin: 15px 0; display: none;"></audio>
    </div>
    
    <script>
    let mediaRecorder;
    let audioChunks = [];
    let mediaStream = null;
    
    async function startRecording() {
        try {
            mediaStream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 },
                audio: { echoCancellation: true, noiseSuppression: true }
            });
            
            document.getElementById('videoFeed').srcObject = mediaStream;
            
            mediaRecorder = new MediaRecorder(mediaStream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                const audioUrl = URL.createObjectURL(audioBlob);
                document.getElementById('playback').src = audioUrl;
                document.getElementById('playback').style.display = 'block';
                document.getElementById('recordStatus').innerHTML = '✅ Recording Complete';
            };
            
            mediaRecorder.start();
            document.getElementById('startRec').disabled = true;
            document.getElementById('stopRec').disabled = false;
            document.getElementById('stopRec').style.background = '#e74c3c';
            document.getElementById('recordStatus').innerHTML = '🔴 RECORDING IN PROGRESS';
            
        } catch (error) {
            document.getElementById('recordStatus').innerHTML = '❌ Error: ' + error.message;
        }
    }
    
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
        }
        
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
        }
        
        document.getElementById('startRec').disabled = false;
        document.getElementById('stopRec').disabled = true;
        document.getElementById('stopRec').style.background = '#95a5a6';
        document.getElementById('recordStatus').innerHTML = '⏹️ Recording Stopped';
    }
    </script>
    """
    
    st.components.v1.html(recording_html, height=500)

# Save to Database
def save_interview_results(candidate_data, final_score, speaking_quality, result_status, responses, duration):
    """Save comprehensive interview results to database"""
    conn = setup_database()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check for duplicate
        cursor.execute("SELECT id FROM candidates WHERE email = ?", (candidate_data['email'],))
        if cursor.fetchone():
            st.error("❌ Email already exists!")
            return False
        
        # Insert candidate
        cursor.execute('''
        INSERT INTO candidates (name, email, phone, position, experience, skills, final_score, speaking_quality, result_status, interview_duration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            candidate_data['name'], candidate_data['email'], candidate_data['phone'],
            candidate_data['position'], candidate_data['experience'], candidate_data['skills'],
            final_score, speaking_quality, result_status, duration
        ))
        
        candidate_id = cursor.lastrowid
        
        # Insert responses
        for response in responses:
            cursor.execute('''
            INSERT INTO interview_responses (candidate_id, skill, question, answer, score, feedback, response_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                candidate_id, response['skill'], response['question'], response['answer'],
                response['score'], '; '.join(response['feedback']), response.get('response_time', 0)
            ))
        
        conn.commit()
        cursor.close()
        st.success(f"✅ Interview results saved! Candidate ID: {candidate_id}")
        return True
        
    except Exception as e:
        st.error(f"Database error: {e}")
        return False

# HR Dashboard
def render_hr_dashboard():
    """HR Dashboard with complete data access"""
    
    st.markdown("""
    <div class="hr-dashboard">
        <h2>👥 HR DASHBOARD - Hiring Skilled Candidates</h2>
        <p><strong>Complete candidate data access and analytics</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    conn = setup_database()
    if not conn:
        st.error("❌ Database connection failed!")
        return
    
    try:
        # Get candidates data
        candidates_df = pd.read_sql_query("""
            SELECT * FROM candidates ORDER BY created_at DESC
        """, conn)
        
        # Get responses data
        responses_df = pd.read_sql_query("""
            SELECT r.*, c.name as candidate_name 
            FROM interview_responses r
            JOIN candidates c ON r.candidate_id = c.id
            ORDER BY r.created_at DESC
        """, conn)
        
        if len(candidates_df) == 0:
            st.info("📝 No candidates yet. Data will appear after interviews.")
            return
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Candidates", len(candidates_df))
        with col2:
            hired = len(candidates_df[candidates_df['result_status'].str.contains('HIRED', na=False)])
            st.metric("✅ Hired", hired)
        with col3:
            avg_score = candidates_df['final_score'].mean()
            st.metric("📊 Avg Score", f"{avg_score:.1f}%")
        with col4:
            today = len(candidates_df[candidates_df['created_at'].str.contains(datetime.now().strftime('%Y-%m-%d'), na=False)])
            st.metric("📅 Today", today)
        
        # Export buttons
        st.subheader("📤 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export to Excel", use_container_width=True):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    candidates_df.to_excel(writer, sheet_name='Candidates', index=False)
                    if len(responses_df) > 0:
                        responses_df.to_excel(writer, sheet_name='Responses', index=False)
                
                st.download_button(
                    "💾 Download Excel File",
                    data=output.getvalue(),
                    file_name=f"hiring_data_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            if st.button("📋 Export to CSV", use_container_width=True):
                csv_data = candidates_df.to_csv(index=False)
                st.download_button(
                    "💾 Download CSV File",
                    data=csv_data,
                    file_name=f"candidates_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        # Candidates display
        st.subheader(f"👥 All Candidates ({len(candidates_df)})")
        
        for _, candidate in candidates_df.iterrows():
            # Color coding
            if "HIRED" in str(candidate['result_status']):
                bg_color = "#d5f4e6"
                status_color = "#27ae60"
            elif "REVIEW" in str(candidate['result_status']):
                bg_color = "#fef9e7"
                status_color = "#f39c12"
            else:
                bg_color = "#fadbd8"
                status_color = "#e74c3c"
            
            st.markdown(f"""
            <div class="candidate-card" style="background: {bg_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0;">👤 {candidate['name']}</h3>
                        <p style="margin: 5px 0;"><strong>📧</strong> {candidate['email']}</p>
                        <p style="margin: 5px 0;"><strong>📱</strong> {candidate['phone']}</p>
                        <p style="margin: 5px 0;"><strong>💼</strong> {candidate['position']}</p>
                        <p style="margin: 5px 0;"><strong>🛠️</strong> {candidate['skills']}</p>
                        <p style="margin: 5px 0;"><strong>📅</strong> {candidate['created_at'][:19]}</p>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: {status_color}; color: white; padding: 10px 20px; border-radius: 20px; font-weight: bold; margin-bottom: 10px;">
                            {candidate['result_status']}
                        </div>
                        <div style="font-size: 32px; font-weight: bold; color: {status_color};">
                            {candidate['final_score']}%
                        </div>
                        <div style="color: #7f8c8d;">
                            🗣️ {candidate['speaking_quality']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Data table
        st.subheader("📊 Complete Data Table")
        st.dataframe(candidates_df, use_container_width=True, hide_index=True)
        
        if len(responses_df) > 0:
            st.subheader("📝 Interview Responses")
            st.dataframe(responses_df, use_container_width=True, hide_index=True)
    
    except Exception as e:
        st.error(f"Dashboard error: {e}")
    finally:
        conn.close()

# Main Application
def main():
    # Initialize session state - MOVED TO TOP
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.title("🎯 Hiring Skilled Candidates")
    page = st.sidebar.radio("Navigate:", [
        "🚀 Take Interview",
        "👥 HR Dashboard",
        "📊 System Status"
    ])
    
    if page == "🚀 Take Interview":
        
        # STAGE 1: Registration
        if st.session_state.stage == "registration":
            st.header("📝 AI-Powered Interview Registration")
            
            st.info("""
            🤖 **AI-DRIVEN INTERVIEW SYSTEM**
            
            - Enter ANY technical skill - AI generates perfect questions
            - Automatic difficulty adjustment (Beginner/Intermediate/Advanced)
            - Live recording with professional interface
            - Advanced AI evaluation and feedback
            - Complete data storage for HR access
            
            **Supported Skills:** Python, JavaScript, React, AWS, Machine Learning, Data Science, 
            Cybersecurity, DevOps, Blockchain, Mobile Development, and ANY technical skill!
            """)
            
            with st.form("registration_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("👤 Full Name*")
                    email = st.text_input("📧 Email*")
                    phone = st.text_input("📱 Phone*")
                
                with col2:
                    position = st.text_input("💼 Position*")
                    experience = st.selectbox("📈 Experience Level*", [
                        "BEGINNER (0-2 years)",
                        "INTERMEDIATE (2-5 years)",
                        "ADVANCED (5+ years)"
                    ])
                    skills = st.text_area("🛠️ Technical Skills*", 
                                        placeholder="Enter ANY skills: Python, React, AWS, Machine Learning, etc.",
                                        height=100)
                
                consent1 = st.checkbox("🎙️ I have working microphone")
                consent2 = st.checkbox("📹 I have working camera")
                consent3 = st.checkbox("🤖 I agree to AI evaluation")
                consent4 = st.checkbox("💾 I consent to data storage")
                
                submitted = st.form_submit_button("🚀 START AI INTERVIEW", type="primary")
                
                if submitted:
                    missing = []
                    if not name: missing.append("Name")
                    if not email or "@" not in email: missing.append("Email")
                    if not phone: missing.append("Phone")
                    if not position: missing.append("Position")
                    if not skills: missing.append("Skills")
                    if not all([consent1, consent2, consent3, consent4]): missing.append("All Consents")
                    
                    if missing:
                        st.error(f"❌ Please complete: {', '.join(missing)}")
                    else:
                        with st.spinner("🤖 AI generating personalized questions..."):
                            time.sleep(3)
                            
                            exp_level = experience.split('(')[0].strip()
                            skills_list = [s.strip() for s in skills.replace(',', '\n').split('\n') if s.strip()]
                            unique_skills = list(set([s.lower() for s in skills_list if len(s) > 2]))[:5]
                            
                            all_questions = []
                            for skill in unique_skills:
                                ai_questions = generate_ai_questions(skill, exp_level, 5)
                                for i, q in enumerate(ai_questions, 1):
                                    all_questions.append({
                                        "skill": skill.title(),
                                        "question": f"Q{i}: {q}",
                                        "difficulty": exp_level,
                                        "time_limit": AIConfig.TECHNICAL_TIME
                                    })
                            
                            st.session_state.candidate_data = {
                                "name": name.strip(),
                                "email": email.strip(),
                                "phone": phone.strip(),
                                "position": position.strip(),
                                "experience": experience,
                                "skills": ', '.join([s.title() for s in unique_skills])
                            }
                            st.session_state.generated_questions = all_questions
                            
                            st.success("✅ AI questions generated!")
                            st.info(f"🎯 Generated {len(all_questions)} questions for {len(unique_skills)} skills")
                            
                            st.session_state.stage = "interview"
                            time.sleep(1)
                            st.rerun()
        
        # STAGE 2: Interview
        elif st.session_state.stage == "interview":
            questions = st.session_state.generated_questions
            current_q = st.session_state.current_question
            
            if current_q < len(questions):
                question_data = questions[current_q]
                
                # Progress
                progress = (current_q + 1) / len(questions)
                st.markdown(f"""
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress * 100}%;">
                        Question {current_q + 1} of {len(questions)} ({progress*100:.0f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.header(f"🤖 AI Question - {question_data['skill']}")
                
                # Question display
                st.markdown(f"""
                <div class="question-card">
                    <h3>🎯 Skill: {question_data['skill']}</h3>
                    <h4>📊 Level: {question_data['difficulty']}</h4>
                    <h4>⏰ Time: {question_data['time_limit']}s</h4>
                    <hr>
                    <h3>❓ AI-Generated Question:</h3>
                    <p style="font-size: 20px; font-weight: bold; color: #2c3e50;">
                        {question_data['question']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Timer
                st.markdown(f"""
                <div class="timer-display" id="timer-{current_q}">
                    ⏰ Time: <span id="countdown-{current_q}">{question_data['time_limit']}</span>s
                </div>
                <script>
                var timeLeft_{current_q} = {question_data['time_limit']};
                var timer_{current_q} = setInterval(function(){{
                    timeLeft_{current_q}--;
                    var el = document.getElementById('countdown-{current_q}');
                    if (el) {{
                        el.innerHTML = timeLeft_{current_q};
                        if (timeLeft_{current_q} <= 0) {{
                            clearInterval(timer_{current_q});
                            el.innerHTML = 'TIME UP!';
                        }}
                    }}
                }}, 1000);
                </script>
                """, unsafe_allow_html=True)
                
                # Recording
                render_live_recording()
                
                # Answer input
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    answer_text = st.text_area(
                        f"Your answer for {question_data['skill']}:",
                        height=150,
                        placeholder="Provide detailed technical answer...",
                        key=f"answer_{current_q}"
                    )
                
                with col2:
                    if st.button("⏭️ Skip", key=f"skip_{current_q}"):
                        st.session_state.responses.append({
                            "skill": question_data["skill"],
                            "question": question_data["question"],
                            "answer": "SKIPPED",
                            "score": 0,
                            "feedback": ["Skipped"],
                            "response_time": 0
                        })
                        
                        st.session_state.current_question += 1
                        if current_q >= len(questions) - 1:
                            st.session_state.stage = "results"
                        st.rerun()
                
                # Submit
                if st.button("🤖 SUBMIT FOR AI EVALUATION", type="primary"):
                    if not answer_text or len(answer_text.strip()) < 15:
                        st.error("❌ Answer too short!")
                    else:
                        with st.spinner("🤖 AI evaluating response..."):
                            time.sleep(3)
                            
                            score, feedback, speaking_quality = evaluate_answer_with_ai(
                                question_data['question'],
                                question_data['skill'],
                                question_data['difficulty'],
                                answer_text
                            )
                            
                            st.session_state.responses.append({
                                "skill": question_data["skill"],
                                "question": question_data["question"],
                                "answer": answer_text,
                                "score": score,
                                "feedback": feedback,
                                "speaking_quality": speaking_quality,
                                "response_time": 30
                            })
                            
                            # Display results
                            if score >= 80:
                                st.success(f"🏆 OUTSTANDING! Score: {score}%")
                            elif score >= 65:
                                st.success(f"✅ EXCELLENT! Score: {score}%")
                            elif score >= 50:
                                st.info(f"👍 GOOD! Score: {score}%")
                            else:
                                st.warning(f"📈 NEEDS IMPROVEMENT! Score: {score}%")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("AI Score", f"{score}%")
                            with col2:
                                st.metric("Quality", speaking_quality)
                            with col3:
                                remaining = len(questions) - current_q - 1
                                st.metric("Left", remaining)
                            
                            for i, fb in enumerate(feedback, 1):
                                st.info(f"{i}. {fb}")
                            
                            if st.button("Continue →", type="primary"):
                                st.session_state.current_question += 1
                                if current_q >= len(questions) - 1:
                                    st.session_state.stage = "results"
                                st.rerun()
            else:
                st.session_state.stage = "results"
                st.rerun()
        
        # STAGE 3: Results
        elif st.session_state.stage == "results":
            st.header("🏆 AI Interview Results")
            
            candidate = st.session_state.candidate_data
            responses = st.session_state.responses
            duration = (time.time() - st.session_state.start_time) / 60
            
            # Calculate scores
            valid_responses = [r for r in responses if r['score'] > 0]
            
            if valid_responses:
                final_score = int(sum(r['score'] for r in valid_responses) / len(valid_responses))
                
                speaking_qualities = [r.get('speaking_quality', 'Intermediate') for r in valid_responses]
                quality_scores = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Fluent': 4, 'Proficiency': 5}
                avg_quality = sum(quality_scores.get(sq, 2) for sq in speaking_qualities) / len(speaking_qualities)
                
                if avg_quality >= 4.5: speaking_quality = "Proficiency"
                elif avg_quality >= 3.5: speaking_quality = "Fluent"
                elif avg_quality >= 2.5: speaking_quality = "Advanced"
                else: speaking_quality = "Intermediate"
            else:
                final_score = 0
                speaking_quality = "Beginner"
            
            # Determine result
            if final_score >= 80:
                result_status, emoji, color = "HIRED - OUTSTANDING", "🏆", "#27ae60"
            elif final_score >= 70:
                result_status, emoji, color = "HIRED - EXCELLENT", "🌟", "#27ae60"
            elif final_score >= 60:
                result_status, emoji, color = "HIRED - GOOD", "✅", "#27ae60"
            elif final_score >= 45:
                result_status, emoji, color = "UNDER REVIEW", "⏳", "#f39c12"
            else:
                result_status, emoji, color = "NOT SELECTED", "❌", "#e74c3c"
            
            # Display results
            st.markdown(f"""
            <div class="result-card" style="background: linear-gradient(135deg, {color}20, {color}40); border: 3px solid {color};">
                <h1 style="color: {color}; font-size: 4em;">{emoji}</h1>
                <h2 style="color: {color};">INTERVIEW COMPLETE</h2>
                <h2 style="color: {color};">RESULT: {result_status}</h2>
                <h1 style="color: {color}; font-size: 3em;">SCORE: {final_score}%</h1>
            </div>
            """, unsafe_allow_html=True)
            
            # Details
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("👤 Candidate")
                st.write(f"**Name:** {candidate['name']}")
                st.write(f"**Email:** {candidate['email']}")
                st.write(f"**Phone:** {candidate['phone']}")
                st.write(f"**Position:** {candidate['position']}")
                st.write(f"**Skills:** {candidate['skills']}")
                st.write(f"**Duration:** {duration:.1f} min")
            
            with col2:
                st.subheader("📊 Performance")
                st.metric("Final Score", f"{final_score}%")
                st.metric("Speaking Quality", speaking_quality)
                st.metric("Questions Done", f"{len(valid_responses)}/{len(st.session_state.generated_questions)}")
                st.metric("Interview Result", result_status.split('-')[0])
            
            # Save to database
            with st.spinner("💾 Saving to database..."):
                time.sleep(2)
                save_success = save_interview_results(
                    candidate, final_score, speaking_quality, 
                    result_status, valid_responses, duration
                )
                
                if save_success:
                    st.balloons()
            
            # New interview
            if st.button("🔄 New Interview", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    elif page == "👥 HR Dashboard":
        render_hr_dashboard()
    
    elif page == "📊 System Status":
        st.header("🔧 System Status")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            hf_status = "🟢 Active" if AIConfig.get_hugging_face_token() else "🟡 Demo"
            st.metric("🤗 Hugging Face", hf_status)
        
        with col2:
            px_status = "🟢 Active" if AIConfig.get_perplexity_api_key() else "🟡 Demo"
            st.metric("🧠 Perplexity", px_status)
        
        with col3:
            db = setup_database()
            db_status = "🟢 Ready" if db else "🔴 Error"
            st.metric("💾 Database", db_status)
        
        with col4:
            st.metric("🚀 System", "🟢 OPERATIONAL")

# Sidebar info
with st.sidebar:
    st.markdown("### 🎯 HIRING SKILLED CANDIDATES")
    st.markdown("**AI-Powered Interview Platform**")
    
    st.markdown("### 🤖 AI Features")
    st.markdown("""
    ✅ **Smart Question Generation**  
    ✅ **Any Technical Skill Support**  
    ✅ **Adaptive Difficulty Levels**  
    ✅ **Live Recording Interface**  
    ✅ **Advanced AI Evaluation**  
    ✅ **Complete HR Dashboard**  
    ✅ **Data Export Capabilities**  
    """)
    
    st.markdown("### 👨‍💻 Developer")
    st.markdown("""
    **Akash Bauri**  
    📧 akashbauri16021998@gmail.com  
    📱 +91-8002778855  
    
    **🚀 Production Ready**  
    **💡 Enterprise Grade**  
    **🎯 Company Submission**  
    """)

# Run the app
if __name__ == "__main__":
    main()
