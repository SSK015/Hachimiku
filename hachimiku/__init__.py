"""
Hachimiku - A comprehensive Python plotting library with unified color management and chart types.

This library provides:
- Unified color palette management
- Multiple chart types (bar, line, CDF)
- Color showcase utilities
- Customizable plotting parameters

Example usage:
    from hachimiku import ColorShowcase, BarChart, LineChart, CDFChart

    # Create a color showcase
    showcase = ColorShowcase()
    showcase.create_artistic_showcase(save_path='colors.png')

    # Create a bar chart
    bar_chart = BarChart()
    bar_chart.create_grouped_bar_chart(x_data=['A', 'B'], y_data_list=[[5,3,8], [6,2,9]])

    # Create a line chart
    line_chart = LineChart()
    line_chart.create_line_chart(x_data=[1,2,3,4], y_data_list=[[1,4,9,16], [1,2,3,4]])
"""

__version__ = "1.0.0"

from .core import auto_fontsize, setup_matplotlib_style, general_line_style, LabelGenerator, LayoutManager
from .colors import (
    colors_list_opt,
    colors_list_raw_warm,
    colors_list_raw_cool,
    colors_list_opt_warm,
    colors_list_opt_cool,
    get_color_palette,
    ColorPalette,
    ColorPresetManager,
    get_colors,
    get_highlight_colors,
    preset_2_colors,
    preset_3_colors,
    preset_4_colors,
    preset_5_colors,
    preset_6_colors,
    ColorShowcase
)
from .charts import BarChart, LineChart, CDFChart, ComboChart, AreaChart

__all__ = [
    # Version
    '__version__',

    # Core utilities
    'auto_fontsize',
    'setup_matplotlib_style',
    'general_line_style',
    'LabelGenerator',
    'LayoutManager',

    # Color management
    'colors_list_opt',
    'colors_list_raw_warm',
    'colors_list_raw_cool',
    'colors_list_opt_warm',
    'colors_list_opt_cool',
    'get_color_palette',
    'ColorPalette',
    'ColorPresetManager',
    'get_colors',
    'get_highlight_colors',
    'preset_2_colors',
    'preset_3_colors',
    'preset_4_colors',
    'preset_5_colors',
    'preset_6_colors',
    'ColorShowcase',

    # Chart types
    'BarChart',
    'LineChart',
    'CDFChart',
    'ComboChart',
    'AreaChart'
]
