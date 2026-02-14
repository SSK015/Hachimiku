"""
Layout manager for creating figures with multiple subplots.
"""

import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional, Tuple
from ..charts.bar import BarChart
from ..charts.line import LineChart
from ..charts.cdf import CDFChart
from ..charts.combo import ComboChart
from ..charts.area import AreaChart

class LayoutManager:
    """Class for managing multi-plot layouts using mosaic grids"""

    def __init__(self):
        """Initialize LayoutManager with instances of all supported chart types"""
        self.charts = {
            'bar': BarChart(),
            'line': LineChart(),
            'cdf': CDFChart(),
            'combo': ComboChart(),
            'area': AreaChart()
        }

    def create_multi_plot(self, 
                         config: List[Dict[str, Any]], 
                         mosaic: List[List[str]],
                         figsize: Tuple[float, float] = (12, 8),
                         title: Optional[str] = None,
                         title_fontsize: int = 32,
                         shared_legend: bool = True,
                         legend_loc: str = 'lower center',
                         legend_ncol: Optional[int] = None,
                         legend_bbox_to_anchor: Optional[Tuple[float, float]] = None,
                         legend_fontsize: int = 20,
                         wspace: Optional[float] = None,
                         hspace: Optional[float] = None,
                         width_ratios: Optional[List[float]] = None,
                         height_ratios: Optional[List[float]] = None,
                         left: Optional[float] = None,
                         right: Optional[float] = None,
                         top: Optional[float] = None,
                         bottom: Optional[float] = None,
                         save_path: Optional[str] = None,
                         show: bool = True,
                         tight_layout: bool = True,
                         constrained_layout: bool = False):
        """
        Create a figure with multiple subplots using a mosaic layout.

        Args:
            config (list): List of dicts, each containing:
                - 'type': 'bar', 'line', 'cdf', 'combo', or 'area'
                - 'ax_key': Key used in mosaic layout
                - 'args': Dict of arguments for the respective create_..._chart method
                - 'method': (optional) Specific method name if not default (e.g. 'create_grouped_bar_chart')
            mosaic (list of lists): Subplot layout mosaic definition (e.g., [['A', 'A'], ['B', 'C']])
            figsize (tuple): Figure dimensions (width, height)
            title (str): Global figure title
            title_fontsize (int): Font size for the global title
            shared_legend (bool): Whether to create a unified legend for all subplots
            legend_loc (str): Location of the shared legend
            legend_ncol (int): Number of columns in shared legend
            legend_bbox_to_anchor (tuple): Bounding box for fine-tuning shared legend position
            legend_fontsize (int): Font size for shared legend text
            wspace (float): Width spacing between subplots
            hspace (float): Height spacing between subplots
            width_ratios (list): Relative width ratios for each column
            height_ratios (list): Relative height ratios for each row
            left, right, top, bottom (float): Manual margins (0-1). Auto-calculated if None.
            save_path (str): File path to save the generated figure
            show (bool): Whether to display the figure immediately
            tight_layout (bool): Whether to apply tight_layout adjustment
            constrained_layout (bool): Whether to use constrained_layout
        """
        import math
        gridspec_kw = {}
        if wspace is not None: gridspec_kw['wspace'] = wspace
        if hspace is not None: gridspec_kw['hspace'] = hspace
        if width_ratios is not None: gridspec_kw['width_ratios'] = width_ratios
        if height_ratios is not None: gridspec_kw['height_ratios'] = height_ratios
        
        fig, ax_dict = plt.subplot_mosaic(mosaic, figsize=figsize, 
                                         constrained_layout=constrained_layout,
                                         gridspec_kw=gridspec_kw)
        
        if title:
            fig.suptitle(title, fontsize=title_fontsize, fontweight='bold')

        # 1. Plot all subplots based on configuration
        for item in config:
            chart_type, ax_key = item.get('type'), item.get('ax_key')
            args, method_name = item.get('args', {}).copy(), item.get('method')
            if ax_key not in ax_dict: continue
                
            ax = ax_dict[ax_key]
            chart_instance = self.charts.get(chart_type)
            if not chart_instance: continue

            # Map default methods for each chart type
            if not method_name:
                defaults = {'bar': 'create_grouped_bar_chart', 'line': 'create_line_chart',
                            'cdf': 'create_cdf_chart', 'combo': 'create_bar_line_combo_chart',
                            'area': 'create_stacked_area_chart'}
                method_name = defaults.get(chart_type)

            method = getattr(chart_instance, method_name, None)
            if not method: continue

            # Suppress individual chart saving/showing/legend when part of a multi-plot
            args.update({'show': False, 'save_path': None, 'ax': ax, 'show_legend': False})
            method(**args)

        # 2. Handle shared legend
        if shared_legend:
            # Collect all legend handles and labels from all subplots
            handles_all, labels_all = [], []
            for ax in ax_dict.values():
                h, l = ax.get_legend_handles_labels()
                handles_all.extend(h); labels_all.extend(l)
            
            if labels_all:
                # Deduplicate while preserving order
                by_label = dict(zip(labels_all, handles_all))
                labels, handles = list(by_label.keys()), list(by_label.values())
                
                ncol = legend_ncol if legend_ncol else len(labels)
                anchor = legend_bbox_to_anchor if legend_bbox_to_anchor else (0.5, -0.05)
                
                fig.legend(handles, labels, loc=legend_loc, bbox_to_anchor=anchor,
                           ncol=ncol, frameon=False, fontsize=legend_fontsize)

        # 3. Fine-tune layout and margins
        if tight_layout and not constrained_layout:
            rect_left, rect_right = left if left is not None else 0, right if right is not None else 1
            rect_top = top if top is not None else (0.88 if title else 1)
            rect_bottom = bottom if bottom is not None else (0.12 if shared_legend else 0)
            
            fig.tight_layout(rect=[rect_left, rect_bottom, rect_right, rect_top])
            
            # Ensure manually set wspace and hspace are respected after tight_layout
            if wspace is not None or hspace is not None:
                fig.subplots_adjust(wspace=wspace, hspace=hspace)

        # 4. Save and Show
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        if show:
            plt.show()

        return fig
