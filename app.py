import streamlit as st
import plotly.graph_objects as go

from resume_parser import parse_resume
from nlp_processor import extract_skills, extract_experience, extract_education
from similarity_engine import rank_resumes
from utils import get_score_color, get_score_emoji, get_grade, create_ranking_dataframe
from styles import MAIN_CSS


st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide"
)

st.markdown(MAIN_CSS, unsafe_allow_html=True)


st.markdown(
    """
    <div class="main-header">
        <h1>🤖 AI Resume Screening System</h1>
        <p>Upload multiple resumes and compare them with a job description using NLP and AI matching.</p>
    </div>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")

    tfidf_weight = st.slider(
        "Content Similarity Weight",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.05
    )

    skill_weight = 1.0 - tfidf_weight
    st.info(f"Skill Match Weight: {skill_weight:.2f}")

    st.markdown("---")
    st.subheader("📌 System Features")
    st.write("✅ Resume text extraction")
    st.write("✅ NLP preprocessing")
    st.write("✅ Skill extraction")
    st.write("✅ TF-IDF similarity")
    st.write("✅ Resume ranking")
    st.write("✅ CSV report download")

    st.markdown("---")
    st.subheader("📁 Supported Files")
    st.write("PDF, DOCX, TXT")


left_col, right_col = st.columns(2, gap="large")


with left_col:
    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste job description here",
        height=300,
        placeholder=(
            "Example: We are hiring a Python Developer with experience in "
            "machine learning, SQL, AWS, Docker, Flask, data analysis, "
            "communication skills, and 3+ years of experience."
        )
    )

    if job_description:
        st.markdown("### 🔍 Skills Found in Job Description")
        job_skills = extract_skills(job_description)

        if job_skills:
            for category, skills in job_skills.items():
                tags = "".join([f'<span class="skill-matched">{skill}</span>' for skill in skills])
                st.markdown(f"**{category}**<br>{tags}", unsafe_allow_html=True)
        else:
            st.warning("No predefined skills found. Try adding more technical skills.")


with right_col:
    st.subheader("📄 Upload Resumes")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or TXT resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} resume(s) uploaded.")

        for file in uploaded_files:
            size_kb = file.size / 1024
            st.write(f"📄 **{file.name}** — {size_kb:.1f} KB")


st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)


if job_description and uploaded_files:

    if st.button("🚀 Analyze and Rank Resumes", type="primary", use_container_width=True):

        resumes = []

        with st.spinner("Extracting text from resumes..."):
            for file in uploaded_files:
                text = parse_resume(file)

                if text and not text.startswith("Error") and not text.startswith("Unsupported"):
                    resumes.append({
                        "name": file.name,
                        "text": text
                    })
                else:
                    st.warning(f"Could not read {file.name}")

        if len(resumes) == 0:
            st.error("No resumes could be processed.")
            st.stop()

        with st.spinner("Analyzing resumes using NLP..."):
            rankings = rank_resumes(
                job_description,
                resumes,
                tfidf_weight=tfidf_weight,
                skill_weight=skill_weight
            )

        st.session_state["rankings"] = rankings


if "rankings" in st.session_state:

    rankings = st.session_state["rankings"]

    st.header("🏆 Ranking Results")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{len(rankings)}</div>
                <div class="metric-label">Resumes Analyzed</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:
        best_score = rankings[0]["combined_score"] * 100
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value" style="color:#4ade80;">{best_score:.1f}%</div>
                <div class="metric-label">Best Match</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m3:
        average_score = sum(item["combined_score"] for item in rankings) / len(rankings) * 100
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value" style="color:#facc15;">{average_score:.1f}%</div>
                <div class="metric-label">Average Score</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m4:
        top_candidate = rankings[0]["name"]
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value" style="font-size:24px;">🥇</div>
                <div class="metric-label">{top_candidate[:24]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 📊 Ranking Table")
    df = create_ranking_dataframe(rankings)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### 📈 Overall Score Chart")

    names = [item["name"][:25] for item in rankings]
    scores = [item["combined_score"] * 100 for item in rankings]
    colors = [get_score_color(item["combined_score"]) for item in rankings]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=scores,
            y=names,
            orientation="h",
            marker_color=colors,
            text=[f"{score:.1f}%" for score in scores],
            textposition="auto"
        )
    )

    fig.update_layout(
        xaxis_title="Match Score (%)",
        yaxis_title="Resume",
        yaxis=dict(autorange="reversed"),
        height=420,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    st.header("📋 Detailed Resume Analysis")

    for item in rankings:
        score = item["combined_score"]
        color = get_score_color(score)
        emoji = get_score_emoji(score)
        grade = get_grade(score)

        st.markdown(
            f"""
            <div class="rank-card">
                <h2>{emoji} Rank #{item["rank"]}: {item["name"]}</h2>
                <h3 style="color:{color};">Overall Score: {score * 100:.1f}% | Grade: {grade}</h3>
                <div class="progress-bg">
                    <div class="progress-fill" style="width:{score * 100}%; background:{color};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Overall Score", f"{item['combined_score'] * 100:.1f}%")

        with c2:
            st.metric("Content Match", f"{item['tfidf_score'] * 100:.1f}%")

        with c3:
            st.metric("Skill Match", f"{item['skill_match']['score'] * 100:.1f}%")

        with st.expander(f"View details for {item['name']}", expanded=item["rank"] == 1):

            st.subheader("✅ Matched Skills")
            matched = item["skill_match"]["matched_skills"]

            if matched:
                tags = "".join([f'<span class="skill-matched">{skill}</span>' for skill in matched])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.write("No matched skills found.")

            st.subheader("❌ Missing Skills")
            missing = item["skill_match"]["missing_skills"]

            if missing:
                tags = "".join([f'<span class="skill-missing">{skill}</span>' for skill in missing])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.success("No missing skills.")

            st.subheader("💡 Extra Skills")
            extra = item["skill_match"]["extra_skills"]

            if extra:
                tags = "".join([f'<span class="skill-extra">{skill}</span>' for skill in extra])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.write("No extra skills found.")

            st.subheader("📂 Category-wise Match")

            if item["category_scores"]:
                for category, data in item["category_scores"].items():
                    st.write(
                        f"**{category}:** "
                        f"{data['total_matched']} / {data['total_required']} matched "
                        f"({data['score'] * 100:.1f}%)"
                    )
                    st.progress(data["score"])
            else:
                st.write("No category data available.")

            st.subheader("🧾 Resume Quick Info")
            experience = extract_experience(item["preview"])
            education = extract_education(item["preview"])

            st.write(f"**Experience:** {experience}")

            if education:
                st.write("**Education Keywords:** " + ", ".join(education))
            else:
                st.write("**Education Keywords:** Not found")

            st.subheader("📄 Text Preview")
            st.text(item["preview"])

    st.markdown("### 📥 Download Report")

    csv_data = df.to_csv(index=False)

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="resume_screening_report.csv",
        mime="text/csv",
        use_container_width=True
    )

else:
    st.info("Enter a job description and upload resumes to start analysis.")