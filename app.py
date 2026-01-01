import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.express as px

from model.inference_engine import FuzzyInferenceEngine
from visualization.plots import get_membership_figures
from io_utils.csv_loader import process_dataframe

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Système flou d’aide à la décision environnementale",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
    color: #eaeaea;
}
.card {
    background: rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}
.big-metric-label {
    font-size: 26px;
    font-weight: 700;
    color: #e5e7eb;
}

.big-metric-value {
    font-size: 48px;
    font-weight: 800;
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# TITLE
# ======================================================
st.title("🌍 Système flou d’aide à la décision environnementale")

# ======================================================
# TABS
# ======================================================
tabs = st.tabs([
    "🎛️ Évaluation",
    "📊 Visualisation floue",
    "📁 Traitement CSV",
  
    "📜 Règles floues"
])

engine = FuzzyInferenceEngine()

# ======================================================
# TAB 1 — INTERACTIVE EVALUATION
# ======================================================
with tabs[0]:
    st.header("🎛️ Paramètres environnementaux")

    colA, colB, colC = st.columns(3)

    with colA:
        st.markdown('<div class="card"><h3>🌫️ Pollution</h3>', unsafe_allow_html=True)
        pollution_air = st.slider("Pollution de l’air", 0, 100, 50)
        pollution_eau = st.slider("Pollution de l’eau", 0, 100, 50)
        urbanisation = st.slider("Urbanisation", 0, 100, 50)
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="card"><h3>🌱 Sol & végétation</h3>', unsafe_allow_html=True)
        humidite_sol = st.slider("Humidité du sol", 0, 100, 50)
        erosion = st.slider("Érosion", 0, 100, 50)
        vegetation = st.slider("Végétation", 0, 100, 50)
        deforestation = st.slider("Déforestation", 0, 100, 50)
        st.markdown('</div>', unsafe_allow_html=True)

    with colC:
        st.markdown('<div class="card"><h3>🌍 Climat</h3>', unsafe_allow_html=True)
        biodiversite = st.slider("Biodiversité", 0, 100, 50)
        temperature = st.slider("Température", 0, 50, 25)
        stress_hydrique = st.slider("Stress hydrique", 0, 100, 50)
        st.markdown('</div>', unsafe_allow_html=True)

    inputs = {
        "pollution_air": pollution_air,
        "pollution_eau": pollution_eau,
        "humidite_sol": humidite_sol,
        "erosion": erosion,
        "vegetation": vegetation,
        "biodiversite": biodiversite,
        "temperature": temperature,
        "urbanisation": urbanisation,
        "deforestation": deforestation,
        "stress_hydrique": stress_hydrique,
    }

    if st.button("🚀 Évaluer"):
        outputs = engine.compute(inputs)
        result_row = {
            **inputs,
            "risque": round(outputs["risque"], 2),
            "action": outputs["action_label"]
        }
        result_df = pd.DataFrame([result_row])



        col1, col2 = st.columns(2)

        with col1:
             st.markdown(
            f"""
            <div class="card">
                <div class="big-metric-label">🌡️ Risque écologique</div>
                <div class="big-metric-value">{outputs['risque']:.1f} / 100</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(min(outputs["risque"] / 100, 1.0))

        with col2:
            label = outputs["action_label"]


            st.markdown(
            f"""
            <div class="card">
                <div class="big-metric-label">🚨 Action recommandée</div>
                <div class="big-metric-value">{label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        csv = result_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="💾 Télécharger le résultat (CSV)",
            data=csv,
            file_name="evaluation_fuzzy.csv",
            mime="text/csv"
        )

            


# ======================================================
# TAB 2 — FUZZY VISUALIZATION
# ======================================================
with tabs[1]:
    st.header("📊 Fonctions d’appartenance floues")
    figures = get_membership_figures()

    for name, fig in figures:
        with st.expander(name):
            st.pyplot(fig, use_container_width=True)

# ======================================================
# TAB 3 — CSV BATCH
# ======================================================
with tabs[2]:
    st.header("📁 Traitement CSV")

    file = st.file_uploader("Importer un CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        if st.button("▶️ Traiter"):
            result_df = process_dataframe(df)
            st.dataframe(result_df)


# ======================================================
# TAB 5 — FUZZY RULES
# ======================================================
with tabs[3]:
    st.header("📜 Règles floues")

    base_path = Path(__file__).resolve().parent
    rules_path = base_path / "config" / "rules.json"

    with open(rules_path, "r", encoding="utf-8") as f:
        rules = json.load(f)

    st.info(f"{len(rules)} règles actives")

    for i, rule in enumerate(rules, start=1):
        with st.expander(f"Règle {i}"):
            st.write("SI")
            for k, v in rule["if"].items():
                st.write(f"- {k} est {v}")
            st.write("ALORS")
            for k, v in rule["then"].items():
                st.write(f"- {k} est {v}")
