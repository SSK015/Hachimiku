"""
Bar chart functionality for the plotting library.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
from ..core.utils import setup_matplotlib_style, auto_fontsize, setup_spines
from ..colors.palettes import get_colors, get_alphas


class BarChart:
    """Class for creating various types of bar charts with high academic quality."""

    def __init__(self, figsize=(8, 4)):
        """
        Initialize BarChart instance.

        Args:
            figsize (tuple): Default figure size (width, height).
        """
        self.figsize = figsize
        setup_matplotlib_style()

    def create_grouped_bar_chart(self, x_data, y_data_list, labels=None,
                               colors=None, hatch_patterns=None, title=None,
                               save_path=None, show=True, color_preset=None, color_split=None,
                               bar_spacing=1.7, bar_width=0.40,
                               xlabel=None, ylabel=None,
                               title_fontsize=None, title_fontweight='bold',
                               label_fontsize=None, tick_fontsize=None, legend_fontsize=None,
                               legend_loc='upper center', legend_ncol=None,
                               base_fontsize=None, figsize=None,
                               edge_linewidth=1.0, hatch_linewidth=1.0,
                               ylim=None, xlim=None, xticks=None, xticklabels=None,
                               yticks=None, yticklabels=None,
                               grid=False, grid_style=None, grid_x=False, grid_y=False,
                               ax=None, show_legend=True,
                               bar_text_format=None, bar_text_fontsize=None,
                               bar_text_fontweight='normal',
                               bar_text_rotation=0,
                               edge_color='black', alpha=1.0,
                               legend_outside=True, hatch_color=None,
                               manual_hatch=False, manual_hatch_spacing=None,
                               manual_hatch_n_lines=5,
                               manual_hatch_gap=None,
                               manual_hatch_min_lines=1,
                               manual_hatch_max_lines=12,
                               manual_hatch_legend_n_lines=4,
                               manual_hatch_slope=1.0,
                               manual_hatch_slope_in_screen=True,
                               manual_hatch_linewidth=None, manual_hatch_color='black',
                               aspect=None,
                               top_right_spine_style='solid', top_right_spine_color='gray',
                               title_y=1.02,
                               tick_direction='in', tick_length=6.0, tick_pad=None,
                               xlabel_pad=None, ylabel_pad=None,
                               legend_bbox_to_anchor=None, **kwargs):
        """Create a grouped bar chart."""
        if 'group_spacing' in kwargs: bar_spacing = kwargs['group_spacing']
        if 'bar_labels' in kwargs: labels = kwargs['bar_labels']
        if 'bar_alpha' in kwargs: alpha = kwargs['bar_alpha']
        # Handle old parameter names for backward compatibility
        if 'values' in kwargs: y_data_list = kwargs['values']
        if 'group_names' in kwargs: x_data = kwargs['group_names']
        
        num_groups = len(x_data)
        bars_per_group = len(y_data_list[0])
        x = np.arange(num_groups) * bar_spacing
        width = bar_width

        # Setup Colors
        if colors is None:
            colors = get_colors(bars_per_group, preset_name=color_preset or 'academic_vivid')
        elif isinstance(colors, str):
            colors = get_colors(bars_per_group, preset_name=colors)

        if hatch_patterns is None:
            hatch_patterns = [''] * bars_per_group

        if ax is None:
            chart_figsize = figsize if figsize is not None else self.figsize
            fig, ax = plt.subplots(figsize=chart_figsize)
            is_standalone = True
        else:
            fig = ax.get_figure()
            is_standalone = False

        fs = auto_fontsize(fig, base_size=base_fontsize or 16)
        setup_spines(ax, top_right_spine_style=top_right_spine_style, top_right_spine_color=top_right_spine_color)

        # Aspect ratio control: if you set aspect='equal', then 1 unit in x equals 1 unit in y on screen.
        # Note: for categorical-like bar charts this often distorts the layout (very tall/narrow bars),
        # so we keep it opt-in.
        if aspect is not None:
            ax.set_aspect(aspect, adjustable='box')

        # Plot bars
        plt.rcParams['hatch.linewidth'] = hatch_linewidth

        # If using manual hatch, we draw *after* axis limits are finalized so the
        # screen-space slope correction uses the correct x/y scale.
        pending_manual_hatch = []  # list of (rect, pattern, n_lines)

        for i in range(bars_per_group):
            positions = x + (i - bars_per_group / 2) * width + width / 2
            curr_bar_values = [y_data_list[group_idx][i] for group_idx in range(num_groups)]
            color = colors[i % len(colors)]
            hatch = hatch_patterns[i % len(hatch_patterns)]
            
            curr_h_color = (hatch_color[i % len(hatch_color)] if isinstance(hatch_color, list) else hatch_color) or edge_color
            
            bars = ax.bar(positions, curr_bar_values, width, color=color,
                         edgecolor=curr_h_color,
                         hatch='' if (manual_hatch and hatch) else hatch,
                         alpha=alpha, linewidth=edge_linewidth,
                         label=labels[i] if labels else f'Bar {i+1}')

            # Manual hatch: defer drawing until after limits/labels are set.
            if manual_hatch and hatch:
                for rect in bars:
                    n_lines = manual_hatch_n_lines
                    if manual_hatch_gap is not None and manual_hatch_gap > 0:
                        n_lines = int(np.ceil(max(0.0, rect.get_height()) / manual_hatch_gap))
                    n_lines = max(int(manual_hatch_min_lines), int(n_lines))
                    n_lines = min(int(manual_hatch_max_lines), int(n_lines))
                    pending_manual_hatch.append((rect, hatch, n_lines))
            
            if bar_text_format:
                bt_fs = bar_text_fontsize if bar_text_fontsize is not None else fs * 0.7
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2, height,
                            bar_text_format.format(height),
                            ha='center', va='bottom', rotation=bar_text_rotation, 
                            fontsize=bt_fs, fontweight=bar_text_fontweight)

        # Formatting Ticks
        t_fs = tick_fontsize if tick_fontsize is not None else fs
        tp_pad = tick_pad if tick_pad is not None else 4.0
        
        ax.set_xticks(xticks if xticks is not None else x)
        ax.set_xticklabels(xticklabels or x_data, fontsize=t_fs)
        
        if yticks is not None:
            ax.set_yticks(yticks)
        if yticklabels is not None:
            ax.set_yticklabels(yticklabels, fontsize=t_fs)
            
        ax.tick_params(axis='both', labelsize=t_fs, direction=tick_direction, length=tick_length, pad=tp_pad)

        # Title and Labels
        title_fs = title_fontsize if title_fontsize is not None else fs * 0.9
        if title: ax.set_title(title, fontsize=title_fs, fontweight=title_fontweight, y=title_y)
        
        l_fs = label_fontsize if label_fontsize is not None else fs
        if xlabel: ax.set_xlabel(xlabel, fontsize=l_fs, labelpad=xlabel_pad)
        if ylabel: ax.set_ylabel(ylabel, fontsize=l_fs, labelpad=ylabel_pad)

        # Apply axis limits (before manual hatch, since slope correction depends on final scales)
        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        # Draw manual hatch now (after xlim/ylim and tick layout)
        if pending_manual_hatch:
            lw = manual_hatch_linewidth if manual_hatch_linewidth is not None else hatch_linewidth
            for rect, hatch, n_lines in pending_manual_hatch:
                self._draw_manual_hatch(
                    ax,
                    rect,
                    hatch,
                    color=manual_hatch_color,
                    linewidth=lw,
                    n_lines=n_lines,
                    spacing=manual_hatch_spacing,
                    slope=manual_hatch_slope,
                    slope_in_screen=manual_hatch_slope_in_screen,
                )

        # Legend
        if show_legend:
            loc = 'lower center' if legend_outside else legend_loc
            anchor = legend_bbox_to_anchor if legend_bbox_to_anchor is not None else ((0.5, 1.02) if legend_outside else None)
            if manual_hatch and hatch_patterns:
                proxy_handles = []
                proxy_labels = labels or [f'Bar {i+1}' for i in range(bars_per_group)]
                for i in range(bars_per_group):
                    proxy_handles.append(
                        Rectangle(
                            (0, 0),
                            1,
                            1,
                            facecolor=colors[i % len(colors)],
                            edgecolor=manual_hatch_color,
                            hatch=hatch_patterns[i % len(hatch_patterns)],
                            linewidth=edge_linewidth,
                        )
                    )
                # Legend: use proxy patches with built-in hatch (reliable rendering inside legend box).
                # This matches pattern + black hatch color; density inside legend is controlled by Matplotlib.
                orig_hatch_lw = plt.rcParams.get('hatch.linewidth', 1.0)
                plt.rcParams['hatch.linewidth'] = (manual_hatch_linewidth if manual_hatch_linewidth is not None else hatch_linewidth)
                ax.legend(proxy_handles, proxy_labels, fontsize=legend_fontsize or fs, loc=loc, bbox_to_anchor=anchor,
                          ncol=legend_ncol or bars_per_group, frameon=False)
                plt.rcParams['hatch.linewidth'] = orig_hatch_lw
            else:
                ax.legend(fontsize=legend_fontsize or fs, loc=loc, bbox_to_anchor=anchor,
                          ncol=legend_ncol or bars_per_group, frameon=False)
            if legend_outside and is_standalone: fig.subplots_adjust(top=0.85)

        if save_path and is_standalone: plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show and is_standalone: plt.show()
        return fig

    def _draw_manual_hatch(self, ax, rect, pattern, color='black', linewidth=1.0, n_lines=5, spacing=None, slope=1.0, slope_in_screen=True):
        """
        Draw sparse hatch lines inside a bar rectangle by adding a clipped LineCollection.

        Notes:
        - This avoids Matplotlib's fixed hatch density limitation.
        - Supported patterns: '/', '\\\\', 'x' (cross), '|' (vertical), '-' (horizontal).
        """
        if not pattern:
            return

        x0, y0 = rect.get_x(), rect.get_y()
        w, h = rect.get_width(), rect.get_height()
        if w <= 0 or h <= 0:
            return

        segments = []

        x1, y1 = x0 + w, y0 + h

        def _unique_points(pts, eps=1e-9):
            out = []
            for x, y in pts:
                ok = True
                for ox, oy in out:
                    if abs(x - ox) < eps and abs(y - oy) < eps:
                        ok = False
                        break
                if ok:
                    out.append((x, y))
            return out

        def _choose_farthest_two(pts):
            if len(pts) < 2:
                return None
            best = None
            best_d = -1.0
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    dx = pts[i][0] - pts[j][0]
                    dy = pts[i][1] - pts[j][1]
                    d = dx * dx + dy * dy
                    if d > best_d:
                        best_d = d
                        best = (pts[i], pts[j])
            return best

        def _get_effective_m():
            # Interpret `slope` as a *screen-space* slope (dy_px/dx_px) by default.
            # Convert to data-space slope so the visual angle stays consistent even when axes scales differ.
            m = float(slope) if slope is not None else 1.0
            if m <= 0:
                m = 1.0
            if not slope_in_screen:
                return m
            # pixels per data unit along x/y
            p00 = ax.transData.transform((0.0, 0.0))
            p10 = ax.transData.transform((1.0, 0.0))
            p01 = ax.transData.transform((0.0, 1.0))
            sx = abs(p10[0] - p00[0])
            sy = abs(p01[1] - p00[1])
            if sx <= 0 or sy <= 0:
                return m
            # m_px = m_data * (sy/sx)  =>  m_data = m_px * (sx/sy)
            return m * (sx / sy)

        def add_diag_pos(lines):  # '/'
            # y = m x + c  (m>0). Larger m => steeper (more vertical).
            m = _get_effective_m()
            # c = y - m x, compute range from corners so all candidate lines intersect the box.
            cs_corners = [y0 - m * x0, y0 - m * x1, y1 - m * x0, y1 - m * x1]
            c_min = min(cs_corners)
            c_max = max(cs_corners)
            if spacing is not None and spacing > 0:
                # step in c corresponding to spacing in data along x
                step_c = spacing * np.sqrt(2.0)
                cs = np.arange(c_min, c_max + step_c, step_c)
            else:
                lines = max(1, int(lines))
                if lines == 1:
                    cs = np.array([(c_min + c_max) / 2.0])
                else:
                    # Avoid corner-tangent lines by excluding endpoints.
                    cs = np.linspace(c_min, c_max, lines + 2)[1:-1]
            for c in cs:
                pts = []
                # Intersections with vertical edges x=x0,x1
                y_at_x0 = m * x0 + c
                if y0 <= y_at_x0 <= y1:
                    pts.append((x0, y_at_x0))
                y_at_x1 = m * x1 + c
                if y0 <= y_at_x1 <= y1:
                    pts.append((x1, y_at_x1))
                # Intersections with horizontal edges y=y0,y1
                x_at_y0 = (y0 - c) / m
                if x0 <= x_at_y0 <= x1:
                    pts.append((x_at_y0, y0))
                x_at_y1 = (y1 - c) / m
                if x0 <= x_at_y1 <= x1:
                    pts.append((x_at_y1, y1))
                pts = _unique_points(pts)
                chosen = _choose_farthest_two(pts)
                if chosen is not None:
                    segments.append([chosen[0], chosen[1]])

        def add_diag_neg(lines):  # '\\'
            # y = -m x + c  (m>0)
            m = _get_effective_m()
            # c = y + m x
            cs_corners = [y0 + m * x0, y0 + m * x1, y1 + m * x0, y1 + m * x1]
            c_min = min(cs_corners)
            c_max = max(cs_corners)
            if spacing is not None and spacing > 0:
                step_c = spacing * np.sqrt(2.0)
                cs = np.arange(c_min, c_max + step_c, step_c)
            else:
                lines = max(1, int(lines))
                if lines == 1:
                    cs = np.array([(c_min + c_max) / 2.0])
                else:
                    cs = np.linspace(c_min, c_max, lines + 2)[1:-1]
            for c in cs:
                pts = []
                # Intersections with vertical edges
                y_at_x0 = -m * x0 + c
                if y0 <= y_at_x0 <= y1:
                    pts.append((x0, y_at_x0))
                y_at_x1 = -m * x1 + c
                if y0 <= y_at_x1 <= y1:
                    pts.append((x1, y_at_x1))
                # Intersections with horizontal edges
                x_at_y0 = (c - y0) / m
                if x0 <= x_at_y0 <= x1:
                    pts.append((x_at_y0, y0))
                x_at_y1 = (c - y1) / m
                if x0 <= x_at_y1 <= x1:
                    pts.append((x_at_y1, y1))
                pts = _unique_points(pts)
                chosen = _choose_farthest_two(pts)
                if chosen is not None:
                    segments.append([chosen[0], chosen[1]])

        def add_vertical(lines):
            lines = max(1, int(lines))
            xs = np.linspace(x0, x1, lines + 2)[1:-1]
            for xi in xs:
                segments.append([(xi, y0), (xi, y1)])

        def add_horizontal(lines):
            lines = max(1, int(lines))
            ys = np.linspace(y0, y1, lines + 2)[1:-1]
            for yi in ys:
                segments.append([(x0, yi), (x1, yi)])

        p = pattern
        # Interpret 'x' as cross hatch (both diagonals), '+' as both orthogonal.
        if p == '/':
            add_diag_pos(n_lines)
        elif p == '\\':
            add_diag_neg(n_lines)
        elif p == 'x':
            add_diag_pos(n_lines)
            add_diag_neg(n_lines)
        elif p == '|':
            add_vertical(n_lines)
        elif p == '-':
            add_horizontal(n_lines)
        elif p == '+':
            add_vertical(n_lines)
            add_horizontal(n_lines)
        else:
            # Fallback: attempt to use first character if someone passes '///' etc.
            ch = p[0]
            return self._draw_manual_hatch(ax, rect, ch, color=color, linewidth=linewidth, n_lines=n_lines, spacing=spacing)

        if not segments:
            return

        lc = LineCollection(segments, colors=[color], linewidths=linewidth, zorder=rect.get_zorder() + 0.2)
        # Clip to the bar rectangle; critical to keep hatches inside the bar.
        lc.set_clip_path(rect)
        lc.set_clip_on(True)
        # Critical: do NOT autoscale axes based on hatch segment extents (they extend beyond the bar bbox).
        ax.add_collection(lc, autolim=False)

    def create_breakdown_bar_chart(self, y_data_list, x_data=None,
                                 labels=None, colors=None, hatch_patterns=None,
                                 title=None, save_path=None, show=True, color_preset=None,
                                 bar_spacing=1.0, bar_width=0.5,
                                 xlabel=None, ylabel=None, title_fontsize=None, title_fontweight='bold',
                                 label_fontsize=None, tick_fontsize=None, legend_fontsize=None,
                                 legend_loc='upper center', legend_ncol=None,
                                 base_fontsize=None, figsize=None,
                                 edge_linewidth=1.0, hatch_linewidth=1.0,
                                 ylim=None, xlim=None, ax=None, show_legend=True,
                                 edge_color='black', alpha=1.0, legend_outside=True, hatch_color=None,
                                 bar_text_format=None, bar_text_fontsize=None, 
                                 bar_text_fontweight='normal', bar_text_rotation=0,
                                 title_y=1.02, legend_bbox_to_anchor=None,
                                 xticks=None, xticklabels=None,
                                 yticks=None, yticklabels=None,
                                 tick_direction='in', tick_length=6.0, tick_pad=None,
                                 xlabel_pad=None, ylabel_pad=None,
                                 **kwargs):
        """Create a stacked breakdown bar chart."""
        if 'baseline_names' in kwargs: x_data = kwargs['baseline_names']
        if 'part_labels' in kwargs: labels = kwargs['part_labels']
        # Handle old parameter names for backward compatibility
        if 'breakdown_values' in kwargs: y_data_list = kwargs['breakdown_values']
        if 'group_names' in kwargs: x_data = kwargs['group_names']
        
        num_bars = len(y_data_list)
        num_parts = len(y_data_list[0])
        x = np.arange(num_bars) * bar_spacing

        if colors is None:
            colors = get_colors(num_parts, preset_name=color_preset or 'academic_vivid')
        if hatch_patterns is None: hatch_patterns = [''] * num_parts

        if ax is None:
            fig, ax = plt.subplots(figsize=figsize or self.figsize)
            is_standalone = True
        else:
            fig = ax.get_figure()
            is_standalone = False

        fs = auto_fontsize(fig, base_size=base_fontsize or 16)
        plt.rcParams['hatch.linewidth'] = hatch_linewidth

        for i in range(num_bars):
            bottom = 0
            for j in range(num_parts):
                curr_h_color = (hatch_color[j % len(hatch_color)] if isinstance(hatch_color, list) else hatch_color) or edge_color
                ax.bar(x[i], y_data_list[i][j], width=bar_width, bottom=bottom, color=colors[j], 
                       edgecolor=curr_h_color, hatch=hatch_patterns[j], alpha=alpha, linewidth=edge_linewidth)
                bottom += y_data_list[i][j]

        # Formatting
        t_fs = tick_fontsize if tick_fontsize is not None else fs
        tp_pad = tick_pad if tick_pad is not None else 4.0
        
        ax.set_xticks(xticks if xticks is not None else x)
        ax.set_xticklabels(xticklabels or x_data or [f'Bar {i+1}' for i in range(num_bars)], fontsize=t_fs)
        
        if yticks is not None:
            ax.set_yticks(yticks)
        if yticklabels is not None:
            ax.set_yticklabels(yticklabels, fontsize=t_fs)

        ax.tick_params(axis='both', which='major', labelsize=t_fs, direction=tick_direction, length=tick_length, pad=tp_pad)
        if title: ax.set_title(title, fontsize=title_fontsize or fs*0.9, fontweight=title_fontweight, y=title_y)
        l_fs = label_fontsize if label_fontsize is not None else fs
        if xlabel: ax.set_xlabel(xlabel, fontsize=l_fs, labelpad=xlabel_pad)
        if ylabel: ax.set_ylabel(ylabel, fontsize=l_fs, labelpad=ylabel_pad)

        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        if show_legend:
            loc = 'lower center' if legend_outside else legend_loc
            anchor = legend_bbox_to_anchor if legend_bbox_to_anchor is not None else ((0.5, 1.02) if legend_outside else None)
            ax.legend(labels or [f'Part {j+1}' for j in range(num_parts)], 
                      fontsize=legend_fontsize or fs, loc=loc, bbox_to_anchor=anchor,
                      ncol=legend_ncol or num_parts, frameon=False)

        if save_path and is_standalone: plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig

    def create_simple_bar_chart(self, x_data, y_data_list, labels=None, colors=None,
                              hatch_patterns=None, title=None, save_path=None, show=True, 
                              color_preset=None, bar_spacing=1.0, bar_width=0.5,
                              xlabel=None, ylabel=None, title_fontsize=None, title_fontweight='bold',
                              label_fontsize=None, tick_fontsize=None, legend_fontsize=None,
                              legend_loc='upper center', legend_ncol=None,
                              show_legend=True, show_xticks=False, figsize=None,
                              edge_linewidth=1.0, hatch_linewidth=1.0, ylim=None,
                              xlim=None, xticks=None, xticklabels=None,
                              yticks=None, yticklabels=None,
                              ax=None, edge_color='black', alpha=1.0, legend_outside=True, 
                              bar_text_format=None, title_y=1.02,
                              tick_direction='in', tick_length=6.0, tick_pad=None,
                              xlabel_pad=None, ylabel_pad=None,
                              manual_hatch=False,
                              manual_hatch_n_lines=4,
                              manual_hatch_gap=None,
                              manual_hatch_min_lines=1,
                              manual_hatch_max_lines=10,
                              manual_hatch_slope=2.0,
                              manual_hatch_slope_in_screen=True,
                              manual_hatch_linewidth=None,
                              manual_hatch_color='black',
                              **kwargs):
        """Create a simple bar chart."""
        # Handle old parameter names for backward compatibility
        if 'values' in kwargs: y_data_list = kwargs['values']
        if 'group_names' in kwargs: x_data = kwargs['group_names']
        
        num_bars = len(y_data_list)
        x = np.arange(num_bars) * bar_spacing

        if colors is None:
            colors = get_colors(num_bars, preset_name=color_preset or 'academic_vivid')

        # Default hatching for simple bars (when not provided): make bars distinguishable in print.
        if hatch_patterns is None:
            default_cycle = ['/', '\\', 'x', '|']
            hatch_patterns = [default_cycle[i % len(default_cycle)] for i in range(num_bars)]
        
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize or self.figsize)
            is_standalone = True
        else:
            fig = ax.get_figure()
            is_standalone = False

        fs = auto_fontsize(fig, base_size=16)
        plt.rcParams['hatch.linewidth'] = hatch_linewidth

        pending_manual_hatch = []  # list of (rect, pattern, n_lines)
        for i in range(num_bars):
            pattern = hatch_patterns[i] if hatch_patterns else None
            bars = ax.bar(
                x[i],
                y_data_list[i],
                width=bar_width,
                color=colors[i % len(colors)],
                edgecolor=edge_color,
                hatch='' if (manual_hatch and pattern) else pattern,
                alpha=alpha,
                linewidth=edge_linewidth,
            )
            if manual_hatch and pattern:
                for rect in bars:
                    n_lines = manual_hatch_n_lines
                    if manual_hatch_gap is not None and manual_hatch_gap > 0:
                        n_lines = int(np.ceil(max(0.0, rect.get_height()) / manual_hatch_gap))
                    n_lines = max(int(manual_hatch_min_lines), int(n_lines))
                    n_lines = min(int(manual_hatch_max_lines), int(n_lines))
                    pending_manual_hatch.append((rect, pattern, n_lines))

        t_fs = tick_fontsize if tick_fontsize is not None else fs
        tp_pad = tick_pad if tick_pad is not None else 4.0
        if show_xticks or x_data:
            ax.set_xticks(x)
            ax.set_xticklabels(x_data or [f'Item {i+1}' for i in range(num_bars)], fontsize=t_fs)

        if colors is None:
            colors = get_colors(num_bars, preset_name=color_preset or 'academic_vivid')

        # Default hatching for simple bars (when not provided): make bars distinguishable in print.
        if hatch_patterns is None:
            default_cycle = ['/', '\\', 'x', '|']
            hatch_patterns = [default_cycle[i % len(default_cycle)] for i in range(num_bars)]
        
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize or self.figsize)
            is_standalone = True
        else:
            fig = ax.get_figure()
            is_standalone = False

        fs = auto_fontsize(fig, base_size=16)
        plt.rcParams['hatch.linewidth'] = hatch_linewidth

        pending_manual_hatch = []  # list of (rect, pattern, n_lines)
        for i in range(num_bars):
            pattern = hatch_patterns[i] if hatch_patterns else None
            bars = ax.bar(
                x[i],
                y_data_list[i],
                width=bar_width,
                color=colors[i % len(colors)],
                edgecolor=edge_color,
                hatch='' if (manual_hatch and pattern) else pattern,
                alpha=alpha,
                linewidth=edge_linewidth,
            )
            if manual_hatch and pattern:
                for rect in bars:
                    n_lines = manual_hatch_n_lines
                    if manual_hatch_gap is not None and manual_hatch_gap > 0:
                        n_lines = int(np.ceil(max(0.0, rect.get_height()) / manual_hatch_gap))
                    n_lines = max(int(manual_hatch_min_lines), int(n_lines))
                    n_lines = min(int(manual_hatch_max_lines), int(n_lines))
                    pending_manual_hatch.append((rect, pattern, n_lines))

        t_fs = tick_fontsize if tick_fontsize is not None else fs
        tp_pad = tick_pad if tick_pad is not None else 4.0
        
        ax.set_xticks(xticks if xticks is not None else x)
        ax.set_xticklabels(xticklabels or x_data or [f'Item {i+1}' for i in range(num_bars)], fontsize=t_fs)
        
        if not show_xticks and not x_data and xticks is None:
            ax.xaxis.set_visible(False)

        if yticks is not None:
            ax.set_yticks(yticks)
        if yticklabels is not None:
            ax.set_yticklabels(yticklabels, fontsize=t_fs)

        ax.tick_params(axis='both', which='major', labelsize=t_fs, direction=tick_direction, length=tick_length, pad=tp_pad)

        l_fs = label_fontsize if label_fontsize is not None else fs
        if xlabel: ax.set_xlabel(xlabel, fontsize=l_fs, labelpad=xlabel_pad)
        if ylabel: ax.set_ylabel(ylabel, fontsize=l_fs, labelpad=ylabel_pad)

        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        # Draw manual hatch after limits/ticks are set so screen-slope correction is stable
        if pending_manual_hatch:
            lw = manual_hatch_linewidth if manual_hatch_linewidth is not None else hatch_linewidth
            for rect, pattern, n_lines in pending_manual_hatch:
                self._draw_manual_hatch(
                    ax,
                    rect,
                    pattern,
                    color=manual_hatch_color,
                    linewidth=lw,
                    n_lines=n_lines,
                    spacing=None,
                    slope=manual_hatch_slope,
                    slope_in_screen=manual_hatch_slope_in_screen,
                )

        if title: ax.set_title(title, fontsize=title_fontsize or fs*0.9, fontweight=title_fontweight, y=title_y)
        if save_path and is_standalone: plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig

    def create_horizontal_breakdown_bar_chart(self, y_data_list, x_data=None,
                                            labels=None, colors=None, hatch_patterns=None,
                                            title=None, save_path=None, show=True, 
                                            color_preset=None, bar_spacing=1.0, bar_height=0.6,
                                            xlabel=None, ylabel=None, title_fontsize=None,
                                            label_fontsize=None, tick_fontsize=None,
                                            legend_loc='center left', legend_ncol=1,
                                            figsize=None, edge_linewidth=1.0, hatch_linewidth=1.0,
                                            ax=None, show_legend=True, edge_color='black',
                                            alpha=1.0, legend_outside=True, title_y=1.02,
                                            xlim=None, ylim=None,
                                            tick_direction='in', tick_length=6.0, tick_pad=None,
                                            xlabel_pad=None, ylabel_pad=None,
                                            **kwargs):
        """Create a horizontal breakdown bar chart."""
        # Handle old parameter names for backward compatibility
        if 'breakdown_values' in kwargs: y_data_list = kwargs['breakdown_values']
        if 'group_names' in kwargs: x_data = kwargs['group_names']
        
        num_bars = len(y_data_list)
        num_parts = len(y_data_list[0])
        y_pos = np.arange(num_bars) * bar_spacing

        if colors is None:
            colors = get_colors(num_parts, preset_name=color_preset or 'academic_vivid')

        if ax is None:
            fig, ax = plt.subplots(figsize=figsize or self.figsize)
            is_standalone = True
        else:
            fig = ax.get_figure()
            is_standalone = False

        fs = auto_fontsize(fig, base_size=16)
        plt.rcParams['hatch.linewidth'] = hatch_linewidth

        for i in range(num_bars):
            left = 0
            for j in range(num_parts):
                ax.barh(y_pos[i], y_data_list[i][j], height=bar_height, left=left, color=colors[j], 
                        edgecolor=edge_color, hatch=hatch_patterns[j] if hatch_patterns else None, 
                        alpha=alpha, linewidth=edge_linewidth)
                left += y_data_list[i][j]

        ax.set_yticks(y_pos)
        t_fs = tick_fontsize if tick_fontsize is not None else fs
        tp_pad = tick_pad if tick_pad is not None else 4.0
        ax.set_yticklabels(x_data or [f'Bar {i+1}' for i in range(num_bars)], fontsize=t_fs)
        ax.tick_params(axis='both', which='major', labelsize=t_fs, direction=tick_direction, length=tick_length, pad=tp_pad)

        l_fs = label_fontsize if label_fontsize is not None else fs
        if xlabel: ax.set_xlabel(xlabel, fontsize=l_fs, labelpad=xlabel_pad)
        if ylabel: ax.set_ylabel(ylabel, fontsize=l_fs, labelpad=ylabel_pad)

        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        if title: ax.set_title(title, fontsize=title_fontsize or fs*0.9, y=title_y)
        if save_path and is_standalone: plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
