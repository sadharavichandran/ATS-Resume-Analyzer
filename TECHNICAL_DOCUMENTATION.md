# 🏗️ ATS Resume Analyzer v3.0 - Technical Documentation

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Module Overview](#module-overview)
3. [Data Flow](#data-flow)
4. [API Reference](#api-reference)
5. [Database Schema](#database-schema)
6. [Authentication Flow](#authentication-flow)
7. [Extension Guide](#extension-guide)
8. [Performance Optimization](#performance-optimization)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  (app.py - UI Layer with Custom CSS & Dark Theme)          │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌─────────┐ ┌──────────┐ ┌──────────────┐
    │ Auth    │ │ Resume   │ │ Skill Gap    │
    │ System  │ │ Analyzer │ │ & Ranking    │
    │ (auth)  │ │ (ml)     │ │ (analysis)   │
    └────┬────┘ └────┬─────┘ └──────┬───────┘
         │           │              │
         ▼           ▼              ▼
    ┌─────────────────────────────────────┐
    │     Data & Computation Layer        │
    │  • PDF Extraction (PyPDF2)          │
    │  • Skill Detection (NLP)            │
    │  • ATS Scoring (scikit-learn)       │
    │  • Learning Recommendations         │
    │  • Visualization (Plotly)           │
    └────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Persistent Storage  │
         │  users_db.json        │
         │  (user credentials    │
         │   and metadata)       │
         └───────────────────────┘
```

### Component Layers

**Presentation Layer**

- Streamlit UI components
- Custom CSS injection
- Interactive widgets
- Form handling

**Business Logic Layer**

- Authentication logic
- Resume analysis algorithms
- Skill matching
- Report generation

**Data Layer**

- User credentials (JSON)
- Resume data (session state)
- Analysis results (session state)
- Skill database (in-memory)

---

## Module Overview

### 1. app.py - Main Application

**Purpose**: Core Streamlit application with UI and page management

**Key Components**:

#### CSS Injection Function

```python
def inject_custom_css():
    """
    Injects custom CSS for dark theme

    Features:
    - Dark gradient backgrounds
    - Styled buttons and inputs
    - Color-coded status boxes
    - Hover effects and animations
    - Mobile-responsive design

    Returns: Applies styles via st.markdown()
    """
```

**CSS Variables Defined**:

```css
--primary-blue: #0066ff --accent-cyan: #00d4ff --success-green: #16c784
  --error-red: #ff6b6b --warning-orange: #ffa500 --bg-dark: #0f0f1e
  --bg-secondary: #1a1a2e --text-light: #e0e0e0 --text-muted: #b0b0c0;
```

#### Page Functions

**login_page()**

- Displays centered login form
- Email and password inputs (with icons)
- "Remember me" checkbox
- Link to register page
- Error message handling
- Session state management

**register_page()**

- Full name input field
- Email validation
- Password strength requirements
- Confirm password validation
- Terms and conditions checkbox
- Error message display
- Returns to login after success

**dashboard_page()**

- 4 metric cards with icons (📄 📥 ⭐ ⚡)
- Monthly application trend chart (Plotly)
- Top skills bar chart (Plotly)
- Welcome message with user name
- Demo data banner
- Interactive elements

**analyzer_page()**

- Candidate name input (👤)
- PDF file uploader (📑)
- Job description textarea (💼)
- 3-tab interface:
  - **Score & Skills**: ATS score, skill badges
  - **Match Analysis**: Detailed matching results
  - **Recommendations**: Learning resources
- Skill visualization with color coding
- Error handling for missing files

**skillgap_page()**

- Job description input area
- 3 metric cards (matching skills, missing skills, match %)
- Expandable sections (matched/missing skills)
- Learning resource cards with:
  - Skill name with icon
  - Resource list with links
  - Difficulty indicator
  - Time estimate

**ranking_page()**

- Top candidate metric card
- Total candidates metric card
- Ranking table with:
  - Candidate name
  - Calculated scores
  - Skill match percentage
- Bar chart visualization
- CSV export button
- Sorting and filtering (future)

**settings_page()**

- Account information section
- User email and join date
- Number of analyses performed
- Logout button
- Clear all data button
- About section
- Privacy and security info

#### Session State Management

```python
st.session_state initialization:
├── authenticated (bool)     # Login status
├── user_email (str)        # Current user email
├── user_name (str)         # Display name
├── scores (dict)           # Resume analysis scores
├── skills (dict)           # Detected skills by category
└── times (list)            # Processing times
```

### 2. auth_system.py - Authentication Module

**Purpose**: User credential management and authentication logic

**Functions**:

#### load_users()

```python
def load_users() -> dict:
    """
    Load users from JSON database

    Returns:
        dict: {email: {password, full_name, created_at, analyses}}

    Creates empty dict if file missing
    """
```

**Data Structure**:

```json
{
  "user@example.com": {
    "password": "plaintext_password",
    "full_name": "John Doe",
    "created_at": "2025-02-28 10:30:45",
    "analyses": 5
  }
}
```

#### save_users(users)

```python
def save_users(users: dict) -> None:
    """
    Save users to JSON database

    Args:
        users: Dictionary of user data

    Ensures atomic write with proper formatting
    """
```

#### register_user(email, password, full_name)

```python
def register_user(email: str, password: str, full_name: str) -> tuple:
    """
    Register new user with validation

    Args:
        email: User email (must be unique)
        password: User password (min 6 chars)
        full_name: User's full name

    Returns:
        (success: bool, message: str)

    Validates:
    - Email not already registered
    - Password minimum 6 characters
    - Valid email format (optional enhancement)

    Stores user with timestamp and zero analyses
    """
```

#### login_user(email, password)

```python
def login_user(email: str, password: str) -> tuple:
    """
    Authenticate user credentials

    Args:
        email: User email
        password: User password

    Returns:
        (success: bool, result: str OR full_name: str)

    On success: Returns (True, full_name)
    On failure: Returns (False, error_message)
    """
```

#### get_user_info(email)

```python
def get_user_info(email: str) -> dict:
    """
    Retrieve user metadata

    Args:
        email: User email

    Returns:
        dict: User data or empty dict if not found
    """
```

#### increment_analyses(email)

```python
def increment_analyses(email: str) -> None:
    """
    Update analysis counter for user

    Args:
        email: User email

    Increments analyses count and persists to storage
    """
```

### 3. resume_analyzer.py - ML Analysis Engine

**Purpose**: Extract and analyze resume information

**Key Functions**:

#### extract_text(pdf_file)

```python
def extract_text(pdf_file) -> str:
    """
    Extract text from PDF file

    Args:
        pdf_file: Uploaded file object

    Returns:
        str: Extracted text content

    Uses: PyPDF2.PdfReader
    """
```

#### extract_skills(text)

```python
def extract_skills(text: str) -> dict:
    """
    Extract skills from text using keyword matching

    Args:
        text: Resume text content

    Returns:
        dict: {category: [skills]}

    Categories: Programming, Web Dev, Databases, etc.
    Performs case-insensitive matching
    """
```

#### ml_ats_score(resume_text, jd_text)

```python
def ml_ats_score(resume_text: str, jd_text: str) -> float:
    """
    Calculate ATS compatibility score using ML

    Args:
        resume_text: Resume content
        jd_text: Job description content

    Returns:
        float: Score 0-100

    Algorithm:
    1. TF-IDF vectorization of both texts
    2. Cosine similarity calculation
    3. Normalize to 0-100 scale
    4. Apply weighting for keyword density

    Returns realistic score with 2 decimal precision
    """
```

#### skill_gap(resume_skills, jd_skills)

```python
def skill_gap(resume_skills: list, jd_skills: list) -> dict:
    """
    Compare resume skills against job requirements

    Args:
        resume_skills: Skills found in resume
        jd_skills: Skills required by job

    Returns:
        dict: {
            'matched': [...],
            'missing': [...],
            'percentage': float
        }
    """
```

### 4. recommendations.py - Learning Resources Database

**Purpose**: Provide learning paths for skill development

**Structure**:

```python
LEARNING_RESOURCES = {
    'skill_name': [
        'Resource 1 - Link',
        'Resource 2 - Link',
        'Resource 3 - Link',
        ...
    ]
}
```

**Resource Types**:

- Online Courses (Udemy, Coursera, FastAI)
- Official Documentation
- Practice Platforms (HackerRank, LeetCode, Kaggle)
- Books and Articles
- Certification Paths

**Features**:

- 50+ skills covered
- 3-5 resources per skill
- Mix of free and paid options
- Curated from industry standards
- Regular update capability

### 5. skills.py - Skill Database

**Purpose**: Comprehensive skill keyword matching

**Structure**:

```python
SKILLS = {
    'Programming Languages': [
        'Python', 'Java', 'JavaScript', ...
    ],
    'Web Development': [
        'React', 'Angular', 'Vue', ...
    ],
    ...
}
```

**Categories** (11 total):

1. Programming Languages (9 skills)
2. Web Development (13 skills)
3. Databases (7 skills)
4. Data Science (11 skills)
5. DevOps/Cloud (13 skills)
6. Soft Skills (5 skills)
7. Mobile Development
8. Security
9. Big Data
10. Testing
11. Project Management

**Features**:

- Case-insensitive matching
- Partial keyword support
- Version-aware matching (Python 3.x, Java 11, etc.)
- Expandable with custom skills

---

## Data Flow

### User Registration Flow

```
User Input (Register Page)
    ↓
Validation (email, password length)
    ↓
Check email uniqueness (load_users)
    ↓
Create user record with timestamp
    ↓
Save to users_db.json
    ↓
Show success message
    ↓
Redirect to login page
```

### User Login Flow

```
User Input (Login Page)
    ↓
load_users() from JSON
    ↓
Verify email exists
    ↓
Verify password matches
    ↓
Set session_state.authenticated = True
    ↓
Store user_email and user_name
    ↓
Show dashboard page
```

### Resume Analysis Flow

```
User uploads PDF + enters Job Description
    ↓
extract_text(pdf) → resume content
    ↓
extract_skills(resume_text) → found skills
    ↓
Tokenize job description → jd_skills
    ↓
ml_ats_score(resume, jd) → score 0-100
    ↓
skill_gap(found, required) → match analysis
    ↓
Get recommendations for missing skills
    ↓
Format and display results in UI
    ↓
Store in session_state
    ↓
increment_analyses(user_email)
```

### Visualization Pipeline

```
Analyzed Data (scores, skills, times)
    ↓
Format for Plotly
    ↓
Configure dark theme colors
    ↓
Generate interactive charts
    ↓
Render in Streamlit columns
    ↓
User can hover for details
```

---

## API Reference

### Streamlit Functions Used

```python
# Page & Layout
st.set_page_config()        # Configure page title, icon
st.sidebar                  # Sidebar navigation
st.columns()               # Multi-column layouts
st.tabs()                  # Tabbed interfaces
st.expander()              # Expandable sections

# Input Components
st.text_input()            # Text input field
st.text_area()             # Multi-line text
st.file_uploader()         # File upload widget
st.button()                # Clickable button
st.checkbox()              # Checkbox input
st.selectbox()             # Dropdown selection

# Display Components
st.markdown()              # Custom HTML with unsafe_allow_html
st.metric()                # Metric card display
st.dataframe()             # Table display
st.write()                 # General output

# State Management
st.session_state           # Persistent session variables
st.session_state.clear()   # Clear all session data

# Other
st.success()               # Success message
st.error()                 # Error message
st.warning()               # Warning message
st.info()                  # Info message
```

### External Libraries

```python
# PDF Processing
from PyPDF2 import PdfReader

# Data Processing
import pandas as pd
import numpy as np

# Machine Learning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Visualization
import plotly.express as px

# Date/Time
from datetime import datetime

# File System
import os
import json
```

---

## Database Schema

### users_db.json

```json
{
  "email@example.com": {
    "password": "userpassword (plaintext - ⚠️ TODO: Hash)",
    "full_name": "John Doe",
    "created_at": "2025-02-28 10:30:45",
    "analyses": 5
  }
}
```

**Limitations & Future Enhancements**:

- ⚠️ Passwords stored in plaintext (security risk)
- ⚠️ No encryption at rest
- ⚠️ No backup mechanism
- 🔄 Should migrate to PostgreSQL/MongoDB
- 🔄 Implement bcrypt hashing
- 🔄 Add audit logging
- 🔄 Implement database transactions

### Session State (In-Memory)

```python
st.session_state = {
    'authenticated': False,        # bool
    'user_email': '',             # str
    'user_name': '',              # str
    'scores': {                   # dict
        'ats_score': 85.5,
        'match_percentage': 72.0
    },
    'skills': {                   # dict
        'matched': [],
        'missing': [],
        'all_found': []
    },
    'times': [1.23, 0.45, 2.10]  # list of floats
}
```

**Note**: Session state is cleared on page refresh. Use user_db.json for persistence.

---

## Authentication Flow

### User Journey

```
START
  │
  ├─→ Anonymous?
  │    ├─→ No existing account?
  │    │    └─→ REGISTER PAGE
  │    │         ├─ Enter name, email, password
  │    │         ├─ Accept terms
  │    │         └─→ Save to users_db.json
  │    │              └─→ Redirect to LOGIN
  │    │
  │    └─→ Have account?
  │         └─→ LOGIN PAGE
  │              ├─ Enter email, password
  │              ├─ Click "Sign In"
  │              └─→ Verify credentials
  │
  └─→ Authenticated ✓
       │
       ├─→ MAIN APP
       │    ├─ Dashboard (metrics & charts)
       │    ├─ Resume Analyzer (upload & analyze)
       │    ├─ Skill Gap Analysis
       │    ├─ Resume Ranking
       │    └─ Settings (account, logout, clear data)
       │
       └─→ Logout
            └─→ Clear session_state
             └─→ Return to LOGIN PAGE
```

### Session State Transitions

```
Initial Load:
  → session_state = {authenticated: False}
  → Show login_page()

Register → (email not found, password valid):
  → Create user in users_db.json
  → Show success message
  → Stay on register_page()

Login → (credentials valid):
  → Set authenticated = True
  → Store user_email and user_name
  → Show sidebar + main pages

Logout (from settings):
  → Set authenticated = False
  → Clear all session data
  → Show login_page()
```

---

## Extension Guide

### Adding New Skills

**File**: `skills.py`

```python
SKILLS = {
    'Programming Languages': [
        'Python',
        'Java',
        'NewSkill',  # Add here
    ]
}
```

### Adding New Learning Resources

**File**: `recommendations.py`

```python
LEARNING_RESOURCES = {
    'NewSkill': [
        'Udemy: Course Name - https://course-link',
        'Official Documentation - https://docs-link',
        'Practice: LeetCode - https://leetcode.com'
    ]
}
```

### Adding New Dashboard Widget

**File**: `app.py` in `dashboard_page()`

```python
def dashboard_page():
    st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">📊</div>
            <div class="metric-value">42</div>
            <div class="metric-label">New Metric</div>
        </div>
    """, unsafe_allow_html=True)
```

### Adding New Analysis Function

**File**: `resume_analyzer.py`

```python
def new_analysis_function(resume_text: str, jd_text: str) -> dict:
    """
    Description of your new analysis

    Args:
        resume_text: Resume content
        jd_text: Job description

    Returns:
        dict: Results
    """
    # Your implementation
    return results
```

Then use in `app.py`:

```python
from resume_analyzer import new_analysis_function

# In analyzer_page()
results = new_analysis_function(resume_text, jd_text)
```

### Adding Database Integration (Future)

**Replace JSON with PostgreSQL**:

```python
import psycopg2

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def query_users():
    with psycopg2.connect(**DB_CONFIG) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
```

### Custom Theme Extension

**File**: `app.py` in `inject_custom_css()`

```python
def inject_custom_css():
    st.markdown("""
    <style>
    /* Add your custom CSS here */
    .custom-class {
        background: linear-gradient(135deg, #color1, #color2);
        /* More styles */
    }
    </style>
    """, unsafe_allow_html=True)
```

---

## Performance Optimization

### Current Performance Metrics

```
Page Load Time:     0.5-1.5 seconds
PDF Processing:     0.5-3.0 seconds (depends on PDF size)
ML Analysis:        0.3-1.0 seconds
Chart Rendering:    0.2-0.5 seconds
Overall UX:         Fast and responsive
```

### Optimization Strategies

#### 1. Caching

```python
@st.cache_data
def extract_text(pdf_file):
    # Expensive operation cached
    pass

@st.cache_resource
def load_skill_models():
    # Load ML models once
    pass
```

#### 2. Lazy Loading

```python
# Only process when user clicks "Analyze"
if st.button('🔍 Analyze Resume'):
    with st.spinner('⏳ Analyzing...'):
        results = analyze_resume(pdf_content, jd_content)
```

#### 3. Vectorization

```python
# Use vectorized operations
import numpy as np
scores = np.array(scores)  # Better performance
means = scores.mean()      # Vectorized calculation
```

#### 4. Database Indexing (Future)

```sql
-- When migrating to PostgreSQL
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_created_at ON users(created_at);
```

### Memory Management

```python
# Clear large datasets after use
del pdf_content
gc.collect()

# Use generators for large datasets
def load_users_generator():
    for record in users_db:
        yield record
```

---

## Deployment

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run application
streamlit run app.py

# 3. Open browser
# http://localhost:8501
```

### Environment Variables (Future)

Create `.env` file:

```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key-here
```

### Docker Deployment (Advanced)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

### Cloud Deployment (Streamlit Cloud)

```bash
# 1. Push code to GitHub
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main

# 2. Go to share.streamlit.io
# 3. Connect GitHub repository
# 4. Deploy!
```

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: "PDF Not Readable"

**Cause**: Encrypted or corrupt PDF

**Solution**:

```python
try:
    pdf_reader = PdfReader(pdf_file)
except Exception as e:
    st.error(f"❌ Error reading PDF: {str(e)}")
    st.stop()
```

#### Issue: "Users DB Missing"

**Cause**: users_db.json not created

**Solution**:

```python
# auth_system.py handles creation
if not os.path.exists('users_db.json'):
    save_users({})  # Create empty DB
```

#### Issue: "Session State Lost"

**Cause**: Page refresh clears session

**Solution**: Use persistent storage

```python
# Store in users_db.json or database
def save_analysis(email, analysis_data):
    # Save to database
    pass
```

#### Issue: "Slow Performance"

**Cause**: Missing caching or large datasets

**Solution**:

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def expensive_function(param):
    # Your code
    return result
```

#### Issue: "Connection Errors"

**Cause**: Database connection issues

**Solution**:

```python
try:
    # Database operation
except psycopg2.OperationalError as e:
    st.error("🔴 Database connection failed")
    st.stop()
```

### Debug Mode

```python
# Enable debug logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.debug("Debug message here")
```

### Testing

```python
# Unit test example
import pytest

def test_ml_ats_score():
    resume = "Python, JavaScript, SQL"
    jd = "Python and SQL required"
    score = ml_ats_score(resume, jd)
    assert 0 <= score <= 100
    assert isinstance(score, float)

pytest.main(['test_functions.py', '-v'])
```

---

## Security Considerations

### Current Implementation ⚠️

- ✅ Session-based authentication
- ✅ User data isolation
- ❌ **Plaintext passwords** (security risk)
- ❌ No input validation
- ❌ No CSRF protection
- ❌ No rate limiting
- ❌ No audit logging

### Recommended Enhancements 🔒

```python
# 1. Password Hashing
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hash):
    return bcrypt.checkpw(password.encode(), hash)

# 2. Input Validation
import re

def validate_email(email):
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(pattern, email) is not None

# 3. Rate Limiting
from streamlit_rate_limit import limit

@limit(calls=5, period=60)  # 5 calls per minute
def login_attempt(email, password):
    pass

# 4. HTTPS Only (production)
# Enforce HTTPS connections
```

### Data Privacy

```python
# Don't log sensitive data
logger.debug(f"Login: {email}, password: {password}")  # ❌ WRONG
logger.debug(f"Login attempt for: {email}")  # ✅ RIGHT

# Clear sensitive data
password = None
gc.collect()

# GDPR compliance
def delete_user_data(email):
    """Remove user and all their analyses"""
    pass
```

---

## Future Roadmap

### Version 4.0 Features

- [ ] Database migration (PostgreSQL/MongoDB)
- [ ] Password hashing (bcrypt)
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Two-factor authentication (2FA)
- [ ] Team workspaces
- [ ] Batch resume upload (5-100 at once)
- [ ] Email report generation
- [ ] Advanced filtering and search
- [ ] Resume template builder
- [ ] Interview preparation mode
- [ ] Salary predictor
- [ ] Job market analytics
- [ ] Custom domain hosting
- [ ] REST API

### Long-term Vision (v5.0+)

- Mobile app (React Native)
- AI-powered interview coaching
- Real-time collaboration
- Browser extension
- Job board integration
- Career path visualization
- Network recommendations
- Industry benchmarking

---

## Support & Resources

### Getting Help

1. **Check Documentation**: Read this file & README.md
2. **Review Code**: Inspect relevant module
3. **Enable Debug**: Run with logging enabled
4. **Search Issues**: Check GitHub/documentation
5. **Contact Support**: Create issue or discussion

### Useful Links

- [Streamlit Docs](https://docs.streamlit.io)
- [scikit-learn ML Guide](https://scikit-learn.org)
- [Plotly Charts](https://plotly.com/python)
- [PyPDF2 Guide](https://pypdf2.readthedocs.io)
- [Python Best Practices](https://pep8.org)

---

**Documentation Version**: 3.0  
**Last Updated**: February 28, 2025  
**Status**: Complete & Ready for Implementation
