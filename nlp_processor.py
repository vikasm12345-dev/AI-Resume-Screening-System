import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)


SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "php",
        "ruby", "go", "rust", "swift", "kotlin", "r", "sql", "html", "css"
    ],

    "Web Development": [
        "react", "angular", "vue", "node.js", "nodejs", "express", "django",
        "flask", "fastapi", "spring boot", "laravel", "bootstrap", "tailwind",
        "rest api", "graphql", "frontend", "backend", "full stack"
    ],

    "Data Science / AI": [
        "machine learning", "deep learning", "artificial intelligence", "ai",
        "data science", "data analysis", "nlp", "natural language processing",
        "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
        "sklearn", "pandas", "numpy", "matplotlib", "seaborn", "opencv",
        "statistics", "regression", "classification", "clustering",
        "xgboost", "bert", "transformers", "llm"
    ],

    "Cloud / DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "jenkins", "git", "github", "gitlab", "linux", "ci/cd",
        "terraform", "ansible", "microservices"
    ],

    "Databases": [
        "mysql", "postgresql", "mongodb", "redis", "oracle", "sqlite",
        "sql server", "firebase", "dynamodb", "database", "nosql"
    ],

    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "project management", "agile", "scrum",
        "collaboration", "time management", "presentation"
    ]
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess_text(text):
    text = clean_text(text)
    words = text.split()

    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    processed_words = []

    for word in words:
        if word not in stop_words and len(word) > 1:
            processed_words.append(lemmatizer.lemmatize(word))

    return " ".join(processed_words)


def extract_skills(text):
    text = clean_text(text)
    found_skills = {}

    for category, skills in SKILL_CATEGORIES.items():
        matched_skills = []

        for skill in skills:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, text):
                matched_skills.append(skill)

        if matched_skills:
            found_skills[category] = sorted(list(set(matched_skills)))

    return found_skills


def extract_experience(text):
    text = text.lower()

    patterns = [
        r"(\d+)\+?\s+years?\s+of\s+experience",
        r"(\d+)\+?\s+years?\s+experience",
        r"experience\s+of\s+(\d+)\+?\s+years?",
        r"(\d+)\+?\s+yrs?\s+experience"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1) + "+ years"

    return "Not specified"


def extract_education(text):
    education_keywords = [
        "bachelor", "master", "phd", "doctorate", "b.tech", "m.tech",
        "b.sc", "m.sc", "bca", "mca", "computer science", "engineering",
        "information technology", "data science", "mba"
    ]

    text = text.lower()
    found = []

    for keyword in education_keywords:
        if keyword in text:
            found.append(keyword)

    return sorted(list(set(found)))