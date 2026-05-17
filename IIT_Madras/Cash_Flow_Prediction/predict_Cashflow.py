# CASH FLOW FORECASTING USING XGBOOST
# FUNCTION-BASED IMPLEMENTATION
# WITH FOREX EXCHANGE RATE ASSUMPTIONS
# ============================================================

# Install required libraries:
# pip install pandas numpy xgboost scikit-learn matplotlib

# ============================================================
# STEP 1 — IMPORT LIBRARIES
# ============================================================

from cffi import model
import pandas as pd
import numpy as np

from xgboost import XGBRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error

import matplotlib.pyplot as plt
import os
import warnings
import logging
from dotenv import load_dotenv

load_dotenv()




warnings.filterwarnings("ignore")

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))

set_data_path = os.path.join(parent_directory, "Cash_Flow_Prediction\data")
os.makedirs(set_data_path, exist_ok=True)
logs_directory_path = os.path.join(parent_directory, "Cash_Flow_Prediction\logs")
os.makedirs(logs_directory_path, exist_ok=True)
print("=" * 80)
print(f"Data directory path: {set_data_path}")
print("=" * 80)
print(f"Logs directory path: {logs_directory_path}")
print("=" * 80)
file_path = os.path.join(set_data_path, "sample_cashflow.csv")
print(f"Data file path: {file_path}")
print("=" * 80)
log_file_path = os.path.join(logs_directory_path, "Cash_Flow_Logging.log")
print(f"Log file path: {log_file_path}")
print("=" * 80)

logging.basicConfig(
    filename=log_file_path,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True
)

import logging
logging.info("Logging is configured and working")




# # ============================================================
# # STEP 2 — LOAD DATA
# # ============================================================

def load_data(file_path):

    df = pd.read_csv(file_path)
    df['Month'] = pd.to_datetime(df['Month'])
    df = df.sort_values('Month')
    return df

# # ============================================================
# # STEP 3 — CREATE FEATURES
# # ============================================================

def create_features(df):
    # Time-based features
    df['Year'] = df['Month'].dt.year
    df['Month_Num'] = df['Month'].dt.month
    df['Quarter'] = df['Month'].dt.quarter

    # Lag feature
    df['Lag_1'] = df['Net_Cash_Flow'].shift(1)

    # Rolling mean feature

    df['Rolling_Mean_3'] = ( df['Net_Cash_Flow'].rolling(window=3).mean() )

    # Remove null rows
    df = df.dropna()

    return df

# # ============================================================
# # STEP 4 — PREPARE TRAINING DATA
# # ============================================================

def prepare_training_data(df):
    print("\n===========PREPARING TRAINING DATA===================")
    logging.info("Preparing training data by selecting features and target variable")
    
    features = [
        'Revenue',
        'Payroll',
        'Vendor_Payments',
        'Operating_Expenses',
        'FX_Impact',
        'Tax_Payments',
        'Inflation_Rate',
        'Interest_Rate',
        'Projected_Sales_Growth',
        'USD_Budget_Rate_Current_Year',
        'USD_Budget_Rate_Next_Year',
        'Month_Num',
        'Quarter',
        'Lag_1',
        'Rolling_Mean_3'
    ]

    target = 'Net_Cash_Flow'
    print(f"Selected features: {features}")     
    print(f"Target variable: {target}") 
    print("\n")
    
    X = df[features]
    y = df[target]
    print("\n")
    
    # Print first 50 records with headers
    print(df[features].head(50).to_string(index=False))
    print(df[target].head(50).to_string(index=False))
    logging.info("===============================")
    logging.info(f"Data with features:\n{df[features].head(50).to_string(index=False)}")
    logging.info("===============================")
    logging.info(f"Target variable:\n{df[target].head(50).to_string(index=False)}")
    print("=" * 80)
    logging.info("Finished preparing training data")
    logging.info("===============================")
    

    return X, y, features

# # ============================================================
# # STEP 5 — TRAIN MODEL
# # ============================================================

def train_model(X_train, y_train):

    model = XGBRegressor(n_estimators=200,learning_rate=0.05,max_depth=4,random_state=42)
    model.fit(X_train, y_train)
    return model

# # ============================================================
# # STEP 6 — EVALUATE MODEL
# # ============================================================

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mape = mean_absolute_percentage_error(y_test,predictions)
    print("\n==============================")
    print("MODEL EVALUATION")   
    logging.info("Evaluating the model using Mean Absolute Percentage Error (MAPE)")     
    print("==============================")
    print(f"MAPE: {mape * 100:.2f}%")
    logging.info("===============================")
    logging.info("finished evaluating the model and calculating MAPE")
    logging.info(f"MAPE: {mape * 100:.2f}%")
    logging.info("===============================")
    logging.info(f"Predictions:\n{pd.Series(predictions).head(50).to_string(index=False)}")
    logging.info("===============================")

    return predictions

# # ============================================================
# # STEP 7 — PLOT ACTUAL VS PREDICTED
# # ============================================================

def plot_predictions(y_test, predictions):

    plt.figure(figsize=(12,6))
    plt.plot(
    y_test.values,
    label='Actual Cash Flow'
    )

    plt.plot(
    predictions,
    label='Predicted Cash Flow'
    )

    plt.title("Actual vs Predicted Cash Flow")
    plt.xlabel("Time")
    plt.ylabel("Cash Flow")
    plt.legend()
    plt.show()

# # ============================================================
# # STEP 8 — FORECAST FUTURE CASH FLOW
# # ============================================================

def forecast_future_cashflow(
    model,df,
    features,
    forecast_months,
    revenue_growth_rate,
    payroll_growth_rate,
    vendor_growth_rate,
    opex_growth_rate,
    tax_growth_rate,
    inflation_rate_future,
    interest_rate_future,
    projected_sales_growth_future,
    usd_budget_rate_current_year,
    usd_budget_rate_next_year ):

    future_forecasts = []

    last_row = df.iloc[-1:].copy()

# # ----------------------------------------------------
# # APPLY FUTURE BUSINESS ASSUMPTIONS
# # ----------------------------------------------------

    for i in range(forecast_months):

        last_row['Revenue'] *= (1 + revenue_growth_rate)
        last_row['Payroll'] *= (1 + payroll_growth_rate)
        last_row['Vendor_Payments'] *= (1 + vendor_growth_rate)
        last_row['Operating_Expenses'] *= (1 + opex_growth_rate)
        last_row['Tax_Payments'] *= (1 + tax_growth_rate)

# # ----------------------------------------------------
# # APPLY FUTURE ECONOMIC ASSUMPTIONS
# # ----------------------------------------------------

        last_row['Inflation_Rate'] = (inflation_rate_future)
        last_row['Interest_Rate'] = (interest_rate_future)
        last_row['Projected_Sales_Growth'] = (projected_sales_growth_future)

# # ----------------------------------------------------
# # FOREX ASSUMPTIONS
# # ----------------------------------------------------

        last_row['USD_Budget_Rate_Current_Year'] = (usd_budget_rate_current_year)
        last_row['USD_Budget_Rate_Next_Year'] = (usd_budget_rate_next_year)

# # ----------------------------------------------------
# # FX IMPACT CALCULATION
# # ----------------------------------------------------

        fx_variance = (usd_budget_rate_next_year- usd_budget_rate_current_year)

    # Example FX impact calculation

        last_row['FX_Impact'] = (fx_variance * 100000)

#     # ----------------------------------------------------
#     # UPDATE MONTH
#     # ----------------------------------------------------

        next_month = (last_row['Month']+ pd.DateOffset(months=1))
        last_row['Month'] = next_month

#     # ----------------------------------------------------
#     # UPDATE DATE FEATURES
#     # ----------------------------------------------------

        last_row['Month_Num'] = (
        next_month.dt.month.values[0]
        )

        last_row['Quarter'] = (
        next_month.dt.quarter.values[0]
        )

# # ----------------------------------------------------
# # PREDICT FUTURE CASH FLOW
# # ----------------------------------------------------
        print("\n==============================")
        future_X = last_row[features]
        print("FUTURE X : Last row features for prediction:\n", future_X.to_string(index=False))
        logging.info("FUTURE X : last row features for prediction:\n" + future_X.to_string(index=False))
        
        print("\n==============================")
        
        ## Make prediction for the next months cash flow
        future_prediction = model.predict( future_X  )[0]

#     # ----------------------------------------------------
#     # STORE FORECAST
#     # ----------------------------------------------------

        future_forecasts.append({

        'Month': next_month.values[0],

        'Forecasted_Cash_Flow': round(   future_prediction,   2   ),

        'USD_Budget_Rate_Current_Year': usd_budget_rate_current_year,

        'USD_Budget_Rate_Next_Year':   usd_budget_rate_next_year,

        'FX_Impact': round( last_row['FX_Impact'].values[0],  2  )
        
        })

#     # ----------------------------------------------------
#     # UPDATE LAG FEATURES
#     # ----------------------------------------------------

        last_row['Lag_1'] = future_prediction
        last_row['Rolling_Mean_3'] = (  last_row['Rolling_Mean_3'] * 0.7   + future_prediction * 0.3
        )
        last_row['Net_Cash_Flow'] = ( future_prediction   )
    
    
    forecast_df = pd.DataFrame( future_forecasts  )
    print("\n==============================")    
    logging.info("==========================================")
    logging.info(f"FORECAST Prediction from Inside Function    :\n{forecast_df.head(300)}")
    print("Forecast Prediction data  :\n", forecast_df.head(300).to_string(index=False))
    
    return forecast_df

# # ============================================================
# # STEP 9 — PLOT FUTURE FORECAST
# # ============================================================

# def plot_forecast(forecast_df):

#     plt.figure(figsize=(12,6))

#     plt.plot(

#     forecast_df['Month'],

#     forecast_df['Forecasted_Cash_Flow']

#     )

#     plt.title(
#     "Future Cash Flow Forecast"
#     )

#     plt.xlabel("Month")

#     plt.ylabel(
#     "Forecasted Cash Flow"
#     )

#     plt.xticks(rotation=45)

#     plt.show()

# # ============================================================
# # STEP 10 — FEATURE IMPORTANCE
# # ============================================================

# def show_feature_importance(model,features):

#     importance = model.feature_importances_feature_importance_df = pd.DataFrame({

#     'Feature': features,
#     'Importance': importance

#     })
    
#     feature_importance_df = (feature_importance_df
#     .sort_values(
#     by='Importance',
#     ascending=False
#     )
# )

    print("\n==============================")
    print("FEATURE IMPORTANCE")
    print("==============================")
    print("Feature  Importantce :", feature_importance_df.to_string(index=False))
    print("==============================")
    logging.info(f"Features Importante for the model:\n{feature_importance_df.to_string(index=False)}   ")    
    logging.info("==========================================")


# # ============================================================
# # STEP 11 — MAIN PROGRAM
# # ============================================================

def main():

#     # --------------------------------------------------------
#     # FILE PATH
#     # --------------------------------------------------------

    file_path = os.path.join(set_data_path, "sample_cashflow.csv")

#     # --------------------------------------------------------
#     # LOAD DATA
#     # --------------------------------------------------------

    df = load_data(file_path)

#     # --------------------------------------------------------
#     # ADD FOREX BUDGET RATE COLUMNS
#     # --------------------------------------------------------

#     # Example assumptions

    df['USD_Budget_Rate_Current_Year'] = 84.00
    df['USD_Budget_Rate_Next_Year'] = 86.00

#     # --------------------------------------------------------
#     # CREATE FEATURES
#     # --------------------------------------------------------

    df = create_features(df)
    print("\n===========FEATURES created===================")
    print(df)
    print("\n")
    print("--"*80 )
    logging.info("==========================================")
    logging.info(f"Data with features:\n{df.head(50)}")
    # Print first 50 records with headers
    print(df.head(50).to_string(index=False))
    print("=" * 80)
    logging.info(f"Features created successfully")
    logging.info("==========================================")

# # --------------------------------------------------------
# # PREPARE TRAINING DATA
# # --------------------------------------------------------

    X, y, features = prepare_training_data(df)
    print("\n===========TRAINING DATA COMPLETED===================")
    logging.info("==========================================")
    logging.info(f"Training DATA COMPLETED")
    
    
    # --------------------------------------------------------
    # TRAIN TEST SPLIT
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = (
    train_test_split( X, y, test_size=0.2, shuffle=False)
    )

    print("\n===========Training Split DATA COMPLETED===================")
    logging.info("==========================================")
    logging.info(f"Training Split DATA COMPLETED=")
    
# # --------------------------------------------------------
# # TRAIN MODEL
# # --------------------------------------------------------
    import time
    start_time = time.time()
    print("\n===========Start training the Model===================")
    logging.info(f"REcording Model Start time: {start_time}")
    logging.info(f"STARTED Training the Model")
    model = train_model(X_train,y_train)    
    end_time = time.time()
    execution_time = end_time - start_time    
    print("Execution Time:", {execution_time}, "seconds")
    
    logging.info(f"REcording Model End time: {end_time}")
    logging.info("==========================================")    
    logging.info(f"REcording Model End time: {end_time}")
    logging.info(f"Execution Time: {execution_time} seconds")    
    logging.info(f"Completed the Training of the model successfully")
    
#     # --------------------------------------------------------
#     # EVALUATE MODEL
#     # --------------------------------------------------------

    predictions = evaluate_model( model,X_test,y_test)

# # --------------------------------------------------------
# # PLOT PREDICTIONS
# # --------------------------------------------------------

#     plot_predictions(y_test,predictions)

# # --------------------------------------------------------
# # FUTURE FORECASTING
# # --------------------------------------------------------

    forecast_df = forecast_future_cashflow(model=model,
        df=df,
        features=features,
        forecast_months=12,
        revenue_growth_rate=0.03,
        payroll_growth_rate=0.01,
        vendor_growth_rate=0.015,
        opex_growth_rate=0.02,
        tax_growth_rate=0.01,
        inflation_rate_future=4.5,
        interest_rate_future=5.0,
        projected_sales_growth_future=10.0,
        usd_budget_rate_current_year=93.00,
        usd_budget_rate_next_year=95.00
        )

# # # --------------------------------------------------------
# # # DISPLAY FORECAST
# # # --------------------------------------------------------

    print("\n==============================")
    print("12 MONTH CASH FLOW FORECAST")
    print("==============================")
    print(forecast_df)
    logging.info("==========================================")
    logging.info(f"Run #1 : FORECAST Data    :\n{forecast_df.head(300)}")
    print("=" * 80)
    logging.info(f"Run #1 : 12 MONTH CASH FLOW FORECAST:\n{forecast_df.to_string(index=False)}")
    # Print first 300 records with headers
    print(forecast_df.head(300).to_string(index=False))
    print("=" * 80)
    print("=" * 80)
    
    
    forecast_df2 = forecast_future_cashflow(model=model,
        df=df,
        features=features,
        forecast_months=12,
        revenue_growth_rate=0.03,
        payroll_growth_rate=0.05,
        vendor_growth_rate=0.020,
        opex_growth_rate=0.02,
        tax_growth_rate=0.01,
        inflation_rate_future=4.5,
        interest_rate_future=5.0,
        projected_sales_growth_future=12.0,
        usd_budget_rate_current_year=93.00,
        usd_budget_rate_next_year=95.00
        )
     
    print("\n==============================")
    print("Run #2 : After USD Value Changes - 12 MONTH CASH FLOW FORECAST")
    print("==============================")
    print(forecast_df2)
    logging.info("==========================================")
    logging.info(f"Run #2 : After USD Value Changes - 12 MONTH CASH FLOW FORECAST Data    :\n{forecast_df2.head(300)}")
    print("=" * 80)
    logging.info(f"Run #2 : After USD Value Changes - 12 MONTH CASH FLOW FORECAST:\n{forecast_df2.to_string(index=False)}")
    # Print first 300 records with headers
    print(forecast_df2.head(300).to_string(index=False))
    print("=" * 80)
    print("=" * 80)
    

#     # --------------------------------------------------------
#     # PLOT FORECAST
#     # --------------------------------------------------------

#     #plot_forecast(forecast_df)

#     # --------------------------------------------------------
#     # FEATURE IMPORTANCE
#     # --------------------------------------------------------

     # show_feature_importance( model,features)

#     # ============================================================
#     # RUN PROGRAM
#     # ============================================================

if __name__ == "__main__":
    main()
# # ============================================================
# # END OF PROGRAM
# # ============================================================
