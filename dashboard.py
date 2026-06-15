import sys
sys.path.append("C:/pqa")

import streamlit as st
from src.insights import analyze_prompt

st.set_page_config(
    page_title="Prompt IQ",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #080810; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }

    .hero-wrap { text-align: center; padding: 2rem 0 1rem 0; }
    .hero-tag {
        display: inline-block;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.3);
        color: #818cf8; font-size: 0.75rem; font-weight: 600;
        letter-spacing: 0.15em; text-transform: uppercase;
        padding: 0.3rem 1rem; border-radius: 999px; margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 3.5rem; font-weight: 900; line-height: 1.1;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #6366f1 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
    }
    .hero-sub { color: #6b7280; font-size: 1rem; margin-bottom: 1.5rem; }

    .stTextArea textarea {
        background: #0d0d1a !important; color: #e2e8f0 !important;
        border: 1px solid #1e1e3a !important; border-radius: 16px !important;
        font-size: 1rem !important; padding: 1rem !important;
    }
    .stTextArea textarea:focus {
        border: 1px solid #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white; border: none; border-radius: 12px;
        padding: 0.7rem 2rem; font-size: 1rem; font-weight: 600;
        width: 100%; box-shadow: 0 4px 24px rgba(99,102,241,0.3);
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 32px rgba(99,102,241,0.4);
    }

    .custom-divider { border: none; border-top: 1px solid #1a1a2e; margin: 1.5rem 0; }

    .score-ring-wrap {
        background: linear-gradient(135deg, #0d0d1a, #13131f);
        border: 1px solid #1e1e3a; border-radius: 24px;
        padding: 2rem; text-align: center;
    }
    .score-big {
        font-size: 5rem; font-weight: 900; line-height: 1;
        background: linear-gradient(135deg, #a78bfa, #6366f1);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .score-denom { color: #374151; font-size: 1.5rem; font-weight: 600; }
    .score-sublabel { color: #6b7280; font-size: 0.85rem; margin-top: 0.3rem; }

    .badge { display: inline-block; padding: 0.4rem 1.2rem; border-radius: 999px; font-weight: 700; font-size: 0.85rem; margin-top: 1rem; }
    .badge-high   { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
    .badge-medium { background: rgba(245,158,11,0.15);  color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
    .badge-low    { background: rgba(239,68,68,0.15);   color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

    .pbar-wrap {
        background: #1a1a2e; border-radius: 999px;
        height: 8px; width: 100%; margin-top: 1.2rem; overflow: hidden;
    }
    .pbar-fill { height: 8px; border-radius: 999px; }

    .feat-grid { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 0.5rem; }
    .feat-pill {
        background: #0d0d1a; border: 1px solid #1e1e3a;
        border-radius: 10px; padding: 0.5rem 1rem;
        font-size: 0.85rem; color: #9ca3af;
        display: flex; align-items: center; gap: 0.4rem;
    }
    .feat-pill span.val { color: #a78bfa; font-weight: 700; }

    .tip-item {
        display: flex; align-items: flex-start; gap: 0.8rem;
        background: #0d0d1a; border: 1px solid #1e1e3a;
        border-radius: 12px; padding: 0.9rem 1.1rem;
        margin-bottom: 0.6rem; color: #d1d5db;
        font-size: 0.92rem; line-height: 1.5;
    }
    .tip-icon { font-size: 1.1rem; margin-top: 0.1rem; flex-shrink: 0; }

    .improved-box {
        background: linear-gradient(135deg, #0d0d1a, #0f0f20);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 16px; padding: 1.2rem 1.5rem;
        color: #c4b5fd; font-size: 0.95rem;
        line-height: 1.7;
    }

    .history-item {
        background: #0d0d1a; border: 1px solid #1e1e3a;
        border-radius: 12px; padding: 1rem 1.2rem;
        margin-bottom: 0.6rem; color: #d1d5db;
    }
    .history-prompt { font-size: 0.9rem; color: #9ca3af; margin-bottom: 0.3rem; }
    .history-score  { font-size: 1.1rem; font-weight: 700; color: #a78bfa; }

    .template-card {
        background: #0d0d1a; border: 1px solid #1e1e3a;
        border-radius: 12px; padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .template-title { color: #a78bfa; font-weight: 600; font-size: 0.9rem; }
    .template-text  { color: #6b7280; font-size: 0.8rem; margin-top: 0.3rem; }

    .section-label {
        color: #4b5563; font-size: 0.7rem; font-weight: 700;
        letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.8rem;
    }

    .compare-box {
        background: #0d0d1a; border: 1px solid #1e1e3a;
        border-radius: 16px; padding: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
<div class="hero-wrap">
    <div class="hero-tag">⚡ Prompt Intelligence Tool</div>
    <div class="hero-title">Know Your Prompt.<br>Before You Send It.</div>
    <div class="hero-sub">Instantly score your prompt and get tips to make it sharper.</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["⚡ Analyze", "📊 History", "⚖️ Compare", "📋 Templates"])

with tab1:
    prompt = st.text_area("", height=160, placeholder="Type or paste your prompt here...", key="main_prompt")
    analyze_clicked = st.button("Analyze  ⚡", key="analyze_btn")

    if analyze_clicked:
        if not prompt.strip():
            st.warning("Please enter a prompt first.")
        else:
            with st.spinner("Analyzing your prompt..."):
                result = analyze_prompt(prompt)

            score    = result["score"]
            label    = result["label"]
            features = result["features"]
            tips     = result["tips"]
            improved = result.get("improved_prompt", prompt)
            pct      = int((score / 5) * 100)
            bar_color = "#34d399" if label=="high" else ("#fbbf24" if label=="medium" else "#f87171")

            st.session_state.history.append({
                "prompt": prompt,
                "score":  score,
                "label":  label
            })

            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

            left, right = st.columns([1, 2])

            with left:
                st.markdown(f"""
                <div class="score-ring-wrap">
                    <div class="score-big">{score}<span class="score-denom">/5</span></div>
                    <div class="score-sublabel">PROMPT SCORE</div>
                    <div class="badge badge-{label}">{label.upper()}</div>
                    <div class="pbar-wrap">
                        <div class="pbar-fill" style="width:{pct}%; background:{bar_color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with right:
                st.markdown('<div class="section-label">Prompt Signals</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="feat-grid">
                    <div class="feat-pill">Words <span class="val">{features['word_count']}</span></div>
                    <div class="feat-pill">Role <span class="val">{'✅' if features['has_role'] else '❌'}</span></div>
                    <div class="feat-pill">Example <span class="val">{'✅' if features['has_example'] else '❌'}</span></div>
                    <div class="feat-pill">Format <span class="val">{'✅' if features['has_format'] else '❌'}</span></div>
                    <div class="feat-pill">Specificity <span class="val">{features['specificity']}</span></div>
                    <div class="feat-pill">Readability <span class="val">{features['flesch_score']}</span></div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<br><div class="section-label">Tips to Improve</div>', unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f"""
                    <div class="tip-item">
                        <span class="tip-icon">→</span>
                        <span>{tip}</span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Suggested Improvement</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="improved-box">{improved}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### Your Analysis History")
    if not st.session_state.history:
        st.info("No prompts analyzed yet. Go to the Analyze tab to get started!")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            bar = "#34d399" if item['label']=="high" else ("#fbbf24" if item['label']=="medium" else "#f87171")
            st.markdown(f"""
            <div class="history-item">
                <div class="history-prompt">#{len(st.session_state.history)-i} — {item['prompt'][:100]}...</div>
                <div class="history-score" style="color:{bar};">{item['score']} / 5 &nbsp;
                    <span style="font-size:0.8rem; font-weight:400; color:#6b7280;">{item['label'].upper()}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

with tab3:
    st.markdown("### Compare Two Prompts Side by Side")
    c1, c2 = st.columns(2)
    with c1:
        prompt_a = st.text_area("Prompt A", height=150, placeholder="Enter first prompt...", key="compare_a")
    with c2:
        prompt_b = st.text_area("Prompt B", height=150, placeholder="Enter second prompt...", key="compare_b")

    if st.button("Compare Prompts ⚡", key="compare_btn"):
        if not prompt_a.strip() or not prompt_b.strip():
            st.warning("Please enter both prompts.")
        else:
            with st.spinner("Analyzing both prompts..."):
                result_a = analyze_prompt(prompt_a)
                result_b = analyze_prompt(prompt_b)

            col1, col2 = st.columns(2)
            for col, res, label in [(col1, result_a, "A"), (col2, result_b, "B")]:
                with col:
                    bar = "#34d399" if res['label']=="high" else ("#fbbf24" if res['label']=="medium" else "#f87171")
                    st.markdown(f"""
                    <div class="compare-box">
                        <div style="color:#9ca3af; font-size:0.8rem; margin-bottom:0.5rem;">PROMPT {label}</div>
                        <div style="font-size:3rem; font-weight:900; color:{bar};">{res['score']}<span style="font-size:1rem; color:#374151;">/5</span></div>
                        <div style="color:{bar}; font-weight:700; margin-bottom:1rem;">{res['label'].upper()}</div>
                        <div style="color:#6b7280; font-size:0.85rem;">{res['prompt'][:80]}...</div>
                    </div>
                    """, unsafe_allow_html=True)

            winner = "A" if result_a['score'] >= result_b['score'] else "B"
            st.markdown(f"""
            <div style="text-align:center; margin-top:1.5rem; padding:1rem;
                background: rgba(99,102,241,0.1); border-radius:12px;
                border: 1px solid rgba(99,102,241,0.2);">
                <span style="color:#a78bfa; font-size:1.2rem; font-weight:700;">
                    🏆 Prompt {winner} wins!
                </span>
            </div>
            """, unsafe_allow_html=True)

with tab4:
    st.markdown("### High Quality Prompt Templates")

    TEMPLATES = [
        {"title": "Code Expert", "prompt": "You are a senior software engineer. Explain {topic} in Python with a working code example, time complexity analysis, and common use cases. Format your response with clear sections."},
        {"title": "Data Science", "prompt": "You are a data scientist. Describe the step-by-step process to {task} including data preprocessing, model selection, evaluation metrics, and potential pitfalls. Use bullet points."},
        {"title": "Concept Explainer", "prompt": "You are a teacher explaining to a beginner. Explain {concept} using a simple real-world analogy, a clear definition, and one practical example. Keep it under 200 words."},
        {"title": "Debugging Helper", "prompt": "You are a debugging expert. I have the following error: {error}. Explain what caused it, provide a fixed version of the code, and suggest how to prevent it in the future."},
        {"title": "Research Summary", "prompt": "You are a research analyst. Summarize the key points about {topic} including main findings, practical implications, and open questions. Use numbered points for clarity."},
        {"title": "Creative Writing", "prompt": "You are a creative writing expert. Write a short story about {topic} that includes a compelling opening, a conflict, and a surprising resolution. Keep it under 300 words."},
    ]

    cols = st.columns(2)
    for i, template in enumerate(TEMPLATES):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="template-card">
                <div class="template-title">📌 {template['title']}</div>
                <div class="template-text">{template['prompt'][:100]}...</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Use this template", key=f"template_{i}"):
                st.info(f"Copy this: {template['prompt']}")