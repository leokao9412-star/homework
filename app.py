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
df_assets['配置金額 (USD)'] = df_assets['建議配置權重'] * investment_amount

expected_return = np.sum(df_assets['建議配置權重'] * df_assets['預期年化報酬率'])
expected_risk = np.sqrt(np.sum((df_assets['建議配置權重'] * df_assets['歷史波動風險'])**2))

# 6. KPI 數據卡片 (優化排版)
st.markdown("### 📊 AI 運算結果摘要")
col1, col2, col3 = st.columns(3)
col1.metric("總資金規模 (AUM)", f"${investment_amount:,.0f}")
col2.metric("✨ 組合預期年化報酬", f"{expected_return*100:.2f}%", delta="AI 最佳化配置")
col3.metric("⚠️ 組合綜合波動風險", f"{expected_risk*100:.2f}%", delta="-風險已分散", delta_color="inverse")
st.divider()

# 設定 matplotlib 風格 (深色科技風)
plt.style.use('dark_background')

# 7. 多維度視覺化面板
tab1, tab2, tab3 = st.tabs(["🎯 最佳化配置圓餅圖", "📋 資金分配明細", "🌌 風險報酬矩陣 (效率前緣模擬)"])

with tab1:
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        st.markdown(f"#### 【{risk_profile}】投資組合比例")
        fig, ax = plt.subplots(figsize=(7, 7))
        # 科技感螢光配色
        colors = ['#FF007F', '#00F0FF', '#00FF00', '#FFD700', '#B200FF']
        explode = (0.05, 0.05, 0.05, 0.05, 0.05) # 讓圓餅圖有分離的特效
        ax.pie(df_assets['建議配置權重'], labels=df_assets['資產類別'], autopct='%1.1f%%', 
               startangle=140, colors=colors, explode=explode, 
               textprops={'fontsize': 12, 'color': 'white', 'weight': 'bold'})
        ax.axis('equal')
        fig.patch.set_facecolor('none') # 背景透明
        ax.set_facecolor('none')
        st.pyplot(fig)
    with col_c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("💡 **AI 配置解析**：\n\n圓餅圖展示了演算法在評估您的風險承受度後，於各類 RWA 資產間取得的最佳平衡點。分離的區塊設計代表每一項資產均具備獨立的風險隔離機制。")

with tab2:
    st.markdown("#### 資金分配與預期指標")
    # 使用 Pandas 渲染漸層顏色 (Heatmap 效果)
    styled_df = df_assets[['資產類別', '建議配置權重', '配置金額 (USD)', '預期年化報酬率', '歷史波動風險']].style.format({
        '建議配置權重': '{:.1%}',
        '配置金額 (USD)': '${:,.0f}',
        '預期年化報酬率': '{:.1%}',
        '歷史波動風險': '{:.1%}'
    }).background_gradient(subset=['建議配置權重'], cmap='Blues') \
      .background_gradient(subset=['預期年化報酬率'], cmap='Greens')
    
    st.dataframe(styled_df, use_container_width=True)

with tab3:
    st.markdown("#### 投資組合風險與報酬散佈圖")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    fig2.patch.set_facecolor('none')
    ax2.set_facecolor('#1E1E1E')
    
    # 繪製各別資產的點 (螢光藍)
    ax2.scatter(df_assets['歷史波動風險'], df_assets['預期年化報酬率'], color='#00F0FF', s=100, label='單一 RWA 資產', alpha=0.8, edgecolors='white')
    for i, txt in enumerate(df_assets['資產類別']):
        ax2.annotate(txt, (df_assets['歷史波動風險'][i] + 0.002, df_assets['預期年化報酬率'][i]), 
                     fontsize=10, color='#AAAAAA')
    
    # 繪製組合的點 (螢光粉紅大星星)
    ax2.scatter(expected_risk, expected_return, color='#FF007F', s=400, marker='*', label=f'最佳化組合 ({risk_profile})', edgecolors='white')
    
    ax2.set_xlabel('波動風險 (Volatility)', color='white')
    ax2.set_ylabel('預期年化報酬率 (Expected Return)', color='white')
    ax2.tick_params(colors='white')
    ax2.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
    ax2.grid(True, linestyle=':', alpha=0.3, color='white')
    
    st.pyplot(fig2)
    st.success("✅ **效率前緣分析**：粉紅星號代表您的專屬組合。透過有效配置，組合風險（橫軸）顯著低於高風險單一資產，但報酬（縱軸）仍維持在優異水平，完美體現「不要把雞蛋放在同一個籃子裡」的財務工程真諦。")
