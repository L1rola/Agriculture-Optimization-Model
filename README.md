# Agriculture - Optimization Model
This project describes how we can improve our business decisions in order to achieve the annual objective.


# 1. Business Background <a class="anchor" id="overview"></a>

  - **Who is the client? Business Domain?**
  1. Our clients are the farmer coops: A farmer coop (Unica, Agroponiente, La Union, etc) is an intermediary between farmers and buyers.

# 2. Business Problems <a class="anchor" id="overview"></a>

**Price**:
  1. Farmer coops find it difficult to estimate a reference price for how to sell efficiently.
  2. Big buyers give their price, with a prediction model we can be more precise giving our counteroffer
  3. Big buyers give two annual prices (One till week 6, and another from this week).
  4. Other big buyers, like Lidl, ask for quantities for the next week or two.
  5. Below these customers are others like Eurogroup… etc.

**Minimizing loss after big transactions**: 
1. Big buyers work with closed prices for the whole campaign (IPL & Mercadona).
2. We need to know how to balance those losses with above-average paying customers.

# 3. Season Scheduling <a class="anchor" id="overview"></a>

**Decisions in the preparation of the next season are key to getting the best out of the campaign.**
  1. These decisions can be based on predicted prices & calculation of revenue needed for incoming weeks.
  2. If we optimize forecasts for the next month, we can achieve a better price for farmers and coops.

# 4. Data Science Definitions <a class="anchor" id="overview"></a>
A time-series forecasting problem with covariates and 1-3 month horizon.

# 5. Metrics <a class="anchor" id="overview"></a>
1. Qualitative goal: Improve net benefit for coops and farmers by analyzing how the different price scenarios affect the revenue.
2. Regression + optimization problem.
3. Quantified metrics of project: Comparison between an old way to calculate prices vs the output of the model in order to achieve a higher benefit at the end of the season.
4. Quantified metrics of the model: MSE between actual and predicted price.
