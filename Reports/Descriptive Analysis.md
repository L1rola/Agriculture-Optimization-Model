#  Descriptive Analysis

Just looking at the data, we can get very good insights.
I was sure our data would not be stationary. Seasonality is a very clear pattern in all the years, this leaves me an entry point when making the prediction:
- 2020: There is a generally stable trend with some significant fluctuations at certain points. Seasonality shows regular oscillations, indicating clear and consistent seasonal patterns. Residuals are distributed around zero and seem to be quite random.
- 2021: The trend shows a prominent peak due to the Calima (Natural disaster) happened in Almeria. Similar to 2020, there is clear seasonality with regular peaks. The residuals are centered around zero, with fewer outliers compared to 2020
- 2022: The trend shows moderate variability throughout the year. Seasonality continues to be evident with a clear and repetitive pattern. Residuals show a similar pattern to 2021, with little variability and randomly distributed around zero.
- 2023: The trend follow a smoother pattern without drastic peaks. Seasonality remains consistent with similar patterns to previous years and very pronounced peaks. Residuals are well distributed and continue to be around zero.

Through robust modelling (Robust model from Statsmodels) we make our model less sensitive to outliers. We can check robust vs normal to see the difference.
