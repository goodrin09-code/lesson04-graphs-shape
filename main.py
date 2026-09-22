import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# 페이지 설정
# ==================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")


# ==================================================
# 데이터 불러오기
# ==================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 여러 장르가 |로 구분되어 있으면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    # 숫자형 데이터로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    )

    df["first_scrn"] = pd.to_numeric(
        df["first_scrn"],
        errors="coerce"
    )

    return df


df = load_data()

st.write(f"총 **{len(df)}편**의 영화 데이터를 분석합니다.")


# ==================================================
# 1. 장르별 영화 편수 - 도넛 그래프
# ==================================================

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
    hovertemplate=(
        "<b>%{label}</b>"
        "<br>영화 편수: %{value}편"
        "<br>비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    legend_title="장르",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "여기에 장르별 영화 편수와 전체에서 차지하는 비율을 통해 "
    "어떤 장르의 영화가 많이 포함되어 있는지 설명하세요."
)


# ==================================================
# 2. 장르별 영화 총 관객 - 트리맵
# ==================================================

st.divider()

st.subheader("🌳 2. 장르별 영화 총 관객 트리맵")

treemap_data = df.dropna(
    subset=["total_audi", "movieNm"]
).copy()


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

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "여기에 각 장르에서 어떤 영화가 많은 관객을 기록했는지와 "
    "영화별 총 관객 규모의 차이를 설명하세요."
)


# ==================================================
# 3. 영화별 총 관객 분포 - 히스토그램
# ==================================================

st.divider()

st.subheader("📈 3. 영화별 총 관객 분포")

hist_data = df.dropna(
    subset=["total_audi"]
).copy()


fig3 = px.histogram(
    hist_data,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객(명)",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="총 관객(명)",
    yaxis_title="영화 편수",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# ==================================================
# 3번 그래프 설명
# ==================================================

min_audi = hist_data["total_audi"].min()
max_audi = hist_data["total_audi"].max()

bin_width = (max_audi - min_audi) / 20

if bin_width == 0:
    most_common_start = int(min_audi)
    most_common_end = int(max_audi)

else:
    bin_numbers = (
        (hist_data["total_audi"] - min_audi)
        / bin_width
    ).astype(int)

    most_common_bin = bin_numbers.value_counts().idxmax()

    most_common_start = int(
        min_audi + most_common_bin * bin_width
    )

    most_common_end = int(
        min_audi + (most_common_bin + 1) * bin_width
    )


top_movie = hist_data.loc[
    hist_data["total_audi"].idxmax()
]


st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    f"대부분의 영화는 총 관객 "
    f"**{most_common_start:,}명~{most_common_end:,}명 구간**에 "
    f"몰려 있으며, 총 관객이 가장 많은 영화는 "
    f"**{top_movie['movieNm']}**"
    f"({int(top_movie['total_audi']):,}명)입니다."
)


# ==================================================
# 4. 개봉일 스크린 수와 총 관객의 관계 - 산점도
# ==================================================

st.divider()

st.subheader("🔵 4. 개봉일 스크린 수와 총 관객의 관계")

scatter_data = df.dropna(
    subset=["first_scrn", "total_audi", "movieNm", "genre"]
).copy()


fig4 = px.scatter(
    scatter_data,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객(명)",
        "genre": "장르"
    }
)

fig4.update_traces(
    marker=dict(
        size=9,
        opacity=0.75
    )
)

fig4.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객(명)",
    legend_title="장르",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "개봉일 스크린 수와 총 관객의 관계를 살펴보고, "
    "스크린 수가 많은 영화일수록 총 관객도 많은 경향이 나타나는지 확인할 수 있습니다."
)
