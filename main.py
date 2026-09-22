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

    # 여러 장르가 |로 구분되어 있는 경우 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    # 총 관객을 숫자로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    )

    return df

df = load_data()

st.write(f"총 **{len(df)}편**의 영화 데이터를 분석합니다.")

# --------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수
# --------------------------------------------------

st.divider()
st.subheader("📊 1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

fig1 = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="label+percent",
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

fig1.update_layout(
    legend_title="장르",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")
st.info(
    "여기에 장르별 영화 편수와 전체에서 차지하는 비율을 통해 "
    "어떤 장르의 영화가 많이 포함되어 있는지 설명하세요."
)

# --------------------------------------------------
# 두 번째 그래프: 장르별 영화 트리맵
# --------------------------------------------------

st.divider()
st.subheader("🌳 2. 장르별 영화 총 관객 트리맵")

treemap_data = df.dropna(subset=["total_audi"]).copy()

fig2 = px.treemap(
    treemap_data,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객",
    custom_data=["movieNm", "total_audi"]
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b>"
        "<br>총 관객: %{customdata[1]:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")
st.info(
    "여기에 각 장르에서 어떤 영화가 많은 관객을 기록했는지와 "
    "영화별 총 관객 규모의 차이를 설명하세요."
)
