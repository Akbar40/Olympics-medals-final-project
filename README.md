# 120 Years of the Summer Olympics — Final Individual Project (Data Visualization, Summer 2026)

A country-by-edition analysis of Summer Olympics medal tallies from Athens 1896 to Rio 2016,
delivered as an analysis notebook, a slide presentation, and an interactive Streamlit dashboard.

**Live dashboard**: https://olympics-medals-final-project-rwuxvhxn3cbpdntlkieyzo.streamlit.app

## Dataset

Source: country-edition medal tallies (`Olympic_Games_Medal_Tally.csv`) and an NOC-to-country
lookup (`Olympics_Country.csv`), mirrored at
[github.com/ThaliaZn/Olympics-Data-Visualizations](https://github.com/ThaliaZn/Olympics-Data-Visualizations).

`data/build_dataset.py` enriches the raw tally with continent, host-nation status, historical
era, and defunct-political-entity flags to build one harmonized country-edition panel:

- **1,208 rows** · **146 countries & historical NOCs** · **28 Summer Olympiads (1896-2016)**
  (1916, 1940 and 1944 are absent — those Games were cancelled for the two World Wars)
- 6 continents, hand-verified host-nation/host-city facts for every edition
- Derived metrics: per-edition rank, medal share of the Games, gold-conversion ratio
- A `is_defunct_entity` flag for historical political teams (USSR, East/West Germany,
  Czechoslovakia, Yugoslavia, and others)

Raw source files: `data/raw/`. Cleaned panel: `data/clean_olympics_1896_2016.csv`. Regenerate with:

```bash
cd data && python3 build_dataset.py
```

**Data-completeness note**: the 2016 Rio source file is missing roughly 40 low-medal-count
countries (a fetch-size limitation in the upstream mirror) — every country of real analytical
consequence is present down to 8 total medals, but the true country *count* for 2016 is
undercounted (44 recorded vs. 87 in reality). A `edition_data_complete` column flags this, and
every chart in the notebook, dashboard, and presentation that depends on a complete country
count either excludes 2016 or footnotes it explicitly.

## Repository layout

```
analysis.ipynb                 # 10 analytical questions, each with a Plotly visual
build_notebook.py              # regenerates analysis.ipynb
data/
  raw/                         # original medal-tally and NOC-lookup source files
  build_dataset.py             # harmonizes raw files into one clean panel
  clean_olympics_1896_2016.csv
dashboard/
  app.py                       # Streamlit dashboard (3 tabs, live filters)
presentation/
  deck.js                      # regenerates the presentation (pptxgenjs)
  presentation_data.json       # computed stats consumed by deck.js
  Olympics_Final_Project_Presentation_FINAL.pptx
  Olympics_Final_Project_Presentation_FINAL.pdf
requirements.txt
```

## Running it yourself

```bash
pip install -r requirements.txt

# 1. Analysis notebook
jupyter notebook analysis.ipynb
# then: File -> Export Notebook As -> PDF or HTML

# 2. Dashboard, locally
cd dashboard
streamlit run app.py
```


## The 10 analytical questions

1. Does hosting the Olympics boost a nation's medals, and has that boost shrunk across eras?
2. How has the continental balance of Olympic medal power shifted since 1896?
3. Did the Communist Bloc really convert medals to gold more efficiently than the West during the Cold War?
4. As the Olympic field grew from 11 nations to 87, did medal concentration fall at the same pace?
5. Were the defunct Cold War sporting powerhouses more "efficient" than their modern successor states?
6. Which continent's Olympic performance is most volatile, and which most stable?
7. Does hosting the Games benefit historically weaker Olympic continents more than the traditional powerhouses?
8. Which countries show century-long broad dominance versus a compressed one-era powerhouse?
9. Which long-tenured nations climbed the furthest in the Olympic rankings over 120 years?
10. When the USSR dissolved, did its successor states collectively recover its medal output, or was there a lasting loss?
