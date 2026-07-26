const pres = require("pptxgenjs");
const data = require("./presentation_data.json");

const p = new pres();
p.layout = "LAYOUT_WIDE"; // 13.3 x 7.5in
const W = 13.33, H = 7.5;

// ---------------------------------------------------------------
// Palette: "Podium" — deep navy + medal gold + slate, with the same
// Okabe-Ito colour-blind-safe chart colours used in the notebook/dashboard.
// ---------------------------------------------------------------
const NAVY = "0F2A4A";
const GOLD = "C99A2E";
const TEAL = "1B5E6B";
const CORAL = "C1443C";
const SLATE = "4A5560";
const OFFWHITE = "FFFFFF";
const LIGHTGREY = "F4F5F6";

const OKABE = {
  blue: "0072B2", orange: "E69F00", green: "009E73",
  vermillion: "D55E00", sky: "56B4E9", purple: "CC79A7", grey: "B0B0B0",
};
const CONTINENT_COLORS = {
  Europe: OKABE.blue, Americas: OKABE.vermillion, Asia: OKABE.green,
  Africa: OKABE.orange, Oceania: OKABE.purple, "Mixed/Other": OKABE.grey,
};

const HEAD_FONT = "Cambria";
const BODY_FONT = "Calibri";

let pageNum = 1;
function footer(slide, dark) {
  slide.addText("120 Years of the Summer Olympics · Data Visualization, Summer 2026", {
    x: 0.5, y: H - 0.45, w: 8, h: 0.3, fontFace: BODY_FONT, fontSize: 9,
    color: dark ? "9FB3C8" : SLATE, align: "left",
  });
  slide.addText(String(pageNum), {
    x: W - 1, y: H - 0.45, w: 0.5, h: 0.3, fontFace: BODY_FONT, fontSize: 9,
    color: dark ? "9FB3C8" : SLATE, align: "right",
  });
  pageNum += 1;
}

function iconCircle(slide, x, y, diameter, bg, letter, letterColor) {
  slide.addShape("ellipse", { x, y, w: diameter, h: diameter, fill: { color: bg }, line: { type: "none" } });
  slide.addText(letter, {
    x, y, w: diameter, h: diameter, align: "center", valign: "middle",
    fontFace: HEAD_FONT, fontSize: diameter * 28, bold: true, color: letterColor, margin: 0,
  });
}

function questionHeader(slide, qnum, title) {
  slide.addText(`Q${qnum}`, {
    x: 0.5, y: 0.35, w: 1.0, h: 0.5, fontFace: HEAD_FONT, fontSize: 20, bold: true, color: GOLD, margin: 0,
  });
  slide.addText(title, {
    x: 1.4, y: 0.3, w: 11.4, h: 0.85, fontFace: HEAD_FONT, fontSize: 22, bold: true, color: NAVY,
    valign: "top", margin: 0,
  });
}

function insightBox(slide, text) {
  slide.addShape("roundRect", {
    x: 0.5, y: 6.15, w: 12.33, h: 1.0, rectRadius: 0.08,
    fill: { color: LIGHTGREY }, line: { type: "none" },
    shadow: { type: "outer", color: "1A1A1A", opacity: 0.12, blur: 6, offset: 2, angle: 90 },
  });
  slide.addText([{ text: "Takeaway: ", options: { bold: true, color: NAVY } }, { text, options: { color: SLATE } }], {
    x: 0.75, y: 6.15, w: 11.83, h: 1.0, fontFace: BODY_FONT, fontSize: 13, valign: "middle", margin: 0,
  });
}

// =====================================================================
// Slide 1 — Title
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: NAVY };
  s.addShape("ellipse", { x: 10.6, y: -1.3, w: 4.2, h: 4.2, fill: { color: "16375F" }, line: { type: "none" } });
  s.addShape("ellipse", { x: -1.6, y: 5.2, w: 3.6, h: 3.6, fill: { color: "16375F" }, line: { type: "none" } });
  s.addText("120 YEARS OF THE SUMMER OLYMPICS", {
    x: 0.9, y: 2.15, w: 11.5, h: 1.1, fontFace: HEAD_FONT, fontSize: 40, bold: true, color: OFFWHITE, margin: 0,
  });
  s.addText("Geopolitics, Hosts, and Medal Power — 1896 to 2016", {
    x: 0.9, y: 3.2, w: 11.5, h: 0.6, fontFace: BODY_FONT, fontSize: 20, color: GOLD, margin: 0,
  });
  s.addText("Final Individual Project — Data Visualization, Summer 2026", {
    x: 0.9, y: 4.9, w: 11.5, h: 0.4, fontFace: BODY_FONT, fontSize: 14, color: "C7D3DE", margin: 0,
  });
  s.addText(`${data.n_editions} Summer Olympiads  ·  ${data.n_countries} countries & historical entities  ·  ${data.n_rows.toLocaleString()} country-edition records`, {
    x: 0.9, y: 5.4, w: 11.5, h: 0.4, fontFace: BODY_FONT, fontSize: 13, color: "9FB3C8", margin: 0,
  });
}

// =====================================================================
// Slide 2 — Dataset & scope
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  s.addText("The Dataset: A Century of Medal Tallies", {
    x: 0.5, y: 0.4, w: 12.3, h: 0.7, fontFace: HEAD_FONT, fontSize: 30, bold: true, color: NAVY, margin: 0,
  });
  s.addText(
    "One row per country per Games, 1896-2016 (1916/1940/1944 absent — cancelled for the two World Wars). " +
    "Every row carries: medal counts, continent, host-nation flag, historical era, and a defunct-political-entity flag " +
    "(Soviet Union, East/West Germany, Czechoslovakia, Yugoslavia, and more), sourced from a public GitHub mirror and " +
    "cross-referenced against the IOC's NOC code list.",
    { x: 0.5, y: 1.2, w: 7.6, h: 1.6, fontFace: BODY_FONT, fontSize: 14, color: SLATE, valign: "top", margin: 0 }
  );

  const stats = [
    { n: `${data.n_editions}`, label: "Summer Olympiads", color: OKABE.blue },
    { n: `${data.n_countries}`, label: "Countries & historical NOCs", color: OKABE.vermillion },
    { n: `${data.n_continents}`, label: "Continents tracked", color: OKABE.green },
    { n: `${data.year_max - data.year_min}`, label: "Years of history", color: GOLD },
  ];
  stats.forEach((st, i) => {
    const x = 0.5 + i * 3.13;
    s.addShape("roundRect", { x, y: 3.1, w: 2.9, h: 1.5, rectRadius: 0.08, fill: { color: LIGHTGREY }, line: { type: "none" } });
    s.addText(st.n, { x, y: 3.2, w: 2.9, h: 0.85, align: "center", fontFace: HEAD_FONT, fontSize: 34, bold: true, color: st.color, margin: 0 });
    s.addText(st.label, { x, y: 4.0, w: 2.9, h: 0.5, align: "center", fontFace: BODY_FONT, fontSize: 11.5, color: SLATE, margin: 0 });
  });

  s.addText("Data-completeness note", {
    x: 0.5, y: 5.0, w: 12.3, h: 0.4, fontFace: HEAD_FONT, fontSize: 15, bold: true, color: CORAL, margin: 0,
  });
  s.addText(
    "The 2016 Rio source file is missing roughly 40 low-medal-count countries (a fetch-size limitation upstream) — " +
    "every country of real analytical consequence is present, and any chart that depends on a complete country count is " +
    "explicitly restricted or footnoted throughout this deck and the analysis notebook.",
    { x: 0.5, y: 5.4, w: 12.3, h: 0.9, fontFace: BODY_FONT, fontSize: 12.5, italic: true, color: SLATE, valign: "top", margin: 0 }
  );
  footer(s, false);
}

// =====================================================================
// Slide 3 — Methodology
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  s.addText("Methodology", {
    x: 0.5, y: 0.4, w: 12.3, h: 0.7, fontFace: HEAD_FONT, fontSize: 30, bold: true, color: NAVY, margin: 0,
  });
  const rows = [
    ["1", GOLD, "Source & clean", "Merged country-edition medal tallies with an NOC-to-continent lookup; hand-verified host-nation and host-city facts for all 28 editions."],
    ["2", TEAL, "Enrich", "Derived per-edition rank, medal share, gold-conversion ratio, era buckets, and a defunct-entity flag for historical political teams."],
    ["3", OKABE.vermillion, "Analyze", "10 genuinely multi-dimensional questions — each combines at least a temporal, categorical, and quantitative dimension, not single-variable lookups."],
    ["4", NAVY, "Visualize", "10 explanatory Plotly visuals: colour-blind-safe (Okabe-Ito) palette, decluttered gridlines, and a stated takeaway in every chart title."],
  ];
  rows.forEach((r, i) => {
    const y = 1.4 + i * 1.15;
    iconCircle(s, 0.6, y, 0.65, r[1], r[0], OFFWHITE);
    s.addText(r[2], { x: 1.5, y: y - 0.05, w: 3.0, h: 0.7, fontFace: HEAD_FONT, fontSize: 15, bold: true, color: NAVY, valign: "middle", margin: 0 });
    s.addText(r[3], { x: 4.6, y: y - 0.05, w: 8.2, h: 0.85, fontFace: BODY_FONT, fontSize: 12.5, color: SLATE, valign: "middle", margin: 0 });
  });
  footer(s, false);
}

// =====================================================================
// Q1 — Host boost by era (bar chart)
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 1, "Does hosting boost a nation's medals — and has the boost shrunk over time?");
  const shortEras = ["Founding\n(1896-1912)", "Interwar\n(1920-1936)", "Cold War\n(1948-1988)", "Post-Cold War\n(1992-2000)", "Modern\n(2004-2016)"];
  s.addChart("bar", [
    { name: "Host nation", labels: shortEras, values: data.q1.host },
    { name: "Everyone else", labels: shortEras, values: data.q1.nonhost },
  ], {
    x: 0.5, y: 1.3, w: 12.3, h: 4.7, barGrouping: "clustered",
    chartColors: [CORAL, OKABE.grey],
    showTitle: true, title: "Mean share of a Games' medals: host nation vs. everyone else",
    titleFontFace: BODY_FONT, titleFontSize: 13, titleColor: SLATE,
    showLegend: true, legendPos: "b", legendFontFace: BODY_FONT, legendFontSize: 11,
    showValue: true, dataLabelFormatCode: "0.0", dataLabelFontSize: 10, dataLabelColor: SLATE,
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 10.5, catAxisLabelColor: SLATE,
    valAxisLabelFontFace: BODY_FONT, valAxisLabelColor: SLATE, valAxisTitle: "Mean medal share (%)",
    showValAxisTitle: true, valAxisTitleFontSize: 11, valAxisTitleColor: SLATE,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, "The host boost is real in every era but has fallen from ~46% of all medals (1896-1912) to ~5% today, as fields grew from a handful of nations to 80+.");
  footer(s, false);
}

// =====================================================================
// Q2 — Continental shift (stacked bar across 3 snapshot years)
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 2, "How has the continental balance of Olympic power shifted since 1896?");
  const conts = data.q2.continents;
  const colors = conts.map(c => CONTINENT_COLORS[c] || OKABE.grey);
  s.addChart("bar", [
    { name: "1896", labels: conts, values: data.q2.y1896 },
    { name: "1956", labels: conts, values: data.q2.y1956 },
    { name: "2016", labels: conts, values: data.q2.y2016 },
  ], {
    x: 0.5, y: 1.3, w: 12.3, h: 4.7, barGrouping: "clustered",
    chartColors: [NAVY, TEAL, GOLD],
    showTitle: true, title: "Continental share of total medals awarded, by snapshot year",
    titleFontFace: BODY_FONT, titleFontSize: 13, titleColor: SLATE,
    showLegend: true, legendPos: "b", legendFontFace: BODY_FONT, legendFontSize: 11,
    showValue: true, dataLabelFormatCode: "0.0", dataLabelFontSize: 10, dataLabelColor: SLATE,
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 10.5, catAxisLabelColor: SLATE,
    valAxisLabelFontFace: BODY_FONT, valAxisLabelColor: SLATE, valAxisTitle: "Share of medals (%)",
    showValAxisTitle: true, valAxisTitleFontSize: 11, valAxisTitleColor: SLATE,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, "Europe's share fell from 80% (1896) to 48% (2016). The gain went overwhelmingly to Asia — near zero before the 1950s, ~21% by 2016 — not primarily the Americas.");
  footer(s, false);
}

// =====================================================================
// Q3 — Cold War bloc gold ratio
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 3, "Myth-check: did the Communist Bloc convert medals to gold more efficiently?");
  s.addChart("bar", [
    { name: "Gold ratio", labels: ["Communist Bloc", "Western Bloc"], values: [data.q3.communist, data.q3.western] },
  ], {
    x: 2.5, y: 1.4, w: 8.3, h: 4.6,
    chartColors: [CORAL],
    showTitle: true, title: "Mean gold ÷ total-medal ratio per country-edition, 1948-1988",
    titleFontFace: BODY_FONT, titleFontSize: 13, titleColor: SLATE,
    showLegend: false,
    showValue: true, dataLabelFormatCode: "0.000", dataLabelFontSize: 13, dataLabelColor: OFFWHITE, dataLabelPosition: "inEnd",
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 13, catAxisLabelColor: SLATE,
    valAxisLabelFontFace: BODY_FONT, valAxisLabelColor: SLATE, valAxisMaxVal: 0.5,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, "The popular Cold War narrative doesn't hold: Communist Bloc (0.290) and Western Bloc (0.288) converted medals to gold at nearly identical rates. The real difference was volume, not efficiency.");
  footer(s, false);
}

// =====================================================================
// Q4 — Concentration vs field growth (combo line chart)
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 4, "As the field grew 8x, did medal concentration fall at the same pace?");
  s.addChart([
    { type: "line", data: [{ name: "Top-10 nations' medal share (%)", labels: data.q4.years.map(String), values: data.q4.top10_share }], options: { chartColors: [CORAL] } },
    { type: "line", data: [{ name: "Number of competing nations", labels: data.q4.years.map(String), values: data.q4.n_countries }], options: { secondaryValAxis: true, secondaryCatAxis: true, chartColors: [NAVY] } },
  ], {
    x: 0.5, y: 1.3, w: 12.3, h: 4.6,
    chartColors: [CORAL, NAVY],
    showTitle: true, title: "Top-10 share of medals vs. number of competing nations (2016 excluded — see data note)",
    titleFontFace: BODY_FONT, titleFontSize: 12.5, titleColor: SLATE,
    showLegend: true, legendPos: "b", legendFontFace: BODY_FONT, legendFontSize: 11,
    lineDataSymbol: "circle", lineDataSymbolSize: 5, lineSize: 2.5,
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 9, catAxisLabelColor: SLATE, catAxisLabelRotate: 45,
    valAxes: [
      { showValAxisTitle: true, valAxisTitle: "Top-10 share (%)", valAxisTitleColor: SLATE, valAxisTitleFontSize: 10, valAxisLabelColor: SLATE, valGridLine: { style: "none" } },
      { showValAxisTitle: true, valAxisTitle: "Nations competing", valAxisTitleColor: SLATE, valAxisTitleFontSize: 10, valAxisLabelColor: SLATE, valGridLine: { style: "none" }, valAxisMinVal: 0 },
    ],
    catAxes: [ { catAxisHidden: false }, { catAxisHidden: true } ],
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, "Concentration fell hard, from 98% (1896) to ~55% (2000s), then flattened — even in a global field of 85+ nations, the top 10 still take roughly half of all medals.");
  footer(s, false);
}

// =====================================================================
// Q5 — Defunct entities vs successors
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 5, "Were the defunct Cold War powerhouses more efficient than their successors?");
  s.addChart("bar", [
    { name: "Defunct system", labels: ["USSR → Russia", "East Germany → Germany"], values: [data.q5.urs, data.q5.gdr] },
    { name: "Modern successor", labels: ["USSR → Russia", "East Germany → Germany"], values: [data.q5.rus, data.q5.ger_post92] },
  ], {
    x: 1.2, y: 1.4, w: 11.0, h: 4.6, barGrouping: "clustered",
    chartColors: [CORAL, OKABE.sky],
    showTitle: true, title: "Mean gold ÷ total-medal ratio: historical entity vs. modern successor state",
    titleFontFace: BODY_FONT, titleFontSize: 13, titleColor: SLATE,
    showLegend: true, legendPos: "b", legendFontFace: BODY_FONT, legendFontSize: 11,
    showValue: true, dataLabelFormatCode: "0.000", dataLabelFontSize: 11, dataLabelColor: SLATE,
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 12, catAxisLabelColor: SLATE,
    valAxisLabelFontFace: BODY_FONT, valAxisLabelColor: SLATE, valAxisMaxVal: 0.5,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, "Both defunct state-run systems out-converted their successors: USSR 0.384 vs Russia 0.304; East Germany 0.369 vs reunified Germany 0.322 — a real, if modest, efficiency legacy.");
  footer(s, false);
}

// =====================================================================
// Q6 — Continent volatility scatter
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 6, "Which continent's performance is most volatile, and which most stable?");
  const conts = data.q6.continents;
  s.addChart([
    { type: "bar", data: [{ name: "Mean share of medals (%)", labels: conts, values: data.q6.mean }], options: { chartColors: [TEAL] } },
    { type: "line", data: [{ name: "Volatility (std. dev., pct points)", labels: conts, values: data.q6.std }], options: { secondaryValAxis: true, secondaryCatAxis: true, chartColors: [CORAL] } },
  ], {
    x: 0.8, y: 1.3, w: 11.7, h: 4.6,
    chartColors: [TEAL, CORAL],
    showTitle: true, title: "Mean medal share vs. year-to-year volatility (std. dev.), by continent",
    titleFontFace: BODY_FONT, titleFontSize: 13, titleColor: SLATE,
    showLegend: true, legendPos: "b", legendFontFace: BODY_FONT, legendFontSize: 11,
    lineDataSymbol: "circle", lineDataSymbolSize: 8, lineSize: 2.5,
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 12, catAxisLabelColor: SLATE,
    valAxes: [
      { showValAxisTitle: true, valAxisTitle: "Mean share (%)", valAxisTitleColor: SLATE, valAxisTitleFontSize: 10, valAxisLabelColor: SLATE, valGridLine: { style: "none" } },
      { showValAxisTitle: true, valAxisTitle: "Volatility (std. dev.)", valAxisTitleColor: SLATE, valAxisTitleFontSize: 10, valAxisLabelColor: SLATE, valGridLine: { style: "none" }, valAxisMinVal: 0 },
    ],
    catAxes: [ { catAxisHidden: false }, { catAxisHidden: true } ],
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, "Europe is both the biggest (63%) and most volatile (std 15.8) continent — its share is on a long downward trend, not just noise. Africa and Oceania are small but stable.");
  footer(s, false);
}

// =====================================================================
// Q7 — Host boost by continent
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 7, "Does hosting help weaker continents more, or amplify existing strength?");
  s.addChart("bar", [
    { name: "Host-year boost (pct points)", labels: data.q7.continents, values: data.q7.boost },
  ], {
    x: 1.5, y: 1.4, w: 10.3, h: 4.6, barDir: "bar",
    chartColors: [GOLD],
    showTitle: true, title: "Host-year medal share minus non-host-year medal share, by continent",
    titleFontFace: BODY_FONT, titleFontSize: 13, titleColor: SLATE,
    showLegend: false,
    showValue: true, dataLabelFormatCode: "0.0", dataLabelFontSize: 12, dataLabelColor: SLATE, dataLabelPosition: "outEnd",
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 12.5, catAxisLabelColor: SLATE,
    valAxisLabelFontFace: BODY_FONT, valAxisLabelColor: SLATE, valAxisTitle: "Boost (percentage points)",
    showValAxisTitle: true, valAxisTitleFontSize: 11, valAxisTitleColor: SLATE,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, "Hosting amplifies existing strength most: the Americas (+20.7 pts) and Europe (+13.8 pts) gain far more than Asia (+5.9) or Oceania (+5.3) — it is not primarily an equaliser.");
  footer(s, false);
}

// =====================================================================
// Q8 — Depth vs breadth scatter
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 8, "Century-long dominance, or a compressed one-era powerhouse?");
  s.addChart([
    { type: "bar", data: [{ name: "Career total medals", labels: data.q8.nocs, values: data.q8.career_total }], options: { chartColors: [NAVY] } },
    { type: "line", data: [{ name: "Editions medalled at (breadth)", labels: data.q8.nocs, values: data.q8.editions }], options: { secondaryValAxis: true, secondaryCatAxis: true, chartColors: [GOLD] } },
  ], {
    x: 0.8, y: 1.3, w: 11.7, h: 4.6,
    chartColors: [NAVY, GOLD],
    showTitle: true, title: "Career total medals vs. number of editions medalled at, top 8 nations",
    titleFontFace: BODY_FONT, titleFontSize: 13, titleColor: SLATE,
    showLegend: true, legendPos: "b", legendFontFace: BODY_FONT, legendFontSize: 11,
    lineDataSymbol: "circle", lineDataSymbolSize: 8, lineSize: 2.5,
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 12, catAxisLabelColor: SLATE,
    valAxes: [
      { showValAxisTitle: true, valAxisTitle: "Career total medals", valAxisTitleColor: SLATE, valAxisTitleFontSize: 10, valAxisLabelColor: SLATE, valGridLine: { style: "none" } },
      { showValAxisTitle: true, valAxisTitle: "Editions medalled at", valAxisTitleColor: SLATE, valAxisTitleFontSize: 10, valAxisLabelColor: SLATE, valGridLine: { style: "none" }, valAxisMinVal: 0 },
    ],
    catAxes: [ { catAxisHidden: false }, { catAxisHidden: true } ],
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, "USA and GBR dominate broadly across 27-28 editions. The USSR tells a different story: only 9 editions of existence, yet 1,010 career medals — the highest per-edition rate of any nation.");
  footer(s, false);
}

// =====================================================================
// Q9 — Rising powers
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 9, "Which long-tenured nations climbed furthest in the Olympic rankings?");
  s.addChart("bar", [
    { name: "Rank places climbed", labels: data.q9.nocs, values: data.q9.improve },
  ], {
    x: 1.5, y: 1.4, w: 10.3, h: 4.6, barDir: "bar",
    chartColors: [TEAL],
    showTitle: true, title: "Rank at first vs. most recent Games appearance, nations in ≥ 8 editions",
    titleFontFace: BODY_FONT, titleFontSize: 13, titleColor: SLATE,
    showLegend: false,
    showValue: true, dataLabelFormatCode: "0", dataLabelFontSize: 12, dataLabelColor: SLATE, dataLabelPosition: "outEnd",
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 12.5, catAxisLabelColor: SLATE,
    valAxisLabelFontFace: BODY_FONT, valAxisLabelColor: SLATE, valAxisTitle: "Places climbed",
    showValAxisTitle: true, valAxisTitleFontSize: 11, valAxisTitleColor: SLATE,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, "South Korea climbed 12 places (23rd to 11th), the largest rise among established nations. 3 of the top 4 climbers (KOR, JPN, KEN) are Asian or African — matching the Q2 continental shift.");
  footer(s, false);
}

// =====================================================================
// Q10 — Soviet breakup
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  questionHeader(s, 10, "Did the USSR's successor states recover its medal output, or lose ground?");
  s.addChart("line", [
    { name: "Successor states, combined total", labels: data.q10.years.map(String), values: data.q10.totals },
  ], {
    x: 1.0, y: 1.3, w: 11.3, h: 4.6,
    chartColors: [NAVY],
    showTitle: true, title: "Combined total medals of 14 former-Soviet states vs. the USSR's 1952-1988 average",
    titleFontFace: BODY_FONT, titleFontSize: 12.5, titleColor: SLATE,
    showLegend: true, legendPos: "b", legendFontFace: BODY_FONT, legendFontSize: 11,
    lineDataSymbol: "circle", lineDataSymbolSize: 6, lineSize: 3,
    showValue: true, dataLabelFormatCode: "0", dataLabelFontSize: 11, dataLabelColor: SLATE,
    catAxisLabelFontFace: BODY_FONT, catAxisLabelFontSize: 12, catAxisLabelColor: SLATE,
    valAxisLabelFontFace: BODY_FONT, valAxisLabelColor: SLATE, valAxisTitle: "Total medals",
    showValAxisTitle: true, valAxisTitleFontSize: 11, valAxisTitleColor: SLATE,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  insightBox(s, `Successor states exceeded the USSR's own historical average (${data.q10.urs_avg} medals/Games) at first (123 in 1996, peaking at 164 in 2000), then drifted back down to 135 by 2016 as the inherited talent pipeline was not fully replaced.`);
  footer(s, false);
}

// =====================================================================
// Dashboard slide
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  s.addText("Interactive Dashboard", {
    x: 0.5, y: 0.4, w: 12.3, h: 0.7, fontFace: HEAD_FONT, fontSize: 30, bold: true, color: NAVY, margin: 0,
  });
  s.addText(
    "A Streamlit app (dashboard/app.py) lets a reader explore the same dataset live — filter by year range and " +
    "continent, highlight any single country against its continent's average, and drive a live scatter explorer " +
    "of career breadth vs. depth.",
    { x: 0.5, y: 1.15, w: 12.3, h: 0.75, fontFace: BODY_FONT, fontSize: 13.5, color: SLATE, valign: "top", margin: 0 }
  );
  const tabs = [
    ["1", GOLD, "Overview", "Choropleth map of career medal totals, top-15 leaderboard, and gold/silver/bronze split for the top 10 countries in the selected filters."],
    ["2", TEAL, "Continental Trends", "Stacked area chart of continental medal share over time, plus a country-vs-continent-average highlight line for any country the reader picks."],
    ["3", CORAL, "Host & Efficiency", "Host-nation boost by continent, and a live scatter explorer of career total, editions medalled, and gold-conversion ratio."],
  ];
  tabs.forEach((t, i) => {
    const x = 0.5 + i * 4.15;
    s.addShape("roundRect", { x, y: 2.2, w: 3.9, h: 3.1, rectRadius: 0.08, fill: { color: LIGHTGREY }, line: { type: "none" } });
    iconCircle(s, x + 0.3, 2.5, 0.6, t[1], t[0], OFFWHITE);
    s.addText(t[2], { x: x + 0.25, y: 2.95, w: 3.4, h: 0.45, fontFace: HEAD_FONT, fontSize: 15, bold: true, color: NAVY, margin: 0 });
    s.addText(t[3], { x: x + 0.25, y: 3.45, w: 3.4, h: 1.7, fontFace: BODY_FONT, fontSize: 11.5, color: SLATE, valign: "top", margin: 0 });
  });
  s.addShape("roundRect", { x: 0.5, y: 5.6, w: 12.33, h: 0.9, rectRadius: 0.08, fill: { color: NAVY }, line: { type: "none" } });
  s.addText([
    { text: "Live URL: ", options: { bold: true, color: GOLD } },
    { text: "add after deploying to Streamlit Community Cloud (see README) — e.g. https://<your-app>.streamlit.app", options: { color: "D8E1E9" } },
  ], { x: 0.75, y: 5.6, w: 11.83, h: 0.9, fontFace: BODY_FONT, fontSize: 13, valign: "middle", margin: 0 });
  footer(s, false);
}

// =====================================================================
// Deliverables slide (icon-in-circle badges, no accent stripes)
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: OFFWHITE };
  s.addText("Deliverables & Submission", {
    x: 0.5, y: 0.4, w: 12.3, h: 0.7, fontFace: HEAD_FONT, fontSize: 30, bold: true, color: NAVY, margin: 0,
  });
  const items = [
    ["N", NAVY, "Analysis Notebook", "analysis.ipynb — 10 questions, 10 Plotly visuals, CVD-safe & annotated"],
    ["D", TEAL, "Dashboard", "dashboard/app.py — interactive Streamlit app, deploy to Streamlit Community Cloud"],
    ["P", CORAL, "Presentation", "This deck, exported to PDF, with dashboard snapshots and live link"],
    ["R", GOLD, "Repository", "Public GitHub repo (not the classwork repo) with all code, data, and this deck"],
  ];
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.6 + col * 6.2, y = 1.5 + row * 2.1;
    s.addShape("roundRect", { x, y, w: 5.9, h: 1.8, rectRadius: 0.08, fill: { color: LIGHTGREY }, line: { type: "none" } });
    iconCircle(s, x + 0.3, y + 0.3, 0.7, it[1], it[0], OFFWHITE);
    s.addText(it[2], { x: x + 1.25, y: y + 0.25, w: 4.4, h: 0.5, fontFace: HEAD_FONT, fontSize: 16, bold: true, color: NAVY, margin: 0 });
    s.addText(it[3], { x: x + 1.25, y: y + 0.78, w: 4.4, h: 0.85, fontFace: BODY_FONT, fontSize: 12, color: SLATE, valign: "top", margin: 0 });
  });
  s.addText("Submit the repo link via a 1-to-1 Microsoft Teams message. Deadline: Friday, 31 July 2026 — no late submissions.", {
    x: 0.6, y: 5.85, w: 12.1, h: 0.5, fontFace: BODY_FONT, fontSize: 13, italic: true, color: CORAL, margin: 0,
  });
  footer(s, false);
}

// =====================================================================
// Conclusions
// =====================================================================
{
  const s = p.addSlide();
  s.background = { color: NAVY };
  s.addText("Conclusions", {
    x: 0.7, y: 0.55, w: 11.5, h: 0.8, fontFace: HEAD_FONT, fontSize: 32, bold: true, color: OFFWHITE, margin: 0,
  });
  const concl = [
    ["1", GOLD, "Geopolitics leaves a measurable trace on sport", "Cold War bloc dynamics, the Soviet collapse, and the century-long European-to-Asian power shift all show up directly in the numbers, not just the history books."],
    ["2", TEAL, "Hosting still helps, but scale has diluted it", "The host boost is real in every era, but 1,000%-of-average effects from 1896 are gone in a globalised field — and hosting amplifies existing strength more than it lifts the weak."],
    ["3", CORAL, "Broader participation hasn't meant equal outcomes", "Far more nations medal today than ever before, but the top 10 still take roughly half of all medals — globalisation broadened the field without levelling it."],
  ];
  concl.forEach((c, i) => {
    const y = 1.7 + i * 1.65;
    iconCircle(s, 0.7, y, 0.7, c[1], c[0], NAVY);
    s.addText(c[2], { x: 1.7, y: y - 0.05, w: 10.8, h: 0.55, fontFace: HEAD_FONT, fontSize: 17, bold: true, color: OFFWHITE, margin: 0 });
    s.addText(c[3], { x: 1.7, y: y + 0.5, w: 10.8, h: 0.85, fontFace: BODY_FONT, fontSize: 12.5, color: "C7D3DE", valign: "top", margin: 0 });
  });
  footer(s, true);
}

p.writeFile({ fileName: "Olympics_Final_Project_Presentation.pptx" }).then(() => {
  console.log("Wrote Olympics_Final_Project_Presentation.pptx");
});
