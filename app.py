import streamlit as st
import pandas as pd
import time

# Project Configuration
st.set_page_config(
    page_title="Hiring Skilled Candidates",
    page_icon="🎯",
    layout="wide"
)

# Header with Developer Info
st.markdown("""
# 🎯 Hiring Skilled Candidates
---
**Developed by:** Akash Bauri  
📧 **Email:** akashbauri16021998@gmail.com  
📞 **Phone:** 8002778855  
---
""")

# Simple Audio Processing Function
def simple_transcript(audio_data):
    if audio_data:
        return f"Audio recorded successfully ({len(audio_data)} bytes). Professional transcript would be generated with full AI deployment."
    return "No audio recorded"

# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = "info_collection"
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

# Audio Processing Ready
st.success("✅ Audio Processing System Ready")

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
                                    ["0-1 years", "1-3 years", "3-5 years", "5+ years"])
            skills = st.text_area("Technical Skills*", 
                                placeholder="Python, APIs, Django, MySQL, etc.")
        
        submitted = st.form_submit_button("Continue to Voice Interview →", use_container_width=True)
        
        if submitted:
            if all([name, email, phone, position, experience, skills]):
                st.session_state.candidate_data = {
                    "name": name,
                    "email": email, 
                    "phone": phone,
                    "position": position,
                    "experience": experience,
                    "skills": skills,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.stage = "voice_intro"
                st.rerun()
            else:
                st.error("❌ Please fill all required fields marked with *")

# Stage 2: Voice Introduction
elif st.session_state.stage == "voice_intro":
    st.header("🎤 Voice Introduction")
    st.info(f"**Hello {st.session_state.candidate_data['name']}!** Please record a brief introduction about yourself (30-90 seconds)")
    
    intro_audio = st.audio_input("🎙️ Record your introduction")
    
    if intro_audio is not None:
        st.audio(intro_audio, format='audio/wav')
        
        with st.spinner("🤖 Processing your introduction..."):
            intro_transcript = simple_transcript(intro_audio)
            st.session_state.candidate_data["intro_audio"] = intro_audio
            st.session_state.candidate_data["intro_transcript"] = intro_transcript
            
            st.success("✅ Introduction recorded successfully!")
            st.write("**Status:**", intro_transcript)
            
            if st.button("Continue to Skills Assessment →", use_container_width=True):
                st.session_state.stage = "skills_test"
                st.rerun()
    else:
        st.warning("⚠️ Please record your introduction to continue")

# Stage 3: Skills Test
elif st.session_state.stage == "skills_test":
    questions = [
        {"q": "Explain the fundamentals of Python.", "time_limit": "3 minutes", "keywords": ["variable", "loop", "function", "syntax", "library"]},
        {"q": "Describe your experience with APIs.", "time_limit": "3 minutes", "keywords": ["api", "request", "response", "json", "endpoint"]},
        {"q": "Tell us about a challenging project you worked on.", "time_limit": "5 minutes", "keywords": ["challenge", "solution", "problem", "team", "result"]}
    ]
    
    current_q = st.session_state.current_question
    
    if current_q < len(questions):
        question_data = questions[current_q]
        
        st.header(f"📋 Question {current_q + 1} of {len(questions)}")
        st.subheader(f"❓ {question_data['q']}")
        st.info(f"⏱️ **Time Limit:** {question_data['time_limit']} | **Speak clearly and concisely**")
        
        answer_audio = st.audio_input(f"🎙️ Record your answer to Question {current_q + 1}")
        
        if answer_audio is not None:
            st.audio(answer_audio, format='audio/wav')
            
            with st.spinner("🤖 Processing your answer..."):
                answer_transcript = simple_transcript(answer_audio)
                
                # Simple scoring based on audio length
                audio_length = len(answer_audio) if answer_audio else 0
                score = min(100, max(60, (audio_length // 1000) * 10))  # Basic scoring
                
                answer_data = {
                    "question": question_data["q"],
                    "audio": answer_audio,
                    "transcript": answer_transcript,
                    "score": round(score),
                    "audio_length": audio_length
                }
                
                st.session_state.answers.append(answer_data)
                
                st.success("✅ Answer recorded successfully!")
                st.write("**Status:**", answer_transcript)
                st.write(f"**Preliminary Score:** {round(score)}%")
                
                if st.button("Next Question →" if current_q < len(questions)-1 else "Complete Assessment →", 
                           use_container_width=True):
                    st.session_state.current_question += 1
                    if current_q >= len(questions)-1:
                        st.session_state.stage = "results"
                    st.rerun()
        else:
            st.warning("⚠️ Please record your answer to continue")
    
# Stage 4: Results
elif st.session_state.stage == "results":
    st.header("📊 Interview Results")
    
    candidate = st.session_state.candidate_data
    answers = st.session_state.answers
    
    # Calculate overall score
    total_score = sum(answer["score"] for answer in answers) // len(answers) if answers else 0
    pass_status = "PASS" if total_score >= 70 else "FAIL"
    
    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Candidate Profile")
        st.write(f"**Name:** {candidate['name']}")
        st.write(f"**Email:** {candidate['email']}")
        st.write(f"**Phone:** {candidate['phone']}")
        st.write(f"**Position:** {candidate['position']}")
        st.write(f"**Experience:** {candidate['experience']}")
        st.write(f"**Skills:** {candidate['skills']}")
    
    with col2:
        st.subheader("📈 Assessment Summary")
        if pass_status == "PASS":
            st.success(f"✅ **Status: {pass_status}**")
        else:
            st.error(f"❌ **Status: {pass_status}**")
        st.metric("Overall Score", f"{total_score}%")
        st.write(f"**Interview Date:** {candidate['timestamp']}")
    
    # Voice Introduction
    st.subheader("🎤 Voice Introduction")
    if "intro_audio" in candidate:
        st.audio(candidate["intro_audio"], format='audio/wav')
    st.write("**Status:**", candidate.get("intro_transcript", "No introduction recorded"))
    
    # Question Answers
    st.subheader("📝 Question Responses")
    for i, answer in enumerate(answers):
        with st.expander(f"Question {i+1}: {answer['question']} (Score: {answer['score']}%)"):
            st.audio(answer["audio"], format='audio/wav')
            st.write("**Status:**", answer["transcript"])
            st.write(f"**Score:** {answer['score']}%")
    
    # Download Report
    st.subheader("📄 Download Report")
    
    # Create comprehensive report
    report_data = {
        "Candidate_Name": [candidate["name"]],
        "Email": [candidate["email"]],
        "Phone": [candidate["phone"]],
        "Position": [candidate["position"]],
        "Experience": [candidate["experience"]],
        "Skills": [candidate["skills"]],
        "Interview_Date": [candidate["timestamp"]],
        "Introduction_Status": [candidate.get("intro_transcript", "No introduction")],
        "Overall_Score": [f"{total_score}%"],
        "Status": [pass_status]
    }
    
    # Add question responses
    for i, answer in enumerate(answers):
        report_data[f"Question_{i+1}"] = [answer["question"]]
        report_data[f"Answer_{i+1}_Status"] = [answer["transcript"]]
        report_data[f"Answer_{i+1}_Score"] = [f"{answer['score']}%"]
    
    report_df = pd.DataFrame(report_data)
    
    csv_data = report_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Complete Interview Report (CSV)",
        data=csv_data,
        file_name=f"{candidate['name']}_Interview_Report_{candidate['timestamp'].replace(':', '-').replace(' ', '_')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Reset for new candidate
    if st.button("🔄 Start New Interview", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Footer
st.markdown("---")
st.markdown("*Live Audio Recording & Professional Assessment Platform*")
