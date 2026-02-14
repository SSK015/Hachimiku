"""
CDF (Cumulative Distribution Function) chart functionality for the plotting library.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, MultipleLocator
from ..core.utils import setup_matplotlib_style, auto_fontsize, general_line_style, setup_spines
from ..colors.palettes import get_colors, get_alphas


class CDFChart:
    """Class for creating various types of CDF charts with high academic quality."""

    def __init__(self, figsize=(8, 4)):
        """
        Initialize CDFChart instance.

        Args:
            figsize (tuple): Default figure size (width, height).
        """
        self.figsize = figsize
        setup_matplotlib_style()

    def create_cdf_chart(self, x_data_list, y_data_list, labels=None, colors=None,
                        markers=None, linewidths=None, markersizes=None,
                        title=None, xlabel='Value', ylabel='CDF (%)',
                        save_path=None, show=True, log_scale_x=True,
                        grid=False, grid_x=False, grid_y=False, grid_style=None,
                        title_fontsize=None, title_fontweight='bold', title_y=1.02,
                        label_fontsize=None, tick_fontsize=None, legend_fontsize=None,
                        color_preset=None, color_split=None, ax=None,
                        show_legend=True, legend_outside=True, 
                        legend_loc='lower center', legend_ncol=None,
                        legend_bbox_to_anchor=None, alpha=1.0,
                        xlabel_pad=None, ylabel_pad=None,
                        top_right_spine_style='solid', top_right_spine_color='gray',
                        spine_linewidth=1.5,
                        tick_direction='in', tick_length=6.0, tick_pad=None, **kwargs):
        """
        Create a CDF chart.

        Args:
            x_data_list (list): List of X-axis data arrays for each curve.
            y_data_list (list): List of Y-axis data arrays for each curve.
            labels (list): Legend labels for each curve.
            colors (list or str): Color list or preset name.
            title (str): Chart title.
            xlabel (str): X-axis label.
            ylabel (str): Y-axis label.
            save_path (str): File path to save the chart.
            show (bool): Whether to display the figure.
            log_scale_x (bool): Whether to use a logarithmic X-axis.
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
            marker_list = ['', '', '', '', '']
        else:
            marker_list = markers if isinstance(markers, list) else ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'x', '+']

        line_style_base = general_line_style()

        for i, y_data in enumerate(y_data_list):
            color = colors[i % len(colors)]
            marker = marker_list[i % len(marker_list)]
            
            # Handle both single x_data and list of x_data
            curr_x = x_data_list[i] if isinstance(x_data_list, list) else x_data_list
            
            curr_lw = linewidths[i % len(linewidths)] if isinstance(linewidths, list) else linewidths
            curr_ms = markersizes[i % len(markersizes)] if isinstance(markersizes, list) else markersizes
            curr_alpha = alpha[i % len(alpha)] if isinstance(alpha, list) else alpha
            
            plot_kwargs = line_style_base.copy()
            if curr_lw is not None: plot_kwargs['linewidth'] = curr_lw
            if curr_ms is not None: plot_kwargs['markersize'] = curr_ms
            if curr_alpha is not None: plot_kwargs['alpha'] = curr_alpha
            
            # For CDFs, we strongly recommend using markevery if markers are present
            if 'markevery' in kwargs:
                plot_kwargs['markevery'] = kwargs['markevery']
            elif marker != '':
                # Default to a sparse markevery if markers are enabled but no frequency is set
                plot_kwargs['markevery'] = max(1, len(y_data) // 10)
                
            ax.plot(curr_x, y_data, marker=marker, color=color, 
                    label=labels[i] if labels else f'Line {i+1}', **plot_kwargs)

        self._setup_formatting(ax, fig, title, xlabel, ylabel, title_fontsize, title_fontweight, title_y,
                             label_fontsize, tick_fontsize, tick_pad, tick_direction, tick_length,
                             xlabel_pad, ylabel_pad, None, (0, 105), None, None, None, None,
                             grid, grid_x, grid_y, grid_style, log_scale_x)

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

    def create_multi_cdf_chart(self, datasets, title=None, xlabel='Value', ylabel='CDF (%)',
                             save_path=None, show=True, linewidths=None, markersizes=None,
                             grid=False, grid_x=False, grid_y=False, grid_style=None,
                             title_fontsize=None, title_fontweight='bold', title_y=1.02,
                             label_fontsize=None, tick_fontsize=None, legend_fontsize=None,
                             color_preset=None, alpha=1.0, 
                             xlabel_pad=None, ylabel_pad=None,
                             tick_direction='in', tick_length=6.0, tick_pad=None,
                             ax=None, show_legend=True, legend_outside=True, 
                             legend_loc='lower center', legend_ncol=None,
                             legend_bbox_to_anchor=None, log_scale_x=True, **kwargs):
        """
        Create a CDF chart from a list of dataset dictionaries.
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

            ax.plot(dataset['x'], dataset['y'], marker=dataset.get('marker', ''), 
                    color=dataset.get('color', colors[i % len(colors)]), 
                    label=dataset.get('label', f'Line {i+1}'), **plot_kwargs)

        self._setup_formatting(ax, fig, title, xlabel, ylabel, title_fontsize, title_fontweight, title_y,
                             label_fontsize, tick_fontsize, tick_pad, tick_direction, tick_length,
                             xlabel_pad, ylabel_pad, None, (0, 105), None, None, None, None,
                             grid, grid_x, grid_y, grid_style, log_scale_x)

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
                         grid, grid_x, grid_y, grid_style, log_scale_x):
        """Helper to apply common formatting consistently across all CDF chart types."""
        fs = auto_fontsize(fig, base_size=16)
        
        if log_scale_x: 
            ax.set_xscale('log')
            ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=7))
        
        ax.yaxis.set_major_locator(MultipleLocator(20))

        # Grid logic
        if grid or grid_x or grid_y:
            style = {'linestyle': '--', 'color': '#333333', 'alpha': 0.5, 'which': 'major'}
            if grid_style: style.update(grid_style)
            grid_which = style.pop('which', 'major')
            if log_scale_x: grid_which = 'both'
            
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
