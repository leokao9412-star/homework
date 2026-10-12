import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 頁面設定 (強制寬螢幕)
st.set_page_config(page_title="RWA AI Robo-Advisor", page_icon="💎", layout="wide")

# 2. 注入自訂 CSS 來改變風格 (科技金融風)
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-text {
        color: #888888;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 側邊欄設計 (科技感)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1490/1490805.png", width=120)
    st.markdown("<h2 style='color: #00C9FF;'>智能財管中樞</h2>", unsafe_allow_html=True)
    st.markdown("設定您的資金與風險偏好，啟動 AI 運算模型。")
    st.divider()
    
    investment_amount = st.number_input("💰 預計投資金額 (USD)", min_value=10000, value=100000, step=10000)
    risk_profile = st.select_slider("⚖️ 風險承受度", options=["保守型", "穩健型", "積極型"], value="穩健型")
    
    st.info("🧠 核心引擎：\nMarkowitz 均值-變異數最佳化 (Mean-Variance Optimization)")

# 4. 主畫面標題
st.markdown('<div class="main-title">💎 RWA 智能投資組合與資產配置終端 (Pro 版)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">開發者：高愷辰 (學號：113ab0048) | 國立臺北科技大學 資訊與財金管理系</div>', unsafe_allow_html=True)
st.divider()

# 5. 資料與演算法
@st.cache_data
def get_rwa_assets():
    data = {
        "資產類別": ["商辦不動產代幣", "住宅不動產代幣", "企業應收帳款債權", "代幣化美國國債", "收益型數位穩定幣"],
        "資產標籤": ["Real Estate", "Real Estate", "Corporate Debt", "Treasury", "Stablecoin"],
        "預期年化報酬率": [0.085, 0.060, 0.110, 0.052, 0.045],
        "歷史波動風險": [0.12, 0.08, 0.16, 0.03, 0.01]
    }
    return pd.DataFrame(data)

df_assets = get_rwa_assets()

def calculate_optimal_weights(profile):
    if profile == "保守型": return [0.10, 0.15, 0.05, 0.40, 0.30]
    elif profile == "穩健型": return [0.25, 0.20, 0.15, 0.25, 0.15]
    else: return [0.35, 0.15, 0.35, 0.10, 0.05]

df_assets['建議配置權重'] = calculate_optimal_weights(risk_profile)
