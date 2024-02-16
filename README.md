# Agriculture-Optimization-Model
This project describes how we can optimize our business decisions in order to achieve an annual objective

Project Charter

Business Background

- Who is the client? Business Domain?
  i. Our clients are the farmer coops. A farmer coop (Unica, Agroponiente, La Union) is an intermediary between farmers and buyers.

Business Problems

  i. Price
    * As a farmer coop, I find it difficult to estimate a reference price for how to sell efficiently.
    * Big buyers give us their price, with a prediction model we can be more precise giving our counteroffer
    * Big buyers give us two annual prices (One till week 6, and another from this week).
    * Other big buyers, like Lidl, ask for quantities for the next week or two.
    * Below these customers are others like Eurogroup… etc.

  ii. The key issue is minimizing loss after big transactions: Closed prices for the whole campaign (IPL & Mercadona). We need to know how to balance those losses with above-average paying customers.

Season scheduling.

- Decisions in the preparation of the next season are key to getting the best out of the campaign.
  i. These decisions can be based on predicted prices & calculation of revenue needed for incoming weeks.
  ii. If we optimize forecasts for the next month, we can achieve a better price for farmers and coops.

Data Science Definitions
- A time-series forecasting problem with covariates and 1-3 month horizon.

Metrics
- Qualitative goal?
  i. Improve net benefit for coops and farmers by analyzing how the different price scenarios affect the revenue.
- Regression + optimization problem.
- Quantified metrics of project: Comparison between an old way to calculate prices vs the output of the model in order to achieve a higher benefit at the end of the season.
- Quantified metrics of the model: MSE between actual and predicted price.
