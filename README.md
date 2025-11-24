# QS World University Rankings 2024 — Data Cleaning and Analysis

This project analyzes the QS World University Rankings 2024 dataset using Python, pandas, and NumPy. The goal is to clean the raw ranking data, convert inconsistent fields into usable formats, and extract several insights related to institutional performance, year-to-year rank changes, and country-level averages. A small visualization is also included to show the distribution of overall scores across universities.

## Data Cleaning Summary

The raw dataset included several structural issues that needed to be addressed before any analysis could be performed. First, the file contained an additional header-like row that appeared as regular data. This row included placeholder text such as “rank display,” so it was removed entirely. Column names were also inconsistent, with mixed capitalization and spaces, so they were standardized to lowercase with underscores to make the data easier to work with in Python.

Many ranking and score fields were stored as strings or contained non-numeric symbols. These columns were converted to numeric values, with invalid entries set to missing. The dataset also included duplicate entries, which were dropped. To maintain a consistent base for analysis, only rows with a valid overall score were kept. This reduced the dataset to a clean and reliable subset suitable for statistical analysis.

Finally, a new column was created to measure rank changes between 2023 and 2024. This allowed for additional insights into which institutions improved or declined the most from one year to the next.

## Analysis Steps

The analysis focuses on several questions:

1. **Which universities achieved the highest overall scores in 2024?**  
   This identifies global leaders.

2. **Which institutions improved or declined the most compared to 2023?**  
   Rank changes highlight significant movement in the rankings.

3. **How do average scores compare across countries?**  
   Country-level patterns reveal differences between higher-education systems.

4. **What does the distribution of overall scores look like?**  
   A histogram was used to visualize how scores are spread across institutions.

## Findings

The overall score distribution shows that most universities fall between 20 and 60 points, with only a small group reaching values above 90. The highest scoring institutions were MIT, Cambridge, Oxford, Harvard, and Stanford, which aligns with expectations from global rankings.

When comparing year-to-year movement, several universities made notable improvements. York University, the University of Waikato, and La Trobe University recorded the strongest upward shifts in the rankings between 2023 and 2024. On the other hand, Hiroshima University, Case Western Reserve University, and Vanderbilt University experienced the largest drops during the same period.

Average scores by country revealed clear regional differences. Hong Kong SAR recorded the highest average overall score, followed by Singapore, Mexico, Switzerland, and the Netherlands. The United States also ranked within the top ten, though with a lower average compared to these leading regions.

Overall, the data suggests that while top-ranked institutions remain consistent across years, there is considerable movement in the middle of the distribution. Certain countries also show stronger overall performance, reflecting variations in higher education systems and research output.

## Visualization

A simple histogram was created to show the distribution of overall scores:
score_distribution.png

