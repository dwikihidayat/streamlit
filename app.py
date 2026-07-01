import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import time

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Prediksi Ukuran Pakaian",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== PROFESSIONAL / CLEAN CSS ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* === BACKGROUND === */
    .stApp {
        background: #F0F4F8;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1400px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* === CARD === */
    .card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2.2rem 2rem;
        box-shadow: 0 2px 12px rgba(44, 62, 80, 0.08);
        margin-bottom: 1.4rem;
        border: 1px solid rgba(44, 62, 80, 0.06);
    }

    /* === HEADER === */
    .header {
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .eyebrow {
        font-size: 0.65rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #3D8C9A;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .header h1 {
        font-size: 2.2rem;
        font-weight: 600;
        margin: 0;
        color: #1A2332;
        letter-spacing: -0.5px;
    }

    .header h1 em {
        font-style: italic;
        color: #3D8C9A;
        font-weight: 700;
    }

    .divider {
        width: 40px;
        height: 2px;
        background: #3D8C9A;
        margin: 0.8rem auto;
        border-radius: 2px;
    }

    /* === SUBHEAD === */
    .subhead {
        color: #1A2332;
        font-size: 0.85rem;
        text-align: center;
        margin: 0 0 1.8rem 0;
        line-height: 1.6;
        font-weight: 400;
    }

    .subhead strong {
        color: #1A2332;
        font-weight: 600;
    }

    /* === SECTION LABEL === */
    .section-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        color: #1A2332;
        margin: 0.2rem 0 0.8rem 0;
        border-bottom: 1px solid rgba(61, 140, 154, 0.15);
        padding-bottom: 0.4rem;
    }

    /* === SLIDER LABEL === */
    .slider-wrapper {
        margin-bottom: 1.1rem;
    }

    .slider-label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 400;
        font-size: 0.85rem;
        color: #1A2332;
        margin-bottom: 0.3rem;
        padding: 0 2px;
    }

    .slider-value {
        color: #FFFFFF;
        font-weight: 600;
        background: #3D8C9A;
        padding: 0.1rem 0.9rem;
        border-radius: 4px;
        font-size: 0.75rem;
        letter-spacing: 0.3px;
    }

    /* === STREAMLIT SLIDER OVERRIDE === */
    div[data-baseweb="slider"] {
        margin-bottom: 0.1rem;
    }

    div[data-baseweb="slider"] > div {
        background: #D4E6E9 !important;
        height: 3px !important;
        border-radius: 3px !important;
    }

    div[data-baseweb="slider"] div[role="slider"] {
        background: #3D8C9A !important;
        box-shadow: 0 0 0 3px rgba(61, 140, 154, 0.15) !important;
        border: 2px solid #FFFFFF !important;
        width: 18px !important;
        height: 18px !important;
        border-radius: 50% !important;
        transition: all 0.2s ease;
    }

    div[data-baseweb="slider"] div[role="slider"]:hover {
        box-shadow: 0 0 0 5px rgba(61, 140, 154, 0.2) !important;
        transform: scale(1.05);
    }

    div[data-baseweb="slider"] > div > div {
        background: linear-gradient(90deg, #3D8C9A, #5BA3B0) !important;
        border-radius: 3px !important;
    }

    /* === RADIO (height unit) - TEKS HITAM === */
    .stRadio > div {
        gap: 0 !important;
        background: #F0F4F8;
        border-radius: 6px;
        display: inline-flex !important;
        width: auto !important;
        overflow: hidden;
        border: 1px solid #D4E6E9;
        padding: 2px;
    }

    .stRadio > div label {
        background: transparent !important;
        padding: 0.3rem 1.2rem !important;
        border-radius: 4px !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.3px !important;
        color: #1A2332 !important;  /* TEKS HITAM */
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }

    .stRadio > div label:hover {
        color: #1A2332 !important;  /* TETAP HITAM SAAT HOVER */
        background: rgba(61, 140, 154, 0.15) !important;
    }

    .stRadio > div label[data-selected="true"] {
        background: #3D8C9A !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(61, 140, 154, 0.2) !important;
    }

    /* === NUMBER INPUT (ft/in) === */
    .stNumberInput input {
        border-radius: 6px !important;
        border: 1px solid #D4E6E9 !important;
        background: #FFFFFF !important;
        color: #1A2332 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 0.75rem !important;
    }

    .stNumberInput input:focus {
        border-color: #3D8C9A !important;
        box-shadow: 0 0 0 3px rgba(61, 140, 154, 0.1) !important;
    }

    /* === PREDICT BUTTON === */
    .stButton > button {
        background: #1A2332;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 0.85rem 1.8rem;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: none;
        letter-spacing: 0.5px;
        width: 100%;
        transition: all 0.25s ease;
        box-shadow: 0 2px 8px rgba(26, 35, 50, 0.12);
    }

    .stButton > button:hover {
        background: #2C3E50;
        box-shadow: 0 4px 16px rgba(26, 35, 50, 0.2);
        transform: translateY(-1px);
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }

    /* === RESULT CARD === */
    .result-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2.2rem 1.6rem;
        text-align: center;
        margin-top: 0.2rem;
        border: 1px solid rgba(61, 140, 154, 0.15);
        box-shadow: 0 2px 12px rgba(44, 62, 80, 0.06);
    }

    .result-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #1A2332;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .result-size {
        font-size: 4rem;
        font-weight: 700;
        color: #1A2332;
        line-height: 1.1;
        margin: 0.1rem 0;
        letter-spacing: -1px;
    }

    .result-size .highlight {
        color: #3D8C9A;
    }

    .result-desc {
        color: #1A2332;
        max-width: 350px;
        margin: 0.6rem auto 0;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    .result-placeholder {
        color: #B0C4CC;
        font-size: 2.5rem;
        font-weight: 300;
    }

    /* === CLOTHING SIZE TABLE === */
    .size-table {
        width: 100%;
        margin: 1.5rem 0 0.5rem 0;
        border-collapse: collapse;
        font-size: 0.8rem;
    }

    .size-table th {
        background: #F0F4F8;
        color: #1A2332;
        font-weight: 600;
        padding: 0.6rem 0.4rem;
        text-align: center;
        border: 1px solid #D4E6E9;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .size-table td {
        padding: 0.5rem 0.4rem;
        text-align: center;
        border: 1px solid #D4E6E9;
        color: #1A2332;
    }

    .size-table .size-label {
        font-weight: 600;
        color: #3D8C9A;
    }

    .size-table tr:hover {
        background: #F8FAFC;
    }

    /* === STATS BAR === */
    .stats-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 1.2rem;
        background: #FFFFFF;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        border: 1px solid rgba(44, 62, 80, 0.06);
        font-size: 0.7rem;
        letter-spacing: 0.3px;
        color: #1A2332;
        margin-top: 1.2rem;
        box-shadow: 0 1px 6px rgba(44, 62, 80, 0.04);
    }

    .stats-bar span {
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    .stats-bar .highlight {
        color: #3D8C9A;
        font-weight: 600;
    }

    .stats-divider {
        width: 1px;
        height: 20px;
        background: #D4E6E9;
    }

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid rgba(44, 62, 80, 0.06) !important;
        min-width: 280px !important;
        width: 280px !important;
    }

    .sidebar-info {
        background: #F0F4F8;
        border-radius: 8px;
        padding: 1.2rem;
        font-size: 0.8rem;
        color: #1A2332;
        border: 1px solid #D4E6E9;
    }

    .sidebar-info strong {
        color: #1A2332;
        font-weight: 600;
    }

    .sidebar-info .label {
        color: #1A2332;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* === EXPANDER (Detail Pakaian) === */
    .streamlit-expanderHeader {
        color: #1A2332 !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderContent {
        color: #1A2332 !important;
    }

    /* === SELECTBOX, RADIO, SLIDER di dalam expander === */
    .stSelectbox label,
    .stRadio label,
    .stSlider label {
        color: #1A2332 !important;
    }

    .stSelectbox div[data-baseweb="select"] span {
        color: #1A2332 !important;
    }

    /* === LAYOUT DESKTOP === */
    .desktop-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
    }

    .full-width {
        grid-column: 1 / -1;
    }

    /* === FOOTER === */
    .footer {
        text-align: center;
        color: #B0C4CC;
        font-size: 0.65rem;
        margin-top: 1.4rem;
        letter-spacing: 1px;
        font-weight: 400;
    }

    /* === HIDE DEFAULTS === */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .block-container {
            max-width: 100% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .card { padding: 1.5rem 1.2rem; }
        .header h1 { font-size: 1.8rem; }
        .result-size { font-size: 3rem; }
        .stats-bar { gap: 0.8rem; padding: 0.6rem 1rem; }
        .stats-divider { display: none; }
        .size-table { font-size: 0.65rem; }
        .size-table th, .size-table td { padding: 0.3rem 0.2rem; }
        .desktop-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========== LOAD MODEL ==========
MODEL_FILE = "model_pakaian_rf_terbaik.pkl"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_FILE):
        return None
    with open(MODEL_FILE, "rb") as f:
        payload = pickle.load(f)
    return payload

payload = load_model()

if payload is None:
    st.error(f"🚨 **File model `{MODEL_FILE}` tidak ditemukan.**")
    st.stop()

# Set up medians manually
medians = {
    'height': 165.1,
    'waist': 30.0,
    'hips': 39.0,
    'bust': 36.0,
    'bra size': 36.0
}

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:1.5rem;">
        <span style="font-weight:600; font-size:0.9rem; letter-spacing:0.5px; color:#1A2332;">👑 Ukuran Cerdas</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-info">
        <div style="margin-bottom:0.8rem;">
            <div class="label">Metode</div>
            <strong style="font-size:0.95rem; color:#1A2332;">Random Forest</strong>
        </div>
        <div style="margin-bottom:0.8rem;">
            <div class="label">Kategori Ukuran</div>
            <strong style="font-size:0.95rem; color:#1A2332;">S · M · L · XL</strong>
        </div>
        <div style="margin-bottom:0.8rem;">
            <div class="label">Data Pelatihan</div>
            <strong style="font-size:0.95rem; color:#1A2332;">756 profil (bersih & SMOTE)</strong>
        </div>
        <div>
            <div class="label">Nilai Tengah (Median)</div>
            <span style="font-size:0.85rem; color:#1A2332;">
                Tinggi: <strong style="color:#1A2332;">{medians['height']:.1f} cm</strong><br>
                Pinggang: <strong style="color:#1A2332;">{medians['waist']:.1f} inci</strong><br>
                Pinggul: <strong style="color:#1A2332;">{medians['hips']:.1f} inci</strong><br>
                Dada: <strong style="color:#1A2332;">{medians['bust']:.1f} inci</strong><br>
                Bra: <strong style="color:#1A2332;">{medians['bra size']:.1f} inci</strong>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:2rem; text-align:center; color:#B0C4CC; font-size:0.6rem; letter-spacing:1px;">
        Antigravity AI
    </div>
    """, unsafe_allow_html=True)

# ========== MAIN CONTENT ==========
st.markdown("""
<div class="card">
    <div class="header">
        <div class="eyebrow">Ukuran yang Tepat</div>
        <h1>Temukan <em>Ukuranmu</em></h1>
    </div>
    <div class="divider"></div>
    <div class="subhead">
        Masukkan ukuran tubuhmu untuk rekomendasi yang presisi<br>
        berdasarkan data yang telah dikurasi
    </div>
""", unsafe_allow_html=True)

# --- HEIGHT UNIT ---
st.markdown('<div class="section-label">Satuan Tinggi</div>', unsafe_allow_html=True)
height_unit = st.radio(
    "Satuan tinggi",
    ["Centimeter (cm)", "Kaki & Inci"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown('<div style="height:1.2rem;"></div>', unsafe_allow_html=True)

# Desktop layout: 2 columns for sliders
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-label">Ukuran Tubuh</div>', unsafe_allow_html=True)

    st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
    if height_unit == "Centimeter (cm)":
        height_cm = st.slider(
            "Tinggi badan",
            min_value=120.0, max_value=220.0,
            value=float(medians['height']),
            step=0.5,
            label_visibility="collapsed"
        )
    else:
        c_ft, c_in = st.columns(2)
        with c_ft:
            ft = st.number_input("kaki", min_value=3, max_value=8, value=5, step=1, label_visibility="collapsed")
        with c_in:
            inch = st.number_input("inci", min_value=0, max_value=11, value=5, step=1, label_visibility="collapsed")
        height_cm = round((ft * 12 + inch) * 2.54, 2)
    st.markdown(f"""
    <div class="slider-label">
        <span>Tinggi</span>
        <span class="slider-value">{height_cm:.1f} cm</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
    waist = st.slider(
        "Pinggang",
        min_value=15.0, max_value=60.0,
        value=float(medians['waist']),
        step=0.5,
        label_visibility="collapsed"
    )
    st.markdown(f"""
    <div class="slider-label">
        <span>Pinggang</span>
        <span class="slider-value">{waist:.1f} inci</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
    hips = st.slider(
        "Pinggul",
        min_value=20.0, max_value=70.0,
        value=float(medians['hips']),
        step=0.5,
        label_visibility="collapsed"
    )
    st.markdown(f"""
    <div class="slider-label">
        <span>Pinggul</span>
        <span class="slider-value">{hips:.1f} inci</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-label">&nbsp;</div>', unsafe_allow_html=True)

    st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
    bust = st.slider(
        "Dada",
        min_value=20.0, max_value=70.0,
        value=float(medians['bust']),
        step=0.5,
        label_visibility="collapsed"
    )
    st.markdown(f"""
    <div class="slider-label">
        <span>Dada</span>
        <span class="slider-value">{bust:.1f} inci</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
    bra_size = st.slider(
        "Ukuran Bra",
        min_value=20.0, max_value=50.0,
        value=float(medians['bra size']),
        step=0.5,
        label_visibility="collapsed"
    )
    st.markdown(f"""
    <div class="slider-label">
        <span>Ukuran Bra</span>
        <span class="slider-value">{bra_size:.1f} inci</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ========== PREDICT AND RESULT SECTIONS ==========
# Use columns for better desktop layout
col_pred, col_result = st.columns([1, 1], gap="large")

with col_pred:
    with st.expander("Detail Pakaian & Preferensi (Opsional)", expanded=False):
        ec1, ec2 = st.columns(2)
        with ec1:
            cup_map_keys = ["AA", "A", "B", "C", "D", "DD/E", "DDD/F", "G", "H", "I", "J", "K"]
            cup_size = st.selectbox("Ukuran Cup", cup_map_keys, index=3)
            fit_pref = st.radio("Preferensi Fit", ["Small", "Fit", "Large"], index=1, horizontal=True)
            quality = st.slider("Kualitas Pakaian", 1.0, 5.0, 3.0, 1.0)
        with ec2:
            sorted_cat = sorted(payload['le_category'].classes_)
            category = st.selectbox("Kategori Pakaian", sorted_cat, index=0)
            sorted_len = sorted(payload['le_length'].classes_)
            length = st.selectbox("Panjang Pakaian", sorted_len, index=0)

    # ========== PREDICT BUTTON ==========
    predict_clicked = st.button("Prediksi Ukuran Saya", use_container_width=True)

with col_result:
    # ========== RESULT ==========
    if predict_clicked:
        cup_map = {'aa':0, 'a':1, 'b':2, 'c':3, 'd':4, 'dd/e':5, 'ddd/f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11}
        fit_map = {'Small': 0, 'Fit': 1, 'Large': 2}

        cup_numeric = cup_map[cup_size.lower()]
        fit_numeric = fit_map[fit_pref]

        cat_encoded = payload['le_category'].transform([category])[0]
        len_encoded = payload['le_length'].transform([length])[0]

        EPS = 1e-6
        bust_height_ratio = bust / (height_cm + EPS)
        bra_cup_ratio = bra_size / (cup_numeric + EPS)
        waist_hip_ratio = waist / (hips + EPS)
        bust_waist_ratio = bust / (waist + EPS)
        bust_hip_ratio = bust / (hips + EPS)

        input_dict = {
            'height': height_cm,
            'bra size': bra_size,
            'cup size': cup_numeric,
            'bust': bust,
            'waist': waist,
            'hips': hips,
            'quality': quality,
            'fit_numeric': fit_numeric,
            'category': cat_encoded,
            'length': len_encoded,
            'bust_height_ratio': bust_height_ratio,
            'bra_cup_ratio': bra_cup_ratio,
            'waist_hip_ratio': waist_hip_ratio,
            'bust_waist_ratio': bust_waist_ratio,
            'bust_hip_ratio': bust_hip_ratio
        }

        input_df = pd.DataFrame([input_dict])[payload['fitur_model']]

        with st.spinner("Sedang menganalisis ukuran tubuhmu..."):
            time.sleep(0.6)
            scaled_input = payload['scaler'].transform(input_df)
            pred_encoded = payload['model'].predict(scaled_input)[0]
            prediction = payload['le_target'].inverse_transform([pred_encoded])[0]

        desc_map = {
            "S": "Cocok untuk ukuran 0–6 (Kecil). Siluet ramping yang pas untuk tubuh mungil.",
            "M": "Ideal untuk ukuran 8–10 (Sedang). Potongan klasik yang serbaguna untuk berbagai bentuk tubuh.",
            "L": "Terbaik untuk ukuran 12–18 (Besar). Potongan elegan yang mengikuti lekuk alami tubuh.",
            "XL": "Dirancang untuk ukuran 20+ (Sangat Besar). Siluet penuh dan anggun yang merayakan keindahan alami."
        }
        desc = desc_map.get(prediction, "")

        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Ukuran yang Direkomendasikan</div>
            <div class="result-size"><span class="highlight">{prediction}</span></div>
            <div class="result-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="result-card">
            <div class="result-label">Ukuran yang Direkomendasikan</div>
            <div class="result-placeholder">—</div>
            <div class="result-desc" style="color:#B0C4CC; font-size:0.85rem;">Atur ukuran tubuhmu lalu klik prediksi</div>
        </div>
        """, unsafe_allow_html=True)

# ========== SIZE CONVERSION TABLE ==========
# Show table after prediction or always
st.markdown("""
<div style="margin-top: 1.5rem; background: #FFFFFF; border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(61, 140, 154, 0.15);">
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; color: #1A2332; font-weight: 600;">Konversi Ukuran</span>
        <h4 style="color: #1A2332; margin: 0.2rem 0 0 0; font-weight: 500;">Tabel Ukuran Pakaian Wanita (US)</h4>
    </div>
    <table class="size-table">
        <thead>
            <tr>
                <th>Ukuran</th>
                <th>US Size</th>
                <th>Dada (inci)</th>
                <th>Pinggang (inci)</th>
                <th>Pinggul (inci)</th>
                <th>Dada (cm)</th>
                <th>Pinggang (cm)</th>
                <th>Pinggul (cm)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="size-label">S</td>
                <td>4-6</td>
                <td>33-35</td>
                <td>25-27</td>
                <td>35-37</td>
                <td>84-89</td>
                <td>64-69</td>
                <td>89-94</td>
            </tr>
            <tr>
                <td class="size-label">M</td>
                <td>8-10</td>
                <td>36-38</td>
                <td>28-30</td>
                <td>38-40</td>
                <td>91-97</td>
                <td>71-76</td>
                <td>97-102</td>
            </tr>
            <tr>
                <td class="size-label">L</td>
                <td>12-14</td>
                <td>39-41</td>
                <td>31-33</td>
                <td>41-43</td>
                <td>99-104</td>
                <td>79-84</td>
                <td>104-109</td>
            </tr>
            <tr>
                <td class="size-label">XL</td>
                <td>16-18</td>
                <td>42-44</td>
                <td>34-36</td>
                <td>44-46</td>
                <td>107-112</td>
                <td>86-91</td>
                <td>112-117</td>
            </tr>
        </tbody>
    </table>
    <div style="text-align: center; color: #B0C4CC; font-size: 0.6rem; margin-top: 0.8rem; letter-spacing: 0.5px;">
        *Ukuran standar wanita AS. Setiap merek mungkin memiliki variasi.
    </div>
</div>
""", unsafe_allow_html=True)

# ========== STATS BAR ==========
st.markdown(f"""
<div class="stats-bar">
    <span>Random Forest</span>
    <span class="stats-divider"></span>
    <span><span class="highlight">S · M · L · XL</span></span>
    <span class="stats-divider"></span>
    <span>{medians['height']:.0f}cm · {medians['waist']:.0f}in · {medians['hips']:.0f}in</span>
    <span class="stats-divider"></span>
    <span>756 Profil Bersih</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Antigravity AI · Prediktor Ukuran Premium
</div>
""", unsafe_allow_html=True)
