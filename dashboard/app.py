"""
Interactive Streamlit dashboard for the Summer Olympics medal-tally project
(1896-2016). Reads the cleaned country-edition panel and offers three views:
overview map/leaderboard, continental trends, and host/efficiency analysis.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="120 Years of Olympic Medals", layout="wide", page_icon="🏅")

GREY, BLUE, ORANGE, GREEN, VERMILLION, SKY, PURPLE = (
    "#B0B0B0", "#0072B2", "#E69F00", "#009E73", "#D55E00", "#56B4E9", "#CC79A7",
)
CONTINENT_COLORS = {
    "Europe": BLUE, "Americas": VERMILLION, "Asia": GREEN,
    "Africa": ORANGE, "Oceania": PURPLE, "Mixed/Other": GREY,
}
TEMPLATE = "plotly_white"

# Country names that need remapping for Plotly's built-in choropleth
# ("country names" locationmode expects modern, ISO-recognisable names).
CHOROPLETH_NAME_FIX = {
    "United States": "United States of America", "Russian Federation": "Russia",
    "Republic of Korea": "South Korea", "Democratic People's Republic of Korea": "North Korea",
    "Islamic Republic of Iran": "Iran", "Czechia": "Czech Republic", "Türkiye": "Turkey",
    "Great Britain": "United Kingdom", "People's Republic of China": "China",
    "United Republic of Tanzania": "Tanzania", "Syrian Arab Republic": "Syria",
    "The Bahamas": "Bahamas", "Côte d'Ivoire": "Ivory Coast",
    "Kingdom of Saudi Arabia": "Saudi Arabia", "Republic of Moldova": "Moldova",
}


@st.cache_data
def load_data():
    df = pd.read_csv("../data/clean_olympics_1896_2016.csv")
    df["choropleth_country"] = df["country"].replace(CHOROPLETH_NAME_FIX)
    return df


df = load_data()

st.title("🏅 120 Years of the Summer Olympics (1896-2016)")
st.caption(
    "Country-edition medal tallies across 28 Games, enriched with continent, host-nation, "
    "era and defunct-entity flags. Data note: the 2016 edition is missing ~40 low-medal "
    "countries in the source file (see sidebar) — every totals-dependent view below is "
    "footnoted where this matters."
)

# ---------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------
st.sidebar.header("Filters")

year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max), step=4)

continents = sorted(df["continent"].unique())
selected_continents = st.sidebar.multiselect("Continents", continents, default=continents)

countries = sorted(df["country"].unique())
highlight_country = st.sidebar.selectbox(
    "Highlight a country in the Trends tab", countries,
    index=countries.index("United States") if "United States" in countries else 0,
)

exclude_2016 = st.sidebar.checkbox(
    "Exclude 2016 from country-count charts (recommended — see data note)", value=True,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Data note:** the 2016 Rio source file captured every country of real consequence "
    "(down to 8 total medals) but is missing ~40 additional low-medal NOCs. Top-country "
    "and host-boost views are unaffected; country-*count* views can be toggled to exclude it."
)

mask = (df["year"] >= year_range[0]) & (df["year"] <= year_range[1]) & (df["continent"].isin(selected_continents))
fdf = df[mask].copy()

count_df = fdf[fdf["edition_data_complete"]] if exclude_2016 else fdf

tab1, tab2, tab3 = st.tabs(["🗺️ Overview", "📈 Continental Trends", "🏅 Host & Efficiency"])

# =====================================================================
# TAB 1: Overview
# =====================================================================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Editions in view", fdf["year"].nunique())
    col2.metric("Countries with a medal", fdf["country_noc"].nunique())
    col3.metric("Total medals awarded", int(fdf["total"].sum()))
    top_country = fdf.groupby("country")["total"].sum().idxmax() if len(fdf) else "-"
    col4.metric("Top country in view", top_country)

    st.subheader("Career medal totals by country (map)")
    map_totals = fdf.groupby(["country", "choropleth_country"])["total"].sum().reset_index()
    fig_map = px.choropleth(
        map_totals, locations="choropleth_country", locationmode="country names", color="total",
        color_continuous_scale=["#F2F2F2", SKY, BLUE], template=TEMPLATE,
        labels={"total": "Total medals"},
        title="Total medals won, filtered to the selected years and continents",
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Top 15 countries")
        top15 = fdf.groupby(["country", "continent"])["total"].sum().nlargest(15, keep="all").reset_index()
        top15 = top15.sort_values("total")
        fig_top = px.bar(top15, x="total", y="country", orientation="h", color="continent",
                          color_discrete_map=CONTINENT_COLORS, template=TEMPLATE,
                          labels={"total": "Total medals", "country": ""})
        st.plotly_chart(fig_top, use_container_width=True)
    with right:
        st.subheader("Medal split: gold / silver / bronze (top 10)")
        top10 = fdf.groupby("country")["total"].sum().nlargest(10).index
        split = fdf[fdf["country"].isin(top10)].groupby("country")[["gold", "silver", "bronze"]].sum().reset_index()
        split = split.melt(id_vars="country", var_name="medal", value_name="count")
        fig_split = px.bar(split, x="country", y="count", color="medal", barmode="stack", template=TEMPLATE,
                            color_discrete_map={"gold": ORANGE, "silver": GREY, "bronze": VERMILLION})
        st.plotly_chart(fig_split, use_container_width=True)

# =====================================================================
# TAB 2: Continental trends
# =====================================================================
with tab2:
    st.subheader("Continental share of medals over time")
    cont_year = fdf.groupby(["year", "continent"])["total"].sum().reset_index()
    cont_year["pct"] = cont_year["total"] / cont_year.groupby("year")["total"].transform("sum") * 100
    fig_area = px.area(cont_year, x="year", y="pct", color="continent", template=TEMPLATE,
                        color_discrete_map=CONTINENT_COLORS,
                        labels={"pct": "Share of that Games' medals (%)", "year": ""})
    st.plotly_chart(fig_area, use_container_width=True)

    st.subheader(f"{highlight_country} vs. its continent's average medal share")
    country_row = df[df["country"] == highlight_country]
    if len(country_row):
        c_continent = country_row["continent"].iloc[0]
        country_series = fdf[fdf["country"] == highlight_country].groupby("year")["medal_share_pct"].sum()
        continent_avg = (fdf[fdf["continent"] == c_continent]
                          .groupby(["year", "country"])["medal_share_pct"].sum()
                          .groupby("year").mean())
        fig_hl = go.Figure()
        fig_hl.add_trace(go.Scatter(x=continent_avg.index, y=continent_avg.values, name=f"{c_continent} average (per country)",
                                     line=dict(color=GREY, dash="dash")))
        fig_hl.add_trace(go.Scatter(x=country_series.index, y=country_series.values, name=highlight_country,
                                     line=dict(color=VERMILLION, width=3)))
        fig_hl.update_layout(template=TEMPLATE, yaxis_title="Medal share of the Games (%)", xaxis_title="")
        st.plotly_chart(fig_hl, use_container_width=True)
    else:
        st.info("No data for that country in the current filter selection.")

# =====================================================================
# TAB 3: Host & efficiency explorer
# =====================================================================
with tab3:
    st.subheader("Host-nation boost, by continent")
    host_cont = fdf.groupby(["continent", "is_host"])["medal_share_pct"].mean().unstack()
    if True in host_cont.columns and False in host_cont.columns:
        host_cont.columns = ["Non-host years", "Host year"]
        host_cont["boost_pct_points"] = host_cont["Host year"] - host_cont["Non-host years"]
        host_cont = host_cont.dropna().reset_index().sort_values("boost_pct_points")
        fig_host = px.bar(host_cont, x="boost_pct_points", y="continent", orientation="h", template=TEMPLATE,
                           color="continent", color_discrete_map=CONTINENT_COLORS,
                           labels={"boost_pct_points": "Host-year boost (percentage points)", "continent": ""})
        st.plotly_chart(fig_host, use_container_width=True)
    else:
        st.info("Widen the year range to include at least one host-nation appearance.")

    st.subheader("Live explorer: career breadth vs. depth")
    x_axis = st.selectbox("X axis", ["editions_medaled", "career_total", "mean_gold_ratio"], index=0)
    y_axis = st.selectbox("Y axis", ["career_total", "editions_medaled", "mean_gold_ratio"], index=0)
    career = fdf.groupby(["country_noc", "continent"]).agg(
        career_total=("total", "sum"), editions_medaled=("year", "nunique"), mean_gold_ratio=("gold_ratio", "mean"),
    ).reset_index()
    fig_explore = px.scatter(career, x=x_axis, y=y_axis, color="continent", hover_name="country_noc",
                              color_discrete_map=CONTINENT_COLORS, template=TEMPLATE, size="career_total")
    st.plotly_chart(fig_explore, use_container_width=True)
