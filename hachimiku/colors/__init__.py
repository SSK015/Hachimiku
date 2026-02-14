"""
Color management module for the plotting library.
"""

from .palettes import (
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
)
from .showcase import ColorShowcase

__all__ = [
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
    'ColorShowcase'
]
