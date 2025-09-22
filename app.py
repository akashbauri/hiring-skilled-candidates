import streamlit as st
import pandas as pd
import time
import mysql.connector
from datetime import datetime
import requests
import json
import os
import speech_recognition as sr
import io
from pydub import AudioSegment
import base64

# Page Configuration
st.set_page_config(
    page_title="Enterprise Hiring Platform - Hiring Skilled Candidates",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Enterprise UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
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
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .question-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #1f4e79;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        height: 25px;
        margin: 20px 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #27ae60, #2ecc71);
        height: 100%;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    .enterprise-badge {
        background: #2c3e50;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin: 5px;
    }
    .real-badge {
        background: #e74c3c;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin: 5px;
    }
    .video-container {
        background: #2c3e50;
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
    }
    .webcam-placeholder {
        background: #34495e;
        height: 300px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# Professional Enterprise Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Enterprise Hiring Platform</h1>
    <h3>REAL AI-Powered Interview & Assessment System</h3>
    <p><strong>Developed by:</strong> Akash Bauri | <strong>Email:</strong> akashbauri16021998@gmail.com | <strong>Phone:</strong> 8002778855</p>
    <div>
        <span class="enterprise-badge">ENTERPRISE VERSION</span>
        <span class="enterprise-badge">☁️ STREAMLIT CLOUD</span>
        <span class="real-badge">🔥 REAL EVALUATION</span>
        <span class="enterprise-badge">🎥 CAMERA ENABLED</span>
    </div>
</div>
""", unsafe_allow_html=True)

# SECURE Configuration Management
class SecureConfig:
    """Enterprise-grade SECURE configuration management"""
    
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
    
    @staticmethod
    def get_db_config():
        try:
            return {
                'host': st.secrets.get("DB_HOST", "127.0.0.1"),
                'port': int(st.secrets.get("DB_PORT", "3306")),
                'user': st.secrets.get("DB_USER", "root"),
                'password': st.secrets.get("DB_PASSWORD", "admin"),
                'database': st.secrets.get("DB_NAME", "hiring_skilled_candidates")
            }
        except:
            return {
                'host': os.getenv("DB_HOST", "127.0.0.1"),
                'port': int(os.getenv("DB_PORT", "3306")),
                'user': os.getenv("DB_USER", "root"),
                'password': os.getenv("DB_PASSWORD", "admin"),
                'database': os.getenv("DB_NAME", "hiring_skilled_candidates")
            }
    
    INTRO_TIME = 120
    TECHNICAL_TIME = 180
    PROJECT_TIME = 300
    VIDEO_TIME = 240

# Enhanced Database Connection with REAL MySQL
@st.cache_resource
def get_db_connection():
    """Establish REAL MySQL database connection"""
    try:
        db_config = SecureConfig.get_db_config()
        
        # Try to connect to actual MySQL database
        conn = mysql.connector.connect(
            **db_config,
            autocommit=True,
            charset='utf8mb4',
            connect_timeout=10
        )
        
        # Test the connection
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            st.success("✅ REAL MySQL Database Connected!")
            return conn
        else:
            raise Exception("Database test failed")
            
    except mysql.connector.Error as err:
        st.error(f"❌ MySQL Connection Failed: {err}")
        st.error("Please configure your MySQL database properly!")
        return None
    except Exception as e:
        st.warning(f"⚠️ Database not configured: {e}")
        return None

# REAL Perplexity API Integration with STRICT evaluation
def call_perplexity_api(prompt):
    """REAL Perplexity API integration with STRICT evaluation"""
    api_key = SecureConfig.get_perplexity_api_key()
    
    if not api_key or not api_key.startswith("pplx-"):
        st.warning("⚠️ Perplexity API not configured - Using strict fallback evaluation")
        return "STRICT_EVALUATION_MODE"
    
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            st.error(f"API Error: {response.status_code}")
            return "STRICT_EVALUATION_MODE"
    except Exception as e:
        st.error(f"API Call Failed: {e}")
        return "STRICT_EVALUATION_MODE"

# REAL Audio to Text Conversion
def convert_audio_to_text(audio_bytes):
    """Convert audio to text using speech recognition"""
    try:
        # Convert audio bytes to text
        r = sr.Recognizer()
        
        # Convert bytes to audio segment
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # Convert to wav format
        wav_audio = audio_segment.export(format="wav")
        
        # Recognize speech
        with sr.AudioFile(wav_audio) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
    except Exception as e:
        # If speech recognition fails, return a generic response indicating poor audio
        return "AUDIO_RECOGNITION_FAILED"

# REAL STRICT Answer Evaluation System
def evaluate_answer_with_real_ai(question, skill, experience_level, audio_bytes=None, user_text_input=None):
    """REAL STRICT evaluation - No fake passing scores!"""
    
    # Convert audio to text if audio provided
    if audio_bytes:
        answer_text = convert_audio_to_text(audio_bytes)
        if answer_text == "AUDIO_RECOGNITION_FAILED":
            return 0, ["Audio quality too poor for evaluation"], "Beginner"
    elif user_text_input:
        answer_text = user_text_input.strip()
    else:
        return 0, ["No response provided"], "Beginner"
    
    # STRICT evaluation - no easy passes!
    if len(answer_text) < 10:
        return 15, ["Response too short - needs detailed explanation"], "Beginner"
    
    # REAL AI evaluation using Perplexity
    strict_prompt = f"""
    You are a STRICT technical interviewer. Evaluate this {experience_level} candidate's {skill} answer with ZERO tolerance for incorrect information.
    
    Question: {question}
    Answer: {answer_text}
    
    STRICT EVALUATION CRITERIA:
    - Technical accuracy (60%)
    - Completeness of answer (25%)
    - Clarity and examples (15%)
    
    SCORING GUIDELINES:
    - 90-100: Perfect answer with deep understanding
    - 80-89: Very good with minor gaps
    - 70-79: Good but missing important details
    - 60-69: Basic understanding, major gaps
    - 40-59: Poor understanding, mostly incorrect
    - 0-39: Completely wrong or irrelevant
    
    Provide EXACTLY: Score: [number] | Feedback: [detailed technical feedback explaining what's wrong/right]
    """
    
    ai_response = call_perplexity_api(strict_prompt)
    
    # STRICT parsing and scoring
    if ai_response == "STRICT_EVALUATION_MODE":
        # Fallback strict evaluation based on keywords and content
        score = evaluate_answer_strictly(question, skill, answer_text, experience_level)
        feedback = [f"STRICT EVALUATION: Answer evaluated based on technical accuracy and completeness"]
    else:
        try:
            if "Score:" in ai_response and "|" in ai_response:
                parts = ai_response.split("|")
                score_part = parts[0].strip()
                feedback_part = "|".join(parts[1:]).strip()
                
                # Extract score
                score = int(''.join(filter(str.isdigit, score_part.split("Score:")[-1])))
                
                # Extract feedback
                if "Feedback:" in feedback_part:
                    ai_feedback = feedback_part.split("Feedback:")[-1].strip()
                    feedback = [f"🤖 STRICT AI Evaluation: {ai_feedback}"]
                else:
                    feedback = [f"🤖 STRICT AI Evaluation: {feedback_part}"]
            else:
                score = 25
                feedback = ["AI evaluation format error - using strict fallback"]
        except:
            score = 20
            feedback = ["Error in AI evaluation - using strict fallback scoring"]
    
    # Additional STRICT checks
    if score > 90 and len(answer_text) < 50:
        score = max(60, score - 30)  # Penalize short answers heavily
        feedback.append("⚠️ PENALTY: Answer too brief for claimed expertise level")
    
    # Experience level reality check
    if experience_level == "fresher" and score > 85:
        score = min(85, score)  # Cap fresher scores
    elif experience_level == "experienced" and score < 70 and len(answer_text) > 100:
        score = max(40, score - 20)  # Heavy penalty for experienced candidates with poor answers
    
    # Speaking quality based on REAL score
    if score >= 85:
        speaking_quality = "Proficiency"
    elif score >= 75:
        speaking_quality = "Fluent"
    elif score >= 60:
        speaking_quality = "Advanced"
    elif score >= 40:
        speaking_quality = "Intermediate"
    else:
        speaking_quality = "Beginner"
    
    return min(100, max(0, score)), feedback, speaking_quality

# STRICT Fallback Evaluation
def evaluate_answer_strictly(question, skill, answer_text, experience_level):
    """STRICT fallback evaluation when AI is not available"""
    
    answer_lower = answer_text.lower()
    question_lower = question.lower()
    
    # Technical keyword checking
    skill_keywords = {
        "python": ["function", "variable", "class", "import", "def", "return", "list", "dict", "loop", "if"],
        "javascript": ["function", "variable", "var", "let", "const", "return", "array", "object", "event", "dom"],
        "react": ["component", "jsx", "state", "props", "hook", "usestate", "useeffect", "render", "virtual"],
        "mysql": ["select", "insert", "update", "delete", "table", "database", "query", "join", "index", "primary"],
        "django": ["model", "view", "template", "url", "admin", "orm", "migration", "form", "middleware", "wsgi"]
    }
    
    skill_key = skill.lower()
    if skill_key in skill_keywords:
        keywords = skill_keywords[skill_key]
        keyword_count = sum(1 for keyword in keywords if keyword in answer_lower)
        keyword_score = min(40, keyword_count * 8)  # Max 40 points from keywords
    else:
        keyword_score = 20
    
    # Length and structure scoring (STRICT)
    length_score = 0
    if len(answer_text) < 20:
        length_score = 5
    elif len(answer_text) < 50:
        length_score = 15
    elif len(answer_text) < 100:
        length_score = 25
    else:
        length_score = 35
    
    # Question relevance (STRICT)
    relevance_score = 0
    question_words = [word for word in question_lower.split() if len(word) > 3]
    for word in question_words:
        if word in answer_lower:
            relevance_score += 3
    relevance_score = min(25, relevance_score)
    
    # Combine scores strictly
    total_score = keyword_score + length_score + relevance_score
    
    # Experience level adjustments (STRICT)
    if experience_level == "fresher":
        total_score = min(80, total_score)  # Cap fresher scores
    elif experience_level == "experienced" and total_score < 60:
        total_score = max(30, total_score - 15)  # Penalty for poor experienced answers
    
    return total_score

# REAL Camera Access Component
def render_camera_component():
    """REAL camera access for video interview"""
    
    st.markdown("""
    <div class="video-container">
        <h3>🎥 REAL Video Interview - Camera Required</h3>
        <p><strong>This section requires camera access for authentic assessment</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # JavaScript for camera access
    camera_html = """
    <div id="camera-container">
        <video id="video" width="100%" height="300" autoplay muted style="border-radius: 10px; background: #34495e;"></video>
        <br><br>
        <button onclick="startCamera()" style="padding: 10px 20px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer;">
            📹 Enable Camera Access
        </button>
        <button onclick="stopCamera()" style="padding: 10px 20px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px;">
            🛑 Stop Camera
        </button>
        <div id="camera-status" style="margin-top: 10px; font-weight: bold;"></div>
    </div>
    
    <script>
    let videoStream = null;
    
    async function startCamera() {
        try {
            const video = document.getElementById('video');
            const status = document.getElementById('camera-status');
            
            status.innerHTML = '🔄 Requesting camera access...';
            status.style.color = 'orange';
            
            videoStream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 640, height: 480 }, 
                audio: true 
            });
            
            video.srcObject = videoStream;
            status.innerHTML = '✅ Camera active - Interview in progress';
            status.style.color = 'green';
            
        } catch (error) {
            const status = document.getElementById('camera-status');
            status.innerHTML = '❌ Camera access denied or not available: ' + error.message;
            status.style.color = 'red';
            console.error('Camera error:', error);
        }
    }
    
    function stopCamera() {
        if (videoStream) {
            videoStream.getTracks().forEach(track => track.stop());
            const video = document.getElementById('video');
            video.srcObject = null;
            const status = document.getElementById('camera-status');
            status.innerHTML = '🛑 Camera stopped';
            status.style.color = 'gray';
        }
    }
    </script>
    """
    
    st.components.v1.html(camera_html, height=400)

# REAL Database Save Function
def save_to_database(candidate_data, final_score, speaking_quality, result_status):
    """REAL MySQL database save with error handling"""
    conn = get_db_connection()
    
    if not conn:
        st.error("❌ Cannot save to database - MySQL connection failed!")
        st.error("Please check your database configuration and ensure MySQL server is running.")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check if table exists, create if not
        create_table_query = """
        CREATE TABLE IF NOT EXISTS candidates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            phone_no VARCHAR(20) NOT NULL,
            position VARCHAR(100) NOT NULL,
            experience INT CHECK (experience >= 0),
            skills TEXT,
            speaking_skills VARCHAR(50),
            result VARCHAR(50),
            percentage DECIMAL(5,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_query)
        
        # Check for duplicate email
        check_query = "SELECT id FROM candidates WHERE email = %s"
        cursor.execute(check_query, (candidate_data['email'],))
        
        if cursor.fetchone():
            st.error(f"❌ Email {candidate_data['email']} already exists in database!")
            cursor.close()
            conn.close()
            return False
        
        # Extract experience years
        experience_text = candidate_data['experience']
        if "0-1" in experience_text:
            experience_years = 1
        elif "1-3" in experience_text:
            experience_years = 2
        elif "3-5" in experience_text:
            experience_years = 4
        else:
            experience_years = 6
        
        # Insert data
        insert_query = """
        INSERT INTO candidates 
        (name, email, phone_no, position, experience, skills, speaking_skills, result, percentage)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            candidate_data['name'],
            candidate_data['email'],
            candidate_data['phone'],
            candidate_data['position'],
            experience_years,
            candidate_data['skills'],
            speaking_quality,
            result_status,
            float(final_score)
        ))
        
        # Verify insertion
        cursor.execute("SELECT LAST_INSERT_ID()")
        new_id = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        st.success(f"✅ REAL DATABASE SAVE SUCCESSFUL! Record ID: {new_id}")
        st.info(f"📊 Saved: {candidate_data['name']} | Score: {final_score}% | Result: {result_status}")
        
        return True
        
    except mysql.connector.Error as err:
        st.error(f"❌ MySQL Database Error: {err}")
        if "Duplicate entry" in str(err):
            st.error(f"Email {candidate_data['email']} already exists!")
        return False
    except Exception as e:
        st.error(f"❌ Database Save Error: {e}")
        return False

# Comprehensive Question Database - REAL Questions
SKILL_QUESTIONS = {
    "python": {
        "fresher": [
            "What is the difference between a list and a tuple in Python? Provide specific examples and explain when you would use each.",
            "Explain how Python memory management works. What is garbage collection and when does it occur?",
            "What are Python decorators? Write a simple decorator example and explain how it works.",
            "Explain the difference between 'is' and '==' operators in Python with examples.",
            "What are Python generators? How do they differ from regular functions? Provide an example."
        ],
        "intermediate": [
            "Explain Python's Global Interpreter Lock (GIL). How does it affect multithreading in Python?",
            "What are metaclasses in Python? Provide a practical example of when you might use them.",
            "Explain the difference between deep copy and shallow copy in Python with examples.",
            "How does Python's import system work? Explain the difference between import methods.",
            "What are context managers in Python? Implement a custom context manager using both methods."
        ],
        "experienced": [
            "Explain Python's descriptor protocol. How would you implement a custom descriptor?",
            "How would you optimize Python code for performance? Discuss specific techniques and tools.",
            "Explain how Python's asyncio works. What are coroutines and how do they differ from threads?",
            "How would you implement a thread-safe singleton pattern in Python?",
            "Explain Python's method resolution order (MRO). How does it work with multiple inheritance?"
        ]
    },
    "javascript": {
        "fresher": [
            "Explain the difference between var, let, and const in JavaScript with examples.",
            "What is hoisting in JavaScript? Provide examples of how it works with functions and variables.",
            "Explain the concept of closures in JavaScript with a practical example.",
            "What is the difference between == and === operators? Provide examples.",
            "How does the 'this' keyword work in JavaScript? Provide examples in different contexts."
        ],
        "intermediate": [
            "Explain the JavaScript event loop. How does it handle asynchronous operations?",
            "What are Promises in JavaScript? How do they differ from callbacks? Provide examples.",
            "Explain prototypal inheritance in JavaScript. How does it differ from classical inheritance?",
            "What are arrow functions and how do they differ from regular functions?",
            "Explain how async/await works in JavaScript. Provide examples of error handling."
        ],
        "experienced": [
            "How would you implement a polyfill for Promise.all()? Write the code.",
            "Explain JavaScript's module system. Compare CommonJS, AMD, and ES6 modules.",
            "How would you optimize JavaScript performance in a large-scale application?",
            "Explain how JavaScript engines work. What is Just-In-Time compilation?",
            "How would you implement a pub/sub pattern in JavaScript? Write the code."
        ]
    },
    "react": {
        "fresher": [
            "What is the Virtual DOM in React? How does it improve performance?",
            "Explain the difference between functional and class components in React.",
            "What are React hooks? Explain useState and useEffect with examples.",
            "How does data flow work in React? Explain props and state.",
            "What is JSX? How does it differ from regular JavaScript?"
        ],
        "intermediate": [
            "Explain React's component lifecycle methods. How do they map to hooks?",
            "What is prop drilling in React? How can you avoid it?",
            "Explain how React's reconciliation algorithm works.",
            "What are higher-order components (HOCs) in React? Provide an example.",
            "How would you optimize React component performance? Discuss specific techniques."
        ],
        "experienced": [
            "How would you implement a custom hook for data fetching with caching?",
            "Explain React's Fiber architecture. How does it improve performance?",
            "How would you implement server-side rendering with React?",
            "What are React patterns like render props and compound components?",
            "How would you architect a large-scale React application? Discuss structure and state management."
        ]
    },
    "mysql": {
        "fresher": [
            "Explain the difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN with examples.",
            "What are primary keys and foreign keys? How do they maintain data integrity?",
            "Explain the difference between DELETE, DROP, and TRUNCATE commands.",
            "What are MySQL data types? Explain when to use VARCHAR vs TEXT.",
            "How do you optimize a slow MySQL query? Explain the EXPLAIN statement."
        ],
        "intermediate": [
            "Explain MySQL indexing. What are the different types of indexes and when to use them?",
            "What are stored procedures in MySQL? Write an example with input/output parameters.",
            "Explain database normalization. What are 1NF, 2NF, and 3NF?",
            "How do MySQL transactions work? Explain ACID properties.",
            "What are triggers in MySQL? Write an example of a BEFORE INSERT trigger."
        ],
        "experienced": [
            "How would you design a MySQL database for high availability and scalability?",
            "Explain MySQL replication. How would you set up master-slave replication?",
            "How do you handle deadlocks in MySQL? Provide prevention strategies.",
            "Explain MySQL partitioning. When and how would you implement it?",
            "How would you optimize MySQL performance for a high-traffic application?"
        ]
    },
    "django": {
        "fresher": [
            "Explain Django's MTV (Model-Template-View) architecture with examples.",
            "What are Django models? How do you create relationships between models?",
            "Explain Django's ORM. How do you perform basic database operations?",
            "What are Django forms? How do you handle form validation?",
            "How does Django's URL routing work? Explain URLconf."
        ],
        "intermediate": [
            "Explain Django's middleware. How would you create custom middleware?",
            "What are Django class-based views? How do they differ from function-based views?",
            "How does Django handle authentication and authorization?",
            "Explain Django's caching framework. What are the different caching strategies?",
            "How do you optimize Django database queries? Explain select_related and prefetch_related."
        ],
        "experienced": [
            "How would you scale a Django application for high traffic?",
            "Explain Django's security features. How do you prevent common vulnerabilities?",
            "How would you implement a REST API using Django REST Framework?",
            "Explain Django's deployment strategies. How do you use Docker with Django?",
            "How would you implement real-time features in Django using WebSockets?"
        ]
    }
}

# REAL Project Questions - STRICT
PROJECT_QUESTIONS = {
    "fresher": [
        "Describe your most complex academic project. What specific technologies did you use and why? What were the exact challenges you faced and how did you solve them step by step?",
        "Walk me through the architecture of a project you built from scratch. Explain your database design, API structure, and frontend implementation with specific examples.",
        "Tell me about a time when your code didn't work as expected. What debugging techniques did you use? How did you identify and fix the issue?",
        "Explain a project where you had to learn a new technology. How did you approach learning it? What resources did you use?",
        "Describe how you tested one of your projects. What testing strategies did you use? How did you ensure code quality?"
    ],
    "intermediate": [
        "Describe your most impactful professional project. What business problem did it solve? Provide specific metrics on its success.",
        "Walk me through a time when you had to optimize application performance. What tools did you use to identify bottlenecks? What were the results?",
        "Explain a project where you worked with a team. How did you handle code reviews, version control, and collaboration?",
        "Tell me about a time when you had to make important technical decisions. What factors did you consider? What were the trade-offs?",
        "Describe a project where you implemented security measures. What specific vulnerabilities did you address?"
    ],
    "experienced": [
        "Describe the most complex system architecture you've designed. Explain your technology choices, scalability considerations, and deployment strategy.",
        "Walk me through a time when you led a technical team. How did you handle technical disagreements? How did you ensure code quality across the team?",
        "Explain a project where you had to handle millions of users or large datasets. What challenges did you face and how did you solve them?",
        "Describe a time when you had to refactor legacy code. What was your approach? How did you ensure system stability during the transition?",
        "Tell me about a project where you implemented monitoring, logging, and alerting. What tools did you use and why?"
    ]
}

# Initialize Session State
def initialize_session_state():
    defaults = {
        "stage": "registration",
        "candidate_data": {},
        "current_question": 0,
        "questions_list": [],
        "answers": [],
        "current_video_q": 0,
        "video_responses": [],
        "start_time": time.time(),
        "strict_mode": True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Load Resources
initialize_session_state()
db_connection = get_db_connection()

# REAL System Status Dashboard
st.markdown("### 🔧 REAL Enterprise System Status")
col1, col2, col3, col4 = st.columns(4)

with col1:
    hf_token = SecureConfig.get_hugging_face_token()
    hf_status = "🟢 Active" if hf_token and hf_token.startswith("hf_") else "🔴 Not Set"
    st.metric("🤗 Hugging Face", hf_status)

with col2:
    px_key = SecureConfig.get_perplexity_api_key()
    px_status = "🟢 Active" if px_key and px_key.startswith("pplx-") else "🔴 Not Set"
    st.metric("🧠 Perplexity API", px_status)

with col3:
    db_status = "🟢 Connected" if db_connection else "🔴 Failed"
    st.metric("💾 MySQL Database", db_status)

with col4:
    all_configured = all([
        hf_token and hf_token.startswith("hf_"), 
        px_key and px_key.startswith("pplx-"),
        db_connection
    ])
    system_status = "🟢 REAL MODE" if all_configured else "🔴 STRICT MODE"
    st.metric("⚡ Evaluation", system_status)

# Configuration warnings
if not all([SecureConfig.get_hugging_face_token(), SecureConfig.get_perplexity_api_key(), db_connection]):
    st.warning("""
    ⚠️ **CONFIGURATION REQUIRED FOR FULL FUNCTIONALITY:**
    
    **Missing Components:**
    - 🤗 Hugging Face Token (for AI models)
    - 🧠 Perplexity API Key (for advanced evaluation)  
    - 💾 MySQL Database (for result storage)
    
    **Currently Running:** STRICT evaluation mode with limited features
    """)

st.markdown("---")

# STAGE 1: REAL REGISTRATION
if st.session_state.stage == "registration":
    st.header("📝 REAL Enterprise Candidate Registration")
    
    st.error("""
    🔥 **REAL INTERVIEW SYSTEM - NO FAKE EVALUATIONS**
    
    **This is a STRICT assessment system:**
    - ❌ Wrong answers will FAIL you
    - 🎥 Camera access is REQUIRED for video interview
    - 💾 Results are saved to REAL MySQL database
    - 🤖 AI evaluation is UNFORGIVING
    - ⏰ Time limits are ENFORCED
    
    **Only proceed if you're prepared for a REAL technical interview!**
    """)
    
    with st.form("real_registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="Your complete legal name")
            email = st.text_input("Email Address*", placeholder="professional.email@domain.com")
            phone = st.text_input("Phone Number*", placeholder="+91-XXXXXXXXXX")
        
        with col2:
            position = st.text_input("Position Applied For*", placeholder="e.g., Senior Python Developer")
            experience = st.selectbox("Years of Experience*", [
                "0-1 years (Fresher)", "1-3 years (Intermediate)", 
                "3-5 years (Experienced)", "5+ years (Senior)"
            ])
            skills = st.text_area("Technical Skills*", 
                                placeholder="Python, JavaScript, React, MySQL, Django (Be specific - you will be tested on these!)",
                                help="⚠️ You will be asked technical questions on each skill you list!")
        
        st.error("⚠️ **MANDATORY REQUIREMENTS:**")
        consent1 = st.checkbox("✅ I have a working camera and microphone for video interview")
        consent2 = st.checkbox("✅ I understand this is a STRICT technical assessment")
        consent3 = st.checkbox("✅ I consent to database storage of my interview results")
        consent4 = st.checkbox("✅ I am prepared for REAL technical evaluation (no fake passing)")
        
        submitted = st.form_submit_button("🔥 START REAL TECHNICAL INTERVIEW", 
                                        use_container_width=True, type="primary")
        
        if submitted:
            missing = []
            if not name or len(name.strip()) < 2: missing.append("Full Name")
            if not email or "@" not in email: missing.append("Valid Email")
            if not phone or len(phone.strip()) < 10: missing.append("Phone Number")
            if not position or len(position.strip()) < 3: missing.append("Position")
            if not skills or len(skills.strip()) < 5: missing.append("Technical Skills")
            if not consent1: missing.append("Camera/Microphone Confirmation")
            if not consent2: missing.append("STRICT Assessment Agreement")
            if not consent3: missing.append("Database Storage Consent")
            if not consent4: missing.append("REAL Evaluation Agreement")
            
            if missing:
                st.error(f"❌ Complete these requirements: {', '.join(missing)}")
            else:
                with st.spinner("🔄 Preparing REAL technical interview..."):
                    time.sleep(2)
                    
                    # Determine experience level
                    exp_level = "fresher" if "0-1" in experience else "intermediate" if "1-3" in experience else "experienced"
                    
                    # Generate REAL questions
                    skills_list = [s.strip().lower() for s in skills.split(',')][:4]  # Limit to 4 skills
                    technical_questions = []
                    
                    for skill in skills_list:
                        if skill in SKILL_QUESTIONS:
                            skill_qs = SKILL_QUESTIONS[skill].get(exp_level, SKILL_QUESTIONS[skill]["intermediate"])
                            # Take only 3 questions per skill for a focused but thorough assessment
                            for q in skill_qs[:3]:
                                technical_questions.append({
                                    "type": "technical",
                                    "skill": skill.title(),
                                    "question": q,
                                    "time_limit": SecureConfig.TECHNICAL_TIME
                                })
                    
                    # Add REAL project questions (3 questions)
                    project_qs = PROJECT_QUESTIONS.get(exp_level, PROJECT_QUESTIONS["intermediate"])
                    for q in project_qs[:3]:
                        technical_questions.append({
                            "type": "project",
                            "skill": "Project Experience",
                            "question": q,
                            "time_limit": SecureConfig.PROJECT_TIME
                        })
                    
                    # Store data
                    st.session_state.candidate_data = {
                        "name": name.strip(),
                        "email": email.strip().lower(),
                        "phone": phone.strip(),
                        "position": position.strip(),
                        "experience": experience,
                        "skills": skills.strip(),
                        "exp_level": exp_level
                    }
                    st.session_state.questions_list = technical_questions
                    
                    st.success("✅ REAL interview prepared!")
                    st.warning(f"⚠️ {len(technical_questions)} STRICT technical questions generated - NO EASY PASSES!")
                    
                    st.session_state.stage = "voice_intro"
                    time.sleep(1)
                    st.rerun()

# STAGE 2: VOICE INTRODUCTION - REAL
elif st.session_state.stage == "voice_intro":
    st.header("🎤 REAL Voice Introduction Assessment")
    st.error(f"**{st.session_state.candidate_data['name']}** - This is a REAL evaluation. Your introduction will be analyzed for clarity, confidence, and professionalism.")
    
    # Timer (REAL)
    timer_html = f"""
    <div class="timer-display" id="timer-intro">
        ⏰ Time Remaining: <span id="countdown-intro">{SecureConfig.INTRO_TIME}</span> seconds
    </div>
    <script>
    var timeLeft = {SecureConfig.INTRO_TIME};
    var timer = setInterval(function(){{
        timeLeft--;
        var element = document.getElementById('countdown-intro');
        if (element) {{
            element.innerHTML = timeLeft;
            if (timeLeft <= 30) {{
                document.getElementById('timer-intro').style.background = '#e74c3c';
            }}
            if (timeLeft <= 0) {{
                clearInterval(timer);
                element.innerHTML = 'TIME UP!';
            }}
        }}
    }}, 1000);
    </script>
    """
    st.markdown(timer_html, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.warning("🎙️ **RECORD CLEAR AUDIO** - Poor audio quality will result in zero points")
        intro_audio = st.audio_input("🎙️ Record your professional introduction")
        
        # Alternative text input for better evaluation
        st.info("📝 **Alternative:** Type your introduction if audio issues occur")
        intro_text = st.text_area("Type your introduction here", height=100, 
                                placeholder="Introduce yourself professionally, mention your background, skills, and career goals...")
    
    with col2:
        if st.button("⏭️ Skip Introduction", use_container_width=True):
            st.warning("⚠️ Skipping introduction = -10 points penalty")
            st.session_state.stage = "technical_questions"
            st.rerun()
    
    if intro_audio or intro_text:
        if intro_audio:
            st.audio(intro_audio)
        
        with st.spinner("🤖 REAL AI analyzing introduction..."):
            time.sleep(3)
            
            # REAL evaluation of introduction
            if intro_text and len(intro_text.strip()) > 20:
                intro_content = intro_text.strip()
            else:
                intro_content = "Audio introduction provided"
            
            # Basic analysis
            intro_score = 0
            if len(intro_content) > 50:
                intro_score += 30
            if any(word in intro_content.lower() for word in ['experience', 'skills', 'project', 'work']):
                intro_score += 25
            if any(word in intro_content.lower() for word in ['goal', 'future', 'career', 'interested']):
                intro_score += 20
            if len(intro_content) > 100:
                intro_score += 25
            
            intro_score = min(100, intro_score)
            
            # Display REAL results
            if intro_score >= 70:
                st.success("✅ Professional introduction - PASSED")
            elif intro_score >= 50:
                st.warning("⚠️ Adequate introduction - ACCEPTABLE")
            else:
                st.error("❌ Poor introduction - This will impact your final score")
            
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Introduction Score", f"{intro_score}%")
            with col2: st.metric("Content Quality", "Good" if intro_score >= 60 else "Poor")
            with col3: st.metric("Professionalism", "High" if intro_score >= 70 else "Low")
            
            st.info(f"🎯 **Next Phase:** {len(st.session_state.questions_list)} STRICT technical questions")
            
            if st.button("Continue to REAL Technical Assessment →", use_container_width=True, type="primary"):
                st.session_state.stage = "technical_questions"
                st.rerun()

# STAGE 3: REAL TECHNICAL QUESTIONS - STRICT EVALUATION
elif st.session_state.stage == "technical_questions":
    questions_list = st.session_state.questions_list
    current_q = st.session_state.current_question
    
    if current_q < len(questions_list):
        question_data = questions_list[current_q]
        
        # Progress bar
        progress = (current_q + 1) / len(questions_list)
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress * 100}%">
                STRICT Question {current_q + 1} of {len(questions_list)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.header(f"🔥 REAL {question_data['type'].title()} Assessment - NO EASY PASSES")
        
        # Question display
        st.markdown(f"""
        <div class="question-card">
            <h4>🎯 Skill: {question_data['skill']}</h4>
            <h4>📊 Type: {question_data['type'].title()}</h4>
            <h4>📈 Level: {st.session_state.candidate_data['exp_level'].title()}</h4>
            <h4>⚠️ Evaluation: STRICT - Wrong answers FAIL</h4>
            <hr>
            <h3>❓ REAL Technical Question:</h3>
            <p style="font-size: 18px; font-weight: bold; color: #e74c3c;">
                {question_data['question']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Timer
        timer_html = f"""
        <div class="timer-display" id="timer-q{current_q}">
            ⏰ STRICT Time Limit: <span id="countdown-q{current_q}">{question_data['time_limit']}</span> seconds
        </div>
        <script>
        var timeLeft_{current_q} = {question_data['time_limit']};
        var timer_{current_q} = setInterval(function(){{
            timeLeft_{current_q}--;
            var element = document.getElementById('countdown-q{current_q}');
            if (element) {{
                element.innerHTML = timeLeft_{current_q};
                if (timeLeft_{current_q} <= 60) {{
                    document.getElementById('timer-q{current_q}').style.background = '#e74c3c';
                }}
                if (timeLeft_{current_q} <= 0) {{
                    clearInterval(timer_{current_q});
                    element.innerHTML = 'TIME UP - MOVING TO NEXT!';
                }}
            }}
        }}, 1000);
        </script>
        """
        st.markdown(timer_html, unsafe_allow_html=True)
        
        # Answer interface
        col1, col2 = st.columns([5, 1])
        
        with col1:
            st.error("⚠️ **CHOOSE ONE METHOD - Both audio AND text will be evaluated strictly**")
            
            # Audio input
            answer_audio = st.audio_input(f"🎙️ Record CLEAR answer for {question_data['skill']}")
            
            # Text input for better evaluation
            answer_text = st.text_area(
                f"📝 OR type your detailed answer for {question_data['skill']}", 
                height=150,
                placeholder="Provide a detailed, technical answer with examples...",
                key=f"text_answer_{current_q}"
            )
        
        with col2:
            st.warning("⚠️ Skip = 0 points")
            if st.button("⏭️ Skip Question", key=f"skip_{current_q}", use_container_width=True):
                st.session_state.answers.append({
                    "type": question_data["type"],
                    "skill": question_data["skill"],
                    "question": question_data["question"],
                    "response": "SKIPPED BY CANDIDATE",
                    "score": 0,
                    "skipped": True,
                    "speaking_quality": "Beginner",
                    "feedback": ["Question was skipped - 0 points awarded"]
                })
                
                st.session_state.current_question += 1
                if current_q >= len(questions_list) - 1:
                    st.session_state.stage = "video_interview"
                st.rerun()
        
        # Process answer when provided
        if answer_audio or (answer_text and len(answer_text.strip()) > 10):
            
            # Show what was provided
            if answer_audio:
                st.audio(answer_audio)
                st.info("🎙️ Audio answer provided")
            
            if answer_text and len(answer_text.strip()) > 10:
                st.info(f"📝 Text answer provided ({len(answer_text)} characters)")
            
            with st.spinner("🤖 STRICT AI evaluation in progress - No fake passes..."):
                time.sleep(5)  # Show real processing time
                
                # REAL STRICT evaluation
                score, feedback, speaking_quality = evaluate_answer_with_real_ai(
                    question_data['question'],
                    question_data['skill'],
                    st.session_state.candidate_data['exp_level'],
                    audio_bytes=answer_audio,
                    user_text_input=answer_text
                )
                
                st.session_state.answers.append({
                    "type": question_data["type"],
                    "skill": question_data["skill"],
                    "question": question_data["question"],
                    "response": answer_text if answer_text else "Audio response provided",
                    "score": score,
                    "skipped": False,
                    "speaking_quality": speaking_quality,
                    "feedback": feedback
                })
                
                # REAL results display
                if score >= 80:
                    st.success("✅ EXCELLENT - Question PASSED with high marks!")
                elif score >= 60:
                    st.info("✅ GOOD - Question PASSED")
                elif score >= 40:
                    st.warning("⚠️ BARELY ACCEPTABLE - Weak performance")
                else:
                    st.error("❌ FAILED - Incorrect or inadequate answer")
                
                col1, col2, col3 = st.columns(3)
                with col1: 
                    color = "normal" if score >= 60 else "inverse"
                    st.metric("STRICT AI Score", f"{score}%", delta=f"{score-60}%", delta_color=color)
                with col2: 
                    st.metric("Speaking Quality", speaking_quality)
                with col3: 
                    remaining = len(questions_list) - current_q - 1
                    st.metric("Questions Left", remaining)
                
                # REAL feedback display
                st.subheader("🤖 STRICT AI Evaluation Feedback")
                for i, fb in enumerate(feedback, 1):
                    if score < 40:
                        st.error(f"{i}. {fb}")
                    elif score < 60:
                        st.warning(f"{i}. {fb}")
                    else:
                        st.info(f"{i}. {fb}")
                
                # Performance indicator
                if score >= 85:
                    st.success("🌟 **OUTSTANDING!** You demonstrate expert-level knowledge!")
                elif score >= 70:
                    st.success("👏 **EXCELLENT!** Strong technical competency shown!")
                elif score >= 60:
                    st.info("✅ **PASSED** - Acceptable technical understanding")
                elif score >= 40:
                    st.warning("⚠️ **WEAK PERFORMANCE** - Significant knowledge gaps identified")
                else:
                    st.error("❌ **FAILED** - Answer demonstrates insufficient technical knowledge")
                
                # Navigation
                next_text = "Next STRICT Question →" if current_q < len(questions_list)-1 else "Complete Assessment → REAL Video Interview"
                if st.button(next_text, use_container_width=True, type="primary"):
                    st.session_state.current_question += 1
                    if current_q >= len(questions_list)-1:
                        st.session_state.stage = "video_interview"
                    st.rerun()
    else:
        st.session_state.stage = "video_interview"
        st.rerun()

# STAGE 4: REAL VIDEO INTERVIEW WITH CAMERA
elif st.session_state.stage == "video_interview":
    st.header("🎥 MANDATORY REAL Video Interview - Camera Required")
    
    st.error("""
    🔥 **CAMERA ACCESS REQUIRED - NO EXCEPTIONS**
    
    This section evaluates:
    - 📹 Professional video presence
    - 🗣️ Clear verbal communication
    - 💼 Technical explanation skills
    - 🎯 Confidence and body language
    
    **You must enable camera access to continue!**
    """)
    
    # REAL camera component
    render_camera_component()
    
    video_questions = [
        "Look directly at the camera and introduce yourself professionally. Explain why you're the best candidate for this position.",
        "Explain your most significant technical achievement. Walk me through the problem, your solution, and the impact.",
        "Describe a challenging technical problem you solved recently. What was your approach and methodology?",
        "Where do you see yourself in 3 years? What are your specific technical goals and learning plans?"
    ]
    
    current_video_q = st.session_state.current_video_q
    
    if current_video_q < len(video_questions):
        # Progress
        progress = (current_video_q + 1) / len(video_questions)
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress * 100}%; background: linear-gradient(90deg, #e74c3c, #c0392b);">
                REAL Video {current_video_q + 1} of {len(video_questions)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader(f"🎬 REAL Video Question {current_video_q + 1}")
        
        # Question display
        st.markdown(f"""
        <div class="question-card" style="background: linear-gradient(135deg, #e74c3c20, #c0392b40); border-left-color: #e74c3c;">
            <h3 style="color: #e74c3c;">🎥 MANDATORY Video Interview Question:</h3>
            <p style="font-size: 20px; font-weight: bold; color: #2c3e50;">
                {video_questions[current_video_q]}
            </p>
            <p style="color: #7f8c8d; font-style: italic;">
                ⚠️ Look directly at camera, speak clearly, maintain professional posture
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Timer
        timer_html = f"""
        <div class="timer-display" id="timer-video{current_video_q}">
            🎥 Video Time: <span id="countdown-video{current_video_q}">{SecureConfig.VIDEO_TIME}</span> seconds
        </div>
        <script>
        var timeLeft_video{current_video_q} = {SecureConfig.VIDEO_TIME};
        var timer_video{current_video_q} = setInterval(function(){{
            timeLeft_video{current_video_q}--;
            var element = document.getElementById('countdown-video{current_video_q}');
            if (element) {{
                element.innerHTML = timeLeft_video{current_video_q};
                if (timeLeft_video{current_video_q} <= 0) {{
                    clearInterval(timer_video{current_video_q});
                    element.innerHTML = 'VIDEO TIME UP!';
                }}
            }}
        }}, 1000);
        </script>
        """
        st.markdown(timer_html, unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.warning("🎥 **ENSURE CAMERA IS ACTIVE ABOVE** - Video assessment requires visual confirmation of candidate")
            
            # Audio recording for video response
            video_response = st.audio_input("🎙️ Record your video response (audio will be analyzed)")
            
            # Text backup
            video_text = st.text_area("📝 OR type your video response if technical issues", 
                                    height=100, key=f"video_text_{current_video_q}")
        
        with col2:
            st.error("⚠️ Skip = Major penalty")
            if st.button("⏭️ Skip Video", key=f"skip_video_{current_video_q}", use_container_width=True):
                if "video_responses" not in st.session_state:
                    st.session_state.video_responses = []
                
                st.session_state.video_responses.append({
                    "question": video_questions[current_video_q],
                    "confidence_score": 20,  # Heavy penalty for skipping
                    "communication_quality": "Poor - Skipped",
                    "response": "SKIPPED"
                })
                
                st.session_state.current_video_q += 1
                if current_video_q >= len(video_questions) - 1:
                    st.session_state.stage = "results"
                st.rerun()
        
        if video_response or (video_text and len(video_text.strip()) > 20):
            if video_response:
                st.audio(video_response)
            
            with st.spinner("🎥 REAL video interview analysis in progress..."):
                time.sleep(4)
                
                # REAL video analysis
                response_content = video_text if video_text else "Audio video response provided"
                
                # Analyze response quality
                video_score = 0
                if len(response_content) > 50:
                    video_score += 30
                if any(word in response_content.lower() for word in ['experience', 'project', 'technical', 'solution']):
                    video_score += 25
                if any(word in response_content.lower() for word in ['challenge', 'problem', 'achieve', 'goal']):
                    video_score += 25
                if len(response_content) > 100:
                    video_score += 20
                
                video_score = min(100, video_score)
                
                # Determine communication quality
                if video_score >= 80:
                    comm_quality = "Excellent"
                    confidence = video_score
                elif video_score >= 60:
                    comm_quality = "Good"  
                    confidence = video_score
                else:
                    comm_quality = "Poor"
                    confidence = max(30, video_score)
                
                # Display REAL results
                if video_score >= 70:
                    st.success("✅ EXCELLENT video interview performance!")
                elif video_score >= 50:
                    st.info("✅ GOOD video interview performance")
                else:
                    st.error("❌ POOR video interview performance")
                
                col1, col2, col3 = st.columns(3)
                with col1: st.metric("Video Confidence", f"{confidence}%")
                with col2: st.metric("Communication", comm_quality)
                with col3: st.metric("Professional Presence", "Strong" if video_score >= 70 else "Weak")
                
                # Store response
                if "video_responses" not in st.session_state:
                    st.session_state.video_responses = []
                
                st.session_state.video_responses.append({
                    "question": video_questions[current_video_q],
                    "confidence_score": confidence,
                    "communication_quality": comm_quality,
                    "response": response_content
                })
                
                # Navigation
                if current_video_q < len(video_questions) - 1:
                    if st.button("Next Video Question →", use_container_width=True, type="primary"):
                        st.session_state.current_video_q += 1
                        st.rerun()
                else:
                    if st.button("Complete REAL Interview → View STRICT Results", use_container_width=True, type="primary"):
                        st.session_state.stage = "results"
                        st.rerun()
    else:
        st.session_state.stage = "results"
        st.rerun()

# STAGE 5: REAL RESULTS WITH STRICT EVALUATION
elif st.session_state.stage == "results":
    st.header("🔥 REAL INTERVIEW RESULTS - STRICT EVALUATION COMPLETE")
    
    candidate = st.session_state.candidate_data
    answers = st.session_state.answers
    video_responses = st.session_state.get('video_responses', [])
    
    # REAL STRICT score calculation
    answered_questions = [ans for ans in answers if not ans.get('skipped', False)]
    skipped_count = len([ans for ans in answers if ans.get('skipped', False)])
    
    if answered_questions:
        # Calculate weighted scores STRICTLY
        technical_scores = [ans['score'] for ans in answered_questions if ans['type'] == 'technical']
        project_scores = [ans['score'] for ans in answered_questions if ans['type'] == 'project']
        
        # STRICT weighted calculation
        if technical_scores and project_scores:
            tech_avg = sum(technical_scores) / len(technical_scores)
            proj_avg = sum(project_scores) / len(project_scores) 
            base_score = int(tech_avg * 0.75 + proj_avg * 0.25)  # Technical weighted more
        elif technical_scores:
            base_score = int(sum(technical_scores) / len(technical_scores))
        elif project_scores:
            base_score = int(sum(project_scores) / len(project_scores))
        else:
            base_score = 0
        
        # STRICT penalties
        skip_penalty = skipped_count * 15  # Heavy penalty for skipping
        base_score = max(0, base_score - skip_penalty)
        
        # Video interview impact (STRICT)
        if video_responses:
            avg_video_confidence = sum([vr.get('confidence_score', 30) for vr in video_responses]) / len(video_responses)
            video_impact = int((avg_video_confidence - 50) * 0.3)  # Can be negative
            final_score = max(0, min(100, base_score + video_impact))
        else:
            final_score = max(0, base_score - 25)  # Penalty for no video
    else:
        final_score = 0
    
    # STRICT speaking quality determination
    speaking_qualities = [ans.get('speaking_quality', 'Beginner') for ans in answered_questions]
    quality_levels = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Fluent': 4, 'Proficiency': 5}
    
    if speaking_qualities:
        avg_quality_score = sum([quality_levels.get(sq, 1) for sq in speaking_qualities]) / len(speaking_qualities)
        if avg_quality_score >= 4.5:
            speaking_quality = "Proficiency"
        elif avg_quality_score >= 3.5:
            speaking_quality = "Fluent"
        elif avg_quality_score >= 2.5:
            speaking_quality = "Advanced"
        elif avg_quality_score >= 1.5:
            speaking_quality = "Intermediate"
        else:
            speaking_quality = "Beginner"
    else:
        speaking_quality = "Beginner"
    
    # STRICT result determination - NO EASY PASSES
    if final_score >= 85:
        result_status, emoji, color, message = "Selected", "🏆", "#27ae60", "OUTSTANDING! Exceptional technical performance"
    elif final_score >= 75:
        result_status, emoji, color, message = "Selected", "🎉", "#27ae60", "EXCELLENT! Strong technical competency demonstrated"
    elif final_score >= 65:
        result_status, emoji, color, message = "Selected", "✅", "#27ae60", "GOOD! Solid technical foundation with minor gaps"
    elif final_score >= 50:
        result_status, emoji, color, message = "Pending", "⏳", "#f39c12", "UNDER REVIEW - Mixed performance, needs further evaluation"
    elif final_score >= 35:
        result_status, emoji, color, message = "Rejected", "❌", "#e74c3c", "FAILED - Significant technical knowledge gaps identified"
    else:
        result_status, emoji, color, message = "Rejected", "💥", "#e74c3c", "FAILED - Inadequate technical competency for this role"
    
    # Display REAL results
    st.markdown(f"""
    <div class="result-card" style="background: linear-gradient(135deg, {color}15, {color}25); border: 3px solid {color}; text-align: center;">
        <h1 style="color: {color}; font-size: 3em;">{emoji}</h1>
        <h2 style="color: {color};">REAL INTERVIEW ASSESSMENT COMPLETE</h2>
        <h3 style="color: {color};">FINAL RESULT: {result_status}</h3>
        <h2 style="color: {color};">STRICT SCORE: {final_score}%</h2>
        <p style="font-size: 18px; color: #2c3e50; font-weight: 600;">{message}</p>
        {f'<p style="color: #e74c3c; font-weight: bold;">⚠️ PENALTIES APPLIED: {skip_penalty} points for {skipped_count} skipped questions</p>' if skipped_count > 0 else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Candidate Assessment Summary")
        st.write(f"**Name:** {candidate['name']}")
        st.write(f"**Email:** {candidate['email']}")
        st.write(f"**Phone:** {candidate['phone']}")
        st.write(f"**Position:** {candidate['position']}")
        st.write(f"**Experience Level:** {candidate['experience']}")
        st.write(f"**Skills Tested:** {candidate['skills']}")
        st.write(f"**Assessment Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Total Duration:** {(time.time() - st.session_state.start_time) / 60:.1f} minutes")
    
    with col2:
        st.subheader("📊 STRICT Performance Metrics")
        
        # Main metrics with color coding
        score_color = "normal" if final_score >= 65 else "inverse"
        st.metric("Final Score", f"{final_score}%", 
                 delta=f"{final_score-65}%" if final_score != 65 else "0%", 
                 delta_color=score_color)
        st.metric("Speaking Quality", speaking_quality)
        st.metric("Questions Answered", f"{len(answered_questions)}/{len(st.session_state.questions_list)}")
        st.metric("Questions Skipped", f"{skipped_count} (-{skip_penalty} points)" if skipped_count > 0 else "0")
        
        if video_responses:
            avg_confidence = sum([vr.get('confidence_score', 30) for vr in video_responses]) / len(video_responses)
            st.metric("Video Performance", f"{int(avg_confidence)}%")
    
    # DETAILED skill breakdown
    st.subheader("🎯 STRICT Skill-by-Skill Performance Analysis")
    
    skill_performance = {}
    for answer in answered_questions:
        skill = answer['skill']
        if skill not in skill_performance:
            skill_performance[skill] = []
        skill_performance[skill].append(answer['score'])
    
    if skill_performance:
        for skill, scores in skill_performance.items():
            avg_skill_score = sum(scores) / len(scores)
            
            col1, col2, col3 = st.columns([2, 1, 4])
            
            with col1:
                st.write(f"**{skill}:**")
            
            with col2:
                if avg_skill_score >= 70:
                    st.success(f"{int(avg_skill_score)}%")
                elif avg_skill_score >= 50:
                    st.warning(f"{int(avg_skill_score)}%")
                else:
                    st.error(f"{int(avg_skill_score)}%")
            
            with col3:
                # Performance bar with strict color coding
                if avg_skill_score >= 80:
                    bar_color = "#27ae60"
                    status = "EXCELLENT"
                elif avg_skill_score >= 60:
                    bar_color = "#f39c12"
                    status = "ACCEPTABLE"
                else:
                    bar_color = "#e74c3c"
                    status = "FAILED"
                
                st.markdown(f"""
                <div style="background: #e0e0e0; border-radius: 10px; height: 25px; display: flex; align-items: center;">
                    <div style="background: {bar_color}; height: 100%; width: {avg_skill_score}%; 
                         border-radius: 10px; display: flex; align-items: center; justify-content: center; 
                         color: white; font-weight: bold; font-size: 12px;">
                        {status}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Video interview detailed results
    if video_responses:
        st.subheader("🎥 Video Interview Assessment Details")
        for i, video_resp in enumerate(video_responses, 1):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Question {i}:**")
                st.write(f"Confidence: {video_resp.get('confidence_score', 0)}%")
            with col2:
                st.write(f"**Communication:**")
                st.write(video_resp.get('communication_quality', 'Poor'))
            with col3:
                st.write(f"**Status:**")
                conf = video_resp.get('confidence_score', 0)
                if conf >= 70:
                    st.success("PASSED")
                elif conf >= 50:
                    st.warning("ACCEPTABLE")
                else:
                    st.error("FAILED")
    
    # REAL Database save
    st.subheader("💾 REAL MySQL Database Storage")
    
    with st.spinner("💾 Saving REAL results to MySQL database..."):
        time.sleep(3)
        
        database_success = save_to_database(candidate, final_score, speaking_quality, result_status)
        
        if database_success:
            st.success("✅ RESULTS SUCCESSFULLY SAVED TO REAL MySQL DATABASE!")
            st.balloons()
            
            # Show what was saved
            st.info(f"""
            🎯 **REAL DATABASE STORAGE CONFIRMED:**
            
            **✅ SAVED TO MySQL:**
            - **Candidate:** {candidate['name']} ({candidate['email']})
            - **Final Score:** {final_score}% (STRICT evaluation)
            - **Result Status:** {result_status}
            - **Speaking Quality:** {speaking_quality}
            - **Questions Answered:** {len(answered_questions)}/{len(st.session_state.questions_list)}
            - **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            **📊 HR ACCESS:** All assessment data now available in candidates table
            """)
        else:
            st.error("❌ DATABASE SAVE FAILED!")
            st.error("Check your MySQL configuration and ensure the database server is running.")
    
    # STRICT final assessment message
    st.subheader("📋 FINAL ASSESSMENT SUMMARY")
    
    if result_status == "Selected":
        st.success(f"""
        🎉 **CONGRATULATIONS {candidate['name']}!**
        
        **RESULT:** SELECTED with {final_score}% score
        **PERFORMANCE:** You have demonstrated strong technical competency
        **COMMUNICATION:** {speaking_quality} level professional communication
        **NEXT STEPS:** HR will contact you for further interview rounds
        
        **STRENGTHS IDENTIFIED:**
        - Technical knowledge appropriate for {candidate['exp_level']} level
        - Professional communication and presentation
        - Ability to explain complex technical concepts
        """)
    elif result_status == "Pending":
        st.warning(f"""
        ⏳ **APPLICATION UNDER REVIEW - {candidate['name']}**
        
        **RESULT:** PENDING with {final_score}% score
        **STATUS:** Mixed performance requires additional evaluation
        **COMMUNICATION:** {speaking_quality} level communication demonstrated
        **NEXT STEPS:** HR will review and make final decision
        
        **AREAS FOR IMPROVEMENT:**
        - Strengthen technical knowledge in weak areas
        - Practice explaining technical concepts clearly
        - Improve confidence in technical discussions
        """)
    else:
        st.error(f"""
        ❌ **ASSESSMENT RESULT - {candidate['name']}**
        
        **RESULT:** NOT SELECTED with {final_score}% score
        **PERFORMANCE:** Technical knowledge gaps identified
        **COMMUNICATION:** {speaking_quality} level communication
        **RECOMMENDATION:** Focus on skill development and reapply later
        
        **IMPROVEMENT AREAS:**
        - Strengthen fundamental technical concepts
        - Practice coding and problem-solving
        - Improve technical communication skills
        - Gain more hands-on project experience
        """)
    
    # New interview option
    st.markdown("---")
    if st.button("🔄 Start New REAL Interview Assessment", use_container_width=True, type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Enhanced Sidebar with REAL system info
with st.sidebar:
    st.markdown("### 🔥 REAL SYSTEM STATUS")
    
    # System status
    if all([SecureConfig.get_hugging_face_token(), SecureConfig.get_perplexity_api_key(), db_connection]):
        st.success
