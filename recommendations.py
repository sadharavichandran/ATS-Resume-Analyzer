RECOMMENDATIONS = {
    # Programming Languages
    "python": "Master Python fundamentals | Udemy: Complete Python & OOP",
    "javascript": "Learn JS interactively | Codecademy + LeetCode coding challenges",
    "java": "Java development path | Udemy: Complete Java Masterclass",
    "typescript": "TypeScript deep dive | Official TypeScript Handbook & practice",
    "go": "Go programming basics | A Tour of Go + Build projects",
    "rust": "Systems programming | The Rust Book + RustByExample",
    "kotlin": "Kotlin for Android | Google's Kotlin Bootcamp course",
    "c": "C fundamentals | Tutorialspoint + competitive programming",
    "c++": "C++ mastery | LeetCode C++ problems + Design patterns",
    
    # Web Frameworks
    "react": "Learn React professionally | Scrimba React course + Build projects",
    "angular": "Angular framework course | Official Angular tutorials",
    "vue": "Vue.js progression | Vue University + Build real apps",
    "express": "Node.js backend with Express | Build REST APIs",
    "django": "Django web development | Django for Beginners book",
    "flask": "Flask microframework | Miguel Grinberg's Flask Mega-Tutorial",
    "fastapi": "Modern FastAPI development | Official FastAPI + real projects",
    "rest": "RESTful architecture | Design patterns & best practices",
    "graphql": "GraphQL API design | How to GraphQL tutorial",
    "api": "API development excellence | API design patterns & security",
    
    # Databases
    "sql": "SQL mastery | HackerRank + Advanced SQL Tutorials",
    "mysql": "MySQL administration | Udemy MySQL courses",
    "postgresql": "PostgreSQL advanced | Official docs + PG Exercises",
    "mongodb": "NoSQL with MongoDB | Udemy MongoDB courses",
    "redis": "Redis caching | Redis documentation + Real-world patterns",
    "firebase": "Firebase development | Official Firebase docs + Codelab",
    "cassandra": "Distributed DB with Cassandra | DataStax Academy",
    
    # Data Science & ML
    "machine learning": "ML fundamentals | Andrew Ng's ML Course on Coursera",
    "deep learning": "Deep Learning mastery | Fast.ai or Udacity Deep Learning",
    "tensorflow": "TensorFlow techniques | Official TensorFlow tutorials",
    "pytorch": "PyTorch learning | PyTorch tutorials + practical projects",
    "sklearn": "Scikit-learn proficiency | Official docs + Kaggle competitions",
    "data analysis": "Analytics skills | DataCamp or Mode Analytics SQL",
    "pandas": "Pandas data manipulation | Pandas documentation + Projects",
    "numpy": "NumPy numerical computing | NumPy docs + exercises",
    "matplotlib": "Visualization with Matplotlib | Gallery + practice",
    "seaborn": "Statistical visualization | Seaborn docs + tutorials",
    "nlp": "Natural Language Processing | Hugging Face + NLP tutorials",
    
    # DevOps & Cloud
    "docker": "Docker containerization | Docker docs + Udemy courses",
    "kubernetes": "Kubernetes orchestration | Kubernetes official tutorials",
    "aws": "AWS cloud services | AWS Architect Associate certification path",
    "azure": "Microsoft Azure | AZ-900 certification + hands-on labs",
    "gcp": "Google Cloud Platform | Google Cloud skills boost",
    "terraform": "Infrastructure as Code | Terraform documentation + projects",
    "jenkins": "CI/CD with Jenkins | Jenkins tutorials + pipelines",
    "git": "Version control mastery | Pro Git book + GitHub learning",
    
    # System & Tools
    "linux": "Linux administration | Linux Academy or Udemy courses",
    "bash": "Bash scripting excellence | BASH Academy + automation",
    "powershell": "PowerShell scripting | Microsoft documentation",
    "pytest": "Python testing | Pytest documentation + Real-world examples",
    "junit": "Java testing framework | JUnit 4/5 documentation",
    
    # Frontend
    "html": "HTML5 semantics | MDN Web Docs tutorials",
    "css": "CSS expertise | CSS Tricks + Layout practices",
    
    # Soft Skills
    "agile": "Agile methodology | Agile manifesto + Scrum Master certification",
    "scrum": "Scrum mastery | Scrum.org + Team leadership",
    "leadership": "Leadership development | Coursera leadership courses",
    "communication": "Communication skills | Toastmasters + public speaking",
    "teamwork": "Team collaboration | Group projects + mentoring"
}

def get_recommendations(missing_skills):
    return {skill: RECOMMENDATIONS.get(skill, "Learn fundamentals using Udemy, Coursera, or official documentation")
            for skill in missing_skills}
