# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0,
    "Orlando": 0.85,
    "Miami": 1.2,
    "Jacksonville": 0.75,
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9

    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday

    for store in stores:
        store_factor = store_performance[store]

        for dept in departments:
            dept_factor = dept_performance[dept]

            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)

                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise

                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range

                # Calculate profit
                profit = sales_amount * profit_margin

                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range

    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])

    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income

    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)

    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))

    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)

    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)

    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"

    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]

    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()

    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) *
                                (store_performance[store] ** 0.5))

    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# TODO 1: Descriptive Analytics - Overview of Current Performance
# 1.1 Calculate and display basic descriptive statistics for sales and profit
# REQUIRED: Store results in variables for testing
def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    total_sales = float(sales_df["Sales"].sum())
    total_profit = float(sales_df["Profit"].sum())
    avg_profit_margin = float(sales_df["ProfitMargin"].mean())

    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)

    print(f"Total Annual Sales: ${total_sales:,.2f}")
    print(f"Total Annual Profit: ${total_profit:,.2f}")
    print(f"Average Profit Margin: {avg_profit_margin:.2%}")
    print(f"Sales Mean: ${sales_df['Sales'].mean():.2f}, Median: ${sales_df['Sales'].median():.2f}, Std: ${sales_df['Sales'].std():.2f}")
    print(f"Profit Mean: ${sales_df['Profit'].mean():.2f}, Median: ${sales_df['Profit'].median():.2f}, Std: ${sales_df['Profit'].std():.2f}")

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_profit_margin": avg_profit_margin,
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept,
    }


# 1.2 Create visualizations showing sales distribution by store, department, and time
# REQUIRED: Return matplotlib figures
def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.to_period("M"))["Sales"].sum()

    store_fig, store_ax = plt.subplots(figsize=(8, 5))
    sales_by_store.plot(kind="bar", color="seagreen", ax=store_ax)
    store_ax.set_title("Annual Sales by Store")
    store_ax.set_xlabel("Store")
    store_ax.set_ylabel("Sales ($)")
    store_ax.tick_params(axis="x", rotation=30)
    store_fig.tight_layout()

    dept_fig, dept_ax = plt.subplots(figsize=(8, 5))
    sales_by_dept.plot(kind="bar", color="teal", ax=dept_ax)
    dept_ax.set_title("Annual Sales by Department")
    dept_ax.set_xlabel("Department")
    dept_ax.set_ylabel("Sales ($)")
    dept_ax.tick_params(axis="x", rotation=30)
    dept_fig.tight_layout()

    time_fig, time_ax = plt.subplots(figsize=(10, 5))
    monthly_sales.index = monthly_sales.index.to_timestamp()
    time_ax.plot(monthly_sales.index, monthly_sales.values, marker="o", color="darkorange")
    time_ax.set_title("Monthly Sales Trend")
    time_ax.set_xlabel("Month")
    time_ax.set_ylabel("Sales ($)")
    time_ax.grid(alpha=0.3)
    time_fig.autofmt_xdate()
    time_fig.tight_layout()

    return store_fig, dept_fig, time_fig


# 1.3 Analyze customer segments and their spending patterns
# REQUIRED: Return analysis results
def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    segment_counts = customer_df["Segment"].value_counts()
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False)
    segment_loyalty = pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])

    print("Customer Segment Counts:")
    print(segment_counts)
    print("\nAverage Monthly Spend by Segment:")
    print(segment_avg_spend.round(2))

    return {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty,
    }


# TODO 2: Diagnostic Analytics - Understanding Relationships
# 2.1 Identify factors correlated with sales performance
# REQUIRED: Return correlation results
def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    merged = pd.merge(store_df, operational_df, on="Store", how="inner")
    numeric_cols = [
        "SquareFootage",
        "StaffCount",
        "YearsOpen",
        "WeeklyMarketingSpend",
        "AnnualSales",
        "AnnualProfit",
        "SalesPerSqFt",
        "ProfitPerSqFt",
        "SalesPerStaff",
        "InventoryTurnover",
        "CustomerSatisfaction",
    ]
    store_correlations = merged[numeric_cols].corr()

    annual_sales_corr = store_correlations["AnnualSales"].drop("AnnualSales").sort_values(key=np.abs, ascending=False)
    top_correlations = [(factor, float(value)) for factor, value in annual_sales_corr.head(5).items()]

    correlation_fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(annual_sales_corr.index[:6], annual_sales_corr.values[:6], color="steelblue")
    ax.axhline(0, color="black", linewidth=1)
    ax.set_title("Top Correlations with Annual Sales")
    ax.set_ylabel("Correlation Coefficient")
    ax.tick_params(axis="x", rotation=40)
    correlation_fig.tight_layout()

    print("Top factors correlated with Annual Sales:")
    for factor, corr in top_correlations:
        print(f"- {factor}: {corr:.3f}")

    return {
        "store_correlations": store_correlations,
        "top_correlations": top_correlations,
        "correlation_fig": correlation_fig,
    }


# 2.2 Compare stores based on operational metrics
# REQUIRED: Return comparison results
def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    efficiency_metrics = operational_df.set_index("Store")[["SalesPerSqFt", "SalesPerStaff"]]
    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)

    comparison_fig, ax = plt.subplots(figsize=(8, 5))
    performance_ranking.plot(kind="bar", color="mediumpurple", ax=ax)
    ax.set_title("Store Ranking by Annual Profit")
    ax.set_xlabel("Store")
    ax.set_ylabel("Annual Profit ($)")
    ax.tick_params(axis="x", rotation=30)
    comparison_fig.tight_layout()

    print("Store performance ranking by annual profit:")
    print(performance_ranking)

    return {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": comparison_fig,
    }


# 2.3 Analyze seasonal patterns and their impact
# REQUIRED: Return seasonal analysis
def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum()
    dow_sales = sales_df.groupby(sales_df["Date"].dt.day_name())["Sales"].mean().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    seasonal_fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(monthly_sales.index, monthly_sales.values, marker="o", color="forestgreen")
    axes[0].set_title("Monthly Sales Seasonality")
    axes[0].set_xlabel("Month")
    axes[0].set_ylabel("Sales ($)")
    axes[0].grid(alpha=0.3)

    dow_sales.plot(kind="bar", ax=axes[1], color="coral")
    axes[1].set_title("Average Sales by Day of Week")
    axes[1].set_xlabel("Day")
    axes[1].set_ylabel("Average Sales ($)")
    axes[1].tick_params(axis="x", rotation=45)

    seasonal_fig.tight_layout()

    return {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": seasonal_fig,
    }


# TODO 3: Predictive Analytics - Basic Forecasting
# 3.1 Create a simple linear regression model to predict store sales
# REQUIRED: Return model results
def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    merged = pd.merge(store_df, operational_df[["Store", "AnnualSales"]], on="Store", how="inner")
    feature_cols = ["SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]

    X = merged[feature_cols].values.astype(float)
    y = merged["AnnualSales"].values.astype(float)

    # Ordinary Least Squares using numpy
    X_design = np.column_stack([np.ones(len(X)), X])
    beta, _, _, _ = np.linalg.lstsq(X_design, y, rcond=None)
    y_pred = X_design @ beta

    ss_total = float(np.sum((y - y.mean()) ** 2))
    ss_res = float(np.sum((y - y_pred) ** 2))
    r_squared = 1 - (ss_res / ss_total if ss_total != 0 else 0)

    coefficients = {feature_cols[i]: float(beta[i + 1]) for i in range(len(feature_cols))}
    predictions = pd.Series(y_pred, index=merged["Store"], name="PredictedAnnualSales")

    model_fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(y, y_pred, color="darkcyan")
    line_min, line_max = min(y.min(), y_pred.min()), max(y.max(), y_pred.max())
    ax.plot([line_min, line_max], [line_min, line_max], linestyle="--", color="gray")
    ax.set_title("Actual vs Predicted Annual Sales")
    ax.set_xlabel("Actual Annual Sales")
    ax.set_ylabel("Predicted Annual Sales")
    model_fig.tight_layout()

    print("Regression coefficients:")
    print(coefficients)
    print(f"Model R-squared: {r_squared:.4f}")

    return {
        "coefficients": coefficients,
        "r_squared": float(r_squared),
        "predictions": predictions,
        "model_fig": model_fig,
    }


# 3.2 Forecast departmental sales trends
# REQUIRED: Return forecast results
def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    monthly_dept = (
        sales_df.groupby([sales_df["Date"].dt.to_period("M"), "Department"])["Sales"]
        .sum()
        .unstack()
        .sort_index()
    )
    monthly_dept.index = monthly_dept.index.to_timestamp()

    growth_rates = ((monthly_dept.iloc[-1] - monthly_dept.iloc[0]) / monthly_dept.iloc[0]).sort_values(ascending=False)

    # Simple 3-month moving average forecast for next month
    moving_avg = monthly_dept.rolling(window=3).mean()
    next_month_forecast = moving_avg.iloc[-1]
    forecast_row = pd.DataFrame([next_month_forecast], index=[monthly_dept.index[-1] + pd.offsets.MonthBegin(1)])
    dept_trends = pd.concat([monthly_dept, forecast_row])

    forecast_fig, ax = plt.subplots(figsize=(10, 6))
    for dept in monthly_dept.columns:
        ax.plot(monthly_dept.index, monthly_dept[dept], label=f"{dept} (Actual)")
        ax.scatter(forecast_row.index, forecast_row[dept], marker="x", s=70)
    ax.set_title("Department Sales Trends with Next-Month Forecast")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales ($)")
    ax.legend(fontsize=8, ncol=2)
    ax.grid(alpha=0.2)
    forecast_fig.tight_layout()

    return {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": forecast_fig,
    }


# TODO 4: Integrated Analysis - Business Insights and Recommendations
# 4.1 Identify the most profitable combinations of store, department, and customer segments
# REQUIRED: Return opportunity analysis
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    store_dept_profit = (
        sales_df.groupby(["Store", "Department"]).agg(
            TotalSales=("Sales", "sum"),
            TotalProfit=("Profit", "sum"),
            AvgMargin=("ProfitMargin", "mean"),
        )
    )
    top_combinations = store_dept_profit.sort_values("TotalProfit", ascending=False).head(10)
    underperforming = store_dept_profit.sort_values("TotalProfit", ascending=True).head(10)

    # Opportunity score favors high margin + low relative sales
    store_totals = store_dept_profit.groupby(level=0).agg({"TotalSales": "sum", "TotalProfit": "sum", "AvgMargin": "mean"})
    sales_rank = store_totals["TotalSales"].rank(pct=True)
    margin_rank = store_totals["AvgMargin"].rank(pct=True)
    opportunity_score = (margin_rank * (1 - sales_rank)).sort_values(ascending=False)

    return {
        "top_combinations": top_combinations,
        "underperforming": underperforming,
        "opportunity_score": opportunity_score,
    }


# 4.2 Develop recommendations for improving performance
# REQUIRED: Return list of recommendations
def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    low_store = sales_by_store.index[-1]
    high_store = sales_by_store.index[0]

    dept_profitability = sales_df.groupby("Department")["Profit"].sum().sort_values(ascending=False)
    best_dept = dept_profitability.index[0]
    weakest_dept = dept_profitability.index[-1]

    top_segment = customer_df.groupby("Segment")["MonthlySpend"].mean().idxmax()

    recommendations = [
        f"Increase weekly marketing spend by 10-15% in {low_store} and tie campaigns to high-performing categories from {high_store} to lift traffic.",
        f"Expand shelf space and promotional bundles for {best_dept}, which is currently the top profit contributor across stores.",
        f"Launch margin-improvement initiatives in {weakest_dept} (supplier renegotiation, waste reduction, private-label options).",
        f"Create targeted loyalty offers for the {top_segment} segment to increase retention and encourage cross-department purchases.",
        "Use month-ahead inventory planning based on seasonal peaks (summer and December) to reduce stockouts and markdown losses.",
        "Track store-level KPIs weekly (sales per sq ft, sales per staff, profit margin) and implement quarterly coaching for underperforming stores.",
    ]

    return recommendations


# TODO 5: Summary Report
# REQUIRED: Generate comprehensive summary
def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    sales_metrics = analyze_sales_performance()
    store_rank = compare_store_performance()["performance_ranking"]
    growth_rates = forecast_department_sales()["growth_rates"]
    recs = develop_recommendations()

    print("Overview:")
    print(
        "GreenGrocer delivered strong annual revenue with clear variation by store, department, and season. "
        "Performance is highest in larger, more mature stores, while lower-volume stores show targeted upside "
        "when paired with focused marketing, assortment, and operational improvements."
    )

    print("\nKey Findings:")
    print(f"- Total annual sales reached ${sales_metrics['total_sales']:,.0f} with total profit of ${sales_metrics['total_profit']:,.0f}.")
    print(f"- {store_rank.index[0]} is the highest-profit store, while {store_rank.index[-1]} has the most improvement potential.")
    print(f"- Average profit margin is {sales_metrics['avg_profit_margin']:.2%}, with meaningful department-level variation.")
    print(f"- The fastest recent department growth was observed in {growth_rates.index[0]} based on monthly trend analysis.")

    print("\nRecommendations:")
    for rec in recs[:5]:
        print(f"- {rec}")

    print("\nExpected Impact:")
    print(
        "If executed in the next planning cycle, these actions are expected to improve revenue mix, lift store productivity, "
        "and increase company-wide profitability. A pragmatic target is low-to-mid single-digit annual sales growth with margin "
        "expansion driven by better department allocation and more precise customer targeting."
    )


# Main function to execute all analyses
# REQUIRED: Do not modify function name
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)

    # Execute analyses in a logical order
    # REQUIRED: Store all results for potential testing

    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()

    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()

    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()

    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()

    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()

    # Show all figures
    plt.show()

    # Return results for testing purposes
    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations,
        'dist_figs': dist_figs,
    }


# Run the main function
if __name__ == "__main__":
    results = main()