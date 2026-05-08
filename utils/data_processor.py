import pandas as pd
import numpy as np
from scipy import stats

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates()
    
    # Optimize data types
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.6:
            df[col] = df[col].astype('category')
    
    # Try numeric conversion
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col], errors='ignore')
    return df

def generate_profile(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    profile = {
        "shape": list(df.shape),
        "columns": list(df.columns),
        "missing": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        "numeric_stats": df[numeric_cols].describe().round(4).to_dict() if numeric_cols else {},
        "cat_unique": {col: int(df[col].nunique()) for col in cat_cols},
        "correlation": df[numeric_cols].corr().round(4).to_dict() if len(numeric_cols) > 1 else {},
        "outliers": {col: int(np.sum(np.abs(stats.zscore(df[col].dropna())) > 3)) for col in numeric_cols}
    }
    return profile
