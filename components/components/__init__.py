"""
Components Package for DashAuto Analytics
=========================================

This package contains all reusable Dash components for the 
Postgraduate Diploma Project: Automated Data Analytics and Visualization.
"""

# Import layouts and callback registration functions
# This allows cleaner imports in app.py

from .upload_component import upload_layout, register_upload_callbacks
from .eda_component import eda_layout, register_eda_callbacks
from .viz_component import viz_layout, register_viz_callbacks
from .table_component import table_layout, register_table_callbacks

__all__ = [
    # Layouts
    'upload_layout',
    'eda_layout',
    'viz_layout',
    'table_layout',
    
    # Callback Registrations
    'register_upload_callbacks',
    'register_eda_callbacks',
    'register_viz_callbacks',
    'register_table_callbacks'
]

# Optional: Version info for the components package
__version__ = "1.0.0"
__author__ = "Chukwuemeka Udogadi - Postgraduate Diploma Project"
