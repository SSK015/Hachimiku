"""
Core utility functions for plotting.
"""

import matplotlib.pyplot as plt
import numpy as np


def auto_fontsize(fig, base_size=12):
    """Automatically adjust font size based on figure dimensions and number of subplots"""
    w, h = fig.get_size_inches()
    num_axes = len(fig.axes)
    
    # Base scale on area
    scale = np.sqrt(w * h) / np.sqrt(8 * 3)
    
    # If there are many subplots, reduce the font size scale
    if num_axes > 1:
        scale = scale / np.sqrt(num_axes) * 1.5 # Empirical correction for subplots
        
    return base_size * scale


def setup_matplotlib_style():
    """Set up global matplotlib style parameters"""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif', 'Liberation Serif', 'Bitstream Vera Serif', 'serif'],
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
        'mathtext.fontset': 'stix', # Ensure math formulas use a similar serif style
        'hatch.linewidth': 0.8,
    })


def general_line_style():
    """General line style configuration"""
    return {
        'linewidth': 2.5,
        'markersize': 12,
        'markeredgewidth': 2,
        'alpha': 0.8,
    }


def setup_spines(ax, linewidth=1.5, color='black', top_right_spine_style='solid', top_right_spine_color='gray'):
    """Configure axis spines (borders)"""
    for spine_name in ['top', 'bottom', 'left', 'right']:
        spine = ax.spines[spine_name]
        spine.set_visible(True)
        
        if spine_name in ['top', 'right']:
            # If solid, color follows main (default black); otherwise use specified color (default gray)
            current_color = color if top_right_spine_style == 'solid' else top_right_spine_color
            spine.set_color(current_color)
            spine.set_linestyle(top_right_spine_style)
            # For dashed borders, suggest slightly thinner or allow external width control
            spine.set_linewidth(linewidth)
        else:
            spine.set_color(color)
            spine.set_linestyle('solid')
            spine.set_linewidth(linewidth)


def is_dark_color(color):
    """Determine if a color is dark (used for text color decisions)"""
    try:
        # Convert to RGB
        if color.startswith('#'):
            r = int(color[1:3], 16) / 255.0
            g = int(color[3:5], 16) / 255.0
            b = int(color[5:7], 16) / 255.0
        else:
            # Simple check for named colors
            dark_colors = ['blue', 'green', 'purple', 'black', 'navy', 'maroon']
            return color in dark_colors

        # Calculate brightness using standard luminance formula
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness < 0.5
    except:
        return False


def get_rgb_from_color(color):
    """Extract RGB values from a color specification"""
    try:
        if color.startswith('#'):
            return (int(color[1:3], 16) / 255.0,
                   int(color[3:5], 16) / 255.0,
                   int(color[5:7], 16) / 255.0)
        else:
            # Simple color mapping for named colors
            color_map = {
                'red': (1, 0, 0), 'orange': (1, 0.5, 0), 'yellow': (1, 1, 0),
                'blue': (0, 0, 1), 'green': (0, 1, 0), 'purple': (0.5, 0, 0.5),
                'black': (0, 0, 0), 'white': (1, 1, 1)
            }
            return color_map.get(color, (0.5, 0.5, 0.5))
    except:
        return (0.5, 0.5, 0.5)


def calculate_color_contrast(color1, color2):
    """Calculate color contrast between two colors (Euclidean distance)"""
    r1, g1, b1 = get_rgb_from_color(color1)
    r2, g2, b2 = get_rgb_from_color(color2)
    return np.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)
