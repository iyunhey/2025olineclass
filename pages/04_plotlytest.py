import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="경기도 인구 데이터 시각화",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    """데이터 로드 및 전처리"""
    try:
        # CP-949 인코딩으로 파일 읽기
        df = pd.read_csv('people_sum.cvs.csv', encoding='cp949')
    except:
        # 다른 인코딩으로 시도
        try:
            df = pd.read_csv('people_sum.cvs.csv', encoding='utf-8')
        except:
            df = pd.read_csv('people_sum.cvs.csv', encoding='euc-kr')
    
    # 컬럼명 정리
    df.columns = df.columns.str.strip()
    
    # 연령대별 컬럼 추출 (0세~100세 이상)
    age_cols = [col for col in df.columns if '세' in col or '세' in col]
    
    # 데이터 타입 변환
    numeric_cols = ['2025년05월_전체_총인구수', '2025년05월_전체_연령구간인구수'] + age_cols
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
    
    return df

def create_age_pyramid(df, selected_region, age_range):
    """인구 피라미드 생성"""
    # 선택된 지역 데이터 필터링
    region_data = df[df['행정구역'] == selected_region].iloc[0]
    
    # 연령대별 데이터 추출
    age_data = []
    for i in range(101):  # 0세부터 100세 이상까지
        if i == 100:
            col_name = f'2025년05월_전체_100세 이상'
        else:
            col_name = f'2025년05월_전체_{i}세'
        
        if col_name in region_data:
            age_data.append({
                'age': i,
                'population': region_data[col_name] if pd.notna(region_data[col_name]) else 0
            })
    
    age_df = pd.DataFrame(age_data)
    
    # 연령대 필터링
    age_df = age_df[(age_df['age'] >= age_range[0]) & (age_df['age'] <= age_range[1])]
    
    # 인구 피라미드 생성 (성별 구분이 없으므로 전체 인구로 표시)
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=age_df['age'],
        x=age_df['population'],
        orientation='h',
        name='인구수',
        marker_color='skyblue',
        text=age_df['population'],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f'{selected_region} 연령별 인구 분포',
        xaxis_title='인구수',
        yaxis_title='연령',
        height=600,
        showlegend=False
    )
    
    return fig

def create_age_group_chart(df, selected_region):
    """연령대별 그룹 차트 생성"""
    region_data = df[df['행정구역'] == selected_region].iloc[0]
    
    # 연령대 그룹 정의
    age_groups = {
        '유아 (0-4세)': list(range(0, 5)),
        '아동 (5-9세)': list(range(5, 10)),
        '청소년 (10-19세)': list(range(10, 20)),
        '청년 (20-29세)': list(range(20, 30)),
        '중년 (30-49세)': list(range(30, 50)),
        '장년 (50-64세)': list(range(50, 65)),
        '고령자 (65세 이상)': list(range(65, 101))
    }
    
    group_data = []
    for group_name, ages in age_groups.items():
        total_pop = 0
        for age in ages:
            if age == 100:
                col_name = f'2025년05월_전체_100세 이상'
            else:
                col_name = f'2025년05월_전체_{age}세'
            
            if col_name in region_data:
                pop = region_data[col_name] if pd.notna(region_data[col_name]) else 0
                total_pop += pop
        
        group_data.append({
            'age_group': group_name,
            'population': total_pop
        })
    
    group_df = pd.DataFrame(group_data)
    
    fig = px.bar(
        group_df,
        x='age_group',
        y='population',
        title=f'{selected_region} 연령대별 인구 분포',
        color='population',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        xaxis_title='연령대',
        yaxis_title='인구수',
        height=500
    )
    
    return fig

def create_comparison_chart(df, selected_regions):
    """지역별 비교 차트"""
    comparison_data = []
    
    for region in selected_regions:
        region_data = df[df['행정구역'] == region].iloc[0]
        total_pop = region_data['2025년05월_전체_총인구수'] if pd.notna(region_data['2025년05월_전체_총인구수']) else 0
        
        comparison_data.append({
            'region': region,
            'total_population': total_pop
        })
    
    comp_df = pd.DataFrame(comparison_data)
    
    fig = px.bar(
        comp_df,
        x='region',
        y='total_population',
        title='지역별 총 인구 비교',
        color='total_population',
        color_continuous_scale='plasma'
    )
    
    fig.update_layout(
        xaxis_title='지역',
        yaxis_title='총 인구수',
        height=500
    )
    
    return fig

def main():
    st.title("📊 경기도 인구 데이터 시각화")
    st.markdown("---")
    
    # 데이터 로드
    with st.spinner('데이터를 로드하는 중...'):
        df = load_data()
    
    # 사이드바 설정
    st.sidebar.header("🔧 설정")
    
    # 지역 선택
    regions = df['행정구역'].unique().tolist()
    selected_region = st.sidebar.selectbox(
        "📍 지역 선택",
        regions,
        index=0
    )
    
    # 연령대 슬라이더
    age_range = st.sidebar.slider(
        "📅 연령대 범위",
        min_value=0,
        max_value=100,
        value=(0, 100),
        step=1
    )
    
    # 메인 콘텐츠
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"🏘️ {selected_region} 인구 현황")
        
        # 기본 통계 정보
        region_data = df[df['행정구역'] == selected_region].iloc[0]
        total_pop = region_data['2025년05월_전체_총인구수'] if pd.notna(region_data['2025년05월_전체_총인구수']) else 0
        
        st.metric("총 인구", f"{total_pop:,}명")
    
    with col2:
        st.subheader("📈 시각화 옵션")
        chart_type = st.radio(
            "차트 유형 선택",
            ["인구 피라미드", "연령대별 분포", "지역별 비교"]
        )
    
    st.markdown("---")
    
    # 차트 표시
    if chart_type == "인구 피라미드":
        st.subheader("👥 인구 피라미드")
        fig = create_age_pyramid(df, selected_region, age_range)
        st.plotly_chart(fig, use_container_width=True)
        
        # 연령대별 상세 정보
        with st.expander("📊 연령대별 상세 정보"):
            region_data = df[df['행정구역'] == selected_region].iloc[0]
            
            # 선택된 연령 범위의 데이터만 표시
            age_detail = []
            for age in range(age_range[0], min(age_range[1] + 1, 101)):
                if age == 100:
                    col_name = f'2025년05월_전체_100세 이상'
                else:
                    col_name = f'2025년05월_전체_{age}세'
                
                if col_name in region_data:
                    pop = region_data[col_name] if pd.notna(region_data[col_name]) else 0
                    age_detail.append({
                        '연령': f"{age}세" if age < 100 else "100세 이상",
                        '인구수': f"{pop:,}명"
                    })
            
            detail_df = pd.DataFrame(age_detail)
            st.dataframe(detail_df, use_container_width=True)
    
    elif chart_type == "연령대별 분포":
        st.subheader("📊 연령대별 인구 분포")
        fig = create_age_group_chart(df, selected_region)
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "지역별 비교":
        st.subheader("🔍 지역별 인구 비교")
        
        # 비교할 지역 선택
        selected_regions = st.multiselect(
            "비교할 지역을 선택하세요",
            regions,
            default=[selected_region]
        )
        
        if len(selected_regions) > 1:
            fig = create_comparison_chart(df, selected_regions)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("비교를 위해 2개 이상의 지역을 선택해주세요.")
    
    # 데이터 테이블
    st.markdown("---")
    with st.expander("📋 원본 데이터 보기"):
        st.dataframe(df, use_container_width=True)
    
    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888;'>
            <p>📊 경기도 인구 데이터 시각화 대시보드</p>
            <p>데이터 기준: 2025년 05월</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
