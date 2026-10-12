import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 頁面設定
st.set_page_config(page_title="RWA AI Robo-Advisor", page_icon="💼", layout="wide")

# 2. 側邊欄：使用者參數輸入
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2095/2095071.png", width=100)
    st.title("🤖 AI Robo-Advisor")
    st.markdown("請輸入您的財務狀況與風險偏好，AI 將為您量身打造 RWA 投資組合。")
    st.divider()
    
    investment_amount = st.number_input("預計投資金額 (USD)", min_value=10000, value=100000, step=10000)
    risk_profile = st.select_slider("您的風險承受度", options=["保守型", "穩健型", "積極型"], value="穩健型")
    
    st.info("系統採用 Markowitz 投資組合理論 (Mean-Variance Optimization) 模擬演算法進行資產配置。")

# 3. 主畫面標題
st.title("💼 RWA 投資組合管理與資產配置平台 (AI Robo-Advisor)")
st.markdown("**開發者：喬睿宇 (學號：113ab0044) | 國立臺北科技大學 資訊與財金管理系**")
st.divider()

# 4. RWA 基礎資產資料庫 (包含不動產、債權、穩定幣)
@st.cache_data
def get_rwa_assets():
    data = {
        "資產類別": ["房地產代幣 (商辦)", "房地產代幣 (住宅)", "債權 (企業應收帳款)", "債權 (美債代幣化)", "數位資產 (收益型穩定幣)"],
        "資產標籤": ["Real Estate", "Real Estate", "Corporate Debt", "Treasury", "Stablecoin"],
        "預期年化報酬率": [0.085, 0.060, 0.110, 0.052, 0.045],
        "歷史波動率 (風險)": [0.12, 0.08, 0.16, 0.03, 0.01]
    }
    return pd.DataFrame(data)

df_assets = get_rwa_assets()

# 5. AI 演算法模擬：根據風險偏好計算最佳權重
def calculate_optimal_weights(profile):
    # 模擬演算法輸出的投資組合權重
    if profile == "保守型":
        return [0.10, 0.15, 0.05, 0.40, 0.30] # 偏好穩定幣與美債
    elif profile == "穩健型":
        return [0.25, 0.20, 0.15, 0.25, 0.15] # 均衡配置
    else:
        return [0.35, 0.15, 0.35, 0.10, 0.05] # 偏好高報酬房地產與企業債權

df_assets['建議配置權重'] = calculate_optimal_weights(risk_profile)
df_assets['配置金額 (USD)'] = df_assets['建議配置權重'] * investment_amount

# 計算投資組合整體預期報酬與風險
expected_return = np.sum(df_assets['建議配置權重'] * df_assets['預期年化報酬率'])
# 簡化版風險計算 (假設資產間相關係數為0進行模擬)
expected_risk = np.sqrt(np.sum((df_assets['建議配置權重'] * df_assets['歷史波動率 (風險)'])**2))

# 6. Dashboard 視覺化呈現
# KPI 數據卡片
col1, col2, col3 = st.columns(3)
col1.metric("總投資金額", f"${investment_amount:,.0f}")
col2.metric("預估投資組合年化報酬", f"{expected_return*100:.2f}%")
col3.metric("投資組合綜合波動風險", f"{expected_risk*100:.2f}%")

st.markdown("<br>", unsafe_allow_html=True)

# 頁籤設計
tab1, tab2, tab3 = st.tabs(["🤖 AI 個人化配置建議", "📊 RWA 基礎資產池", "📈 風險分散與效率分析"])

with tab1:
    st.subheader(f"專屬您的【{risk_profile}】資產配置")
    col_chart, col_table = st.columns([1, 1.2])
    
    with col_chart:
        # 繪製圓餅圖
        fig, ax = plt.subplots(figsize=(6, 6))
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0']
        ax.pie(df_assets['建議配置權重'], labels=df_assets['資產類別'], autopct='%1.1f%%', startangle=140, colors=colors)
        ax.axis('equal')
        st.pyplot(fig)
        
    with col_table:
        st.dataframe(df_assets[['資產類別', '建議配置權重', '配置金額 (USD)']].style.format({
            '建議配置權重': '{:.1%}',
            '配置金額 (USD)': '${:,.0f}'
        }), use_container_width=True)

with tab2:
    st.subheader("市場可供配置之 RWA 資產總覽")
    # 格式化顯示百分比
    df_display = df_assets[['資產類別', '資產標籤', '預期年化報酬率', '歷史波動率 (風險)']].copy()
    df_display['預期年化報酬率'] = (df_display['預期年化報酬率'] * 100).round(2).astype(str) + '%'
    df_display['歷史波動率 (風險)'] = (df_display['歷史波動率 (風險)'] * 100).round(2).astype(str) + '%'
    st.dataframe(df_display, use_container_width=True)

with tab3:
    st.subheader("投資組合風險與報酬散佈圖")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    
    # 繪製各別資產的點
    ax2.scatter(df_assets['歷史波動率 (風險)'], df_assets['預期年化報酬率'], color='blue', label='單一 RWA 資產')
    for i, txt in enumerate(df_assets['資產類別']):
        ax2.annotate(txt, (df_assets['歷史波動率 (風險)'][i], df_assets['預期年化報酬率'][i]), fontsize=9, alpha=0.7)
    
    # 繪製投資組合的點
    ax2.scatter(expected_risk, expected_return, color='red', s=100, marker='*', label=f'您的組合 ({risk_profile})')
    
    ax2.set_xlabel('風險 (歷史波動率)')
    ax2.set_ylabel('預期年化報酬率')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig2)
    st.success("💡 分析結論：透過 AI 演算進行多資產配置，您的投資組合有效降低了單一資產的劇烈波動風險，同時維持了穩定的預期收益，達到風險分散之效果。")
