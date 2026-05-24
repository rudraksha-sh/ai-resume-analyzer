def calculate_ats_score(skills):

    score = 0

    score += min(len(skills) * 10, 60)

    return min(score, 100)