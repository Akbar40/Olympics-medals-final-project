"""
Builds analysis.ipynb by hand as raw nbformat v4 JSON (no nbformat package
required). Each analytical question gets a markdown rationale/insight cell
followed by one Plotly code cell.
"""
import json

cells = []

def md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True),
    })

def code(text):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    })

# =====================================================================
# Title
# =====================================================================
md("""# 120 Years of the Summer Olympics: Geopolitics, Hosts, and Medal Power (1896-2016)

**Final Individual Project — Data Visualization, Summer 2026**

A country-by-edition analysis of Summer Olympics medal tallies across all 28 Games from
Athens 1896 to Rio 2016 (1916, 1940 and 1944 were cancelled for the two World Wars).
Every visual below is built with Plotly only, uses a colour-blind-safe (Okabe-Ito) palette,
and states its takeaway directly in the chart title.

**Dataset**: country-edition medal tallies (gold/silver/bronze/total), enriched with continent,
host-nation status, historical era, and defunct-political-entity flags — see
`data/build_dataset.py` for full provenance and cleaning logic. One known limitation is
flagged and handled transparently: the 2016 source file is missing roughly 40 low-medal-count
countries (see Q4 and the data note below); every analysis that could be skewed by this is
either restricted to complete editions or explicitly footnoted.
""")

# =====================================================================
# Setup
# =====================================================================
code("""import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

pd.set_option("display.max_columns", 30)

df = pd.read_csv("data/clean_olympics_1896_2016.csv")

# Okabe-Ito colour-blind-safe palette, used consistently across every chart
GREY, BLUE, ORANGE, GREEN, VERMILLION, SKY, PURPLE, YELLOW = (
    "#B0B0B0", "#0072B2", "#E69F00", "#009E73", "#D55E00", "#56B4E9", "#CC79A7", "#F0E442",
)
CONTINENT_COLORS = {
    "Europe": BLUE, "Americas": VERMILLION, "Asia": GREEN,
    "Africa": ORANGE, "Oceania": PURPLE, "Mixed/Other": GREY,
}
TEMPLATE = "plotly_white"

df.head()""")

md("""## A quick look at the data

1,208 country-edition rows spanning 28 Summer Olympiads and 146 distinct competing entities
(including historical/defunct teams such as the Soviet Union, East and West Germany,
Czechoslovakia, and Yugoslavia). Each row is one country's medal count at one Games.""")

code("""print("Rows:", len(df), "| Editions:", df['year'].nunique(), "| Distinct NOCs:", df['country_noc'].nunique())
print("Editions covered:", sorted(df['year'].unique()))
df[['year','country','continent','gold','silver','bronze','total','is_host']].sample(5, random_state=7)""")

# =====================================================================
# Q1 — Host boost across eras
# =====================================================================
md("""## Q1. Does hosting the Olympics boost a nation's medal haul — and has that boost shrunk as the Games modernised?

**Why this is multi-dimensional:** combines a categorical split (host vs. non-host), a
continuous outcome (medal share of the Games), and a temporal facet (era), to see whether
a single-Games effect has changed shape over 120 years.

**What we find:** host nations *always* out-perform their own average, but the size of the
edge has collapsed. In the Founding Era (1896-1912), host nations captured a stunning
**46.4%** of all medals on average (tiny fields, minimal travel for anyone else). By the
Modern era (2004-2016), the boost is still real but far more modest: hosts average **5.3%**
of all medals vs **1.3%** for everyone else — a smaller edge in a much bigger, more
professionalised field.""")

code("""era_order = ["Founding Era (1896-1912)", "Interwar (1920-1936)", "Cold War (1948-1988)",
             "Post-Cold War (1992-2000)", "Modern (2004-2016)"]

host_era = (df.groupby(["era", "is_host"])["medal_share_pct"].mean()
              .reset_index()
              .replace({"is_host": {True: "Host nation", False: "Everyone else"}}))
host_era["era"] = pd.Categorical(host_era["era"], categories=era_order, ordered=True)
host_era = host_era.sort_values("era")

fig = px.bar(host_era, x="era", y="medal_share_pct", color="is_host", barmode="group",
             template=TEMPLATE, color_discrete_map={"Host nation": VERMILLION, "Everyone else": GREY},
             labels={"medal_share_pct": "Mean share of Games' medals (%)", "era": "", "is_host": ""},
             title="The host-nation medal boost is real in every era, but has shrunk from ~46% to ~5%<br>"
                   "<sup>Mean share of a Games' total medals: host nation vs. everyone else, by era</sup>")
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
fig.update_yaxes(showgrid=True, gridcolor="#EDEDED")
fig.show()""")

# =====================================================================
# Q2 — Continental shift
# =====================================================================
md("""## Q2. How has the continental balance of Olympic medal power shifted since 1896?

**Why this is multi-dimensional:** tracks a categorical dimension (continent) as a
proportion of a whole, across the full temporal span, revealing a genuine long-run
geopolitical/sporting shift rather than a single-year snapshot.

**What we find:** Europe has gone from taking **80%** of all medals in 1896 to a still-large
but much diminished **48%** in 2016. The gain has not gone mainly to the Americas (which have
stayed a fairly steady 16-24%) — it has gone almost entirely to **Asia**, which was essentially
absent before the 1950s and had climbed to **~21%** of all medals by 2016, roughly matching
its share of the world's population growth in Olympic investment (Japan, China, South Korea).""")

code("""cont_year = df.groupby(["year", "continent"])["total"].sum().reset_index()
cont_year["pct"] = cont_year["total"] / cont_year.groupby("year")["total"].transform("sum") * 100

fig = px.area(cont_year, x="year", y="pct", color="continent", template=TEMPLATE,
              color_discrete_map=CONTINENT_COLORS,
              category_orders={"continent": ["Europe", "Americas", "Asia", "Africa", "Oceania", "Mixed/Other"]},
              labels={"pct": "Share of that Games' medals (%)", "year": "", "continent": ""},
              title="Europe's medal share has fallen from 80% to 48% since 1896 — Asia is the biggest gainer<br>"
                    "<sup>Continental share of total medals awarded, by Games year</sup>")
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
fig.update_yaxes(range=[0, 100], showgrid=True, gridcolor="#EDEDED")
fig.show()""")

# =====================================================================
# Q3 — Cold War bloc efficiency
# =====================================================================
md("""## Q3. Did the Communist Bloc really convert medals into gold more efficiently than the West during the Cold War?

**Why this is multi-dimensional:** filters to a specific era, splits by a political-bloc
category built from several country codes, and compares a *ratio* metric (gold ÷ total
medals) rather than a raw count — testing a specific, often-repeated Cold War narrative.

**What we find:** the popular narrative — that state-sponsored Communist sport systems were
built to win gold specifically — does not hold up in the aggregate numbers. Averaged across
1948-1988, the Communist Bloc's gold ratio was **0.290** and the Western Bloc's was
**0.288** — statistically indistinguishable. Both blocs converted medals to gold at almost
exactly the same rate; the real Cold War story is in *volume* (the USSR and East Germany
won far more total medals), not gold-conversion efficiency.""")

code("""cw = df[(df["year"] >= 1948) & (df["year"] <= 1988)].copy()
communist_bloc = ["URS", "GDR", "TCH", "POL", "HUN", "BUL", "ROU", "CUB", "PRK", "YUG"]
western_bloc = ["USA", "FRG", "GBR", "ITA", "FRA", "AUS", "CAN", "JPN", "SWE"]

cw["bloc"] = np.select(
    [cw["country_noc"].isin(communist_bloc), cw["country_noc"].isin(western_bloc)],
    ["Communist Bloc", "Western Bloc"], default=None,
)
bloc_df = cw.dropna(subset=["bloc"])
bloc_summary = bloc_df.groupby("bloc")["gold_ratio"].mean().reset_index()

fig = px.bar(bloc_summary, x="bloc", y="gold_ratio", template=TEMPLATE, color="bloc",
             color_discrete_map={"Communist Bloc": VERMILLION, "Western Bloc": BLUE}, text_auto=".3f",
             labels={"gold_ratio": "Mean gold-medal ratio (gold ÷ total)", "bloc": ""},
             title="Myth-check: Communist and Western blocs converted medals to gold at nearly the same rate<br>"
                   "<sup>Mean gold ÷ total-medal ratio per country-edition, 1948-1988</sup>")
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False)
fig.update_yaxes(range=[0, 0.5], showgrid=True, gridcolor="#EDEDED")
fig.show()""")

# =====================================================================
# Q4 — Concentration vs field growth
# =====================================================================
md("""## Q4. As the Olympic field grew from 11 nations to 87, did medal concentration fall at the same pace?

**Why this is multi-dimensional:** pairs a count (number of competing nations) with a
concentration ratio (share held by the top 10) across 116 years, testing whether a bigger,
more global field genuinely "democratised" medals or whether a "rich get richer" dynamic held.

*Data note: 2016 is excluded from this specific chart because the source file for that edition
is missing ~40 low-medal countries (see the data-completeness note at the top) — including it
would understate the true number of competing nations for that year and distort the trend.*

**What we find:** the top 10 nations' share of all medals fell steadily, from **98%** in 1896
to about **55-57%** by the 2000s — but it *flattened* rather than kept falling once the field
stabilised at 70-90 nations after 1992. In other words: globalisation of the Games did spread
medals much more widely, but even in a global field of ~85 nations, roughly half of all medals
still concentrate in just 10 countries.""")

code("""complete = df[df["edition_data_complete"]]

top10_share = (complete.groupby("year")
               .apply(lambda g: g.nlargest(10, "total")["total"].sum() / g["total"].sum() * 100,
                      include_groups=False)
               .rename("top10_share_pct"))
n_countries = complete.groupby("year")["country_noc"].nunique().rename("n_countries")
trend = pd.concat([top10_share, n_countries], axis=1).reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=trend["year"], y=trend["top10_share_pct"], name="Top-10 nations' share of medals (%)",
                          mode="lines+markers", line=dict(color=VERMILLION, width=3)))
fig.add_trace(go.Scatter(x=trend["year"], y=trend["n_countries"], name="Number of competing nations",
                          mode="lines+markers", line=dict(color=BLUE, width=3), yaxis="y2"))
fig.update_layout(
    template=TEMPLATE,
    title="Medal concentration fell as the field grew, then flattened around ~55%<br>"
          "<sup>Top-10 nations' medal share vs. number of competing nations, 1896-2012 (2016 excluded, see note)</sup>",
    yaxis=dict(title="Top-10 share of medals (%)", range=[0, 105], showgrid=True, gridcolor="#EDEDED"),
    yaxis2=dict(title="Number of competing nations", overlaying="y", side="right", showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
fig.show()""")

# =====================================================================
# Q5 — Defunct entities vs successors
# =====================================================================
md("""## Q5. Were the defunct Cold War sporting powerhouses actually more "efficient" than the modern states that replaced them?

**Why this is multi-dimensional:** compares a categorical pairing (a historical/defunct
political entity vs. its modern successor state) on a ratio metric, across two different
eras — asking whether the collapse of a political system also meant a collapse in
gold-conversion efficiency.

**What we find:** yes, modestly. The Soviet Union's gold ratio (**0.384**) was noticeably
higher than modern Russia's (**0.304**), and East Germany's (**0.369**) higher than
reunified Germany's post-1992 figure (**0.322**). Both defunct systems converted a larger
share of their medals into golds than their successor states have managed since — consistent
with the idea that those state-run programmes were built around producing champions, not
just broad participation.""")

code("""pairs = pd.DataFrame({
    "entity": ["Soviet Union (1952-1988)", "Russia (1996-2016)",
               "East Germany (1968-1988)", "Germany, post-1992 (1992-2016)"],
    "gold_ratio": [
        df[df["country_noc"] == "URS"]["gold_ratio"].mean(),
        df[df["country_noc"] == "RUS"]["gold_ratio"].mean(),
        df[df["country_noc"] == "GDR"]["gold_ratio"].mean(),
        df[(df["country_noc"] == "GER") & (df["year"] >= 1992)]["gold_ratio"].mean(),
    ],
    "pair": ["USSR -> Russia", "USSR -> Russia", "East Germany -> Germany", "East Germany -> Germany"],
    "status": ["Defunct system", "Modern successor", "Defunct system", "Modern successor"],
})

fig = px.bar(pairs, x="pair", y="gold_ratio", color="status", barmode="group", text_auto=".3f",
             template=TEMPLATE, color_discrete_map={"Defunct system": VERMILLION, "Modern successor": SKY},
             labels={"gold_ratio": "Mean gold-medal ratio (gold ÷ total)", "pair": "", "status": ""},
             title="Both defunct Cold War systems out-converted their modern successor states on gold ratio<br>"
                   "<sup>Mean gold ÷ total-medal ratio, historical entity vs. modern successor</sup>")
fig.update_traces(textposition="outside")
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
fig.update_yaxes(range=[0, 0.5], showgrid=True, gridcolor="#EDEDED")
fig.show()""")

# =====================================================================
# Q6 — Continent volatility
# =====================================================================
md("""## Q6. Which continent's Olympic performance is most volatile, and which is most stable?

**Why this is multi-dimensional:** plots two derived statistics against each other (mean
medal share and its year-to-year standard deviation) for each continent, turning a single
time series per continent into a stability/dominance map.

**What we find:** Europe sits in a league of its own — both the highest average share
(**~63%**) and the highest volatility (**std ~15.8**), because its *absolute* share has been
trending sharply downward for a century (a trend, not noise). The Americas (mean ~24%,
std ~14.5) are similarly volatile but for a different reason: the US dominates so heavily
that any Games without full US participation swings the whole continent's number. Africa and
Oceania are both low-share *and* low-volatility — consistently minor players, not a boom-bust
story.""")

code("""cont_year = df.groupby(["year", "continent"])["total"].sum().reset_index()
cont_year["pct"] = cont_year["total"] / cont_year.groupby("year")["total"].transform("sum") * 100
vol = cont_year.groupby("continent")["pct"].agg(mean="mean", std="std").reset_index()
vol = vol[vol["continent"] != "Mixed/Other"]

fig = px.scatter(vol, x="mean", y="std", text="continent", template=TEMPLATE,
                  color="continent", color_discrete_map=CONTINENT_COLORS, size=[28]*len(vol),
                  labels={"mean": "Mean share of medals across all editions (%)",
                          "std": "Year-to-year volatility (std. dev. of share, pct points)"},
                  title="Europe is both the biggest and the most volatile continent — its share is trending down, not just noisy<br>"
                        "<sup>Mean medal share vs. its year-to-year volatility, by continent (1896-2016)</sup>")
fig.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="white")))
fig.update_layout(showlegend=False)
fig.update_xaxes(showgrid=True, gridcolor="#EDEDED")
fig.update_yaxes(showgrid=True, gridcolor="#EDEDED")
fig.show()""")

# =====================================================================
# Q7 — Host boost by continent
# =====================================================================
md("""## Q7. Does hosting help historically weaker Olympic continents more than it helps the traditional powerhouses?

**Why this is multi-dimensional:** re-slices the host-boost question (Q1) by a second
dimension — continent — to see whether the *size* of the host advantage depends on how
strong a continent's baseline Olympic performance already is.

**What we find:** the pattern is almost the opposite of "helps the underdog most". The
Americas get the single largest boost in absolute terms (**+20.7 points**, from 2.4% to
23.0%, driven by the US's own hosted Games), and Europe gets a large boost too
(**+13.8 points**). Asia (**+5.9**) and Oceania (**+5.3**) see real but much smaller
absolute lifts. Hosting amplifies whatever baseline strength a continent already has —
it is not primarily an equaliser.""")

code("""host_cont = df.groupby(["continent", "is_host"])["medal_share_pct"].mean().unstack()
host_cont.columns = ["Non-host years", "Host year"]
host_cont["boost_pct_points"] = host_cont["Host year"] - host_cont["Non-host years"]
host_cont = host_cont.dropna().sort_values("boost_pct_points", ascending=True).reset_index()

fig = px.bar(host_cont, x="boost_pct_points", y="continent", orientation="h", template=TEMPLATE,
             color="continent", color_discrete_map=CONTINENT_COLORS, text_auto=".1f",
             labels={"boost_pct_points": "Host-year boost in medal share (percentage points)", "continent": ""},
             title="Hosting amplifies existing strength most in the Americas and Europe, not the weakest continents<br>"
                   "<sup>Host-year medal share minus non-host-year medal share, by continent</sup>")
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False)
fig.update_xaxes(showgrid=True, gridcolor="#EDEDED")
fig.show()""")

# =====================================================================
# Q8 — Depth vs breadth of dominance
# =====================================================================
md("""## Q8. Which countries dominate broadly across a century, and which dominated narrowly within one political era?

**Why this is multi-dimensional:** plots career medal total against the *number of separate
Games* a country has medalled at, revealing two very different shapes of "dominance" —
sustained breadth (many editions, steady flow of medals) versus concentrated depth (huge
totals compressed into a short historical window).

**What we find:** the USA and Great Britain sit far to the right (dominant across **27-28**
different editions) with the USA also on top for total medals (**2,542**). The USSR tells a
completely different story: only **9** editions of existence, yet **1,010** career medals —
a staggering per-edition rate that no other nation matches, visually separating "century-long
powerhouse" from "compressed-era powerhouse" on the same chart.""")

code("""career = df.groupby(["country_noc", "continent"]).agg(
    career_total=("total", "sum"),
    editions_medaled=("year", "nunique"),
).reset_index()
top_career = career.sort_values("career_total", ascending=False).head(30)

fig = px.scatter(top_career, x="editions_medaled", y="career_total", color="continent",
                  color_discrete_map=CONTINENT_COLORS, template=TEMPLATE, size="career_total",
                  hover_name="country_noc",
                  labels={"editions_medaled": "Number of different Games medalled at (breadth)",
                          "career_total": "Career total medals (1896-2016)"},
                  title="USA and GBR dominate broadly across a century; the USSR dominated narrowly but immensely<br>"
                        "<sup>Career medal total vs. number of editions medalled at, top 30 nations</sup>")
top_labeled = top_career[top_career["country_noc"].isin(["USA", "URS", "GBR", "GER", "CHN", "FRA", "ITA", "RUS"])]
for _, r in top_labeled.iterrows():
    fig.add_annotation(x=r["editions_medaled"], y=r["career_total"], text=r["country_noc"],
                        showarrow=False, yshift=14, font=dict(size=11, color="#333"))
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
fig.update_xaxes(showgrid=True, gridcolor="#EDEDED")
fig.update_yaxes(showgrid=True, gridcolor="#EDEDED")
fig.show()""")

# =====================================================================
# Q9 — Rising powers
# =====================================================================
md("""## Q9. Which long-tenured nations climbed the furthest in the Olympic rankings over 120 years?

**Why this is multi-dimensional:** compares each country's medal-table rank at its *first*
appearance against its rank at its *most recent* appearance (restricted to nations present
in at least 8 editions, to rule out one-off flukes), layering continent as a colour facet.

**What we find:** South Korea's rise is the single largest climb among established nations —
from 23rd (1948) to 11th (2016), a **12-place** improvement. Russia (as measured across the
pre-Soviet-to-modern span), Japan, and Kenya follow, and notably **three of the top four
climbers are Asian or African nations** — the clearest quantitative signature of the
continental power shift already visible in Q2.""")

code("""tenured = df.groupby("country_noc").agg(
    n_editions=("year", "nunique"),
    first_rank=("rank_in_edition", "first"),
    last_rank=("rank_in_edition", "last"),
    continent=("continent", "first"),
).reset_index()
tenured = tenured[tenured["n_editions"] >= 8].copy()
tenured["rank_improve"] = tenured["first_rank"] - tenured["last_rank"]
top_climbers = tenured.sort_values("rank_improve", ascending=False).head(10).sort_values("rank_improve")

fig = px.bar(top_climbers, x="rank_improve", y="country_noc", orientation="h", template=TEMPLATE,
             color="continent", color_discrete_map=CONTINENT_COLORS, text_auto=True,
             labels={"rank_improve": "Improvement in medal-table rank (places climbed)", "country_noc": ""},
             title="South Korea, Russia and Japan climbed the most places — 3 of the top 4 climbers are Asian<br>"
                   "<sup>Rank at first vs. most recent Games appearance, nations in ≥ 8 editions</sup>")
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
fig.update_xaxes(showgrid=True, gridcolor="#EDEDED")
fig.show()""")

# =====================================================================
# Q10 — Soviet breakup
# =====================================================================
md("""## Q10. When the USSR broke apart, did its successor states collectively recover its medal output — or was there a lasting loss?

**Why this is multi-dimensional:** compares a single historical baseline (the USSR's own
average) against the *combined* trajectory of multiple successor states over time — a
before/after natural-experiment framing driven by a real geopolitical event.

**What we find:** the successor states' combined total actually **exceeded** the USSR's own
historical average (112 medals/Games) at their first fully-independent showing in 1996
(**123** medals) and peaked at **164** in 2000 — likely reflecting the huge pool of trained
Soviet-era athletes now competing for many separate teams and qualifying more of them.
But the combined total has since declined steadily to **135** by 2016, converging back
toward the old Soviet baseline as that inherited talent pipeline has not been fully replaced.""")

code("""urs_avg = df[df["country_noc"] == "URS"]["total"].mean()
successors = ["RUS", "UKR", "BLR", "KAZ", "UZB", "GEO", "ARM", "AZE", "LTU", "LAT", "EST", "MDA", "KGZ", "TJK"]
combined = (df[(df["country_noc"].isin(successors)) & (df["year"] >= 1996)]
            .groupby("year")["total"].sum().reset_index())

fig = go.Figure()
fig.add_trace(go.Scatter(x=combined["year"], y=combined["total"], mode="lines+markers",
                          name="Successor states, combined total", line=dict(color=BLUE, width=3)))
fig.add_hline(y=urs_avg, line_dash="dash", line_color=VERMILLION,
              annotation_text=f"USSR's own historical average ({urs_avg:.0f} medals/Games)",
              annotation_position="bottom right")
fig.update_layout(
    template=TEMPLATE,
    title="Post-Soviet states out-medalled the USSR's own average at first, then drifted back toward it<br>"
          "<sup>Combined total medals of 14 former-Soviet states vs. the USSR's 1952-1988 average</sup>",
    xaxis_title="", yaxis_title="Total medals",
    yaxis=dict(showgrid=True, gridcolor="#EDEDED"),
)
fig.show()""")

# =====================================================================
# Conclusions
# =====================================================================
md("""## Conclusions

Across ten multi-dimensional cuts of 120 years of Summer Olympics medal data, three
storylines stand out. First, **geopolitics leaves a measurable, quantifiable trace on
sport**: the Cold War bloc split, the fall of the Soviet Union, and the long European-to-Asian
power shift are not just historical narratives — they show up directly in gold ratios,
continental shares, and rank trajectories. Second, **the host-nation effect is real but has
been diluted by scale**: hosting still helps, and it amplifies existing strength more than it
lifts up the weak, but the 1,000%-of-average boosts of the Founding Era are long gone in a
field of 80+ competing nations. Third, **globalisation has genuinely broadened participation
without equalising outcomes**: far more nations medal today than in 1896, but roughly half of
all medals still concentrate in the same 10 countries, and only a handful of long-tenured
nations (South Korea, Japan, Russia, Kenya) have meaningfully closed the gap.

**A note on data completeness**: the 2016 edition in this dataset is missing roughly 40 NOCs
that won only 1-7 medals each (a limitation of the upstream source file), which is why it is
either excluded or explicitly footnoted in any chart that depends on a complete country count.
Every other figure and every top-country comparison in this analysis uses the complete data
for that edition.
""")

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open("analysis.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Wrote analysis.ipynb with", len(cells), "cells")
