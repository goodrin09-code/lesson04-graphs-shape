import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 제목
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 여러 장르가 세로막대(|)로 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].fillna("미상").astype(str).str.split("|").str[0]

    return df

df = load_data()

st.write(f"총 **{len(df)}편**의 영화 데이터를 분석합니다.")

st.divider()

# --------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수
# --------------------------------------------------

st.subheader("📊 1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

fig = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="label+percent",
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

fig.update_layout(
    legend_title="장르",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig, use_container_width=True)

# 그래프 설명 영역
st.markdown("#### 💡 이 그래프로 알 수 있는 것")
st.info("여기에 장르별 영화 편수와 전체에서 차지하는 비율을 통해 어떤 장르의 영화가 많이 포함되어 있는지 설명하세요.")

st.divider()
