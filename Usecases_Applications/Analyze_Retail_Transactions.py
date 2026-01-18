## Rajendra Bichu. 
## Date : 8.11.2025  Version 1.0 , Retail Transaction data file analysis
## This is an assignment for Graded Assignment for IIT Course
## This program is written in VS code Visual Studio Code editor.

##========================================================================================

import pandas as pd
import os 
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from ast import literal_eval

# ===============================
# Load the dataset
# ===============================

current_directory = os.getcwd()
print("Current working directory:", current_directory)

#folder_path = r"C:\Rajendra_2015\AgenticAI_Programs\Agentic_Batch2\data_files"
folder_path = current_directory

print("Folder Path :"  + folder_path)

csv_filename = folder_path + "\data_files\Data_Set_Sample.csv"

print(csv_filename)


# Define the folder path and the CSV filename
#folder_path = r"C:\Users\YourUser\Documents\Data"  # Use 'r' for raw string to handle backslashes
csv_filename = folder_path + "\data_files\Data_Set_Sample.csv"
print(csv_filename)

# Construct the full file path
#file_path = os.path.join(folder_path, csv_filename)
file_path = csv_filename

print(file_path)

print("File to be loaded  :"  + file_path)

##Now start reading the contents of CSV file

data = pd.read_csv(file_path)

# ===============================
# 2️⃣ Define a function to extract date components
# ===============================

## Add all analysis to a file. 

def log_analysis_to_file(action, details):
    """Logs every transaction into a text file with timestamp and append it to a simple log file"""
    with open("Data_Analysis.txt", "a") as f:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {action}: {details}\n")


def extract_date_components(df, date_column='Date'):
    """
    Extracts year, month, and day of week from a given date column.
    Returns these as new Series and also adds them to the DataFrame.
    """
    # Convert date column to datetime
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    # Extract components
    df['Year'] = df[date_column].dt.year
    df['Month'] = df[date_column].dt.month
    df['DayOfWeek'] = df[date_column].dt.day_name()
    
    # Return extracted columns
    return df['Year'], df['Month'], df['DayOfWeek']

# ===============================
# 3️⃣ Apply the function
# ===============================
year, month, day_of_week = extract_date_components(data)

# ===============================
# 4️⃣ Basic dataset insights
# ===============================
total_transactions = len(data)
unique_customers = data['Customer_Name'].nunique()

# ===============================
# 5️⃣ Print summary results
# ===============================
print("===== DATA ANALYSIS SUMMARY =====")
print("=" * 60)

print(f"Total Transactions: {total_transactions}")
print(f"Unique Customers: {unique_customers}")


print("\nSample of Extracted Date Components:")
print("=" * 60)
print(data[['Date', 'Year', 'Month', 'DayOfWeek']].head())
print("=" * 60)

# ===============================
# 6️⃣ Optional: Save updated dataset
# ===============================
# This will include the new date component columns
data.to_csv("Processed_Data.csv", index=False)
print("\nProcessed dataset saved as 'Processed_Data.csv'")
print("=" * 60)
print(f"Total Transactions : {total_transactions}")
print(f"Unique Customers in the Data SET : {unique_customers}")

## Create a file for Analysis and add it to the file in the append mode

log_analysis_to_file("Total Transactions", f"{total_transactions}")
                  
log_analysis_to_file("Unique Customers Data SET", f"{unique_customers}")
                     

print("=" * 60)
print("=" * 60)

# ===============================
#   Top 5 most common products sold
# ===============================
# Convert the Product column (stored as string lists) into actual lists
data['Product'] = data['Product'].apply(lambda x: literal_eval(x) if isinstance(x, str) else [])

print("========Showing the Products====== :")
print(data['Product'])
print("=" * 60)


# Flatten all products into one list
all_products = [item for sublist in data['Product'] for item in sublist]

# Count frequency of each product
product_counts = pd.Series(all_products).value_counts().head(5)

print("===== TOP 5 MOST COMMON PRODUCTS =====")
print(product_counts)

print("=" * 60)
log_analysis_to_file("======= ", "===")
log_analysis_to_file("TOP FIVE COMMON PRODUCTS ", f"{product_counts}")
print()


# ===============================
# Cities with highest number of transactions
# ===============================
city_counts = data['City'].value_counts().head(5)

print("===== TOP 5 CITIES BY TRANSACTION COUNT =====")
print(city_counts)
print()

print("=" * 60)
log_analysis_to_file("======= ", "===")
log_analysis_to_file("TOP 5 CITIES BY TRANSACTION COUNT ", f"{city_counts}")


# ===============================
# Customer categories with highest average spending
# ===============================
avg_spend_by_category = (
    data.groupby('Customer_Category')['Total_Cost']
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

print("===== TOP CUSTOMER CATEGORIES BY AVERAGE SPEND =====")
print(avg_spend_by_category)
print()

print("=" * 60)
log_analysis_to_file("======= ", "===")
log_analysis_to_file("Customer Categories by Average Spends ", f"{avg_spend_by_category}")

# ===============================
# Season with highest total revenue
# ===============================
revenue_by_season = (
    data.groupby('Season')['Total_Cost']
    .sum()
    .sort_values(ascending=False)
)

top_season = revenue_by_season.idxmax()
top_season_revenue = revenue_by_season.max()

print("===== SEASONAL REVENUE =====")
print(revenue_by_season)
print(f"\n The season with the highest total revenue is **{top_season}**, "
      f"with total revenue of ${top_season_revenue:,.2f}.")
print()
print("=" * 60)


print("=" * 60)
log_analysis_to_file("======= ", "===")
log_analysis_to_file("The season with the highest total revenue ", f"{top_season}")
log_analysis_to_file("The season with the total revenue of ", f"{top_season_revenue}")

# ===============================
# To provide data for  effective promotion (by total cost)
# ===============================

promotional_effectiveness = (
    data[data['Promotion'].notna()]
    .groupby('Promotion')['Total_Cost']
    .mean()
    .sort_values(ascending=False)
)

top_promotion =  promotional_effectiveness.idxmax()
top_promotion_value =  promotional_effectiveness.max()

print("===== PROMOTION EFFECTIVENESS (by avg Total Cost) =====")
print( promotional_effectiveness)
print(f"\n The most effective promotion type is **{top_promotion}**, "
      f"with an average transaction value of ${top_promotion_value:,.2f}.")
print()


print("=" * 60)
log_analysis_to_file("======= ", "===")
log_analysis_to_file("The most effective promotion type ", f"{top_promotion}")
log_analysis_to_file("The average transaction value of effective promotion ", f"{top_promotion_value}")

# ===============================
# Average number of items bought per transaction per store type
# ===============================
avg_items_by_store = (
    data.groupby('Store_Type')['Total_Items']
    .mean()
    .sort_values(ascending=False)
)

print("===== AVERAGE ITEMS PER TRANSACTION (by Store Type) =====")
print(avg_items_by_store)
print()

print("=" * 60)
log_analysis_to_file("======= ", "===")
log_analysis_to_file("AVERAGE Items per transactions (by Store Type) ", f"{avg_items_by_store}")

# ===============================
# Average cost of transactions with vs without discount
# ===============================
avg_cost_discount = (
    data.groupby('Discount_Applied')['Total_Cost']
    .mean()
    .rename({True: 'Discount Applied', False: 'No Discount'})
)

print("===== AVERAGE COST: DISCOUNT VS NO DISCOUNT =====")
print(avg_cost_discount)
print("=" * 60)

log_analysis_to_file("======= ", "===")
log_analysis_to_file("AVERAGE COST: DISCOUNT VS NO DISCOUNT ", f"{avg_cost_discount}")

# ===============================
# Average number of items by promotion type
# ===============================
avg_items_by_promotion = (
    data[data['Promotion'].notna()]
    .groupby('Promotion')['Total_Items']
    .mean()
    .sort_values(ascending=False)
)

print("===== AVERAGE ITEMS PURCHASED BY PROMOTION TYPE =====")
print(avg_items_by_promotion)
print()
print("=" * 60)

log_analysis_to_file("======= ", "===")
log_analysis_to_file("AVERAGE Items Purchase(Promotion Type) ", f"{avg_items_by_promotion}")

# ========

# Cross-tab counts
category_payment_ct = pd.crosstab(
    data['Customer_Category'],
    data['Payment_Method']
)

print("===== CUSTOMER CATEGORY vs PAYMENT METHOD (Counts) =====")
print(category_payment_ct)

log_analysis_to_file("======= ", "===")
log_analysis_to_file("CUSTOMER CATEGORY vs PAYMENT METHOD ", f"{category_payment_ct}")
print()

# Normalized cross-tab (percentage of each category)
category_payment_pct = pd.crosstab(
    data['Customer_Category'],
    data['Payment_Method'],
    normalize='index'
).round(3)

print("===== CUSTOMER CATEGORY vs PAYMENT METHOD (Preference %) =====")
print(category_payment_pct)
print()
print("=" * 60)

from ast import literal_eval

# Ensure product strings are parsed into Python lists
data['Product'] = data['Product'].apply(
    lambda x: literal_eval(x) if isinstance(x, str) else x
)

# Explode list of products into individual rows
exploded = data.explode('Product')

# Count of products by Season × Product
season_product_counts = pd.crosstab(
    exploded['Season'],
    exploded['Product']
)

print("===== SEASONAL PREFERENCE FOR PRODUCT CATEGORIES (Counts) =====")
print(season_product_counts)
print()

# Percent distribution within each season
season_product_percent = pd.crosstab(
    exploded['Season'],
    exploded['Product'],
    normalize='index'
).round(3)

print("===== SEASONAL PREFERENCE FOR PRODUCT CATEGORIES (Percentages) =====")
print(season_product_percent)
print()
print("=" * 60)


## Few of the Charts to show the data for visualization

# Bar chart for average items per promotion type
avg_items_by_promotion.plot(kind='bar', title='Average Items Purchased per Promotion Type')
plt.ylabel('Average Number of Items')
plt.savefig('Average_Items.png', dpi=300) 
plt.show()

# Bar chart for average items per promotion type
city_counts.plot(kind='bar', title='Top Five Cities(Transaction Wise)')
plt.ylabel('Top 5 Cities')
plt.savefig('Top_Cities.png', dpi=300) 
plt.show()

# Ensure Date column is datetime
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Extract year and month
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Group by Year + Month and sum total revenue
monthly_revenue = data.groupby(['Year', 'Month'])['Total_Cost'].sum().reset_index()

# Pivot so each year becomes its own line in the chart
pivot_rev = monthly_revenue.pivot(index='Month', columns='Year', values='Total_Cost')

# Plot the line chart
plt.figure(figsize=(10,6))
plt.plot(pivot_rev)
plt.title("Monthly Revenue Trends by Year")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.legend(pivot_rev.columns, title="Year")
plt.grid(True)
plt.savefig('Revenue_Chart.png', dpi=300) 
plt.show()

# Calculate average spending per season
avg_spending_season = (
    data.groupby('Season')['Total_Cost']
    .mean()
    .sort_values()
)

# Plot the bar chart
plt.figure(figsize=(8,5))
plt.bar(avg_spending_season.index, avg_spending_season.values)
plt.title("Average Spending per Season")
plt.xlabel("Season")
plt.ylabel("Average Total Cost")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('Average_Season_Chart.png', dpi=300) 
plt.show()



# Aggregate revenue
rev_season_category = data.groupby(['Season', 'Customer_Category'])['Total_Cost'].sum().unstack()

# Plot heatmap
plt.figure(figsize=(10,6))
sns.heatmap(rev_season_category, annot=True, fmt=".1f", cmap="Blues")
plt.title("Revenue by Season and Customer Category (Heatmap)")
plt.xlabel("Customer Category")
plt.ylabel("Season")
plt.tight_layout()

plt.savefig('Heatmap_Data.png', dpi=300) 

plt.show()


print("Analaysis of the data is now completed.......")


print("=" * 60)