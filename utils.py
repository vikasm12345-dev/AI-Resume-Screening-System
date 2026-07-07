"""
🔧 Utility Functions
Helper functions for the application
"""

import pandas as pd


def get_score_color(score: float) -> str:
    """Return color based on score value."""
    if score >= 0.75:
        return "#00C853"  # Green
    elif score >= 0.50:
        return "#FFD600"  # Yellow
    elif score >= 0.25:
        return "#FF9100"  # Orange
    else:
        return "#FF1744"  # Red


def get_score_emoji(score: float) -> str:
    """Return emoji based on score value."""
    if score >= 0.75:
        return "🟢"
    elif score >= 0.50:
        return "🟡"
    elif score >= 0.25:
        return "🟠"
    else:
        return "🔴"


def get_grade(score: float) -> str:
    """Return letter grade based on score."""
    if score >= 0.90:
        return "A+"
    elif score >= 0.80:
        return "A"
    elif score >= 0.70:
        return "B+"
    elif score >= 0.60:
        return "B"
    elif score >= 0.50:
        return "C+"
    elif score >= 0.40:
        return "C"
    elif score >= 0.30:
        return "D"
    else:
        return "F"


def create_ranking_dataframe(rankings: list) -> pd.DataFrame:
    """Convert rankings to a pandas DataFrame for display."""
    data = []
    for r in rankings:
        data.append({
            "Rank": f"#{r['rank']}",
            "Resume": r['name'],
            "Overall Score": f"{r['combined_score'] * 100:.1f}%",
            "Content Match": f"{r['tfidf_score'] * 100:.1f}%",
            "Skill Match": f"{r['skill_match']['score'] * 100:.1f}%",
            "Matched Skills": len(r['skill_match']['matched_skills']),
            "Missing Skills": len(r['skill_match']['missing_skills']),
            "Grade": get_grade(r['combined_score'])
        })
    return pd.DataFrame(data)


def format_skill_list(skills: list) -> str:
    """Format a list of skills as styled tags."""
    if not skills:
        return "<em>None</em>"
    tags = ""
    for skill in skills:
        tags += f'<span style="background: rgba(255,255,255,0.15); padding: 3px 10px; border-radius: 15px; margin: 2px 4px; display: inline-block; font-size: 0.85em;">{skill}</span>'
    return tags