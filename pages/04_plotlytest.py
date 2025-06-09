import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 인구 통계 시각화")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (cp949 인코딩)", type=["csv"])
if uploaded_file:
    # 데이터 로딩
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except UnicodeDecodeError:
        st.error("📛 파일 인코딩이 cp949가 아닙니다.")
        st.stop()

    df.columns = [col.strip() for col in df.columns]  # 공백 제거
    컬럼집합 = set(df.columns)

    # 1️⃣ 인구 피라미드용
    if {'행정구역', '나이', '남자', '여자'}.issubset(컬럼집합):
        st.subheader("🧍‍♂️🧍‍♀️ 성별/연령별 인구 피라미드")
        지역_리스트 = df['행정구역'].unique()
        선택_지역 = st.selectbox("지역 선택", 지역_리스트)
        최소_나이, 최대_나이 = st.slider("연령 범위 선택", 0, 100, (0, 100), step=5)

        필터 = (df['행정구역'] == 선택_지역) & (df['나이'] >= 최소_나이) & (df['나이'] <= 최대_나이)
        filtered_df = df[필터].copy()
        filtered_df['남자'] = -filtered_df['남자']  # 좌측 표현

        fig = px.bar(
            filtered_df,
            x='남자',
            y='나이',
            orientation='h',
            color_discrete_sequence=['#1f77b4'],
            labels={'남자': '남성'},
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

    # 2️⃣ 전체 인구 요약 시각화용
    elif {'행정구역', '총인구수', '남자', '여자'}.issubset(컬럼집합):
        st.subheader("🏙️ 지역별 총인구 시각화")

        # 남녀 비율 계산
        df['여성비율'] = df['여자'] / df['총인구수'] * 100
        df['남성비율'] = df['남자'] / df['총인구수'] * 100

        fig = px.bar(
            df,
            x='행정구역',
            y='총인구수',
            color='행정구역',
            title='지역별 총인구수',
            labels={'총인구수': '총인구'},
            text='총인구수'
        )

        fig.update_layout(
            font=dict(family="Malgun Gothic, NanumGothic, sans-serif"),
            xaxis_tickangle=-45,
            height=600
        )
        st.plotly_chart(fig)

        st.subheader("🧮 성별 비율 비교")
        fig2 = px.bar(
            df.melt(id_vars='행정구역', value_vars=['남성비율', '여성비율']),
            x='행정구역',
            y='value',
            color='variable',
            barmode='group',
            labels={'value': '비율(%)'},
            title='지역별 남녀 인구 비율'
        )
        fig2.update_layout(
            font=dict(family="Malgun Gothic, NanumGothic, sans-serif"),
            height=600
        )
        st.plotly_chart(fig2)

    else:
        st.warning("⚠️ 업로드한 CSV는 지원하는 형식이 아닙니다.\n필수 컬럼 조합:\n- 피라미드용: '행정구역', '나이', '남자', '여자'\n- 요약용: '행정구역', '총인구수', '남자', '여자'")

else:
    st.info("👆 왼쪽 사이드바 또는 위에서 CSV 파일을 업로드해 주세요.")

