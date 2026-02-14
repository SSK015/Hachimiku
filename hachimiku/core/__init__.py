"""
Core utilities for the plotting library.
"""

from .utils import auto_fontsize, setup_matplotlib_style, general_line_style
from .label_generator import LabelGenerator
from .layout import LayoutManager

__all__ = ['auto_fontsize', 'setup_matplotlib_style', 'general_line_style', 'LabelGenerator', 'LayoutManager']
