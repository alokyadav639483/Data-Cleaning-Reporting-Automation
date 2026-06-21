"""
Data Cleaning & Reporting Automation Engine
Author: Data Analytics Team
Description: Automatically cleans data anomalies and exports structured Excel reports with visual plots.
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress background execution warnings
warnings.filterwarnings("ignore")

def generate_dirty_raw_dataset():
    """Generates a synthetic dirty dataset with missing values, duplicates, and format inconsistencies."""
    print("[INFO] Simulating raw uncleaned transaction database streams...")
    np.random.seed(10)
    
    total_records = 150
    transaction_ids = [f"TXN_{2000 + i}" for i in range(total_records)]
    
    # Intentionally introducing duplicate records
    for i in range(10):
        transaction_ids[140 + i] = transaction_ids[i]
        
    regions = np.random.choice(['North', 'South', 'East', 'West', 'north', 'EAST '], size=total_records)
    revenue = np.random.normal(500, 150, size=total_records)
    units_sold = np.random.randint(5, 50, size=total_records)
    
    df = pd.DataFrame({
        'TransactionID': transaction_ids,
        'Region': regions,
        'Revenue_USD': np.round(revenue, 2),
        'Units_Sold': units_sold
    })
    
    # Intentionally introducing missing values (NaNs)
    df.loc[np.random.choice(df.index, size=12, replace=False), 'Revenue_USD'] = np.nan
    df.loc[np.random.choice(df.index, size=8, replace=False), 'Units_Sold'] = np.nan
    
    return df

def execute_automated_data_cleaning(df):
    """Automates removal of duplicates, treats missing values, and fixes formatting errors."""
    print("[INFO] Initializing rule-based cleaning sequence...")
    
    # 1. Identify and drop duplicate transactions
    duplicate_count = df.duplicated(subset=['TransactionID']).sum()
    df.drop_duplicates(subset=['TransactionID'], keep='first', inplace=True)
    print(f"[CLEAN] Eliminated {duplicate_count} structural duplicate records.")
    
    # 2. Fix inconsistent text casing and white spaces
    df['Region'] = df['Region'].astype(str).str.strip().str.capitalize()
    print("[CLEAN] Standardized text casing and removed trailing whitespaces.")
    
    # 3. Impute missing numeric values using column medians safely
    revenue_median = df['Revenue_USD'].median()
    units_median = df['Units_Sold'].median()
    
    df['Revenue_USD'] = df['Revenue_USD'].fillna(revenue_median)
    df['Units_Sold'] = df['Units_Sold'].fillna(units_median).astype(int)
    print("[CLEAN] Handled missing values using median imputation strategies.")
    
    return df

def generate_automated_report_assets(df):
    """Compiles metric performance summaries and saves data assets locally."""
    print("[INFO] Creating analytical summary tables...")
    
    # Grouping performance metrics by operational business region
    regional_summary = df.groupby('Region').agg(
        Total_Transactions=('TransactionID', 'count'),
        Total_Revenue_USD=('Revenue_USD', 'sum'),
        Total_Units_Sold=('Units_Sold', 'sum'),
        Average_Order_Value_USD=('Revenue_USD', 'mean')
    ).round(2).reset_index()
    
    # Exporting clean excel report workbook sheet
    excel_report_name = 'automated_business_report.xlsx'
    with pd.ExcelWriter(excel_report_name, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Cleaned_Data_Master', index=False)
        regional_summary.to_excel(writer, sheet_name='Regional_KPI_Summary', index=False)
    print(f"[SUCCESS] Multi-sheet Excel workbook exported as '{excel_report_name}'")
    
    # Generating visual summary distribution chart
    print("[INFO] Generating visual performance summaries...")
    plt.figure(figsize=(10, 5.5))
    sns.set_theme(style="whitegrid")
    
    sns.barplot(
        data=regional_summary,
        x='Region',
        y='Total_Revenue_USD',
        palette='Blues_r',
        edgecolor='0.2'
    )
    
    plt.title('Automated Regional Financial Revenue Summary', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Operational Region', fontsize=11)
    plt.ylabel('Total Accumulated Revenue (USD)', fontsize=11)
    
    plt.tight_layout()
    chart_image_name = 'automated_report_chart.png'
    plt.savefig(chart_image_name, dpi=300)
    print(f"[SUCCESS] Visual report summary chart exported as '{chart_image_name}'")
    plt.show()
    
    return regional_summary

if __name__ == "__main__":
    print("=== STARTING DATA CLEANING & REPORTING AUTOMATION PIPELINE ===")
    
    # Step A: Ingest uncleaned raw simulated logs
    dirty_data = generate_dirty_raw_dataset()
    print(f"[STAGE] Raw dataset initialized with shape: {dirty_data.shape}")
    
    # Step B: Pass dataset through pipeline to treat anomalies
    cleaned_data = execute_automated_data_cleaning(dirty_data)
    print(f"[STAGE] Cleaned dataset dimensions confirmed: {cleaned_data.shape}")
    
    # Step C: Compile business KPIs and build automated asset sheets
    kpi_summary = generate_automated_report_assets(cleaned_data)
    
    print("\n=== REGIONAL KPI METRIC PERFORMANCE REPORT ===")
    print(kpi_summary.to_string(index=False))
    print("================================================\n")
    print("=== WORKFLOW AUTOMATION COMPLETELY REDEEMED ===")