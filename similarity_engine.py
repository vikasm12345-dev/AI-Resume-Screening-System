from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp_processor import preprocess_text, extract_skills, SKILL_CATEGORIES


def compute_tfidf_similarity(job_description, resume_texts):
    processed_job = preprocess_text(job_description)
    processed_resumes = [preprocess_text(text) for text in resume_texts]

    all_texts = [processed_job] + processed_resumes

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        lowercase=True
    )

    tfidf_matrix = vectorizer.fit_transform(all_texts)

    job_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    scores = cosine_similarity(job_vector, resume_vectors).flatten()

    return scores.tolist()


def flatten_skills(skill_dict):
    skills = set()

    for skill_list in skill_dict.values():
        for skill in skill_list:
            skills.add(skill)

    return skills


def compute_skill_match_score(job_description, resume_text):
    job_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    job_skill_set = flatten_skills(job_skills)
    resume_skill_set = flatten_skills(resume_skills)

    if len(job_skill_set) == 0:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "extra_skills": sorted(list(resume_skill_set))
        }

    matched_skills = job_skill_set.intersection(resume_skill_set)
    missing_skills = job_skill_set.difference(resume_skill_set)
    extra_skills = resume_skill_set.difference(job_skill_set)

    score = len(matched_skills) / len(job_skill_set)

    return {
        "score": round(score, 4),
        "matched_skills": sorted(list(matched_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "extra_skills": sorted(list(extra_skills))
    }


def compute_category_scores(job_description, resume_text):
    job_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    category_scores = {}

    for category in SKILL_CATEGORIES.keys():
        required = set(job_skills.get(category, []))
        available = set(resume_skills.get(category, []))

        if len(required) > 0:
            matched = required.intersection(available)
            score = len(matched) / len(required)

            category_scores[category] = {
                "score": round(score, 4),
                "matched": sorted(list(matched)),
                "required": sorted(list(required)),
                "total_required": len(required),
                "total_matched": len(matched)
            }

    return category_scores


def rank_resumes(job_description, resumes, tfidf_weight=0.4, skill_weight=0.6):
    resume_texts = [resume["text"] for resume in resumes]
    tfidf_scores = compute_tfidf_similarity(job_description, resume_texts)

    results = []

    for index, resume in enumerate(resumes):
        skill_match = compute_skill_match_score(job_description, resume["text"])
        category_scores = compute_category_scores(job_description, resume["text"])

        combined_score = (
            tfidf_weight * tfidf_scores[index]
            + skill_weight * skill_match["score"]
        )

        results.append({
            "rank": 0,
            "name": resume["name"],
            "combined_score": round(combined_score, 4),
            "tfidf_score": round(tfidf_scores[index], 4),
            "skill_match": skill_match,
            "category_scores": category_scores,
            "preview": resume["text"][:400]
        })

    results.sort(key=lambda item: item["combined_score"], reverse=True)

    for i, result in enumerate(results):
        result["rank"] = i + 1

    return results