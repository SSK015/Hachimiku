"""
Color showcase functionality for creating color palette visualizations.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from ..core.utils import setup_matplotlib_style, auto_fontsize, is_dark_color, calculate_color_contrast
from .palettes import get_color_palette, ColorPalette


class ColorShowcase:
    """Color showcase class for creating various color palette visualizations"""

    def __init__(self, figsize=(16, 10)):
        """
        Initialize color showcase

        Args:
            figsize (tuple): Figure size
        """
        self.figsize = figsize
        setup_matplotlib_style()

    def create_artistic_showcase(self, color_groups=None, save_path=None, show=True):
        """
        Create an artistic color palette showcase

        Args:
            color_groups (list): List of color groups, each element is (group_name, color_list)
            save_path (str): Path to save the figure
            show (bool): Whether to display the figure
        """
        if color_groups is None:
            color_groups = [
                ("Optimized Colors", get_color_palette(ColorPalette.OPTIMIZED)),
                ("Raw Warm Tones", get_color_palette(ColorPalette.RAW_WARM)),
                ("Raw Cool Tones", get_color_palette(ColorPalette.RAW_COOL)),
                ("Optimized Warm", get_color_palette(ColorPalette.OPT_WARM)),
                ("Optimized Cool", get_color_palette(ColorPalette.OPT_COOL))
            ]

        fig = plt.figure(figsize=self.figsize)
        fig.suptitle('🎨 Artistic Color Palette Showcase', fontsize=24, fontweight='bold', y=0.95)

        # Create subplot layout
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

        # 1. Main color wheel
        ax_wheel = fig.add_subplot(gs[0:2, 0:2])
        self._create_wheel(ax_wheel, color_groups)

        # 2. Color intensity bar chart
        ax_bars = fig.add_subplot(gs[0, 2:])
        self._create_intensity_bars(ax_bars, color_groups)

        # 3. Color contrast matrix
        ax_matrix = fig.add_subplot(gs[1, 2:])
        self._create_contrast_matrix(ax_matrix, color_groups)

        # 4. Palette preview
        ax_palette = fig.add_subplot(gs[2, :])
        self._create_palette_preview(ax_palette, color_groups)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')

        if show:
            plt.show()

        return fig

    def create_simple_showcase(self, color_groups=None, save_path=None, show=True):
        """
        Create a simple color showcase

        Args:
            color_groups (list): List of color groups
            save_path (str): Path to save the figure
            show (bool): Whether to display the figure
        """
        if color_groups is None:
            color_groups = [
                ("Optimized Colors", get_color_palette(ColorPalette.OPTIMIZED)),
                ("Raw Warm Colors", get_color_palette(ColorPalette.RAW_WARM)),
                ("Raw Cool Colors", get_color_palette(ColorPalette.RAW_COOL)),
                ("Optimized Warm Colors", get_color_palette(ColorPalette.OPT_WARM)),
                ("Optimized Cool Colors", get_color_palette(ColorPalette.OPT_COOL))
            ]

        # Calculate layout
        max_cols = max(len(colors) for _, colors in color_groups)
        fig, axes = plt.subplots(len(color_groups), 1, figsize=(12, 8))
        fig.suptitle('Color Palette Showcase', fontsize=16, fontweight='bold', y=0.95)

        if len(color_groups) == 1:
            axes = [axes]

        # Create subplot for each color group
        for idx, (group_name, colors) in enumerate(color_groups):
            ax = axes[idx]
            ax.set_xlim(0, max_cols)
            ax.set_ylim(0, 1)
            ax.axis('off')

            # Add group name
            ax.text(-0.1, 0.5, group_name, ha='right', va='center',
                   fontsize=12, fontweight='bold', transform=ax.transAxes)

            # Create rectangle for each color
            rect_height = 0.8
            rect_width = 0.8

            for i, color in enumerate(colors):
                rect = patches.Rectangle((i, (1-rect_height)/2), rect_width, rect_height,
                                       facecolor=color, edgecolor='black', linewidth=2)
                ax.add_patch(rect)

                # Add color code label
                ax.text(i + rect_width/2, 0.5, color, ha='center', va='center',
                       fontsize=10, fontweight='bold', color='white' if is_dark_color(color) else 'black')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        if show:
            plt.show()

        return fig

    def create_wheel_showcase(self, color_groups=None, save_path=None, show=True):
        """
        Create color wheel showcase

        Args:
            color_groups (list): List of color groups
            save_path (str): Path to save the figure
            show (bool): Whether to display the figure
        """
        if color_groups is None:
            color_groups = [
                ("Optimized", get_color_palette(ColorPalette.OPTIMIZED)),
                ("Raw Warm", get_color_palette(ColorPalette.RAW_WARM)),
                ("Raw Cool", get_color_palette(ColorPalette.RAW_COOL)),
                ("Opt Warm", get_color_palette(ColorPalette.OPT_WARM)),
                ("Opt Cool", get_color_palette(ColorPalette.OPT_COOL))
            ]

        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_aspect('equal')
        plt.title('Color Palette Color Wheel', fontsize=20, fontweight='bold', pad=20)

        center_x, center_y = 0, 0
        group_angle = 360 / len(color_groups)

        # Create wedge for each color group
        for group_idx, (group_name, colors) in enumerate(color_groups):
            start_angle = group_idx * group_angle
            color_angle = group_angle / len(colors)

            for color_idx, color in enumerate(colors):
                angle_start = start_angle + color_idx * color_angle
                angle_end = start_angle + (color_idx + 1) * color_angle

                wedge = patches.Wedge((center_x, center_y), 4, angle_start, angle_end,
                                    facecolor=color, edgecolor='white', linewidth=2)
                ax.add_patch(wedge)

                # Add color label
                label_angle = np.radians(angle_start + color_angle / 2)
                label_radius = 3.2
                text_color = 'white' if is_dark_color(color) else 'black'

                ax.text(center_x + label_radius * np.cos(label_angle),
                       center_y + label_radius * np.sin(label_angle),
                       color, ha='center', va='center', fontsize=8,
                       fontweight='bold', color=text_color)

            # Add group name label
            group_label_angle = np.radians(start_angle + group_angle / 2)
            group_label_radius = 5
            ax.text(center_x + group_label_radius * np.cos(group_label_angle),
                   center_y + group_label_radius * np.sin(group_label_angle),
                   group_name, ha='center', va='center', fontsize=12,
                   fontweight='bold', color='black')

        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.axis('off')

        ax.text(0, -6.5, 'Interactive Color Wheel - Each segment represents a color from your palette',
               ha='center', va='center', fontsize=10, style='italic')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=True)

        if show:
            plt.show()

        return fig

    def _create_wheel(self, ax, color_groups):
        """Create color wheel (private method)"""
        ax.set_aspect('equal')
        ax.set_title('Color Wheel', fontsize=14, fontweight='bold')

        center_x, center_y = 0, 0
        group_angle = 360 / len(color_groups)

        for group_idx, (group_name, colors) in enumerate(color_groups):
            start_angle = group_idx * group_angle
            color_angle = group_angle / len(colors)

            for color_idx, color in enumerate(colors):
                angle_start = start_angle + color_idx * color_angle
                angle_end = start_angle + (color_idx + 1) * color_angle

                wedge = patches.Wedge((center_x, center_y), 1, angle_start, angle_end,
                                    facecolor=color, edgecolor='white', linewidth=1)
                ax.add_patch(wedge)

            # Add group name
            angle = np.radians(group_idx * group_angle + group_angle / 2)
            ax.text(center_x + 1.3 * np.cos(angle), center_y + 1.3 * np.sin(angle),
                   group_name, ha='center', va='center', fontsize=8, fontweight='bold')

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')

    def _create_intensity_bars(self, ax, color_groups):
        """Create color intensity bar chart (private method)"""
        ax.set_title('Color Intensity', fontsize=14, fontweight='bold')

        all_colors = []
        labels = []

        for group_name, colors in color_groups:
            for color in colors:
                all_colors.append(color)
                labels.append(f"{group_name[:8]}")

        # Calculate color brightness
        intensities = []
        for color in all_colors:
            try:
                if color.startswith('#'):
                    r = int(color[1:3], 16) / 255.0
                    g = int(color[3:5], 16) / 255.0
                    b = int(color[5:7], 16) / 255.0
                else:
                    # Simple mapping for named colors
                    color_map = {'red': (1,0,0), 'orange': (1,0.5,0), 'yellow': (1,1,0),
                               'blue': (0,0,1), 'green': (0,1,0), 'purple': (0.5,0,0.5)}
                    r, g, b = color_map.get(color, (0.5, 0.5, 0.5))

                intensity = (r + g + b) / 3
                intensities.append(intensity)
            except:
                intensities.append(0.5)

        bars = ax.bar(range(len(all_colors)), intensities, color=all_colors, edgecolor='black', linewidth=0.5)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
        ax.set_ylabel('Intensity')
        ax.set_ylim(0, 1)

    def _create_contrast_matrix(self, ax, color_groups):
        """Create color contrast matrix (private method)"""
        ax.set_title('Color Contrast Matrix', fontsize=14, fontweight='bold')

        all_colors = []
        for _, colors in color_groups:
            all_colors.extend(colors)

        n = len(all_colors)
        contrast_matrix = np.zeros((n, n))

        # Calculate color contrast
        for i in range(n):
            for j in range(n):
                if i != j:
                    contrast_matrix[i, j] = calculate_color_contrast(all_colors[i], all_colors[j])

        im = ax.imshow(contrast_matrix, cmap='viridis', aspect='equal')
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))

        short_labels = [f"C{i+1}" for i in range(n)]
        ax.set_xticklabels(short_labels, fontsize=8)
        ax.set_yticklabels(short_labels, fontsize=8)

        plt.colorbar(im, ax=ax, shrink=0.8)

    def _create_palette_preview(self, ax, color_groups):
        """Create palette preview (private method)"""
        ax.set_title('Palette Preview', fontsize=14, fontweight='bold')
        ax.axis('off')

        total_colors = sum(len(colors) for _, colors in color_groups)
        x_pos = 0

        for group_name, colors in color_groups:
            # Add group name
            ax.text(x_pos, -0.2, group_name, ha='left', va='top',
                   fontsize=10, fontweight='bold')

            for color in colors:
                rect = patches.Rectangle((x_pos, 0), 0.8, 0.8,
                                       facecolor=color, edgecolor='black', linewidth=1)
                ax.add_patch(rect)

                # Add color code (if space allows)
                if len(color) < 8:  # Only show short color codes
                    text_color = 'white' if is_dark_color(color) else 'black'
                    ax.text(x_pos + 0.4, 0.4, color, ha='center', va='center',
                           fontsize=6, fontweight='bold', color=text_color)

                x_pos += 1

        ax.set_xlim(0, total_colors)
        ax.set_ylim(-0.5, 1)
