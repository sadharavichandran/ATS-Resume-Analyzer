import time
import streamlit as st
import pandas as pd
import plotly.express as px
from resume_analyzer import extract_text, extract_skills, ml_ats_score, skill_gap, summarize_text, generate_cover_letter
from recommendations import get_recommendations
from auth_system import register_user, login_user, get_user_info, increment_analyses

# Page config with dark theme
st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern theme (dark and light)
# Custom CSS for modern dark theme

def inject_custom_css(theme="dark"):
    # minimal light theme override
    if theme == "light":
        st.markdown("""
        <style>
        :root {
            --primary-color: #0066ff;
            --secondary-color: #ffffff;
            --accent-color: #16c784;
            --danger-color: #ff6b6b;
            --text-color: #1a1a2c;
            --background: #ffffff;
        }
        html, body, [data-testid="stAppViewContainer"] {
            background: #ffffff;
            color: #1a1a2c;
        }
        [data-testid="stSidebar"] {
            background: #f0f0f0;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            background-color: #ffffff !important;
            color: #1a1a2c !important;
            border: 1px solid #0066ff !important;
        }
        </style>
        """, unsafe_allow_html=True)
        return
    # dark theme by default
    st.markdown("""
    <style>
    :root {
        --primary-color: #0066ff;
        --secondary-color: #1a1a2e;
        --accent-color: #16c784;
        --danger-color: #ff6b6b;
        --text-color: #e0e0e0;
        --background: #0f0f1e;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
    }
    
    /* Auth Card Styling */
    .auth-card {
        background: rgba(26, 26, 46, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 102, 255, 0.3);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #0066ff 0%, #0052cc 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 15px rgba(0, 102, 255, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 102, 255, 0.5) !important;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #1a1a2e !important;
        border: 1px solid #0066ff !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
        padding: 10px !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%);
        border: 1px solid #0066ff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 102, 255, 0.1);
        transition: all 0.3s;
    }
    
    .metric-card:hover {
        border-color: #00d4ff;
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-color: #0066ff;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #0066ff;
    }
    
    .success-box {
        background: linear-gradient(135deg, #16c784 0%, #12a070 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ffa500 0%, #ff8c00 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #0066ff 0%, #0052cc 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
    
    .section-title {
        background: linear-gradient(135deg, #0066ff 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 28px;
        font-weight: 700;
        margin: 20px 0;
    }
    
    .subtitle {
        color: #b0b0c0;
        font-size: 16px;
        margin-bottom: 10px;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%);
        border-left: 4px solid #0066ff;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    hr {
        border-color: #0066ff;
        opacity: 0.3;
        margin: 20px 0;
    }
    
    .skill-badge {
        background: linear-gradient(135deg, #0066ff 0%, #0052cc 100%);
        border-radius: 20px;
        padding: 6px 12px;
        display: inline-block;
        margin: 4px;
        font-weight: 500;
    }
    
    .matched-skill {
        background: linear-gradient(135deg, #16c784 0%, #12a070 100%);
        border-radius: 20px;
        padding: 6px 12px;
        display: inline-block;
        margin: 4px;
        font-weight: 500;
    }
    
    .missing-skill {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        border-radius: 20px;
        padding: 6px 12px;
        display: inline-block;
        margin: 4px;
        font-weight: 500;
    }
    
    [data-testid="stMetricValue"] {
        color: #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)
# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_name = None

# theme preference stored in session
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Inject custom CSS based on current theme
inject_custom_css(st.session_state.theme)

if "scores" not in st.session_state:
    st.session_state["scores"] = {}
if "skills" not in st.session_state:
    st.session_state["skills"] = []
if "times" not in st.session_state:
    st.session_state["times"] = []
if "history" not in st.session_state:
    st.session_state["history"] = []

# ========== AUTH PAGES ==========

def login_page():
    col1, col2, col3 = st.columns([0.5, 1.5, 0.5])
    
    with col2:
        st.markdown("<div style='height: 60px'></div>", unsafe_allow_html=True)
        
        # Auth Card Container
        st.markdown("""
        <div class='auth-card'>
        """, unsafe_allow_html=True)
        
        # Logo/Header - More compact
        st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <div style='font-size: 40px; margin-bottom: 10px;'>🔐</div>
            <h2 style='margin: 0; color: #e0e0e0; font-size: 28px;'>Welcome Back</h2>
            <p style='color: #b0b0c0; font-size: 13px; margin: 8px 0 0 0;'>Enter your credentials to continue</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login Form
        email = st.text_input("📧 Email", placeholder="your.email@example.com", key="login_email")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password", key="login_pass")
        
        # Remember & Forgot
        col_rem, col_forgot = st.columns([1, 1.5])
        with col_rem:
            remember = st.checkbox("Stay logged in", key="login_remember")
        with col_forgot:
            st.markdown(
                "<div style='text-align: right; padding-top: 8px;'><a href='#' style='color: #0066ff; text-decoration: none; font-size: 12px;'>Forgot password?</a></div>",
                unsafe_allow_html=True
            )
        
        st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)
        
        if st.button("🚀 Sign In", use_container_width=True, key="login_btn"):
            if email and password:
                success, result = login_user(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_name = result
                    st.success("✅ Login successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.warning("⚠️ Please enter both email and password")
        # demo credentials shortcut
        if st.button("🧪 Use Demo Account", use_container_width=True, key="demo_login"):
            demo_email = "demo@example.com"
            demo_pass = "demo123"
            success, result = login_user(demo_email, demo_pass)
            if success:
                st.session_state.authenticated = True
                st.session_state.user_email = demo_email
                st.session_state.user_name = result
                st.success("✅ Logged in as demo user")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"❌ {result}")
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        # Register Link - Compact
        st.markdown("""
        <div style='text-align: center; padding-top: 15px; border-top: 1px solid rgba(0, 102, 255, 0.2);'>
            <p style='color: #b0b0c0; font-size: 13px; margin: 0;'>
                Don't have an account? <a href='#' style='color: #0066ff; text-decoration: none; font-weight: 600;'>Create Account</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Create New Account", use_container_width=True, key="register_switch"):
            st.session_state.page = "register"
            st.rerun()
        
        # Close card
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)

def register_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
        
        # Logo/Header
        st.markdown("""
        <div style='text-align: center; margin-bottom: 40px;'>
            <h1 style='font-size: 48px; margin: 0; background: linear-gradient(135deg, #0066ff 0%, #00d4ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🎯 ATS Analyzer</h1>
            <p style='color: #b0b0c0; font-size: 14px; margin: 10px 0 0 0;'>AI-Powered Recruitment Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Create Account")
        st.markdown('<p class="subtitle">Join thousands of recruiters using ATS Analyzer</p>', unsafe_allow_html=True)
        
        # Register Form
        full_name = st.text_input("👤 Full Name", placeholder="John Doe")
        email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
        password = st.text_input("🔑 Password", type="password", placeholder="At least 6 characters")
        confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Re-enter your password")
        
        agree_terms = st.checkbox("✓ I agree to the Terms of Service and Privacy Policy")
        
        if st.button("🚀 Sign Up", use_container_width=True, key="signup_btn"):
            if not full_name or not email or not password:
                st.warning("⚠️ Please fill in all fields")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif not agree_terms:
                st.warning("⚠️ Please agree to the terms")
            else:
                success, message = register_user(email, password, full_name)
                if success:
                    st.success(f"✅ {message}")
                    st.session_state.page = "login"
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        st.markdown("---")
        
        # Login Link
        st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <p style='color: #b0b0c0;'>Already have an account? </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔐 Back to Login", use_container_width=True, key="login_switch"):
            st.session_state.page = "login"
            st.rerun()

# ========== MAIN APP PAGES ==========

def dashboard_page():
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("### 📊 Dashboard")
        st.markdown(f'<p class="subtitle">Welcome back, <strong>{st.session_state.user_name}</strong>! 👋</p>', unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.rerun()
    
    st.markdown("---")
    
    # Demo Banner
    with st.expander("🎯 Demo Mode Active", expanded=True):
        st.markdown("""
        ✨ **Experience the full power of ATS Analyzer**
        - 🤖 AI-powered resume analysis
        - 📊 Real-time skill matching
        - 📈 Candidate ranking & comparison
        - 💡 Personalized learning recommendations
        """)
    
    # Metrics
    total = len(st.session_state["scores"])
    avg_score = sum(st.session_state["scores"].values()) / total if total else 0
    avg_time = sum(st.session_state["times"]) / len(st.session_state["times"]) if st.session_state["times"] else 0
    
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 24px; margin-bottom: 10px;'>📄</div>
            <div style='font-size: 28px; font-weight: 700; margin-bottom: 5px;'>{}</div>
            <div style='color: #b0b0c0; font-size: 12px;'>Total Resumes</div>
        </div>
        """.format(total), unsafe_allow_html=True)
    
    with metric_cols[1]:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 24px; margin-bottom: 10px;'>👥</div>
            <div style='font-size: 28px; font-weight: 700; margin-bottom: 5px;'>{}</div>
            <div style='color: #b0b0c0; font-size: 12px;'>Analyzed Candidates</div>
        </div>
        """.format(total), unsafe_allow_html=True)
    
    with metric_cols[2]:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 24px; margin-bottom: 10px;'>⭐</div>
            <div style='font-size: 28px; font-weight: 700; margin-bottom: 5px;'>{:.1f}%</div>
            <div style='color: #b0b0c0; font-size: 12px;'>Avg Match Score</div>
        </div>
        """.format(avg_score), unsafe_allow_html=True)
    
    with metric_cols[3]:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 24px; margin-bottom: 10px;'>⚡</div>
            <div style='font-size: 28px; font-weight: 700; margin-bottom: 5px;'>{:.2f}s</div>
            <div style='color: #b0b0c0; font-size: 12px;'>Avg Processing Time</div>
        </div>
        """.format(avg_time), unsafe_allow_html=True)
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 📈 Monthly Applications")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        counts = [total * i // 2 + 1 for i in range(len(months))]
        df = pd.DataFrame({"Month": months, "Applications": counts})
        fig = px.line(df, x="Month", y="Applications", markers=True)
        fig.update_layout(
            plot_bgcolor="#1a1a2e",
            paper_bgcolor="#0f0f1e",
            font=dict(color="#e0e0e0"),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("### 🔝 Top Skills Detected")
        if st.session_state["skills"]:
            skill_counts = pd.Series(st.session_state["skills"]).value_counts().head(10)
            fig2 = px.bar(skill_counts, title="")
            fig2.update_layout(
                plot_bgcolor="#1a1a2e",
                paper_bgcolor="#0f0f1e",
                font=dict(color="#e0e0e0"),
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("📊 No skills detected yet. Analyze a resume to get started!")

def analyzer_page():
    st.markdown("### 📄 Resume Analyzer")
    st.markdown('<p class="subtitle">Upload your resume(s) and job description for AI-powered analysis</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        names_input = st.text_input("👤 Candidate Names (comma-separated)", placeholder="Optional, will use file names")
    with col2:
        if st.button("🗑️ Clear", key="clear_analyzer"):
            st.success("✓ Ready for new analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        resumes = st.file_uploader("📑 Upload Resume(s) (PDF)", type=["pdf"], accept_multiple_files=True)
    with col2:
        st.info("✓ Supported: PDF files only")
    
    jd = st.text_area("💼 Paste Job Description", placeholder="Paste the complete job description here", height=150)
    
    if st.button("🔍 Analyze Resume(s)", use_container_width=True):
        if resumes and jd:
            name_list = [n.strip() for n in names_input.split(",")] if names_input else []
            results = []
            for idx, resume in enumerate(resumes):
                if idx < len(name_list) and name_list[idx]:
                    cand_name = name_list[idx]
                else:
                    cand_name = resume.name.rsplit('.', 1)[0]
                with st.spinner(f"⏳ Analyzing {cand_name}..."):
                    start_time = time.time()
                    text = extract_text(resume)
                    score = ml_ats_score(text, jd)
                    end_time = time.time()
                # save summary and allow generation
                summary = summarize_text(text)
                st.session_state["scores"][cand_name] = score
                st.session_state["times"].append(end_time - start_time)
                skills = extract_skills(text)
                st.session_state["skills"].extend(skills)
                st.session_state["last_skills"] = skills
                increment_analyses(st.session_state.user_email)
                record = {"name": cand_name, "score": score, "time": end_time - start_time, "skills": skills, "summary": summary, "jd": jd}
                st.session_state.setdefault("history", []).append({**record, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")})
                results.append(record)
            st.markdown("---")
            for res in results:
                with st.expander(f"{res['name']} - {res['score']:.2f}%"):
                    st.markdown(f"**Score:** {res['score']:.2f}%")
                    st.markdown(f"Processing Time: {res['time']:.2f}s")
                    if res.get("summary"):
                        st.markdown("#### 📄 Resume Preview")
                        st.write(res["summary"])
                        if st.button(f"✍️ Draft Cover Letter for {res['name']}", key=f"cover_{res['name']}"):
                            letter = generate_cover_letter(resume_text=res.get("summary"), jd_text=res.get("jd"), candidate_name=res['name'])
                            st.text_area("📝 Cover Letter", value=letter, height=200)
                    st.markdown("#### 🎯 Detected Skills")
                    if res["skills"]:
                        cols = st.columns(3)
                        for i, sk in enumerate(res["skills"]):
                            with cols[i % 3]:
                                st.markdown(f"<div class='skill-badge'>⭐ {sk.title()}</div>", unsafe_allow_html=True)
                    else:
                        st.info("No skills detected")
            if st.session_state.get("history"):
                st.markdown("### 📜 Analysis History")
                hist_df = pd.DataFrame(st.session_state["history"])
                st.dataframe(hist_df[["timestamp","name","score","time"]], use_container_width=True)
                csv = hist_df.to_csv(index=False)
                st.download_button("📥 Download History (CSV)", data=csv, file_name="analysis_history.csv", mime="text/csv")
        else:
            st.warning("⚠️ Please upload at least one resume and provide a job description")


def coverletter_page():
    st.markdown("### ✉️ Cover Letter Generator")
    st.markdown('<p class="subtitle">Craft a custom cover letter based on resume summary and job description</p>', unsafe_allow_html=True)
    st.markdown("---")

    resume_summary = st.text_area("📝 Resume / Summary", height=150)
    jd_text = st.text_area("💼 Job Description", height=150)
    candidate = st.text_input("👤 Your Name", placeholder="Optional, used in letter")
    if st.button("🖊️ Generate Cover Letter", use_container_width=True):
        if resume_summary and jd_text:
            letter = generate_cover_letter(resume_summary, jd_text, candidate_name=candidate or "Candidate")
            st.text_area("🚀 Your Cover Letter", value=letter, height=300)
        else:
            st.warning("⚠️ Please provide both resume summary and job description")


def skillgap_page():
    st.markdown("### ⚠️ Skill Gap Analysis")
    st.markdown('<p class="subtitle">Identify missing skills and get personalized learning recommendations</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    if "resume_skills" in st.session_state:
        resume_skills = st.session_state.get("resume_skills", [])
    else:
        resume_skills = []
    
    st.markdown("#### 🔍 Analyze Job Fit")
    jd_new = st.text_area("💼 Paste Job Description", placeholder="Enter job description for analysis", height=150)
    
    if st.button("📊 Analyze Gap", use_container_width=True):
        if jd_new:
            jd_skills = extract_skills(jd_new.lower())
            st.session_state["jd_skills"] = jd_skills
            
            gap = skill_gap(resume_skills, jd_skills)
            matched = set(resume_skills) & set(jd_skills)
            
            # Metrics
            metric_cols = st.columns(3)
            with metric_cols[0]:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 24px;'>🌟</div>
                    <div style='font-size: 28px; font-weight: 700;'>{}</div>
                    <div style='color: #b0b0c0;'>Your Skills</div>
                </div>
                """.format(len(resume_skills)), unsafe_allow_html=True)
            
            with metric_cols[1]:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 24px;'>✅</div>
                    <div style='font-size: 28px; font-weight: 700;'>{}</div>
                    <div style='color: #b0b0c0;'>Matching</div>
                </div>
                """.format(len(matched)), unsafe_allow_html=True)
            
            with metric_cols[2]:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 24px;'>🔹</div>
                    <div style='font-size: 28px; font-weight: 700;'>{}</div>
                    <div style='color: #b0b0c0;'>Missing</div>
                </div>
                """.format(len(gap)), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Matching Skills
            if matched:
                with st.expander("✅ Matching Skills", expanded=True):
                    match_cols = st.columns(2)
                    for i, skill in enumerate(matched):
                        with match_cols[i % 2]:
                            st.markdown(f"<div class='matched-skill'>✓ {skill.title()}</div>", unsafe_allow_html=True)
            
            # Missing Skills
            if gap:
                with st.expander("📚 Missing Skills & Learning Resources", expanded=True):
                    rec = get_recommendations(gap)
                    for skill in gap:
                        with st.container(border=True):
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.markdown(f"<div style='color: #ff6b6b;'><strong>{skill.upper()}</strong></div>", unsafe_allow_html=True)
                            with col2:
                                st.write(rec.get(skill, "Learn fundamentals"))
                st.markdown(f"<div class='info-box'>🎯 Priority: Focus on {len(gap)} skill(s) for better alignment</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='success-box'>🎉 Perfect Match! All required skills found!</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a job description")
    
    if resume_skills:
        st.info(f"📋 Last analyzed: {', '.join(resume_skills)}")

def ranking_page():
    st.markdown("### 🏆 Resume Ranking")
    st.markdown('<p class="subtitle">Compare and rank analyzed candidates</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state["scores"]:
        df = pd.DataFrame(
            st.session_state["scores"].items(),
            columns=["Candidate", "ATS Score"]
        ).sort_values(by="ATS Score", ascending=False)
        
        # Top metrics
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 24px;'>🏆</div>
                <div style='font-size: 24px; font-weight: 700;'>{df.iloc[0]['Candidate']}</div>
                <div style='font-size: 28px; color: #00d4ff; font-weight: 700;'>{df.iloc[0]['ATS Score']:.2f}%</div>
                <div style='color: #b0b0c0; font-size: 12px;'>Top Candidate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 24px;'>👥</div>
                <div style='font-size: 28px; font-weight: 700;'>{len(df)}</div>
                <div style='color: #b0b0c0; font-size: 12px;'>Total Candidates</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Table
        st.markdown("#### 📊 Candidate Rankings")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Chart
        st.markdown("#### 📈 Score Distribution")
        fig = px.bar(df, x="Candidate", y="ATS Score", color="ATS Score", color_continuous_scale="RdYlGn")
        fig.update_layout(
            plot_bgcolor="#1a1a2e",
            paper_bgcolor="#0f0f1e",
            font=dict(color="#e0e0e0"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Export
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Rankings (CSV)",
            data=csv,
            file_name="ats_ranking.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("📊 No candidates ranked yet. Analyze resumes to get started!")

def settings_page():
    st.markdown("### ⚙️ Settings")
    st.markdown('<p class="subtitle">Manage your account and preferences</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### 👤 Account Information")
        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Name:** {st.session_state.user_name}")
        st.write(f"**Analyses:** {len(st.session_state['scores'])}")
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("#### 🧹 Data Management")
    if st.button("🗑️ Clear All Data", use_container_width=True):
        st.session_state["scores"].clear()
        st.session_state["skills"].clear()
        st.session_state["times"].clear()
        st.session_state["history"].clear()
        st.success("✓ All session data cleared!")
    
    st.markdown("---")
    st.markdown("#### ℹ️ About")
    st.info("""
    **ATS Resume Analyzer v3.0**
    - 🤖 AI-powered resume analysis
    - 📊 Real-time skill matching
    - 💡 Personalized learning recommendations
    - 🔐 Secure authentication
    - 🎨 Modern dark theme UI
    """)

# ========== MAIN LOGIC ==========

if st.session_state.authenticated:
    # Authenticated - Show main app
    st.sidebar.markdown("### 🎯 ATS Analyzer")
    st.sidebar.markdown(f"👋 Welcome, {st.session_state.user_name}!")
    st.sidebar.markdown("---")
    # theme selector
    theme_choice = st.sidebar.selectbox("🎨 Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "dark" else 1)
    st.session_state.theme = theme_choice.lower()
    inject_custom_css(st.session_state.theme)
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio("📌 Navigation", [
        "📊 Dashboard",
        "📄 Resume Analyzer",
        "✉️ Cover Letter",
        "⚠️ Skill Gap Analysis",
        "🏆 Resume Ranking",
        "⚙️ Settings"
    ])
    
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "📄 Resume Analyzer":
        analyzer_page()
    elif page == "✉️ Cover Letter":
        coverletter_page()
    elif page == "⚠️ Skill Gap Analysis":
        skillgap_page()
    elif page == "🏆 Resume Ranking":
        ranking_page()
    elif page == "⚙️ Settings":
        settings_page()

else:
    # Not authenticated - Show auth pages
    if "page" not in st.session_state:
        st.session_state.page = "login"
    
    if st.session_state.page == "register":
        register_page()
    else:
        login_page()