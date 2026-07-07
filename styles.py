"""
🎨 Custom CSS Styles
Beautiful styling for the Streamlit app
"""

MAIN_CSS = """
<style>
    /* ── Global Styles ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header Styles ── */
    .main-header {
        background: linear-gradient(135deg, #0a1628 0%, #1a237e 50%, #283593 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(26, 35, 126, 0.3);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .main-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }

    .main-header p {
        color: rgba(255,255,255,0.8);
        font-size: 1.1rem;
        position: relative;
        z-index: 1;
    }

    /* ── Score Card ── */
    .score-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .score-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }

    .score-card h3 {
        color: #ffffff;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .score-card .score-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }

    /* ── Rank Cards ── */
    .rank-card {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }

    .rank-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }

    .rank-1::after {
        background: linear-gradient(90deg, #FFD700, #FFA000);
    }
    .rank-2::after {
        background: linear-gradient(90deg, #C0C0C0, #9E9E9E);
    }
    .rank-3::after {
        background: linear-gradient(90deg, #CD7F32, #A0522D);
    }
    .rank-other::after {
        background: linear-gradient(90deg, #42A5F5, #1E88E5);
    }

    .rank-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        font-size: 1.3rem;
        font-weight: 800;
        color: white;
        margin-right: 1rem;
    }

    .rank-1-badge { background: linear-gradient(135deg, #FFD700, #FFA000); }
    .rank-2-badge { background: linear-gradient(135deg, #C0C0C0, #9E9E9E); }
    .rank-3-badge { background: linear-gradient(135deg, #CD7F32, #A0522D); }
    .rank-other-badge { background: linear-gradient(135deg, #42A5F5, #1E88E5); }

    /* ── Skill Tags ── */
    .skill-matched {
        background: rgba(0, 200, 83, 0.2);
        color: #00C853;
        border: 1px solid rgba(0, 200, 83, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        margin: 3px;
        display: inline-block;
        font-size: 0.82rem;
        font-weight: 500;
    }

    .skill-missing {
        background: rgba(255, 23, 68, 0.2);
        color: #FF1744;
        border: 1px solid rgba(255, 23, 68, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        margin: 3px;
        display: inline-block;
        font-size: 0.82rem;
        font-weight: 500;
    }

    .skill-extra {
        background: rgba(41, 121, 255, 0.2);
        color: #2979FF;
        border: 1px solid rgba(41, 121, 255, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        margin: 3px;
        display: inline-block;
        font-size: 0.82rem;
        font-weight: 500;
    }

    /* ── Progress Bar ── */
    .custom-progress {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 8px 0;
    }

    .custom-progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-in-out;
    }

    /* ── Section Divider ── */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 2rem 0;
    }

    /* ── Info Box ── */
    .info-box {
        background: linear-gradient(135deg, rgba(41, 121, 255, 0.1), rgba(41, 121, 255, 0.05));
        border: 1px solid rgba(41, 121, 255, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #90CAF9;
    }

    /* ── Metric Card ── */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #64B5F6;
    }

    .metric-card .metric-label {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
        margin-top: 0.3rem;
    }

    /* ── Sidebar Styles ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #1a1a2e 100%);
    }

    /* ── Hide Streamlit branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""