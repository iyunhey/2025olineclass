import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 지역별 연령대 인구 시각화")

# 📁 데이터 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (cp949 인코딩)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="cp949")
    
    # 📍 지역 선택
    region = st.selectbox("📍 지역을 선택하세요", df['행정구역'].unique())
    
    # ✅ 연령 구간 컬럼만 필터링
    age_cols = [col for col in df.columns if '세' in col and '계' in col]
    age_labels = [col.split('_')[-1] for col in age_cols]  # ex) 0~9세, 10~19세...

    # 🎚️ 연령 구간 슬라이더
    selected_range = st.slider(
        "🎚️ 시각화할 연령 구간을 선택하세요",
        min_value=0,
        max_value=len(age_labels)-1,
        value=(0, len(age_labels)-1),
        format="%d단계"
    )

    # 📌 선택 지역 행 가져오기
    row = df[df['행정구역'] == region].iloc[0]

    # 🧹 인구 수 전처리
    selected_labels = age_labels[selected_range[0]:selected_range[1]+1]
    selected_cols = age_cols[selected_range[0]:selected_range[1]+1]
    population = row[selected_cols].astype(str).str.replace(',', '').astype(int)

    # 📊 데이터프레임 구성
    df_plot = pd.DataFrame({
        "연령구간": selected_labels,
        "인구수": population
    })

    # 📈 시각화
    fig = px.bar(
        df_plot,
        x="연령구간",
        y="인구수",
        title=f"{region} 지역 연령대별 인구 수",
        labels={"연령구간": "연령 구간", "인구수": "인구 수"},
        color_discrete_sequence=["#636EFA"]
    )

    fig.update_layout(
        font=dict(family="Malgun Gothic, NanumGothic, sans-serif"),
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig)

else:
    st.info("👆 위에서 CSV 파일을 업로드해주세요.")
