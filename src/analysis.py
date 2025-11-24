import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# QS World University Rankings 2024
# Small cleaning + analysis project with pandas & NumPy.
# Main steps:
#  - remove placeholder row
#  - standardize column names
#  - preserve tied-rank notation ("6=") in *_raw columns
#  - convert ranks/scores to numeric
#  - keep ranks as nullable integers (so no .0 in CSV)
#  - compute a few quick insights
#  - save cleaned CSV + one plot
# ------------------------------------------------------------

# --- Load dataset ---
DATA_PATH = os.path.join("data", "qs2024.csv")  # change filename if yours differs
df = pd.read_csv(DATA_PATH)

print("Raw shape:", df.shape)
print(df.head())

# --- Basic cleanup / housekeeping ---
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Drop weird placeholder first row (text instead of real data)
if isinstance(df.loc[0, "2024_rank"], str):
    df = df.drop(index=0).reset_index(drop=True)

df = df.drop_duplicates()

print("\nAfter dropping placeholder row + duplicates:", df.shape)

# --- Missing value check ---
print("\nMissing values per column:")
print(df.isna().sum().sort_values(ascending=False))

# --- Preserve originals + fix tied ranks ---
# QS uses "=" to indicate ties (e.g., "6=").
# We keep an original copy so the meaning is visible in the cleaned file.
for col in df.columns:
    if "rank" in col:
        df[col + "_raw"] = df[col]  # keep original string (with "=" if present)
        df[col] = df[col].astype(str).str.replace("=", "", regex=False)

# --- Convert numeric-like columns ---
for col in df.columns:
    if "score" in col or "rank" in col:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Main score column
score_col = "overall_score" if "overall_score" in df.columns else None
if score_col is None:
    score_candidates = [c for c in df.columns if "score" in c]
    score_col = score_candidates[0]

# Keep rows that at least have an overall score
df_clean = df.dropna(subset=[score_col]).copy()

print("\nCleaned shape:", df_clean.shape)

name_col = "institution_name"

# --- Make rank columns look like ranks (ints, not floats) ---
# Nullable Int64 keeps NaNs but displays cleanly without ".0"
rank_cols = [c for c in df_clean.columns if c.endswith("_rank") and not c.endswith("_rank_raw")]
for c in rank_cols:
    df_clean[c] = df_clean[c].round().astype("Int64")

# --- NumPy summary stats ---
scores = df_clean[score_col].to_numpy()

print("\nNumPy summary:")
print("Mean score:", np.mean(scores))
print("Median score:", np.median(scores))
print("Std dev:", np.std(scores))
print("90th percentile:", np.percentile(scores, 90))

# --- Top 10 universities by overall score ---
top10 = df_clean.sort_values(score_col, ascending=False).head(10)
print("\nTop 10 universities by score:")
print(top10[[name_col, score_col]].to_string(index=False))

# --- Rank changes (2023 → 2024) ---
if "2023_rank" in df_clean.columns and "2024_rank" in df_clean.columns:
    df_clean["rank_change"] = df_clean["2023_rank"] - df_clean["2024_rank"]

    biggest_climbers = df_clean.sort_values("rank_change", ascending=False).head(10)
    biggest_fallers = df_clean.sort_values("rank_change").head(10)

    print("\nBiggest climbers (2023 → 2024):")
    print(
        biggest_climbers[[name_col, "2023_rank", "2024_rank", "rank_change"]]
        .to_string(index=False)
    )

    print("\nBiggest fallers (2023 → 2024):")
    print(
        biggest_fallers[[name_col, "2023_rank", "2024_rank", "rank_change"]]
        .to_string(index=False)
    )

# --- Country averages ---
country_avg = (
    df_clean.groupby("country")[score_col]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 countries by average overall score:")
print(country_avg)

# --- Visualization: distribution of overall scores ---
plt.hist(df_clean[score_col].dropna(), bins=30)
plt.title("QS 2024 Overall Score Distribution")
plt.xlabel("Overall Score")
plt.ylabel("Number of Universities")
plt.tight_layout()
plt.savefig("score_distribution.png")
plt.close()

# --- Save cleaned dataset ---
OUT_PATH = os.path.join("data", "qs2024_cleaned.csv")
df_clean.to_csv(OUT_PATH, index=False)
print("\nSaved cleaned file to:", OUT_PATH)
