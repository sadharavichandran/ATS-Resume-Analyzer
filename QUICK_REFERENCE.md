# ATS Resume Analyzer - Quick Reference Guide

## 🚀 Running the Application

### Start the App

```bash
cd "c:\Users\HP\Downloads\files (6)"
python -m streamlit run app.py
```

The app will open at: **http://localhost:8501**

### Stop the App

Press `Ctrl+C` in the terminal

## 📋 Navigation Menu

### 1. **Dashboard** 🎯

- Overview of all analyses
- Key metrics with trends
- Monthly application trends
- Top 10 skills distribution
- Demo mode banner with feature info

### 2. **Resume Analyzer** 📄

- Upload candidate resume (PDF)
- Paste job description
- Get instant ATS compatibility score
- View detected skills
- See skill gaps with recommendations
- **3 Tabs**:
  - Score & Skills: ATS percentage + skill list
  - Match Analysis: Matching vs missing skills
  - Recommendations: Learning resources for gaps

### 3. **Skill Gap & Recommendation** ⚠️

- Input job description for analysis
- Compare with last analyzed resume
- View metrics:
  - Candidate Skills count
  - Matching skills
  - Missing skills
- Get detailed learning paths for each skill
- Links to courses and resources

### 4. **Resume Ranking** 🏆

- View all analyzed candidates
- Sorted by ATS score (highest first)
- Visual metrics:
  - Top candidate highlight
  - Total candidates count
- Bar chart showing score distribution
- Download results as CSV file

### 5. **Settings** ⚙️

- Clear all session data
- Reset metrics
- Start fresh analysis

## 💾 Data Management

### Session Storage

- **Scores**: Candidate names & ATS scores
- **Skills**: All detected skills from all resumes
- **Times**: Processing duration for each analysis
- **Last Skills**: Skills from most recent resume
- **JD Skills**: Skills extracted from job description
- **Resume Skills**: Current resume's skills

### Clear Data

Go to Settings → Click "Clear all data" button

## 📊 Dashboard Widgets

| Widget               | Purpose                   | Auto-Update |
| -------------------- | ------------------------- | ----------- |
| Total Resumes        | Count of analyzed resumes | Yes         |
| Analyzed Candidates  | Number of candidates      | Yes         |
| Avg. Match Score     | Average ATS score         | Yes         |
| Avg. Processing Time | Average analysis time     | Yes         |
| Monthly Applications | Trend line chart          | Yes         |
| Top Skills Detected  | Bar chart of skills       | Yes         |

## 🎓 Skill Categories (70+ Skills)

### Programming Languages

python, java, javascript, c, c++, typescript, go, rust, kotlin

### Web Development

html, css, react, angular, vue, node, express, django, flask, fastapi, graphql, rest, api

### Databases

sql, mysql, postgresql, mongodb, firebase, redis, cassandra

### Data Science & ML

machine learning, deep learning, tensorflow, pytorch, sklearn, pandas, numpy, matplotlib, seaborn, nlp

### DevOps & Cloud

docker, kubernetes, aws, azure, gcp, terraform, jenkins, git, linux, bash, powershell

### Testing & Tools

pytest, junit, and others

### Soft Skills

agile, scrum, leadership, communication, teamwork

## 📚 Learning Resources

Each skill includes:

- **Recommended Online Courses**: Udemy, Coursera, FastAI, Scrimba
- **Official Documentation**: Primary resources
- **Practice Platforms**: HackerRank, LeetCode, Kaggle
- **Certifications**: AWS, Azure, GCP pathways
- **Hands-On Projects**: Real-world applications

### Examples:

- **Python**: Udemy: Complete Python & OOP
- **React**: Scrimba React course + Build projects
- **AWS**: AWS Architect Associate certification path
- **Machine Learning**: Andrew Ng's ML Course on Coursera

## ⚡ Keyboard Shortcuts (Streamlit)

| Action        | Shortcut |
| ------------- | -------- |
| Rerun         | `R`      |
| Clear Cache   | `C`      |
| Open Settings | `K`      |
| Open Help     | `F1`     |

## 🐛 Troubleshooting

### App won't start

```bash
# Check Python availability
python --version

# Install streamlit if missing
pip install streamlit
```

### PDF upload not working

- Ensure PDF file is valid
- Try a different PDF file
- Check file size (must be readable)

### Charts not displaying

- Refresh browser (F5)
- Check if plotly is installed: `pip install plotly`

### Session data lost

- Browser refresh clears session
- Use "Clear all data" button sparingly

## 📈 Performance Tips

1. **Faster Processing**: Keep resumes under 5 pages
2. **Better Results**: Detailed job descriptions improve accuracy
3. **Skill Detection**: Use standard skill names (e.g., "Python", "React")
4. **Export Data**: Download rankings regularly to avoid data loss

## 📞 Support

For issues:

1. Check the demo mode banner on Dashboard
2. Review ENHANCEMENTS.md for feature details
3. Check CODE_CHANGES.md for technical info
4. Verify all dependencies: `pip install -r requirements.txt`

## 📝 File Structure

```
c:\Users\HP\Downloads\files (6)\
├── app.py                    # Main application (Streamlit UI)
├── resume_analyzer.py        # ML analysis logic
├── recommendations.py        # Learning paths database
├── skills.py                 # Skills database (70+ skills)
├── auth.py                   # Authentication utilities
├── database.py               # Database operations
├── ranking.py                # Ranking logic
├── requirements.txt          # Python dependencies
├── ENHANCEMENTS.md          # Feature enhancements doc
├── CODE_CHANGES.md          # Code changes summary
└── assets/                   # UI assets (if any)
```

## 🔄 Update Schedule

- Skills: Updated regularly (currently 70+ skills)
- Recommendations: Course links verified monthly
- UI: Streamlined for better UX
- Features: Continuously enhanced

---

**Version**: 2.0  
**Last Updated**: February 2026  
**Status**: Ready for Production  
**Deployment**: Local (localhost:8501)
