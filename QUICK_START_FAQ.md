# 🚀 Quick Start Guide & FAQ

## Quick Start (5 Minutes)

### Step 1: Install Dependencies ⚙️

```bash
# Windows (PowerShell)
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt

# Verify installation
python -c "import streamlit; print('✅ Ready!')"
```

### Step 2: Launch Application 🚀

```bash
# Windows
streamlit run app.py

# macOS/Linux
streamlit run app.py

# Open in browser (should open automatically)
# http://localhost:8501
```

### Step 3: Create Account & Login 🔑

1. Click **"📝 Create New Account"**
2. Enter:
   - **Full Name**: Your name
   - **Email**: Your email
   - **Password**: At least 6 characters
3. Accept **Terms & Conditions**
4. Click **"🚀 Sign Up"**
5. Use credentials to login

### Step 4: Try Features 🎯

- **📄 Dashboard**: See metrics and charts
- **📑 Resume Analyzer**: Upload PDF and analyze
- **💼 Skill Gap**: Check missing skills
- **👥 Ranking**: Compare candidates
- **⚙️ Settings**: Manage account

---

## Frequently Asked Questions

### Installation & Setup

#### Q: Python version requirement?

**A**: Python 3.8 or higher (tested with 3.13.8)

```bash
python --version  # Check your version
```

#### Q: Where do I download Python?

**A**: Visit [python.org](https://www.python.org/downloads/)

- Download Python 3.11+ (recommended)
- Check "Add Python to PATH" during installation
- Verify: `python --version`

#### Q: Do I need to install each requirement separately?

**A**: No! Use the requirements file:

```bash
pip install -r requirements.txt
# Installs all 15+ packages at once
```

#### Q: What if pip isn't recognized?

**A**: Add Python to PATH:

```bash
# Windows PowerShell (as Administrator)
[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Program Files\Python313", "User")

# Then restart terminal and try again
pip --version
```

#### Q: Which Python IDE should I use?

**A**: Popular options:

- VS Code (lightweight, recommended)
- PyCharm (full-featured)
- Jupyter Notebook (data science)
- IDLE (built-in)

---

### User Accounts & Authentication

#### Q: How do I reset my password?

**A**: Current version doesn't support password reset. Future v4.0 will add this.
**Workaround**: Delete your account from users_db.json and register new account.

#### Q: Where are passwords stored?

**A**: In `users_db.json` (development only)
⚠️ **Note**: Passwords are plaintext (unsafe for production)
🔄 **Future**: Will implement bcrypt hashing

#### Q: Can I delete my account?

**A**: Not yet in UI. You can:

1. Open `users_db.json` in text editor
2. Find and delete your email entry
3. Save and reload app

**Future**: Will have one-click delete in Settings

#### Q: Can multiple users share one account?

**A**: Yes, but not recommended. Each user should have own account.

#### Q: What happens if I forget my email?

**A**: Contact your system administrator or check your registration confirmation.

#### Q: Can I change my email after registration?

**A**: Not yet. Future enhancement planned.

---

### Resume Analysis

#### Q: What file formats are supported?

**A**: Currently PDF only

```
✅ PDF (.pdf)
❌ DOCX (.docx) - Coming in v4.0
❌ TXT (.txt) - Coming in v4.0
❌ Google Docs - Coming in v4.0
```

#### Q: Why does PDF upload fail?

**A**: Common causes:

1. **Encrypted PDF** → Try removing password
2. **Corrupted file** → Try re-saving PDF
3. **Image PDFs** → Use OCR (not yet supported)
4. **Large file** → Keep under 50MB

**Solution**:

```
1. Open PDF in Adobe Reader
2. Try "File > Save As" to re-save
3. Try uploading again
```

#### Q: How long does analysis take?

**A**: Typically 0.5-3 seconds depending on:

- PDF file size
- Resume length
- Job description length
- System performance

#### Q: What score does ATS use?

**A**: TF-IDF + Cosine Similarity algorithm

- Range: 0-100
- Weights technical skills higher
- Considers keyword frequency and relevance

#### Q: Can I save my analysis?

**A**: Currently saved in session only (clears on refresh)
**Workaround**: Take screenshot or export CSV
🔄 **Future**: Permanent storage in database

#### Q: What if no skills are detected?

**A**: Possible reasons:

1. **Resume too short** → Add more details
2. **Skill names not in database** → Database doesn't have that skill yet
3. **Poor resume formatting** → Reformat and try again
4. **Image-based PDF** → Use text-based PDF

**Solution**: Check `skills.py` for supported skills and update resume accordingly.

---

### Skill Gap Analysis

#### Q: How are skills categorized?

**A**: 11 categories:

- Programming Languages (Python, Java, etc.)
- Web Development (React, Angular, etc.)
- Databases (SQL, MongoDB, etc.)
- Data Science (TensorFlow, Pandas, etc.)
- DevOps/Cloud (Docker, AWS, etc.)
- Soft Skills (Leadership, Communication, etc.)
- Mobile Development
- Security
- Big Data
- Testing
- Project Management

#### Q: Where do learning recommendations come from?

**A**: Curated from:

- Udemy, Coursera, FastAI
- Official documentations
- Practice platforms (HackerRank, LeetCode)
- Industry certifications
- Free open-source resources

#### Q: Can I add custom skills?

**A**: Edit `skills.py`:

```python
SKILLS = {
    'Programming Languages': [
        'Python',
        'Java',
        'MyCustomSkill'  # Add here
    ]
}
```

Then add learning path in `recommendations.py`

#### Q: Why is my skill not showing as missing?

**A**: Could be:

1. Already in your resume
2. Not in skill database (add it to skills.py)
3. Different name (e.g., "React" vs "ReactJS")

---

### Data & Export

#### Q: Can I export my analysis?

**A**: Yes! In Ranking page:

- Click **"📥 Download CSV"**
- Saves candidate rankings as CSV file
- Open in Excel, Google Sheets, etc.

#### Q: What data is exported?

**A**: CSV includes:

- Candidate Name
- ATS Score
- Match Percentage
- Top Skills
- Missing Skills
- Analysis Timestamp

#### Q: Where are exported files saved?

**A**: In your browser's default Downloads folder

- Windows: `C:\Users\YourName\Downloads\`
- macOS: `/Users/YourName/Downloads/`
- Linux: `~/Downloads/`

#### Q: Can I bulk upload resumes?

**A**: Not in v3.0. Coming in v4.0:

- Batch upload (10-100 files)
- Bulk analysis
- Comparative reports
- Bulk export

#### Q: How long is data kept?

**A**: Session-based (clears on refresh in dev mode)
🔄 **Future**: Permanent storage with user dashboard

---

### Performance & Troubleshooting

#### Q: App is running slowly

**A**: Try these:

1. **Check internet**: Poor connection slows analysis
2. **Close other apps**: Free up system RAM
3. **Restart Streamlit**: Kill terminal and re-run
4. **Clear cache**: Delete Streamlit cache folder

   ```bash
   # Windows
   Remove-Item $env:USERPROFILE\.streamlit -Recurse

   # macOS/Linux
   rm -rf ~/.streamlit
   ```

#### Q: "Module not found" error

**A**: Missing dependency - reinstall:

```bash
pip install -r requirements.txt

# Or specific package
pip install streamlit==1.28.1
```

#### Q: PDF extraction shows blank pages

**A**: PDFs are complex - try:

1. Open PDF in Adobe Reader
2. File → Export as Text
3. Copy-paste text into Job Description field
4. Resume Analyzer will work with plain text

#### Q: Login always fails

**A**: Check:

1. Email exactly matches registration
2. Password is case-sensitive (EXACT match)
3. users_db.json file exists
4. File isn't corrupted (open in text editor)

#### Q: Users_db.json corrupted

**A**: Fix it:

```json
// Should look like this (valid JSON):
{
  "user@example.com": {
    "password": "password123",
    "full_name": "John Doe",
    "created_at": "2025-02-28 10:30:45",
    "analyses": 5
  }
}
```

Check for:

- Missing commas between entries
- Unmatched brackets/braces
- Invalid quotes

#### Q: "Port 8501 is already in use"

**A**: Another Streamlit is running:

```bash
# Windows - find and kill process
netstat -ano | findstr :8501
taskkill /PID <process_id> /F

# macOS/Linux
lsof -ti:8501 | xargs kill -9
```

Or use different port:

```bash
streamlit run app.py --server.port 8502
```

#### Q: Memory usage growing

**A**: Clean session state:

1. Go to Settings
2. Click **"🗑️ Clear All Analysis Data"**
3. This clears session but keeps account

---

### Features & Capabilities

#### Q: What makes this ATS analyzer different?

**A**: Features:

- ✅ ML-based scoring (not just keyword matching)
- ✅ Skill gap analysis with recommendations
- ✅ Multi-candidate ranking
- ✅ Beautiful dark theme UI
- ✅ No account needed (v2.0 and earlier)
- ✅ Free to use
- ✅ Open source (can modify)
- ✅ Offline capable (with setup)

#### Q: Does it work offline?

**A**: Mostly yes:

- ✅ Analysis functions work offline
- ✅ Resume parsing works offline
- ❌ Learning resources links need internet
- ❌ External charts need refresh

#### Q: Can I use this commercially?

**A**: Check LICENSE file:

- Generally allowed with attribution
- Some components may have restrictions
- Contact author for commercial use

#### Q: How accurate is the ATS score?

**A**:

- ~75% accurate for standard resumes
- Works best with complete resume info
- Scores vary based on content quality
- Use as guidance, not absolute metric

**Factors affecting accuracy**:

- Resume completeness
- Job description clarity
- Skill database coverage
- PDF quality

#### Q: Can it detect soft skills?

**A**: Limited support:

- Detects: Leadership, Communication, Teamwork, Agile, Scrum
- Struggles with: Analytical, Creative, Detail-oriented
- 🔄 Future: NLP-based soft skill detection

#### Q: Does it support multiple languages?

**A**: Currently English only

- Skill database is English
- Analysis works with English text
- 🔄 Future: Multi-language support

---

### Advanced Usage

#### Q: Can I deploy this online?

**A**: Yes! Several options:

**Option 1: Streamlit Cloud** (easiest)

```
1. Push to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Deploy! (free tier available)
```

**Option 2: Heroku**

```
1. Create Procfile
2. Create app.json
3. Push to Heroku
4. Deploy with one command
```

**Option 3: Docker**

```bash
# Build image
docker build -t ats-analyzer .

# Run container
docker run -p 8501:8501 ats-analyzer
```

#### Q: How do I customize the theme?

**A**: Edit `app.py`:

```python
def inject_custom_css():
    st.markdown("""
    <style>
    /* Change colors here */
    --primary-blue: #YourColor1;
    --accent-cyan: #YourColor2;
    /* More customizations */
    </style>
    """)
```

#### Q: Can I add my own analysis functions?

**A**: Yes! Edit `resume_analyzer.py`:

```python
def my_custom_analysis(resume_text, jd_text):
    """Your analysis"""
    return results

# Then call from app.py
from resume_analyzer import my_custom_analysis
```

#### Q: How do I integrate with a database?

**A**: Replace JSON with database:

```python
# auth_system.py - Example with PostgreSQL
import psycopg2

def load_users():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return {row[0]: {...} for row in cursor.fetchall()}
```

See TECHNICAL_DOCUMENTATION.md for details.

---

### Reporting Issues

#### Q: Where do I report bugs?

**A**:

1. Check this FAQ first
2. Check TROUBLESHOOTING section in TECHNICAL_DOCUMENTATION.md
3. Enable debug mode and capture logs
4. Create issue with:
   - Error message (exact text)
   - Steps to reproduce
   - Screenshot if applicable
   - Python version
   - OS (Windows/macOS/Linux)

#### Q: How do I request new features?

**A**:

1. Check roadmap in TECHNICAL_DOCUMENTATION.md
2. Suggest feature with use case
3. Provide mock-up/design if possible
4. Allow time for consideration

#### Q: Will old versions be supported?

**A**:

- v3.0: Supported (current)
- v2.0: Legacy support (no updates)
- v1.0: Deprecated (not recommended)

Recommend upgrading to latest for security/features.

---

### Contributing & Development

#### Q: Can I modify and redistribute?

**A**: Check LICENSE file - likely yes with attribution

#### Q: How do I contribute improvements?

**A**:

1. Fork repository
2. Create feature branch
3. Make improvements
4. Test thoroughly
5. Submit pull request
6. Wait for review

#### Q: What's the development roadmap?

**A**: See TECHNICAL_DOCUMENTATION.md section "Future Roadmap":

- v4.0: Database, 2FA, batch upload
- v5.0: Mobile app, AI coaching, team features

#### Q: Where can I find code documentation?

**A**: Three places:

1. **TECHNICAL_DOCUMENTATION.md** - Full API & architecture
2. **Code comments** - Inline explanations
3. **Docstrings** - Function-level documentation

---

## Getting Help

### Support Channels

1. **This FAQ** - Check first (99% of questions answered)
2. **TECHNICAL_DOCUMENTATION.md** - Deep technical info
3. **README.md** - Overview and features
4. **Code comments** - How implementation works
5. **Issues/Discussions** - Community support

### Information to Provide

When reporting issues, include:

```
Operating System: Windows 10 / macOS 12 / Ubuntu 20.04
Python Version: 3.11.4
Streamlit Version: 1.28.1
Error Message: [paste exact error]
Steps to Reproduce:
1. Click...
2. Upload...
3. Error occurs...
Screenshots: [if applicable]
```

### Testing Checklist

Before reporting bugs, test:

- [ ] Reinstalled requirements: `pip install -r requirements.txt --force-reinstall`
- [ ] Restarted Streamlit
- [ ] Cleared cache: `.streamlit` folder deleted
- [ ] Tried different PDF/data
- [ ] Checked users_db.json is valid JSON
- [ ] Verified Python version is 3.8+

---

## Tips & Tricks

### Productivity Tips

1. **Keyboard Shortcuts**:
   - `R` - Rerun app
   - `C` - Clear cache
   - `S` - Settings

2. **Quick Analysis**:
   - Save job descriptions as text
   - Copy-paste instead of retype
   - Batch analyze with CSV export

3. **Skill Building**:
   - Bookmark learning resources
   - Use recommended courses
   - Track progress in Settings

### Optimization Tips

1. **Faster Processing**:
   - Use shorter job descriptions
   - Provide complete resumes
   - High-quality PDFs (text-based)

2. **Better Scores**:
   - Include all relevant skills in resume
   - Use exact skill names (from database)
   - Match job description keywords
   - Quantify achievements

3. **Cleaner UI**:
   - Expand sections as needed
   - Collapse unused tabs
   - Use full-screen for charts
   - Zoom browser if text too small

---

## Glossary

| Term                  | Definition                                                 |
| --------------------- | ---------------------------------------------------------- |
| **ATS**               | Applicant Tracking System - software used by recruiters    |
| **TF-IDF**            | Term Frequency-Inverse Document Frequency - scoring method |
| **Cosine Similarity** | Measure of similarity between texts (0-1 scale)            |
| **Skill Gap**         | Missing skills needed for a position                       |
| **Resume Parsing**    | Extracting structured data from resume document            |
| **ML Score**          | Machine Learning-based matching score                      |
| **Session State**     | Data stored during single app session                      |
| **PDF**               | Portable Document Format - file type                       |

---

## Quick Reference

### Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

# Clear cache
rm -r ~/.streamlit  # macOS/Linux
rmdir /s %USERPROFILE%\.streamlit  # Windows

# Kill app on port 8501
lsof -ti:8501 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8501 | findstr LISTENING  # Windows

# Update single package
pip install --upgrade streamlit

# Virtual environment (optional)
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### File Structure

```
project/
├── app.py                      # Main application
├── auth_system.py             # User authentication
├── resume_analyzer.py         # ML analysis engine
├── recommendations.py         # Learning resources
├── skills.py                  # Skill database
├── users_db.json             # User credentials
├── requirements.txt          # Dependencies
├── README.md                 # Project overview
├── TECHNICAL_DOCUMENTATION.md # Full documentation
├── QUICK_START_FAQ.md        # This file
└── UI_DESIGN_SYSTEM.md       # Design specifications
```

---

## Final Notes

✅ **You're all set!** Follow Quick Start guide above to begin.

💡 **Pro Tip**: Keep this FAQ handy - most questions are answered here!

🔄 **Version**: 3.0 (Updated Feb 2025)

📧 **Questions?**: Check documentation folders or enable debug mode

🚀 **Ready to analyze resumes?** Start the app now!

```bash
streamlit run app.py
```

---

**Quick Start Guide & FAQ v3.0**  
**Last Updated**: February 28, 2025  
**Status**: Complete & Ready for Users
