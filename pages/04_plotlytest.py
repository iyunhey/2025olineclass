pip install streamlit plotly pandas
import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 로딩 (cp949 인코딩)
@st.cache_data
def load_data():
    df = pd.read_csv("people_gender.csv.csv", encoding='cp949')
    return df

df = load_data()

# 컬럼명 확인 후 전처리
df.columns = [col.strip() for col in df.columns]  # 공백 제거
지역_리스트 = df['행정구역'].unique()

# Streamlit UI
st.title("지역별 성별 인구 피라미드")
선택_지역 = st.selectbox("지역을 선택하세요", 지역_리스트)

최소_나이, 최대_나이 = st.slider("연령대를 선택하세요", 0, 100, (0, 100), step=5)

# 선택 지역 데이터 필터링
filtered_df = df[df['행정구역'] == 선택_지역]

# 연령 컬럼 추출
filtered_df = filtered_df[(filtered_df['나이'] >= 최소_나이) & (filtered_df['나이'] <= 최대_나이)]

# 성별 피라미드용 값 처리
filtered_df['남자'] = -filtered_df['남자']  # 피라미드 좌측 표시용

fig = px.bar(
    filtered_df,
    x='남자',
    y='나이',
    orientation='h',
    color_discrete_sequence=['blue'],
    labels={'남자': '남성 인구수'},
    title=f"{선택_지역} 남성 인구 피라미드"
)

fig.add_bar(
    x=filtered_df['여자'],
    y=filtered_df['나이'],
    orientation='h',
    name='여자',
    marker_color='pink'
)

fig.update_layout(
    barmode='overlay',
    xaxis=dict(title='인구수', tickvals=[-10000, -5000, 0, 5000, 10000]),
    yaxis=dict(title='나이'),
    font=dict(family="NanumGothic, Malgun Gothic, sans-serif"),
    title_font=dict(size=20),
    height=800
)

st.plotly_chart(fig)
