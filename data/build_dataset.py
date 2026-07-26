"""
Builds a harmonized country-edition panel of Summer Olympics medal tallies,
1896-2016 (28 editions; 1916/1940/1944 are absent because those Games were
cancelled for the two World Wars -- this is a real gap in Olympic history,
not missing data).

Sources (mirrored small CSVs, see data/raw/):
  - medal_tally_1896_2016.csv : edition, edition_id, year, country,
    country_noc, gold, silver, bronze, total
    (github.com/ThaliaZn/Olympics-Data-Visualizations)
  - Olympics_Country.csv : country_noc -> country name lookup (235 rows)

This script adds:
  - continent (via a country_noc -> continent mapping, so historical/defunct
    teams like the Soviet Union, East/West Germany, Yugoslavia etc. are all
    classified correctly even though they no longer exist)
  - host_country / is_host (host nation per edition, hand-coded historical
    fact -- used for "host-nation boost" analysis)
  - era bucket (Cold War / Post-Cold War / Post-2000, etc.)
  - is_defunct (whether the competing entity no longer exists as of 2016)
  - per-edition rank, medal share of the Games, gold-efficiency ratio

Output: clean_olympics_1896_2016.csv
"""
import pandas as pd
import numpy as np

DATA = "raw"

tally = pd.read_csv(f"{DATA}/medal_tally_1896_2016.csv")
tally["year"] = tally["year"].astype(int)

# ---------------------------------------------------------------
# 1. Continent mapping, keyed by country_noc (stable across name changes)
# ---------------------------------------------------------------
continent_map = {
    # Europe
    "GBR": "Europe", "FRA": "Europe", "GER": "Europe", "GDR": "Europe", "FRG": "Europe",
    "ITA": "Europe", "HUN": "Europe", "AUT": "Europe", "SUI": "Europe", "SWE": "Europe",
    "DEN": "Europe", "NED": "Europe", "BEL": "Europe", "NOR": "Europe", "FIN": "Europe",
    "POL": "Europe", "TCH": "Europe", "CZE": "Europe", "SVK": "Europe", "ROU": "Europe",
    "BUL": "Europe", "YUG": "Europe", "SCG": "Europe", "SRB": "Europe", "CRO": "Europe",
    "SLO": "Europe", "BIH": "Europe", "MNE": "Europe", "MKD": "Europe", "GRE": "Europe",
    "POR": "Europe", "ESP": "Europe", "IRL": "Europe", "LUX": "Europe", "EST": "Europe",
    "LAT": "Europe", "LTU": "Europe", "URS": "Europe", "RUS": "Europe", "EUN": "Europe",
    "BLR": "Europe", "UKR": "Europe", "MDA": "Europe", "GEO": "Europe", "ARM": "Europe",
    "AZE": "Europe", "TUR": "Europe", "ISL": "Europe", "MON": "Europe", "MLT": "Europe",
    "CYP": "Europe", "BOH": "Europe", "SAA": "Europe", "ALB": "Europe", "AND": "Europe",
    "SMR": "Europe", "LIE": "Europe", "KOS": "Europe", "ROC": "Europe",
    # Americas
    "USA": "Americas", "CAN": "Americas", "MEX": "Americas", "CUB": "Americas",
    "BRA": "Americas", "ARG": "Americas", "CHI": "Americas", "COL": "Americas",
    "VEN": "Americas", "URU": "Americas", "PER": "Americas", "ECU": "Americas",
    "JAM": "Americas", "TTO": "Americas", "BAH": "Americas", "PAN": "Americas",
    "PUR": "Americas", "DOM": "Americas", "GUA": "Americas", "CRC": "Americas",
    "PAR": "Americas", "BOL": "Americas", "SUR": "Americas", "BER": "Americas",
    "GUY": "Americas", "ISV": "Americas", "AHO": "Americas", "WIF": "Americas",
    "BAR": "Americas", "GRN": "Americas", "NFL": "Americas", "HAI": "Americas",
    # Africa
    "RSA": "Africa", "EGY": "Africa", "KEN": "Africa", "ETH": "Africa", "NGR": "Africa",
    "MAR": "Africa", "TUN": "Africa", "ALG": "Africa", "GHA": "Africa", "UGA": "Africa",
    "ZIM": "Africa", "ZAM": "Africa", "CMR": "Africa", "NAM": "Africa", "SEN": "Africa",
    "TAN": "Africa", "NIG": "Africa", "MOZ": "Africa", "BDI": "Africa", "DJI": "Africa",
    "GAB": "Africa", "SUD": "Africa", "MRI": "Africa", "BOT": "Africa", "TOG": "Africa",
    "COD": "Africa", "CGO": "Africa", "IVC": "Africa", "CIV": "Africa", "UAR": "Africa",
    "ERI": "Africa",
    # Asia
    "JPN": "Asia", "CHN": "Asia", "KOR": "Asia", "PRK": "Asia", "IND": "Asia",
    "IRI": "Asia", "ISR": "Asia", "KAZ": "Asia", "UZB": "Asia", "THA": "Asia",
    "INA": "Asia", "PAK": "Asia", "TPE": "Asia", "HKG": "Asia", "MAS": "Asia",
    "PHI": "Asia", "SGP": "Asia", "VIE": "Asia", "MGL": "Asia", "SRI": "Asia",
    "KUW": "Asia", "KSA": "Asia", "QAT": "Asia", "LBN": "Asia", "SYR": "Asia",
    "IRQ": "Asia", "JOR": "Asia", "TJK": "Asia", "KGZ": "Asia", "BRN": "Asia",
    "UAE": "Asia", "AFG": "Asia", "MAL": "Asia", "NBO": "Asia",
    # Oceania
    "AUS": "Oceania", "NZL": "Oceania", "ANZ": "Oceania", "FIJ": "Oceania",
    "SAM": "Oceania", "TGA": "Oceania",
    # Mixed / special / unclassified entities
    "MIX": "Mixed/Other", "IOA": "Mixed/Other", "UNK": "Mixed/Other",
}

country_lookup = pd.read_csv(f"{DATA}/Olympics_Country.csv").set_index("country_noc")["country"].to_dict()

tally["continent"] = tally["country_noc"].map(continent_map)
missing = sorted(tally.loc[tally["continent"].isna(), "country_noc"].unique())
if missing:
    print("NOCs still missing a continent (defaulting to 'Mixed/Other'):", missing)
    tally["continent"] = tally["continent"].fillna("Mixed/Other")

# ---------------------------------------------------------------
# 2. Host nation per edition (public historical record)
# ---------------------------------------------------------------
host_country_noc = {
    1896: "GRE", 1900: "FRA", 1904: "USA", 1908: "GBR", 1912: "SWE",
    1920: "BEL", 1924: "FRA", 1928: "NED", 1932: "USA", 1936: "GER",
    1948: "GBR", 1952: "FIN", 1956: "AUS", 1960: "ITA", 1964: "JPN",
    1968: "MEX", 1972: "FRG", 1976: "CAN", 1980: "URS", 1984: "USA",
    1988: "KOR", 1992: "ESP", 1996: "USA", 2000: "AUS", 2004: "GRE",
    2008: "CHN", 2012: "GBR", 2016: "BRA",
}
host_city = {
    1896: "Athens", 1900: "Paris", 1904: "St. Louis", 1908: "London", 1912: "Stockholm",
    1920: "Antwerp", 1924: "Paris", 1928: "Amsterdam", 1932: "Los Angeles", 1936: "Berlin",
    1948: "London", 1952: "Helsinki", 1956: "Melbourne", 1960: "Rome", 1964: "Tokyo",
    1968: "Mexico City", 1972: "Munich", 1976: "Montreal", 1980: "Moscow", 1984: "Los Angeles",
    1988: "Seoul", 1992: "Barcelona", 1996: "Atlanta", 2000: "Sydney", 2004: "Athens",
    2008: "Beijing", 2012: "London", 2016: "Rio de Janeiro",
}
tally["host_country_noc"] = tally["year"].map(host_country_noc)
tally["host_city"] = tally["year"].map(host_city)
tally["is_host"] = tally["country_noc"] == tally["host_country_noc"]

# ---------------------------------------------------------------
# 3. Era bucket (useful categorical facet layered on top of continuous year)
# ---------------------------------------------------------------
def era(year):
    if year <= 1912:
        return "Founding Era (1896-1912)"
    if year <= 1936:
        return "Interwar (1920-1936)"
    if year <= 1988:
        return "Cold War (1948-1988)"
    if year <= 2000:
        return "Post-Cold War (1992-2000)"
    return "Modern (2004-2016)"

tally["era"] = tally["year"].apply(era)

# ---------------------------------------------------------------
# 4. Defunct-entity flag (does this NOC still compete under this name?)
# ---------------------------------------------------------------
defunct_nocs = {
    "URS", "GDR", "FRG", "TCH", "YUG", "SCG", "EUN", "ANZ", "BOH", "WIF",
    "UAR", "MIX", "AHO", "SAA",
}
tally["is_defunct_entity"] = tally["country_noc"].isin(defunct_nocs)

# ---------------------------------------------------------------
# 5. Per-edition derived metrics
# ---------------------------------------------------------------
tally = tally.sort_values(["year", "total"], ascending=[True, False]).reset_index(drop=True)
tally["rank_in_edition"] = tally.groupby("year")["total"].rank(method="min", ascending=False).astype(int)

edition_totals = tally.groupby("year")["total"].transform("sum")
tally["medal_share_pct"] = (tally["total"] / edition_totals * 100).round(2)

tally["gold_ratio"] = (tally["gold"] / tally["total"].replace(0, np.nan)).round(3)

n_countries_edition = tally.groupby("year")["country_noc"].transform("nunique")
tally["n_countries_in_edition"] = n_countries_edition

# ---------------------------------------------------------------
# 6. Data-completeness flag
#    The 2016 Rio source file was cut short by an upstream fetch/size limit:
#    it captured all of the meaningful medal contenders (down to countries
#    with 8 total medals) but is missing roughly 40 additional NOCs that won
#    only 1-7 medals apiece (the real 2016 Games had 87 medal-winning NOCs;
#    we have 44). Top-country and host-boost analyses are unaffected since
#    every country of consequence is present, but any chart that depends on
#    a complete country *count* (e.g. "how many nations won a medal") would
#    understate 2016. We flag it here so the notebook/dashboard can footnote
#    or exclude it consistently rather than silently mis-plotting a dip.
# ---------------------------------------------------------------
incomplete_editions = {2016}
tally["edition_data_complete"] = ~tally["year"].isin(incomplete_editions)

# ---------------------------------------------------------------
# 7. Tidy, order, save
# ---------------------------------------------------------------
cols = [
    "year", "edition", "edition_id", "host_city", "host_country_noc", "is_host",
    "country", "country_noc", "continent", "is_defunct_entity", "era",
    "gold", "silver", "bronze", "total", "rank_in_edition", "medal_share_pct",
    "gold_ratio", "n_countries_in_edition", "edition_data_complete",
]
tally = tally[cols].sort_values(["year", "rank_in_edition"]).reset_index(drop=True)
tally.to_csv("clean_olympics_1896_2016.csv", index=False)

print("Final shape:", tally.shape)
print("Editions covered:", sorted(tally["year"].unique()))
print("Distinct countries/NOCs:", tally["country_noc"].nunique())
print("Continent breakdown:\n", tally.drop_duplicates("country_noc")["continent"].value_counts())
print("\nMissing values per column:\n", tally.isna().sum())
