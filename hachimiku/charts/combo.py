"""
Combo chart (Bar + Line) functionality for the plotting library.
"""

import matplotlib.pyplot as plt
import numpy as np
from ..core.utils import setup_matplotlib_style, auto_fontsize, setup_spines
from ..colors.palettes import get_colors


class ComboChart:
    """Class for creating combined chart types (e.g., Bar + Line with dual Y-axes)."""

    def __init__(self, figsize=(8, 5)):
        """
        Initialize ComboChart instance.

        Args:
            figsize (tuple): Default figure size (width, height).
        """
        self.figsize = figsize
        setup_matplotlib_style()

    def create_bar_line_combo_chart(self, x_data, bar_values, line_values,
                                   labels=None, line_labels=None,
                                   colors=None, line_colors=None,
                                   hatch_patterns=None,
                                   xlabel=None, ylabel_left=None, ylabel_right=None,
                                   title=None, save_path=None, show=True,
                                   bar_width=0.25, bar_spacing=1.5,
                                   ylim_left=None, ylim_right=None,
                                   grid_y=True, grid_style=None,
                                   title_fontsize=None, title_fontweight='bold', title_y=1.02,
                                   label_fontsize=None, tick_fontsize=None, legend_fontsize=None,
                                   color_preset='academic_vivid',
                                   legend_loc_bar='upper left', legend_loc_line='upper right',
                                   legend_bbox_to_anchor_bar=None, legend_bbox_to_anchor_line=None,
                                   top_right_spine_style='solid', top_right_spine_color='gray',
                                   tick_direction='in', tick_length=6.0, tick_pad=None,
                                   xlabel_pad=None, ylabel_pad=None,
                                   bar_alpha=0.8, line_alpha=1.0,
                                   linewidth=2.5, markersize=8,
                                   combine_legends=True,
                                   legend_outside_bar=True, legend_ncol_bar=None,
                                   ax=None, **kwargs):
        """
        Create a combination chart with grouped bars and a line chart on a twin Y-axis.
        The line points align with each individual bar within the groups.

        Args:
            x_data (list): Labels for groups (X-axis).
            bar_values (list): 2D list of bar heights [groups][bars_per_group].
            line_values (list): 2D list of line points [groups][points_per_group].
            labels (list): Legend labels for the bars.
            line_labels (list): Legend labels for the line series.
            bar_spacing (float): Spacing between centers of groups.
            bar_width (float): Width of individual bars.
            color_preset (str): Color palette to use.
            combine_legends (bool): Whether to combine bar and line legends into one.
            ... (other args standard across library)
        """
        # Compatibility aliases
        if 'group_spacing' in kwargs: bar_spacing = kwargs['group_spacing']
        if 'bar_labels' in kwargs: labels = kwargs['bar_labels']
        
        if ax is None:
            fig, ax1 = plt.subplots(figsize=self.figsize)
            is_standalone = True
        else:
            ax1 = ax
            fig = ax1.get_figure()
            is_standalone = False
            
        ax2 = ax1.twinx()

        num_groups = len(bar_values)
        bars_per_group = len(bar_values[0])
        x = np.arange(num_groups) * bar_spacing
        
        setup_spines(ax1, top_right_spine_style=top_right_spine_style, top_right_spine_color=top_right_spine_color)
        # For twinx, we usually want the right spine of ax2 to be visible
        setup_spines(ax2, top_right_spine_style=top_right_spine_style, top_right_spine_color=top_right_spine_color)

        fs = auto_fontsize(fig, base_size=16)
        
        if colors is None: 
            colors = get_colors(bars_per_group, preset_name=color_preset)
        if hatch_patterns is None: 
            hatch_patterns = [''] * bars_per_group

        # 1. Plot Bars
        bar_positions = np.zeros((num_groups, bars_per_group))
        bar_handles = []
        
        for i in range(bars_per_group):
            pos = x + (i - bars_per_group / 2) * bar_width + bar_width / 2
            bar_positions[:, i] = pos
            vals = [bar_values[g][i] for g in range(num_groups)]
            label = labels[i] if labels else f'Bar {i+1}'
            
            bars = ax1.bar(pos, vals, bar_width, color=colors[i % len(colors)],
                          edgecolor='black', hatch=hatch_patterns[i % len(hatch_patterns)],
                          alpha=bar_alpha, label=label)
            bar_handles.append(bars)

        # 2. Plot Lines (connected within groups, disconnected between)
        if line_colors is None:
            # Default to a neutral dark color for the line to contrast with bars
            line_colors = ['#333333', '#666666']
            
        line_handles = []
        for g in range(num_groups):
            group_x = bar_positions[g, :]
            group_y = line_values[g]
            # Only set label for the first group to avoid duplicate legend entries
            label = line_labels[0] if (line_labels and g == 0) else None
            
            ln, = ax2.plot(group_x, group_y, 'o-', color=line_colors[0], label=label,
                          linewidth=linewidth, markersize=markersize,
                          alpha=line_alpha, zorder=10)
            if g == 0: 
                line_handles.append(ln)

        # 3. Formatting
        l_fs = label_fontsize if label_fontsize is not None else fs
        ax1.set_xlabel(xlabel, fontsize=l_fs, labelpad=xlabel_pad)
        ax1.set_ylabel(ylabel_left, fontsize=l_fs, labelpad=ylabel_pad)
        ax2.set_ylabel(ylabel_right, fontsize=l_fs, labelpad=ylabel_pad)
        
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_data)
        
        if ylim_left: ax1.set_ylim(ylim_left)
        if ylim_right: ax2.set_ylim(ylim_right)
        
        t_fs = tick_fontsize if tick_fontsize is not None else fs
        tp_pad = tick_pad if tick_pad is not None else 4.0
        ax1.tick_params(axis='both', direction=tick_direction, length=tick_length, labelsize=t_fs, pad=tp_pad)
        ax2.tick_params(axis='y', direction=tick_direction, length=tick_length, labelsize=t_fs, pad=tp_pad)

        if grid_y:
            style = {'linestyle': '--', 'color': '#cccccc', 'alpha': 0.5}
            if grid_style: style.update(grid_style)
            ax1.yaxis.grid(True, **style)

        # 4. Legends
        leg_fs = legend_fontsize if legend_fontsize is not None else fs * 0.9
        
        if combine_legends:
            all_handles = bar_handles + line_handles
            all_labels = (labels if labels else []) + (line_labels if line_labels else [])
            ncol = legend_ncol_bar or len(all_handles)
            
            if legend_outside_bar:
                anchor = legend_bbox_to_anchor_bar or (0.5, 1.02)
                ax1.legend(handles=all_handles, labels=all_labels, loc='lower center', 
                          bbox_to_anchor=anchor, ncol=ncol, frameon=False, fontsize=leg_fs)
                if is_standalone: fig.subplots_adjust(top=0.85)
            else:
                ax1.legend(handles=all_handles, labels=all_labels, loc=legend_loc_bar,
                          bbox_to_anchor=legend_bbox_to_anchor_bar, frameon=False, fontsize=leg_fs)
        else:
            if labels:
                ncol = legend_ncol_bar or len(labels)
                if legend_outside_bar:
                    anchor = legend_bbox_to_anchor_bar or (0.5, 1.02)
                    ax1.legend(handles=bar_handles, labels=labels, loc='lower center', 
                              bbox_to_anchor=anchor, 
                              ncol=ncol, frameon=False, fontsize=leg_fs)
                    if is_standalone: 
                        fig.subplots_adjust(top=0.85)
                else:
                    ax1.legend(handles=bar_handles, labels=labels, loc=legend_loc_bar, 
                              bbox_to_anchor=legend_bbox_to_anchor_bar, frameon=False, fontsize=leg_fs)

            if line_labels:
                ax2.legend(handles=line_handles, labels=line_labels, loc=legend_loc_line,
                          bbox_to_anchor=legend_bbox_to_anchor_line, frameon=False, fontsize=leg_fs)

        title_fs_val = title_fontsize if title_fontsize is not None else fs
        if title: 
            ax1.set_title(title, fontsize=title_fs_val, fontweight=title_fontweight, y=title_y)
            
        if save_path and is_standalone: 
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show and is_standalone: 
            plt.show()
        return fig
