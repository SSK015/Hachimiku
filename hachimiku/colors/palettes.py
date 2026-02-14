"""
Color palettes for the plotting library.
"""

from enum import Enum
from typing import List, Optional, Union, Tuple


# Basic color lists
colors_list_opt = ["#8eed99", "#8ebaed", "#db4249", "#eb9935"]
colors_list_raw_warm = ['red', 'orange', 'yellow']
colors_list_raw_cool = ['blue', 'green', 'purple']
colors_list_opt_warm = ["#ff4c35", "#eb9935", "#f7de1c"]
colors_list_opt_cool = ["#1c6bf7", "#1cdff7", "#72CA14", "#A225E4"]
colors_list_reproduce = ['#d62728', '#ffbb78', '#6b4c9a', '#1f77b4']


class ColorPalette(Enum):
    """Predefined color palettes"""
    OPTIMIZED = "optimized"
    RAW_WARM = "raw_warm"
    RAW_COOL = "raw_cool"
    OPT_WARM = "opt_warm"
    OPT_COOL = "opt_cool"


# Create preset palettes for 2-6 colors
# These presets are optimized to ensure good contrast and visual distinction between colors
preset_2_colors = ["#8eed99", "#db4249"]  # Green and red, high contrast
preset_3_colors = ["#8eed99", "#8ebaed", "#db4249"]  # Green, blue, red
preset_4_colors = ["#8eed99", "#8ebaed", "#db4249", "#eb9935"]  # Green, blue, red, orange
preset_5_colors = ["#8eed99", "#8ebaed", "#db4249", "#eb9935", "#A225E4"]  # Add purple
preset_6_colors = ["#8eed99", "#8ebaed", "#db4249", "#eb9935", "#A225E4", "#1cdff7"]  # Add cyan

# Highlight presets (Neutral backgrounds with one/two strong accent colors)
# Backgrounds: #d1d5db (gray), #e5e7eb (light gray)
# Accents: #dc2626 (red), #2563eb (blue), #f59e0b (orange)
highlight_red_colors = ["#dc2626", "#d1d5db", "#94a3b8", "#e5e7eb"]
highlight_blue_colors = ["#2563eb", "#d1d5db", "#94a3b8", "#e5e7eb"]
highlight_orange_colors = ["#f59e0b", "#d1d5db", "#94a3b8", "#e5e7eb"]

# Warm highlight preset (Last color is vivid warm, others are various cold/desaturated tones)
# Cold/Desaturated: #607d8b (Blue Grey), #90a4ae (Light Blue Grey), #455a64 (Dark Blue Grey)
warm_highlight_colors = ["#607d8b", "#90a4ae", "#455a64", "#b0bec5", "#ff4c35"]

# Vivid highlight preset (User provided: 3 cool/neutral, 2 warm highlight)
vivid_highlight_colors = ["#959d58", "#4b9851", "#4365b2", "#f18120", "#f34819"]
vivid_highlight_alphas = [0.8, 0.8, 0.8, 0.9, 0.9]

# Vivid highlight V2 (Subdued Blue, Green, Purple + Vivid Orange, Red)
vivid_highlight_v2_colors = ["#546a8c", "#6a8c78", "#7e6a8c", "#f59e0b", "#ef4444"]
vivid_highlight_v2_alphas = [0.8, 0.8, 0.8, 1.0, 1.0]

# Warm gradient preset (Light orange to deep red)
warm_gradient_colors = ["#ffedd5", "#fed7aa", "#fdba74", "#f97316", "#dc2626", "#991b1b"]

# Academic vivid preset (User provided spectrum)
academic_vivid_colors = ["#867d00", "#248600", "#005289", "#f18120", "#ff4c35", "#991b1b"]

# Preset name mapping
PRESET_NAME_MAP = {
    'optimized': colors_list_opt,
    'raw_warm': colors_list_raw_warm,
    'raw_cool': colors_list_raw_cool,
    'opt_warm': colors_list_opt_warm,
    'opt_cool': colors_list_opt_cool,
    'reproduce': colors_list_reproduce,
    'highlight_red': highlight_red_colors,
    'highlight_blue': highlight_blue_colors,
    'highlight_orange': highlight_orange_colors,
    'warm_highlight': warm_highlight_colors,
    'vivid_highlight': vivid_highlight_colors,
    'vivid_highlight_v2': vivid_highlight_v2_colors,
    'warm_gradient': warm_gradient_colors,
    'academic_vivid': academic_vivid_colors,
    'preset_2': preset_2_colors,
    'preset_3': preset_3_colors,
    'preset_4': preset_4_colors,
    'preset_5': preset_5_colors,
    'preset_6': preset_6_colors,
}

# Alpha preset mapping
ALPHA_PRESET_MAP = {
    'vivid_highlight': vivid_highlight_alphas,
    'vivid_highlight_v2': vivid_highlight_v2_alphas,
}

# Preset mapping for auto-selection by count
COUNT_PRESET_MAP = {
    2: preset_2_colors,
    3: preset_3_colors,
    4: preset_4_colors,
    5: preset_5_colors,
    6: preset_6_colors,
}


def get_color_palette(palette_type):
    """
    Get color palette of specified type

    Args:
        palette_type (str or ColorPalette): Palette type

    Returns:
        list: Color list
    """
    if isinstance(palette_type, ColorPalette):
        palette_type = palette_type.value

    palettes = {
        'optimized': colors_list_opt,
        'raw_warm': colors_list_raw_warm,
        'raw_cool': colors_list_raw_cool,
        'opt_warm': colors_list_opt_warm,
        'opt_cool': colors_list_opt_cool,
    }

    return palettes.get(palette_type, colors_list_opt)


class ColorPresetManager:
    """
    Color preset manager supporting three usage modes:
    1. Specify a preset name to load
    2. For 2-6 colors, if user doesn't specify, maintain a preset for each count
    3. User can specify for n colors: first m colors use one style, remaining n-m use another
    """
    
    def __init__(self):
        """Initialize color preset manager"""
        self.preset_map = PRESET_NAME_MAP.copy()
        self.alpha_map = ALPHA_PRESET_MAP.copy()
        self.count_preset_map = COUNT_PRESET_MAP.copy()
    
    def get_colors(self, 
                   num_colors: int,
                   preset_name: Optional[str] = None,
                   split_config: Optional[Tuple[int, str, str]] = None) -> List[str]:
        # ... (rest of get_colors)
        """
        Get color list based on user input
        
        Args:
            num_colors (int): Number of colors needed
            preset_name (str, optional): Preset name, if specified use this preset
            split_config (tuple, optional): Mixed configuration (m, preset_name_1, preset_name_2)
                - m: First m colors use first style
                - preset_name_1: Preset name for first m colors
                - preset_name_2: Preset name for remaining n-m colors
        
        Returns:
            List[str]: Color list
        
        Examples:
            # Mode 1: Specify preset name
            colors = manager.get_colors(4, preset_name='opt_warm')
            
            # Mode 2: Auto-select by count (2-6 colors)
            colors = manager.get_colors(3)  # Auto-use preset_3
            
            # Mode 3: Mixed style
            colors = manager.get_colors(5, split_config=(2, 'opt_warm', 'opt_cool'))
            # First 2 use opt_warm, remaining 3 use opt_cool
        """
        # Mode 1: If preset name is specified, use it directly
        if preset_name is not None:
            if preset_name not in self.preset_map:
                raise ValueError(f"Unknown preset name: {preset_name}. "
                               f"Available presets: {list(self.preset_map.keys())}")
            colors = self.preset_map[preset_name]
            # If needed colors exceed preset, cycle through
            if preset_name == 'warm_highlight':
                # Special logic for warm_highlight: 
                # keep the last one as the warm accent
                accent = colors[-1]
                cools = colors[:-1]
                if num_colors <= 1:
                    return [accent]
                num_cools = num_colors - 1
                bg_colors = (cools * ((num_cools // len(cools)) + 1))[:num_cools]
                return bg_colors + [accent]
            
            if num_colors <= len(colors):
                return colors[:num_colors]
            else:
                # Cycle extend color list
                return (colors * ((num_colors // len(colors)) + 1))[:num_colors]
        
        # Mode 3: If mixed configuration is specified
        if split_config is not None:
            m, preset_name_1, preset_name_2 = split_config
            if m < 0 or m > num_colors:
                raise ValueError(f"Split position m ({m}) must be between 0 and {num_colors}")
            
            if preset_name_1 not in self.preset_map:
                raise ValueError(f"Unknown preset name: {preset_name_1}")
            if preset_name_2 not in self.preset_map:
                raise ValueError(f"Unknown preset name: {preset_name_2}")
            
            colors_1 = self.preset_map[preset_name_1]
            colors_2 = self.preset_map[preset_name_2]
            
            # First m colors
            first_part = (colors_1 * ((m // len(colors_1)) + 1))[:m]
            # Remaining n-m colors
            second_part = (colors_2 * (((num_colors - m) // len(colors_2)) + 1))[:num_colors - m]
            
            return first_part + second_part
        
        # Mode 2: Auto-select by count (2-6 colors)
        if 2 <= num_colors <= 6:
            colors = self.count_preset_map[num_colors]
            return colors[:num_colors]
        elif num_colors < 2:
            # If less than 2, use first n colors from preset_2
            return preset_2_colors[:num_colors]
        else:
            # If more than 6, use preset_6 and cycle extend
            colors = preset_6_colors
            return (colors * ((num_colors // len(colors)) + 1))[:num_colors]
    
    def get_alphas(self, num_colors: int, preset_name: Optional[str] = None) -> Union[float, List[float]]:
        """
        Get alpha values for bars
        """
        if preset_name is not None and preset_name in self.alpha_map:
            alphas = self.alpha_map[preset_name]
            if num_colors <= len(alphas):
                return alphas[:num_colors]
            else:
                return (alphas * ((num_colors // len(alphas)) + 1))[:num_colors]
        return 1.0

    def register_preset(self, name: str, colors: List[str], alphas: Optional[List[float]] = None):
        """
        Register a new color preset
        
        Args:
            name (str): Preset name
            colors (List[str]): Color list
            alphas (List[float], optional): Alpha list
        """
        self.preset_map[name] = colors
        if alphas:
            self.alpha_map[name] = alphas
    
    def list_presets(self) -> List[str]:
        """
        List all available preset names
        
        Returns:
            List[str]: List of preset names
        """
        return list(self.preset_map.keys())

    def get_highlight_colors(self, num_colors: int, highlight_indices: Union[int, List[int]], 
                             accent_color: str = "#dc2626", 
                             neutral_color: str = "#d1d5db") -> List[str]:
        """
        Generate a color list where specific indices are highlighted
        
        Args:
            num_colors (int): Total number of colors
            highlight_indices (int or list): Index or indices to highlight
            accent_color (str): Color for highlighted items
            neutral_color (str): Color for non-highlighted items
            
        Returns:
            List[str]: List of colors
        """
        if isinstance(highlight_indices, int):
            highlight_indices = [highlight_indices]
            
        colors = []
        for i in range(num_colors):
            if i in highlight_indices:
                colors.append(accent_color)
            else:
                colors.append(neutral_color)
        return colors


# Create global preset manager instance
_default_preset_manager = ColorPresetManager()


def get_colors(num_colors: int,
               preset_name: Optional[str] = None,
               split_config: Optional[Tuple[int, str, str]] = None) -> List[str]:
    # ...
    return _default_preset_manager.get_colors(num_colors, preset_name, split_config)


def get_alphas(num_colors: int, preset_name: Optional[str] = None) -> Union[float, List[float]]:
    """
    Convenience function: Get alpha list for a preset
    """
    return _default_preset_manager.get_alphas(num_colors, preset_name)


def get_highlight_colors(num_colors: int, highlight_indices: Union[int, List[int]], 
                         preset_name: Optional[str] = None,
                         accent_color: Optional[str] = None, 
                         neutral_color: Optional[str] = None) -> List[str]:
    """
    Convenience function: Get colors with specific items highlighted
    
    Args:
        num_colors (int): Total number of colors
        highlight_indices (int or list): Index or indices to highlight
        preset_name (str, optional): Use a preset (e.g., 'highlight_red', 'highlight_blue')
        accent_color (str, optional): Custom accent color
        neutral_color (str, optional): Custom neutral color
    """
    if preset_name:
        presets = {
            'highlight_red': ("#dc2626", "#d1d5db"),
            'highlight_blue': ("#2563eb", "#d1d5db"),
            'highlight_orange': ("#f59e0b", "#d1d5db"),
        }
        if preset_name in presets:
            a, n = presets[preset_name]
            accent_color = accent_color or a
            neutral_color = neutral_color or n
            
    accent_color = accent_color or "#dc2626"
    neutral_color = neutral_color or "#d1d5db"
    
    return _default_preset_manager.get_highlight_colors(
        num_colors, highlight_indices, accent_color, neutral_color
    )
