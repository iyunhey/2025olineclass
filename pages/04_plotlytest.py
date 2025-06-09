import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 지역별 성별 인구 피라미드")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (cp949 인코딩)", type=["csv"])
if uploaded_file:
    # 파일 읽기
    df = pd.read_csv(uploaded_file, encoding='cp949')

    # 컬럼 공백 제거
    df.columns = [col.strip() for col in df.columns]

    # 필수 컬럼 체크
    필수컬럼 = {'행정구역', '나이', '남자', '여자'}
    if not 필수컬럼.issubset(set(df.columns)):
        st.error("⚠️ CSV 파일에 '행정구역', '나이', '남자', '여자' 컬럼이 포함되어 있어야 합니다.")
    else:
        # 지역 선택
        지역_리스트 = df['행정구역'].unique()
        선택_지역 = st.selectbox("지역을 선택하세요", 지역_리스트)

        # 연령대 선택
        최소_나이, 최대_나이 = st.slider("연령대를 선택하세요", 0, 100, (0, 100), step=5)

        # 데이터 필터링
        필터 = (df['행정구역'] == 선택_지역) & (df['나이'] >= 최소_나이) & (df['나이'] <= 최대_나이)
        filtered_df = df[필터].copy()
        filtered_df['남자'] = -filtered_df['남자']  # 피라미드 좌측

        # plotly 시각화
        fig = px.bar(
            filtered_df,
            x='남자',
            y='나이',
            orientation='h',
            labels={'남자': '남성'},
            color_discrete_sequence=['#1f77b4'],
            title=f"{선택_지역} 인구 피라미드"
        )

        fig.add_bar(
            x=filtered_df['여자'],
            y=filtered_df['나이'],
            orientation='h',
            name='여자',
            marker_color='#ff69b4'
        )

        fig.update_layout(
            barmode='overlay',
            xaxis=dict(title='인구수', tickvals=[-10000, -5000, 0, 5000, 10000]),
            yaxis=dict(title='나이'),
            font=dict(family="Malgun Gothic, NanumGothic, sans-serif"),
            height=800
        )

        st.plotly_chart(fig)
else:
    st.info("👆 왼쪽에서 CSV 파일을 업로드해 주세요.")
