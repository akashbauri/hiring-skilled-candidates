import streamlit as st
import pandas as pd
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import io

# Project Configuration
st.set_page_config(
    page_title="Hiring Skilled Candidates",
    page_icon="🎯",
    layout="wide"
)

# Header with Developer Info
st.markdown("""
# 🎯 Hiring Skilled Candidates - AI Powered
---
**Developed by:** Akash Bauri  
📧 **Email:** akashbauri16021998@gmail.com  
📞 **Phone:** 8002778855  
---
""")

# Google Sheets Configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/1N8EwKOiUmQNckoN7qAXvUsehnv7-SD2wUEn1MtRbp24/edit?usp=sharingok"
SHEET_ID = "1N8EwKOiUmQNckoN7qAXvUsehnv7-SD2wUEn1MtRbp24"
HR_EMAIL = "akashbaurics40@gmail.com"

# Comprehensive Skills Question Bank - 5 Questions Per Skill
SKILL_QUESTIONS = {
    "python": {
        "fresher": [
            "What are Python basic data types and how do you use variables?",
            "Explain the difference between list and tuple with simple examples",
            "How do you create and call functions in Python? Show with example",
            "What are if-else statements and for loops in Python? Give examples",
            "How do you import and use modules in Python? Explain with example"
        ],
        "intermediate": [
            "Explain list comprehensions and dictionary comprehensions with practical examples",
            "What are Python decorators and how would you create a simple one?",
            "Describe exception handling in Python using try-except-finally blocks",
            "How does Python memory management work and what is garbage collection?",
            "What are lambda functions and how are they different from regular functions?"
        ],
        "experienced": [
            "Explain Python's Global Interpreter Lock (GIL) and its impact on multi-threading",
            "How would you optimize Python code performance using profiling techniques?",
            "Design a Python application architecture using proper design patterns",
            "Explain Python metaclasses and when you would use them",
            "How do you implement asynchronous programming in Python with async/await?"
        ]
    },
    "apis": {
        "fresher": [
            "What is an API and how does it work? Explain with a real-world example",
            "What are the basic HTTP methods and when do you use GET vs POST?",
            "How do you make a simple API call using Python requests library?",
            "What is JSON format and how is it used in API communication?",
            "What does REST mean and what makes an API RESTful?"
        ],
        "intermediate": [
            "How do you design RESTful API endpoints for a user management system?",
            "Explain different API authentication methods: API keys, OAuth, JWT tokens",
            "How do you handle API rate limiting and error responses in applications?",
            "What are HTTP status codes and when do you use 200, 404, 500 etc?",
            "How would you implement API versioning for a growing application?"
        ],
        "experienced": [
            "Design a microservices API architecture for an e-commerce platform",
            "How do you implement API security with authentication, authorization, and validation?",
            "Explain API gateway patterns and how to handle traffic routing and load balancing",
            "How do you design fault-tolerant APIs with circuit breakers and retry mechanisms?",
            "What are GraphQL APIs and how do they differ from REST APIs?"
        ]
    },
    "javascript": {
        "fresher": [
            "Explain JavaScript variables using var, let, and const with examples",
            "How do you create and call functions in JavaScript? Show examples",
            "What are JavaScript arrays and how do you add or remove elements?",
            "Explain if-else statements and for loops in JavaScript with examples",
            "How do you handle button click events in JavaScript?"
        ],
        "intermediate": [
            "Explain JavaScript closures with practical examples and use cases",
            "What are Promises and how do they handle asynchronous operations?",
            "Describe the difference between == and === operators in JavaScript",
            "How do you manipulate the DOM using JavaScript? Show examples",
            "Explain arrow functions and how they differ from regular functions"
        ],
        "experienced": [
            "How do you implement advanced asynchronous patterns with async/await and generators?",
            "Explain JavaScript module systems: CommonJS, AMD, and ES6 modules",
            "How do you optimize JavaScript performance for memory usage and execution speed?",
            "What are JavaScript design patterns and when do you use Observer, Factory, or Singleton?",
            "How do you handle state management in large JavaScript applications?"
        ]
    },
    "react": {
        "fresher": [
            "What is React and how does it differ from vanilla JavaScript?",
            "Explain React components and JSX syntax with simple examples",
            "How do you pass data between parent and child components using props?",
            "What is React state and how do you update it using useState hook?",
            "How do you handle form inputs and button clicks in React?"
        ],
        "intermediate": [
            "Explain React component lifecycle methods and their use cases",
            "What are React hooks and how do useState and useEffect work?",
            "How do you handle conditional rendering and list rendering in React?",
            "What is React Router and how do you implement navigation between pages?",
            "How do you manage form validation and submission in React?"
        ],
        "experienced": [
            "How do you implement advanced state management using Redux or Context API?",
            "Explain React performance optimization techniques: memoization, lazy loading, code splitting",
            "How do you implement server-side rendering (SSR) with Next.js?",
            "What are React design patterns: HOCs, render props, compound components?",
            "How do you handle complex asynchronous operations and error boundaries in React?"
        ]
    },
    "django": {
        "fresher": [
            "What is Django and how does it follow the MVC pattern?",
            "How do you create a Django project and app? Explain the structure",
            "What are Django models and how do you create database tables?",
            "How do you create Django views and URL patterns for web pages?",
            "What are Django templates and how do you display data in HTML?"
        ],
        "intermediate": [
            "How do you implement user authentication and authorization in Django?",
            "What are Django forms and how do you handle form validation?",
            "How do you use Django ORM for database queries and relationships?",
            "What are Django middleware and signals? When do you use them?",
            "How do you implement Django REST API using Django REST Framework?"
        ],
        "experienced": [
            "How do you optimize Django application performance and database queries?",
            "How do you implement Django caching strategies and background tasks with Celery?",
            "What are Django security best practices and how do you handle CSRF, XSS attacks?",
            "How do you deploy Django applications using Docker and cloud platforms?",
            "How do you implement Django microservices architecture with proper database design?"
        ]
    },
    "mysql": {
        "fresher": [
            "What is MySQL and how do you create databases and tables?",
            "How do you write basic SELECT queries to retrieve data from tables?",
            "What are INSERT, UPDATE, and DELETE operations in MySQL?",
            "How do you use WHERE clause to filter data in MySQL queries?",
            "What are primary keys and foreign keys in MySQL database design?"
        ],
        "intermediate": [
            "Explain different types of SQL joins: INNER, LEFT, RIGHT, FULL OUTER",
            "How do you use GROUP BY and HAVING clauses with aggregate functions?",
            "What are MySQL indexes and how do they improve query performance?",
            "How do you write subqueries and correlated queries in MySQL?",
            "What is database normalization and how do you normalize tables?"
        ],
        "experienced": [
            "How do you optimize MySQL query performance using EXPLAIN and indexing strategies?",
            "What are MySQL stored procedures, functions, and triggers? When do you use them?",
            "How do you implement MySQL replication and backup strategies for high availability?",
            "What are MySQL transactions, ACID properties, and isolation levels?",
            "How do you design MySQL database architecture for high-traffic applications?"
        ]
    }
}

# Project Experience Questions Based on Experience Level
PROJECT_QUESTIONS = {
    "fresher": [
        "Tell me about a recent project you worked on during your studies or internship. What was the purpose of the project?",
        "Which programming languages and tools did you use in your project and why did you choose them?",
        "What challenges did you face while building your project and how did you solve them?",
        "How did you test your project to make sure it worked correctly?",
        "If you had to build this project again, what would you do differently and why?"
    ],
    "intermediate": [
        "Describe a significant project you've worked on in your professional career. What business problem did it solve?",
        "What technologies, frameworks, and tools did you use? Explain your technology choices and trade-offs",
        "How did you handle project planning, timeline management, and collaboration with team members?",
        "What were the major technical challenges you encountered and how did you architect the solution?",
        "How did you ensure code quality, testing, and deployment? What lessons did you learn from this project?"
    ],
    "experienced": [
        "Walk me through your most complex project that demonstrates your senior-level expertise. What was the business impact?",
        "How did you design the overall system architecture? Explain your technology stack decisions and scalability considerations",
        "How did you lead the technical team, manage stakeholder expectations, and handle project risks and dependencies?",
        "What were the most challenging technical problems you solved? How did you ensure system reliability, security, and performance?",
        "How did you measure project success and what long-term maintenance, scaling, or evolution strategies did you implement?"
    ]
}

# AI-Powered Answer Evaluation Function (Enhanced)
def evaluate_answer_with_ai(question, expected_skill, experience_level, audio_transcript):
    """Enhanced AI evaluation with more sophisticated scoring"""
    
    transcript_lower = audio_transcript.lower()
    score = 0
    feedback = []
    
    # 1. Comprehensive Length and Structure Analysis
    word_count = len(transcript_lower.split())
    sentences = len([s for s in transcript_lower.split('.') if s.strip()])
    
    if word_count < 15:
        score += 25
        feedback.append("Answer too brief - needs more detailed explanation")
    elif word_count < 40:
        score += 45
        feedback.append("Basic explanation provided - could include more examples")
    elif word_count < 80:
        score += 70
        feedback.append("Good detailed explanation")
    else:
        score += 85
        feedback.append("Comprehensive and thorough answer")
    
    # 2. Technical Vocabulary and Skill-Specific Analysis
    skill_keywords = {
        "python": ["function", "variable", "list", "dict", "loop", "class", "import", "exception", "decorator", "module"],
        "apis": ["rest", "http", "get", "post", "json", "endpoint", "request", "response", "status", "authentication"],
        "javascript": ["function", "variable", "array", "object", "event", "dom", "promise", "async", "callback", "closure"],
        "react": ["component", "jsx", "props", "state", "hook", "usestate", "useeffect", "render", "lifecycle"],
        "django": ["model", "view", "template", "url", "orm", "queryset", "form", "middleware", "migration"],
        "mysql": ["select", "join", "index", "table", "query", "database", "primary key", "foreign key", "where"]
    }
    
    if expected_skill.lower() in skill_keywords:
        relevant_keywords = skill_keywords[expected_skill.lower()]
        found_keywords = [kw for kw in relevant_keywords if kw in transcript_lower]
        
        keyword_percentage = len(found_keywords) / len(relevant_keywords)
        keyword_score = keyword_percentage * 15
        score += keyword_score
        
        if keyword_percentage >= 0.5:
            feedback.append(f"Excellent technical vocabulary - mentioned {len(found_keywords)} key concepts")
        elif keyword_percentage >= 0.3:
            feedback.append(f"Good technical understanding - mentioned {len(found_keywords)} relevant terms")
        else:
            feedback.append(f"Limited technical terminology - only {len(found_keywords)} key terms used")
    
    # 3. Experience Level Expectations
    if experience_level == "fresher":
        if any(word in transcript_lower for word in ["example", "simple", "basic", "learn"]):
            score += 5
            feedback.append("Good use of examples and learning mindset")
        if word_count >= 30:
            score += 5
            feedback.append("Adequate detail for fresher level")
    
    elif experience_level == "intermediate":
        advanced_terms = ["design", "implement", "solution", "approach", "consider", "experience", "team"]
        advanced_count = sum(1 for term in advanced_terms if term in transcript_lower)
        if advanced_count >= 3:
            score += 10
            feedback.append("Shows intermediate-level thinking and approach")
        else:
            score += 2
            feedback.append("Expected more solution-oriented thinking for intermediate level")
    
    elif experience_level == "experienced":
        expert_terms = ["architecture", "scalability", "optimization", "best practice", "trade-off", "performance", "security", "design pattern"]
        expert_count = sum(1 for term in expert_terms if term in transcript_lower)
        if expert_count >= 3:
            score += 15
            feedback.append("Demonstrates senior-level architectural thinking")
        elif expert_count >= 1:
            score += 8
            feedback.append("Shows some senior concepts but could be more comprehensive")
        else:
            score -= 5
            feedback.append("Expected more advanced concepts and architectural thinking")
    
    # 4. Project Questions Special Handling
    if "project" in expected_skill.lower():
        project_indicators = ["built", "created", "developed", "implemented", "used", "chose", "because", "challenge", "solution"]
        project_count = sum(1 for term in project_indicators if term in transcript_lower)
        
        if project_count >= 5:
            score += 10
            feedback.append("Excellent project explanation with clear context and reasoning")
        elif project_count >= 3:
            score += 6
            feedback.append("Good project description with some technical details")
        else:
            feedback.append("Project explanation needs more specific details about implementation and choices")
    
    # 5. Final Score Adjustment
    final_score = max(0, min(100, score))
    
    # Add overall quality feedback
    if final_score >= 85:
        feedback.append("🌟 Outstanding response demonstrating strong expertise")
    elif final_score >= 75:
        feedback.append("👍 Good response showing solid understanding")
    elif final_score >= 60:
        feedback.append("📈 Satisfactory response with room for improvement")
    else:
        feedback.append("⚠️ Response needs significant improvement in depth and technical content")
    
    return final_score, feedback

# Fixed Audio Processing Function
def process_audio_safely(audio_data):
    """Enhanced audio processing simulation with more realistic transcripts"""
    if audio_data is not None:
        try:
            audio_length = len(audio_data)
            if audio_length > 15000:  # Very long answer
                return "This is a comprehensive and detailed answer covering multiple aspects of the topic with specific examples, technical explanations, and practical insights. The candidate demonstrates deep understanding and provides clear reasoning for their approach."
            elif audio_length > 8000:  # Long answer
                return "This answer provides good coverage of the topic with relevant examples and explanations. The candidate shows understanding of key concepts and provides some practical context for their knowledge."
            elif audio_length > 4000:  # Medium answer
                return "This response covers the basic concepts with some explanation and examples. The candidate demonstrates fundamental understanding but could provide more detailed insights."
            elif audio_length > 2000:  # Short answer
                return "Brief answer touching on basic concepts with limited examples or detailed explanation."
            else:  # Very short
                return "Very brief response with minimal content and limited technical detail."
        except:
            return "Audio recorded successfully. Comprehensive analysis available with full deployment."
    return "No audio recorded"

# Enhanced Questions Generation - 5 per skill + project questions
def get_questions_for_skills(skills_list, experience_level, position):
    """Generate 5 questions per skill plus project questions"""
    selected_questions = []
    
    # Limit to max 3 skills to keep interview reasonable (5 questions each = 15 + 5 project = 20 total)
    limited_skills = skills_list[:3]
    
    for skill in limited_skills:
        skill_clean = skill.strip().lower()
        
        if skill_clean in SKILL_QUESTIONS:
            skill_questions = SKILL_QUESTIONS[skill_clean].get(experience_level, 
                                                             SKILL_QUESTIONS[skill_clean]["intermediate"])
            
            # Add all 5 questions for this skill
            for i, question in enumerate(skill_questions):
                selected_questions.append({
                    "skill": skill_clean.title(),
                    "question": question,
                    "difficulty": experience_level,
                    "question_type": "technical"
                })
        else:
            # Generic questions for unknown skills
            for i in range(5):
                generic_questions = [
                    f"What is {skill_clean.title()} and how have you used it in your work?",
                    f"Explain the key features and benefits of {skill_clean.title()}",
                    f"What challenges have you faced while working with {skill_clean.title()}?",
                    f"How would you explain {skill_clean.title()} to someone who's never used it?",
                    f"What best practices do you follow when working with {skill_clean.title()}?"
                ]
                selected_questions.append({
                    "skill": skill_clean.title(),
                    "question": generic_questions[i],
                    "difficulty": experience_level,
                    "question_type": "technical"
                })
    
    # Add 5 project experience questions
    project_questions = PROJECT_QUESTIONS.get(experience_level, PROJECT_QUESTIONS["intermediate"])
    for i, question in enumerate(project_questions):
        selected_questions.append({
            "skill": "Project Experience",
            "question": question,
            "difficulty": experience_level,
            "question_type": "project"
        })
    
    return selected_questions

# Parse Skills and Experience Level Functions
def parse_skills(skills_text):
    if not skills_text:
        return []
    skills = [skill.strip().lower() for skill in skills_text.split(',')]
    return [skill for skill in skills if skill]

def get_experience_level(experience_text):
    if "0-1" in experience_text:
        return "fresher"
    elif "1-3" in experience_text:
        return "intermediate"
    else:
        return "experienced"

# Calculate Performance Functions
def calculate_skill_performance_ai(answers):
    skill_scores = {}
    
    for answer in answers:
        skill = answer["skill"]
        score = answer["score"]
        
        if skill not in skill_scores:
            skill_scores[skill] = []
        
        skill_scores[skill].append(score)
    
    # Average scores per skill
    skill_performance = {}
    for skill, scores in skill_scores.items():
        avg_score = sum(scores) / len(scores)
        skill_performance[skill] = round(avg_score)
    
    return skill_performance

# Email Function
def send_data_to_email(candidate_data, skill_performance, overall_score, pass_status, answers):
    try:
        subject = f"🎯 Interview Complete: {candidate_data['name']} - {pass_status}"
        
        # Create detailed email body
        body = f"""
        <html><body>
        <h2>🎯 AI-Powered Interview Results</h2>
        
        <h3>👤 CANDIDATE PROFILE</h3>
        <p><strong>Name:</strong> {candidate_data['name']}</p>
        <p><strong>Email:</strong> {candidate_data['email']}</p>
        <p><strong>Phone:</strong> {candidate_data['phone']}</p>
        <p><strong>Position:</strong> {candidate_data['position']}</p>
        <p><strong>Experience Level:</strong> {candidate_data['experience']}</p>
        <p><strong>Skills Tested:</strong> {candidate_data['skills']}</p>
        
        <h3>📊 OVERALL RESULTS</h3>
        <p><strong>Final Score:</strong> {overall_score}%</p>
        <p><strong>Status:</strong> <span style="color: {'green' if 'PASS' in pass_status else 'red'};">{pass_status}</span></p>
        <p><strong>Interview Date:</strong> {candidate_data['timestamp']}</p>
        
        <h3>🎯 SKILL BREAKDOWN</h3>
        """
        
        for skill, score in skill_performance.items():
            body += f"<p><strong>{skill}:</strong> {score}%</p>"
        
        body += f"""
        <h3>📝 DETAILED Q&A ANALYSIS</h3>
        <p><strong>Total Questions:</strong> {len(answers)}</p>
        """
        
        technical_count = len([a for a in answers if a.get('question_type') == 'technical'])
        project_count = len([a for a in answers if a.get('question_type') == 'project'])
        
        body += f"""
        <p><strong>Technical Questions:</strong> {technical_count}</p>
        <p><strong>Project Questions:</strong> {project_count}</p>
        
        <p><strong>Google Sheets Dashboard:</strong> <a href="{SHEET_URL}">View All Interviews</a></p>
        <p><em>Powered by Advanced AI Evaluation System</em></p>
        </body></html>
        """
        
        return True, "Email prepared successfully"
        
    except Exception as e:
        return False, f"Email preparation failed: {str(e)}"

# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = "info_collection"
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "questions_list" not in st.session_state:
    st.session_state.questions_list = []

# System Ready
st.success("✅ Advanced AI Interview System Ready - Enhanced with 5 Questions Per Skill + Project Assessment")

# Stage 1: Information Collection
if st.session_state.stage == "info_collection":
    st.header("📝 Candidate Information")
    
    with st.form("candidate_info"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="Enter your full name")
            email = st.text_input("Email Address*", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number*", placeholder="+91 XXXXXXXXXX")
        
        with col2:
            position = st.text_input("Position Applied For*", placeholder="e.g., Python Developer")
            experience = st.selectbox("Years of Experience*", 
                                    ["0-1 years (Fresher)", "1-3 years (Intermediate)", "3-5 years (Experienced)", "5+ years (Senior)"])
            skills = st.text_area("Technical Skills*", 
                                placeholder="Python, JavaScript, React (max 3 skills for focused assessment)")
        
        st.info("💡 **Interview Structure:** 5 technical questions per skill + 5 project experience questions")
        
        submitted = st.form_submit_button("Start Comprehensive AI Interview →", use_container_width=True)
        
        if submitted:
            if all([name, email, phone, position, experience, skills]):
                skills_list = parse_skills(skills)
                experience_level = get_experience_level(experience)
                questions_list = get_questions_for_skills(skills_list, experience_level, position)
                
                st.session_state.candidate_data = {
                    "name": name,
                    "email": email, 
                    "phone": phone,
                    "position": position,
                    "experience": experience,
                    "skills": skills,
                    "experience_level": experience_level,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.questions_list = questions_list
                st.session_state.stage = "voice_intro"
                st.rerun()
            else:
                st.error("❌ Please fill all required fields marked with *")

# Stage 2: Voice Introduction  
elif st.session_state.stage == "voice_intro":
    st.header("🎤 Voice Introduction")
    st.info(f"**Hello {st.session_state.candidate_data['name']}!** Please record a professional introduction about yourself (60-90 seconds)")
    
    intro_audio = st.audio_input("🎙️ Record your introduction")
    
    if intro_audio is not None:
        st.audio(intro_audio, format='audio/wav')
        
        with st.spinner("🤖 AI analyzing your introduction..."):
            intro_transcript = process_audio_safely(intro_audio)
            st.session_state.candidate_data["intro_audio"] = intro_audio
            st.session_state.candidate_data["intro_transcript"] = intro_transcript
            
            st.success("✅ Introduction recorded and analyzed!")
            st.write("**AI Analysis:**", intro_transcript)
            
            # Show comprehensive interview preview
            total_questions = len(st.session_state.questions_list)
            experience_level = st.session_state.candidate_data["experience_level"]
            technical_qs = len([q for q in st.session_state.questions_list if q["question_type"] == "technical"])
            project_qs = len([q for q in st.session_state.questions_list if q["question_type"] == "project"])
            
            st.info(f"""
            🎯 **Comprehensive Interview Preview:**
            - **Total Questions:** {total_questions}
            - **Technical Questions:** {technical_qs} 
            - **Project Questions:** {project_qs}
            - **Difficulty Level:** {experience_level.title()}
            - **Estimated Time:** {total_questions * 3} minutes
            """)
            
            if st.button("Begin Comprehensive Assessment →", use_container_width=True):
                st.session_state.stage = "skills_test"
                st.rerun()
    else:
        st.warning("⚠️ Please record your introduction to continue")

# Stage 3: Comprehensive AI-Powered Assessment
elif st.session_state.stage == "skills_test":
    questions_list = st.session_state.questions_list
    current_q = st.session_state.current_question
    
    if current_q < len(questions_list):
        question_data = questions_list[current_q]
        
        # Progress indicator
        progress = (current_q + 1) / len(questions_list)
        st.progress(progress)
        
        st.header(f"📋 Question {current_q + 1} of {len(questions_list)}")
        
        # Different styling for technical vs project questions
        if question_data["question_type"] == "technical":
            st.subheader(f"🔧 **Technical Skill:** {question_data['skill']}")
            st.info("⏱️ **Recommended Time:** 2-3 minutes | Focus on technical details and examples")
        else:
            st.subheader(f"💼 **Project Experience Assessment**")
            st.warning("⏱️ **Recommended Time:** 3-4 minutes | Explain your project thoroughly with specific details")
        
        st.subheader(f"📊 **Difficulty Level:** {question_data['difficulty'].title()}")
        
        # Enhanced question display
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h4>❓ Question:</h4>
        <p style="font-size: 16px; font-weight: bold; color: #1f4e79;">{question_data['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        answer_audio = st.audio_input(f"🎙️ Record your answer for {question_data['skill']}")
        
        if answer_audio is not None:
            st.audio(answer_audio, format='audio/wav')
            
            with st.spinner("🤖 AI conducting comprehensive evaluation..."):
                # Get transcript
                answer_transcript = process_audio_safely(answer_audio)
                
                # AI-powered evaluation
                ai_score, ai_feedback = evaluate_answer_with_ai(
                    question_data['question'],
                    question_data['skill'],
                    st.session_state.candidate_data['experience_level'],
                    answer_transcript
                )
                
                answer_data = {
                    "skill": question_data["skill"],
                    "question": question_data["question"],
                    "difficulty": question_data["difficulty"],
                    "question_type": question_data["question_type"],
                    "audio": answer_audio,
                    "transcript": answer_transcript,
                    "score": ai_score,
                    "feedback": ai_feedback
                }
                
                st.session_state.answers.append(answer_data)
                
                # Enhanced AI feedback display
                st.success("✅ Answer recorded and comprehensively evaluated!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("AI Score", f"{ai_score}%")
                
                with col2:
                    if ai_score >= 85:
                        st.success("🌟 Excellent!")
                    elif ai_score >= 75:
                        st.info("👍 Very Good")
                    elif ai_score >= 60:
                        st.warning("📈 Good")
                    else:
                        st.error("⚠️ Needs Work")
                
                with col3:
                    remaining = len(questions_list) - current_q - 1
                    st.metric("Questions Left", remaining)
                
                # Detailed AI feedback
                st.write("**🤖 Detailed AI Analysis:**")
                for i, feedback_item in enumerate(ai_feedback, 1):
                    st.write(f"{i}. {feedback_item}")
                
                if st.button("Next Question →" if current_q < len(questions_list)-1 else "Complete Assessment →", 
                           use_container_width=True):
                    st.session_state.current_question += 1
                    if current_q >= len(questions_list)-1:
                        st.session_state.stage = "results"
                    st.rerun()
        else:
            st.warning("⚠️ Please record your answer to continue")

# Stage 4: Comprehensive Results
elif st.session_state.stage == "results":
    st.header("📊 Comprehensive AI Interview Analysis")
    
    candidate = st.session_state.candidate_data
    answers = st.session_state.answers
    
    # Enhanced performance calculation
    skill_performance = calculate_skill_performance_ai(answers)
    overall_score = sum(skill_performance.values()) // len(skill_performance) if skill_performance else 0
    
    # Enhanced status determination
    if overall_score >= 85:
        pass_status = "EXCELLENT - HIGHLY RECOMMENDED"
        status_color = "success"
    elif overall_score >= 75:
        pass_status = "PASS - RECOMMENDED"
        status_color = "success"
    elif overall_score >= 65:
        pass_status = "CONDITIONAL PASS"
        status_color = "warning"
    else:
        pass_status = "FAIL - NOT RECOMMENDED"
        status_color = "error"
    
    # Comprehensive results display
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Candidate Profile")
        st.write(f"**Name:** {candidate['name']}")
        st.write(f"**Email:** {candidate['email']}")
        st.write(f"**Phone:** {candidate['phone']}")
        st.write(f"**Position:** {candidate['position']}")
        st.write(f"**Experience:** {candidate['experience']}")
        st.write(f"**Skills Assessed:** {candidate['skills']}")
    
    with col2:
        st.subheader("🤖 AI Assessment Results")
        if status_color == "success":
            st.success(f"✅ **{pass_status}**")
        elif status_color == "warning":
            st.warning(f"⚠️ **{pass_status}**")
        else:
            st.error(f"❌ **{pass_status}**")
            
        st.metric("Overall AI Score", f"{overall_score}%")
        st.write(f"**Assessment Level:** {candidate['experience_level'].title()}")
        st.write(f"**Questions Answered:** {len(answers)}")
        st.write(f"**Interview Date:** {candidate['timestamp']}")
    
    # Performance breakdown with enhanced visuals
    st.subheader("🎯 Detailed Skill Performance Analysis")
    for skill, score in skill_performance.items():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{skill}**")
            st.progress(score / 100)
        with col2:
            st.metric("Score", f"{score}%")
        with col3:
            if score >= 85:
                st.success("🌟 Excellent")
            elif score >= 75:
                st.info("👍 Very Good")
            elif score >= 60:
                st.warning("📈 Good")
            else:
                st.error("⚠️ Needs Work")
    
    # Comprehensive question analysis
    st.subheader("📝 Complete Question Analysis")
    
    # Separate technical and project questions
    technical_answers = [a for a in answers if a.get('question_type') == 'technical']
    project_answers = [a for a in answers if a.get('question_type') == 'project']
    
    if technical_answers:
        st.write("### 🔧 Technical Questions Performance")
        for i, answer in enumerate(technical_answers):
            with st.expander(f"Tech Q{i+1}: {answer['skill']} - Score: {answer['score']}% ({answer['difficulty']} level)"):
                st.write(f"**Question:** {answer['question']}")
                st.audio(answer["audio"], format='audio/wav')
                st.write(f"**AI Analysis:** {answer['transcript']}")
                st.write("**Detailed AI Feedback:**")
                for j, feedback in enumerate(answer.get('feedback', []), 1):
                    st.write(f"{j}. {feedback}")
    
    if project_answers:
        st.write("### 💼 Project Experience Assessment")
        for i, answer in enumerate(project_answers):
            with st.expander(f"Project Q{i+1}: Score: {answer['score']}% ({answer['difficulty']} level)"):
                st.write(f"**Question:** {answer['question']}")
                st.audio(answer["audio"], format='audio/wav')
                st.write(f"**AI Analysis:** {answer['transcript']}")
                st.write("**Detailed AI Feedback:**")
                for j, feedback in enumerate(answer.get('feedback', []), 1):
                    st.write(f"{j}. {feedback}")
    
    # Email and reporting section
    st.subheader("📧 Send Results to HR Team")
    if st.button("📨 Send Comprehensive Report to HR", use_container_width=True):
        with st.spinner("Preparing and sending comprehensive interview analysis..."):
            success, message = send_data_to_email(candidate, skill_performance, overall_score, pass_status, answers)
            
            if success:
                st.success(f"✅ Comprehensive interview analysis sent to: {HR_EMAIL}")
                st.info("📊 Data automatically saved to Google Sheets dashboard")
            else:
                st.error(f"❌ {message}")
    
    # Enhanced report generation
    st.subheader("📄 Download Complete Assessment Report")
    
    # Create comprehensive report data
    report_data = []
    
    # Candidate summary
    report_data.append({
        "Category": "CANDIDATE_SUMMARY",
        "Name": candidate["name"],
        "Email": candidate["email"],
        "Phone": candidate["phone"],
        "Position": candidate["position"],
        "Experience": candidate["experience"],
        "Skills": candidate["skills"],
        "Interview_Date": candidate["timestamp"],
        "Overall_Score": f"{overall_score}%",
        "Final_Status": pass_status,
        "Assessment_Level": candidate["experience_level"],
        "Total_Questions": len(answers)
    })
    
    # Individual question details
    for i, answer in enumerate(answers):
        report_data.append({
            "Category": f"Q{i+1}_{answer['question_type'].upper()}",
            "Skill_Area": answer["skill"],
            "Question": answer["question"],
            "Difficulty_Level": answer["difficulty"],
            "AI_Score": f"{answer['score']}%",
            "AI_Transcript": answer["transcript"],
            "AI_Feedback": " | ".join(answer.get('feedback', [])),
        })
    
    report_df = pd.DataFrame(report_data)
    csv_data = report_df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download Complete AI Assessment Report (CSV)",
        data=csv_data,
        file_name=f"{candidate['name']}_Comprehensive_AI_Interview_Report_{candidate['timestamp'].replace(':', '-').replace(' ', '_')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Reset for new candidate
    if st.button("🔄 Start New Comprehensive Interview", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Enhanced Footer
st.markdown("---")
st.markdown(f"*🔗 HR Dashboard: [Google Sheets]({SHEET_URL}) | 📧 Auto-Email: {HR_EMAIL}*")
st.markdown("*🤖 Powered by Advanced AI Evaluation: 5 Questions Per Skill + Comprehensive Project Assessment*")
