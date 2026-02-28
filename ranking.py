def rank_resumes(resume_scores):
    sorted_resumes = sorted(
        resume_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return sorted_resumes