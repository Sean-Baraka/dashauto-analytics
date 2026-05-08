"""
Statistical Utilities for DashAuto Analytics
===========================================
Advanced statistical functions used for Automated EDA and Analysis.

Postgraduate Diploma Project - Data Application for Automated Data Analytics
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from scipy.stats import shapiro, normaltest, kstest
import warnings
warnings.filterwarnings('ignore')


def perform_full_statistical_analysis(df: pd.DataFrame) -> dict:
    """Perform comprehensive statistical analysis on the dataset"""
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    analysis = {
        "numeric_analysis": {},
        "categorical_analysis": {},
        "normality_tests": {},
        "correlation_summary": {},
        "outlier_summary": {}
    }
    
    # ==================== NUMERIC ANALYSIS ====================
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) == 0:
            continue
            
        # Basic statistics
        analysis["numeric_analysis"][col] = {
            "mean": float(data.mean()),
            "median": float(data.median()),
            "std": float(data.std()),
            "min": float(data.min()),
            "max": float(data.max()),
            "skewness": float(stats.skew(data)),
            "kurtosis": float(stats.kurtosis(data)),
            "count": int(len(data)),
            "missing": int(df[col].isnull().sum())
        }
        
        # Normality Tests
        try:
            # Shapiro-Wilk (best for small samples)
            if len(data) <= 5000:
                shapiro_stat, shapiro_p = shapiro(data.sample(min(5000, len(data)), random_state=42))
            else:
                shapiro_stat, shapiro_p = 0, 0  # Skip for very large data
            
            # D'Agostino's K² Test
            k2_stat, k2_p = normaltest(data)
            
            analysis["normality_tests"][col] = {
                "shapiro_p_value": float(shapiro_p),
                "dagostino_p_value": float(k2_p),
                "is_normal": float(shapiro_p) > 0.05 or float(k2_p) > 0.05
            }
        except:
            analysis["normality_tests"][col] = {"error": "Test could not be performed"}
    
    # ==================== OUTLIER DETECTION ====================
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) < 10:
            continue
            
        # Z-Score Method
        z_scores = np.abs(stats.zscore(data))
        z_outliers = (z_scores > 3).sum()
        
        # IQR Method
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = ((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).sum()
        
        analysis["outlier_summary"][col] = {
            "z_score_outliers": int(z_outliers),
            "iqr_outliers": int(iqr_outliers),
            "total_outliers": int(z_outliers + iqr_outliers)
        }
    
    # ==================== CORRELATION ANALYSIS ====================
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        analysis["correlation_summary"] = {
            "matrix": corr_matrix.round(4).to_dict(),
            "strong_positive": [],
            "strong_negative": []
        }
        
        # Find strong correlations
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                
                if abs(corr_val) > 0.7:
                    if corr_val > 0:
                        analysis["correlation_summary"]["strong_positive"].append({
                            "var1": col1, "var2": col2, "correlation": round(float(corr_val), 4)
                        })
                    else:
                        analysis["correlation_summary"]["strong_negative"].append({
                            "var1": col1, "var2": col2, "correlation": round(float(corr_val), 4)
                        })
    
    # ==================== CATEGORICAL ANALYSIS ====================
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        analysis["categorical_analysis"][col] = {
            "unique_count": int(df[col].nunique()),
            "top_categories": value_counts.head(5).to_dict(),
            "mode": str(value_counts.index[0]) if len(value_counts) > 0 else None
        }
    
    return analysis


def detect_variable_types(df: pd.DataFrame) -> dict:
    """Classify variables into types for smart recommendations"""
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    datetime_cols = []
    
    for col in df.columns:
        if df[col].dtype.kind in 'M' or 'date' in str(df[col].dtype).lower():
            datetime_cols.append(col)
    
    return {
        "numeric": numeric,
        "categorical": categorical,
        "datetime": datetime_cols,
        "total": len(df.columns)
    }


def suggest_best_visualization(x_var: str, y_var: str, df: pd.DataFrame) -> str:
    """Suggest best chart type based on variable types"""
    x_dtype = df[x_var].dtype.kind if x_var in df.columns else None
    y_dtype = df[y_var].dtype.kind if y_var and y_var in df.columns else None
    
    if y_var is None:
        return "histogram"
    elif x_dtype in ['i', 'f'] and y_dtype in ['i', 'f']:
        return "scatter"
    elif x_dtype in ['O', 'b'] and y_dtype in ['i', 'f']:
        return "box"
    else:
        return "bar"


def calculate_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return comprehensive descriptive statistics"""
    numeric = df.select_dtypes(include=[np.number])
    if numeric.empty:
        return pd.DataFrame()
    
    desc = numeric.describe().round(4)
    desc.loc['skew'] = numeric.skew().round(4)
    desc.loc['kurtosis'] = numeric.kurtosis().round(4)
    return desc


# ==================== UTILITY FUNCTIONS ====================

def is_numeric_series(series: pd.Series) -> bool:
    """Check if a pandas series is numeric"""
    return pd.api.types.is_numeric_dtype(series)


def count_significant_correlations(corr_matrix: pd.DataFrame, threshold: float = 0.7) -> int:
    """Count number of strong correlations"""
    corr = corr_matrix.abs()
    mask = np.triu(np.ones(corr.shape), k=1).astype(bool)
    return int((corr.where(mask) > threshold).sum().sum())


print("✅ Statistical Utilities Module Loaded Successfully!")
