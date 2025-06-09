import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 페이지 설정
st.set_page_config(
    page_title="글로벌 시가총액 Top 10 주가 분석",
    page_icon="📈",
    layout="wide"
)

st.title("📈 글로벌 시가총액 Top 10 기업 주가 분석")
st.markdown("---")

# 글로벌 시가총액 Top 10 기업 (2024년 기준)
TOP_10_COMPANIES = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'NVDA': 'NVIDIA Corporation',
    'GOOGL': 'Alphabet Inc. (Google)',
    'AMZN': 'Amazon.com Inc.',
    'META': 'Meta Platforms Inc.',
    'TSLA': 'Tesla Inc.',
    'BRK-B': 'Berkshire Hathaway Inc.',
    'AVGO': 'Broadcom Inc.',
    'JPM': 'JPMorgan Chase & Co.'
}

@st.cache_data(ttl=3600)  # 1시간 캐시
def fetch_stock_data(tickers, period='1y'):
    """주식 데이터를 가져오는 함수"""
    try:
        if isinstance(tickers, str):
            tickers = [tickers]
        
        data = {}
        failed_tickers = []
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                
                if hist.empty:
                    failed_tickers.append(ticker)
                    continue
                    
                data[ticker] = hist['Close']
                
            except Exception as e:
                st.warning(f"⚠️ {ticker} 데이터 가져오기 실패: {str(e)}")
                failed_tickers.append(ticker)
        
        if failed_tickers:
            st.error(f"❌ 다음 종목의 데이터를 가져올 수 없습니다: {', '.join(failed_tickers)}")
        
        if not data:
            st.error("❌ 선택된 종목의 데이터를 가져올 수 없습니다.")
            return None
            
        df = pd.DataFrame(data)
        return df
        
    except Exception as e:
        st.error(f"❌ 데이터 가져오기 중 오류 발생: {str(e)}")
        return None

def calculate_cumulative_returns(df):
    """누적 수익률 계산 함수"""
    try:
        returns = df.pct_change().fillna(0)
        cumulative_returns = (1 + returns).cumprod() - 1
        return cumulative_returns * 100  # 퍼센트로 변환
    except Exception as e:
        st.error(f"❌ 누적 수익률 계산 중 오류: {str(e)}")
        return None

def create_price_chart(df, selected_companies):
    """주가 차트 생성 함수"""
    try:
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set1
        
        for i, ticker in enumerate(df.columns):
            company_name = TOP_10_COMPANIES.get(ticker, ticker)
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[ticker],
                mode='lines',
                name=f'{company_name} ({ticker})',
                line=dict(color=color, width=2),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             '날짜: %{x}<br>' +
                             '주가: $%{y:,.2f}<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title={
                'text': f'📊 선택된 기업 주가 추이 (최근 1년)',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='날짜',
            yaxis_title='주가 (USD)',
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig
        
    except Exception as e:
        st.error(f"❌ 주가 차트 생성 중 오류: {str(e)}")
        return None

def create_returns_chart(cumulative_returns, selected_companies):
    """누적 수익률 차트 생성 함수"""
    try:
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set1
        
        for i, ticker in enumerate(cumulative_returns.columns):
            company_name = TOP_10_COMPANIES.get(ticker, ticker)
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatter(
                x=cumulative_returns.index,
                y=cumulative_returns[ticker],
                mode='lines',
                name=f'{company_name} ({ticker})',
                line=dict(color=color, width=2),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             '날짜: %{x}<br>' +
                             '누적 수익률: %{y:.2f}%<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title={
                'text': f'📈 선택된 기업 누적 수익률 (최근 1년)',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='날짜',
            yaxis_title='누적 수익률 (%)',
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # 0% 기준선 추가
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        return fig
        
    except Exception as e:
        st.error(f"❌ 누적 수익률 차트 생성 중 오류: {str(e)}")
        return None

def display_statistics(df, cumulative_returns):
    """통계 정보 표시 함수"""
    try:
        stats_data = []
        
        for ticker in df.columns:
            company_name = TOP_10_COMPANIES.get(ticker, ticker)
            
            # 통계 계산
            current_price = df[ticker].iloc[-1]
            start_price = df[ticker].iloc[0]
            total_return = ((current_price - start_price) / start_price) * 100
            
            daily_returns = df[ticker].pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252) * 100  # 연간 변동성
            
            max_price = df[ticker].max()
            min_price = df[ticker].min()
            
            stats_data.append({
                '기업명': f"{company_name} ({ticker})",
                '현재 주가': f"${current_price:.2f}",
                '총 수익률': f"{total_return:.2f}%",
                '연간 변동성': f"{volatility:.2f}%",
                '최고가': f"${max_price:.2f}",
                '최저가': f"${min_price:.2f}"
            })
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ 통계 정보 계산 중 오류: {str(e)}")

# 사이드바 - 기업 선택
st.sidebar.header("🏢 기업 선택")

# 선택 모드
selection_mode = st.sidebar.radio(
    "선택 모드:",
    ["단일 선택", "다중 선택"],
    index=1
)

if selection_mode == "단일 선택":
    # 단일 선택
    selected_ticker = st.sidebar.selectbox(
        "기업을 선택하세요:",
        options=list(TOP_10_COMPANIES.keys()),
        format_func=lambda x: f"{TOP_10_COMPANIES[x]} ({x})",
        index=0
    )
    selected_companies = [selected_ticker]
    
else:
    # 다중 선택
    selected_companies = st.sidebar.multiselect(
        "기업을 선택하세요 (복수 선택 가능):",
        options=list(TOP_10_COMPANIES.keys()),
        default=['AAPL', 'MSFT', 'NVDA'],
        format_func=lambda x: f"{TOP_10_COMPANIES[x]} ({x})"
    )

# 선택된 기업이 없는 경우 예외 처리
if not selected_companies:
    st.warning("⚠️ 최소 하나의 기업을 선택해주세요.")
    st.stop()

# 단일 선택인데 리스트가 비어있는 경우 예외 처리
if selection_mode == "단일 선택" and len(selected_companies) == 0:
    st.error("❌ 기업 선택에 오류가 발생했습니다. 페이지를 새로고침해주세요.")
    st.stop()

# 데이터 로딩
with st.spinner('📊 주식 데이터를 가져오는 중...'):
    stock_data = fetch_stock_data(selected_companies)

if stock_data is None or stock_data.empty:
    st.error("❌ 선택된 기업의 데이터를 가져올 수 없습니다. 다른 기업을 선택해주세요.")
    st.stop()

# 누적 수익률 계산
cumulative_returns = calculate_cumulative_returns(stock_data)

if cumulative_returns is None:
    st.error("❌ 누적 수익률 계산에 실패했습니다.")
    st.stop()

# 메인 대시보드
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📊 선택된 기업: {len(selected_companies)}개")
    
    # 선택된 기업 목록 표시
    selected_names = [f"{TOP_10_COMPANIES[ticker]} ({ticker})" for ticker in selected_companies]
    st.info(f"**분석 대상:** {', '.join(selected_names)}")

with col2:
    st.subheader("📅 분석 기간")
    st.info("**기간:** 최근 1년")
    st.info(f"**데이터 기준일:** {datetime.now().strftime('%Y-%m-%d')}")

# 차트 표시
st.markdown("---")

# 주가 차트
price_chart = create_price_chart(stock_data, selected_companies)
if price_chart:
    st.plotly_chart(price_chart, use_container_width=True)

# 누적 수익률 차트
returns_chart = create_returns_chart(cumulative_returns, selected_companies)
if returns_chart:
    st.plotly_chart(returns_chart, use_container_width=True)

# 통계 정보
st.markdown("---")
st.subheader("📊 주요 통계 정보")
display_statistics(stock_data, cumulative_returns)

# 추가 정보
st.markdown("---")
st.subheader("ℹ️ 주요 정보")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    **📋 분석 지표 설명:**
    - **총 수익률**: 1년간 주가 상승률
    - **연간 변동성**: 주가 변동의 위험도 지표
    - **최고가/최저가**: 1년간 최대/최소 주가
    """)

with info_col2:
    st.markdown("""
    **⚠️ 유의사항:**
    - 데이터는 Yahoo Finance에서 제공
    - 실시간 데이터가 아닐 수 있음
    - 투자 결정시 추가 분석 필요
    """)

# 데이터 다운로드 기능
st.markdown("---")
if st.button("📥 데이터 다운로드 (CSV)"):
    try:
        # 주가 데이터와 누적 수익률 데이터 합치기
        download_data = pd.concat([
            stock_data.add_suffix('_Price'),
            cumulative_returns.add_suffix('_CumReturn(%)')
        ], axis=1)
        
        csv = download_data.to_csv()
        st.download_button(
            label="CSV 파일 다운로드",
            data=csv,
            file_name=f"stock_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        st.success("✅ 다운로드 준비가 완료되었습니다!")
        
    except Exception as e:
        st.error(f"❌ 다운로드 준비 중 오류: {str(e)}")

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    📈 글로벌 시가총액 Top 10 기업 주가 분석 대시보드<br>
    데이터 제공: Yahoo Finance | 개발: Streamlit + Plotly
    </div>
    """, 
    unsafe_allow_html=True
)
