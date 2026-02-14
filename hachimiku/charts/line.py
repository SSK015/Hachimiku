"""
Line chart functionality for the plotting library.
"""

import matplotlib.pyplot as plt
import numpy as np
from ..core.utils import setup_matplotlib_style, auto_fontsize, general_line_style, setup_spines
from ..colors.palettes import get_colors, get_alphas


class LineChart:
    """Class for creating various types of line charts with high academic quality."""

    def __init__(self, figsize=(8, 4)):
        """
        Initialize LineChart instance.

        Args:
            figsize (tuple): Default figure size (width, height).
        """
        self.figsize = figsize
        setup_matplotlib_style()

    def create_line_chart(self, x_data, y_data_list, labels=None, colors=None,
                         markers=None, linestyles=None, linewidths=None, markersizes=None,
                         markevery=None, title=None, xlabel=None, ylabel=None, 
                         save_path=None, show=True, log_scale_y=False, 
                         grid=False, grid_x=False, grid_y=False,
                         title_fontsize=None, title_fontweight='bold', title_y=1.02,
                         label_fontsize=None, tick_fontsize=None, legend_fontsize=None,
                         color_preset=None, color_split=None,
                         ylim=None, xlim=None, xticks=None, xticklabels=None,
                         yticks=None, yticklabels=None,
                         tick_direction='in', tick_length=6.0, tick_pad=None,
                         xlabel_pad=None, ylabel_pad=None,
                         grid_style=None, ax=None, show_legend=True,
                         legend_outside=True, legend_loc='lower center', legend_ncol=None,
                         legend_bbox_to_anchor=None, alpha=1.0, 
                         top_right_spine_style='solid', top_right_spine_color='gray',
                         spine_linewidth=1.5, **kwargs):
        """
        Create a line chart with multiple series.

        Args:
            x_data (array-like): Shared X-axis data points.
            y_data_list (list): List of Y-axis data arrays for each line.
            labels (list): Legend labels for each line.
            colors (list or str): Color list or preset name.
            markers (list): List of markers for each line (e.g., ['o', 's']).
            linestyles (list): List of linestyles (e.g., ['-', '--', ':']).
            linewidths (list or float): Width of line(s).
            markersizes (list or float): Size of marker(s).
            markevery (int or list): Frequency of markers on the line.
            title (str): Chart title.
            xlabel (str): X-axis label.
            ylabel (str): Y-axis label.
            save_path (str): File path to save the chart.
            show (bool): Whether to display the figure.
            log_scale_y (bool): Whether to use a logarithmic Y-axis.
            grid (bool): Whether to show grid lines.
            alpha (float or list): Transparency of lines (0 to 1).
            **kwargs: Backward compatibility aliases.
        """
        if 'line_alpha' in kwargs: alpha = kwargs['line_alpha']
        
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            is_standalone = True
        else:
            fig = ax.get_figure()
            is_standalone = False

        setup_spines(ax, linewidth=spine_linewidth, 
                     top_right_spine_style=top_right_spine_style, 
                     top_right_spine_color=top_right_spine_color)

        num_lines = len(y_data_list)
        
        # Color and Alpha logic
        if colors is None:
            colors = get_colors(num_lines, preset_name=color_preset or 'academic_vivid')
        elif isinstance(colors, str):
            colors = get_colors(num_lines, preset_name=colors)

        if markers is None:
            # High-contrast marker cycle for academic papers
            markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'x', '+']
        
        if linestyles is None:
            linestyles = ['-', '--', '-.', ':']

        line_style_base = general_line_style()

        # Plot each line
        for i, y_data in enumerate(y_data_list):
            color = colors[i % len(colors)]
            marker = markers[i % len(markers)]
            linestyle = linestyles[i % len(linestyles)]
            curr_lw = linewidths[i % len(linewidths)] if isinstance(linewidths, list) else linewidths
            curr_ms = markersizes[i % len(markersizes)] if isinstance(markersizes, list) else markersizes
            curr_alpha = alpha[i % len(alpha)] if isinstance(alpha, list) else alpha
            
            plot_kwargs = line_style_base.copy()
            if curr_lw is not None: plot_kwargs['linewidth'] = curr_lw
            if curr_ms is not None: plot_kwargs['markersize'] = curr_ms
            if markevery is not None: plot_kwargs['markevery'] = markevery
            if curr_alpha is not None: plot_kwargs['alpha'] = curr_alpha
                
            ax.plot(x_data, y_data, marker=marker, linestyle=linestyle, color=color, 
                    label=labels[i] if labels else f'Line {i+1}', **plot_kwargs)

        if log_scale_y: ax.set_yscale('log')

        self._setup_formatting(ax, fig, title, xlabel, ylabel, title_fontsize, title_fontweight, title_y,
                             label_fontsize, tick_fontsize, tick_pad, tick_direction, tick_length,
                             xlabel_pad, ylabel_pad, xlim, ylim, xticks, xticklabels, yticks, yticklabels,
                             grid, grid_x, grid_y, grid_style, log_scale_y)

        # Legend
        if show_legend and num_lines > 0:
            fs = auto_fontsize(fig, base_size=16)
            legend_fs_val = legend_fontsize if legend_fontsize is not None else fs
            ncol = legend_ncol or (min(2, num_lines) if num_lines > 4 else num_lines)
            
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

    def create_multi_line_chart(self, datasets, title=None, xlabel=None, ylabel=None, 
                              save_path=None, show=True, linewidths=None, markersizes=None,
                              title_fontsize=None, title_fontweight='bold', title_y=1.02,
                              label_fontsize=None, tick_fontsize=None, legend_fontsize=None,
                              color_preset=None, alpha=1.0,
                              ylim=None, xlim=None, xticks=None, xticklabels=None,
                              yticks=None, yticklabels=None,
                              tick_direction='in', tick_length=6.0, tick_pad=None,
                              xlabel_pad=None, ylabel_pad=None,
                              grid=False, grid_x=False, grid_y=False, grid_style=None, 
                              ax=None, show_legend=True, legend_outside=True, 
                              legend_loc='lower center', legend_ncol=None,
                              legend_bbox_to_anchor=None, **kwargs):
        """
        Create a line chart from a list of dataset dictionaries for maximum flexibility.

        Args:
            datasets (list): List of dicts, each containing 'x', 'y', and optionally 'label', 'marker', 'linestyle', etc.
            title, xlabel, ylabel: Labels for the chart.
            **kwargs: Styling parameters similar to create_line_chart.
        """
        if 'line_alpha' in kwargs: alpha = kwargs['line_alpha']
        
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            is_standalone = True
        else:
            fig = ax.get_figure()
            is_standalone = False

        setup_spines(ax, top_right_spine_style='solid', top_right_spine_color='gray')

        num_lines = len(datasets)
        
        # Color and Alpha
        colors = get_colors(num_lines, preset_name=color_preset or 'academic_vivid')
        line_style_base = general_line_style()

        for i, dataset in enumerate(datasets):
            curr_lw = dataset.get('linewidth', linewidths[i % len(linewidths)] if isinstance(linewidths, list) else linewidths)
            curr_ms = dataset.get('markersize', markersizes[i % len(markersizes)] if isinstance(markersizes, list) else markersizes)
            curr_alpha = dataset.get('alpha', alpha[i % len(alpha)] if isinstance(alpha, list) else alpha)

            plot_kwargs = line_style_base.copy()
            if curr_lw: plot_kwargs['linewidth'] = curr_lw
            if curr_ms: plot_kwargs['markersize'] = curr_ms
            if curr_alpha: plot_kwargs['alpha'] = curr_alpha

            ax.plot(dataset['x'], dataset['y'], 
                    marker=dataset.get('marker', 'o'), 
                    linestyle=dataset.get('linestyle', '-'),
                    color=dataset.get('color', colors[i % len(colors)]), 
                    label=dataset.get('label', f'Line {i+1}'), **plot_kwargs)

        self._setup_formatting(ax, fig, title, xlabel, ylabel, title_fontsize, title_fontweight, title_y,
                             label_fontsize, tick_fontsize, tick_pad, tick_direction, tick_length,
                             xlabel_pad, ylabel_pad, xlim, ylim, xticks, xticklabels, yticks, yticklabels,
                             grid, grid_x, grid_y, grid_style, False)

        # Legend
        if show_legend and num_lines > 0:
            fs = auto_fontsize(fig, base_size=16)
            legend_fs_val = legend_fontsize if legend_fontsize is not None else fs
            ncol = legend_ncol or (min(2, num_lines) if num_lines > 4 else num_lines)
            
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
                         grid, grid_x, grid_y, grid_style, log_scale_y):
        """Helper to apply common formatting consistently across all line chart types."""
        fs = auto_fontsize(fig, base_size=16)
        
        # Grid logic
        if grid or grid_x or grid_y:
            style = {'linestyle': '--', 'color': '#333333', 'alpha': 0.5, 'which': 'major'}
            if grid_style: style.update(grid_style)
            grid_which = style.pop('which', 'major')
            if log_scale_y: grid_which = 'both'
            
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
        ax.set_ylabel(ylabel, fontsize=l_fs, labelpad=ylabel_pad)
        ax.set_xlabel(xlabel, fontsize=l_fs, labelpad=xlabel_pad)
        
        title_fs_val = title_fontsize if title_fontsize is not None else fs * 0.9
        if title: ax.set_title(title, fontsize=title_fs_val, fontweight=title_fontweight, y=title_y)
        
        t_fs = tick_fontsize if tick_fontsize is not None else fs
        tp_pad = tick_pad if tick_pad is not None else 4.0
        ax.tick_params(axis='both', which='major', labelsize=t_fs, direction=tick_direction, length=tick_length, pad=tp_pad)
        ax.yaxis.get_offset_text().set_fontsize(t_fs)
        ax.xaxis.get_offset_text().set_fontsize(t_fs)
