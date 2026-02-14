"""
Area chart functionality for the plotting library.
"""

import matplotlib.pyplot as plt
import numpy as np
from ..core.utils import setup_matplotlib_style, auto_fontsize, setup_spines
from ..colors.palettes import get_colors, get_alphas


class AreaChart:
    """Class for creating high-quality area charts, including stacked area charts."""

    def __init__(self, figsize=(8, 4)):
        """
        Initialize AreaChart instance.

        Args:
            figsize (tuple): Default figure size (width, height).
        """
        self.figsize = figsize
        setup_matplotlib_style()

    def create_stacked_area_chart(self, x_data, y_data_list, labels=None,
                                 colors=None, title=None, xlabel=None, ylabel=None,
                                 save_path=None, show=True, color_preset='academic_vivid',
                                 alpha=0.6, edge_linewidth=1.0, edge_color=None,
                                 ylim=None, xlim=None, xticks=None, xticklabels=None,
                                 yticks=None, yticklabels=None,
                                 grid=False, grid_x=False, grid_y=False, grid_style=None,
                                 title_fontsize=None, title_fontweight='bold', title_y=1.02,
                                 label_fontsize=None, tick_fontsize=None, legend_fontsize=None,
                                 legend_loc='upper center', legend_ncol=None,
                                 legend_outside=True, legend_bbox_to_anchor=None,
                                 show_legend=True, ax=None,
                                 top_right_spine_style='solid', top_right_spine_color='gray',
                                 spine_linewidth=1.5,
                                 tick_direction='in', tick_length=6.0, tick_pad=None,
                                 xlabel_pad=None, ylabel_pad=None, **kwargs):
        """
        Create a stacked area chart.

        Args:
            x_data (array-like): X-axis data points.
            y_data_list (list): 2D list or list of arrays [layers][points].
            labels (list): Labels for each layer in the stack.
            colors (list or str): Color list or preset name.
            alpha (float or list): Transparency for the areas (0 to 1).
            ... (other args standard across library)
        """
        num_layers = len(y_data_list)
        
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            is_standalone = True
        else:
            fig = ax.get_figure()
            is_standalone = False

        setup_spines(ax, linewidth=spine_linewidth, 
                     top_right_spine_style=top_right_spine_style, 
                     top_right_spine_color=top_right_spine_color)

        # Color and Alpha logic
        if colors is None:
            colors = get_colors(num_layers, preset_name=color_preset)
        elif isinstance(colors, str):
            colors = get_colors(num_layers, preset_name=colors)

        if isinstance(alpha, (float, int)):
            alpha = [alpha] * num_layers

        # Stackplot plotting
        stacks = ax.stackplot(x_data, y_data_list, labels=labels or [f'L{i}' for i in range(num_layers)], 
                             colors=colors, alpha=1.0, 
                             edgecolor=edge_color if edge_color else 'none',
                             linewidth=edge_linewidth)

        # Apply individual alphas to PolyCollections
        for i, stack in enumerate(stacks):
            stack.set_alpha(alpha[i % len(alpha)])

        # Formatting
        self._setup_formatting(ax, fig, title, xlabel, ylabel, title_fontsize, title_fontweight, title_y,
                             label_fontsize, tick_fontsize, tick_pad, tick_direction, tick_length,
                             xlabel_pad, ylabel_pad, xlim, ylim, xticks, xticklabels, yticks, yticklabels,
                             grid, grid_x, grid_y, grid_style)

        # Legend
        if show_legend and num_layers > 0:
            fs = auto_fontsize(fig, base_size=16)
            legend_fs_val = legend_fontsize or fs
            ncol = legend_ncol or (min(2, num_layers) if num_layers > 4 else num_layers)
            if legend_outside:
                anchor = legend_bbox_to_anchor or (0.5, 1.02)
                ax.legend(loc='lower center', bbox_to_anchor=anchor, ncol=ncol, 
                          frameon=False, fontsize=legend_fs_val, columnspacing=1.0, handletextpad=0.5)
                if is_standalone: fig.subplots_adjust(top=0.85)
            else:
                ax.legend(loc=legend_loc, bbox_to_anchor=legend_bbox_to_anchor,
                          ncol=ncol, frameon=False, fontsize=legend_fs_val)

        if save_path and is_standalone: plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show and is_standalone: plt.show()
        return fig

    def _setup_formatting(self, ax, fig, title, xlabel, ylabel, title_fontsize, title_fontweight, title_y,
                         label_fontsize, tick_fontsize, tick_pad, tick_direction, tick_length,
                         xlabel_pad, ylabel_pad, xlim, ylim, xticks, xticklabels, yticks, yticklabels,
                         grid, grid_x, grid_y, grid_style):
        """Helper to apply common formatting consistently across area chart types."""
        fs = auto_fontsize(fig, base_size=16)
        
        # Grid logic
        if grid or grid_x or grid_y:
            style = {'linestyle': '--', 'color': '#333333', 'alpha': 0.5, 'which': 'major'}
            if grid_style: style.update(grid_style)
            grid_which = style.pop('which', 'major')
            
            if grid: ax.grid(True, which=grid_which, axis='both', **style)
            else:
                if grid_x: ax.grid(True, which=grid_which, axis='x', **style)
                if grid_y: ax.grid(True, which=grid_which, axis='y', **style)

        if ylim: ax.set_ylim(ylim)
        if xlim: ax.set_xlim(xlim)
        
        if xticklabels is not None:
            ax.set_xticks(xticks if xticks is not None else range(len(xticklabels)))
            ax.set_xticklabels(xticklabels)
        elif xticks is not None:
            ax.set_xticks(xticks)

        if yticklabels is not None:
            ax.set_yticks(yticks if yticks is not None else range(len(yticklabels)))
            ax.set_yticklabels(yticklabels)
        elif yticks is not None:
            ax.set_yticks(yticks)

        l_fs = label_fontsize if label_fontsize is not None else fs
        if ylabel: ax.set_ylabel(ylabel, fontsize=l_fs, labelpad=ylabel_pad)
        if xlabel: ax.set_xlabel(xlabel, fontsize=l_fs, labelpad=xlabel_pad)
        
        title_fs_val = title_fontsize if title_fontsize is not None else fs * 0.9
        if title: ax.set_title(title, fontsize=title_fs_val, fontweight=title_fontweight, y=title_y)
        
        t_fs = tick_fontsize if tick_fontsize is not None else fs
        tp_pad = tick_pad if tick_pad is not None else 4.0
        ax.tick_params(axis='both', which='major', labelsize=t_fs, direction=tick_direction, length=tick_length, pad=tp_pad)
        ax.yaxis.get_offset_text().set_fontsize(t_fs)
        ax.xaxis.get_offset_text().set_fontsize(t_fs)
