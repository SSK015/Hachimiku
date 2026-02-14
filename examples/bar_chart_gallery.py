#!/usr/bin/env python3
"""
Bar Chart Gallery - Refined Version.
Focused on stability, academic clarity, and visual balance.
"""

import os
import sys
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hachimiku import BarChart

def main():
    # Create output directories
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/bar_gallery')
    docs_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/images/bar')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(docs_img_dir, exist_ok=True)
    
    # Initialize BarChart handler
    bc = BarChart(figsize=(10, 6))

    # Definitive academic colors (Green, Blue, Red)
    selected_colors = ["#248600", "#005289", "#ff4c35"]

    # Common style settings: Standard and Stable
    common_args = {
        'colors': selected_colors,
        'legend_outside': True,
        'title_y': -0.25,
        'show': False
    }

    # Helper function to save
    def save_plot(filename_base, func, **args):
        pdf_path = os.path.join(output_dir, f"{filename_base}.pdf")
        args['save_path'] = pdf_path
        func(**args)
        
        png_path = os.path.join(docs_img_dir, f"{filename_base}.png")
        args['save_path'] = png_path
        func(**args)

    # -------------------------------------------------------------------------
    # 1. Grouped Bar Chart - Clean Sparse Look
    # -------------------------------------------------------------------------
    print("Generating Grouped Bar Chart...")
    grouped_values = [[2.21, 2.94, 1.85], [8.47, 16.7, 12.30]]
    group_names = ['Small I/O', 'Large I/O']
    bar_labels = ['Baseline A', 'Baseline B', 'Hachimiku']
    
    # Use refined colors for hatches (slightly darker than bar color)
    # This creates a "sparse" feeling without manual line drawing
    h_colors = ["#1a6b00", "#003d66", "#cc3322"] 

    save_plot(
        "01_grouped_bar",
        bc.create_grouped_bar_chart,
        y_data_list=grouped_values,
        x_data=group_names,
        labels=bar_labels,
        # Sparse black hatching (manual, clipped) to beat Matplotlib's fixed hatch density.
        hatch_patterns=['', '/', 'x'],
        manual_hatch=True,
        manual_hatch_color='black',
        manual_hatch_linewidth=1.6,
        manual_hatch_slope=1.0,     # steeper diagonal lines than 45°
        # Dynamic hatch count by bar height: more lines for taller bars.
        manual_hatch_gap=2.5,       # ~1 line per 2.5 units of bar height
        manual_hatch_min_lines=1,
        manual_hatch_max_lines=8,
        # Legend shows hatch via proxy handles (built-in hatch).
        manual_hatch_spacing=None,  # Keep spacing disabled; we control via gap/n_lines
        # Keep borders normal
        hatch_color='black',
        hatch_linewidth=1.0,
        ylabel='Execution Time (ms)',
        title='(a) Grouped Bar: System Performance Comparison',
        bar_text_format='{:.2f}',
        bar_text_fontweight='bold',
        grid_y=True,
        **common_args
    )

    # -------------------------------------------------------------------------
    # 1b. Grouped Bar Chart - Custom Colors (Yellow/Blue/Red)
    # -------------------------------------------------------------------------
    print("Generating Grouped Bar Chart with Custom Colors...")
    custom_colors = ["#eec200", "#0077b6", "#cc0000"] # Yellow, Blue, Red
    
    save_plot(
        "01_grouped_bar_custom",
        bc.create_grouped_bar_chart,
        y_data_list=grouped_values,
        x_data=group_names,
        labels=bar_labels,
        colors=custom_colors,
        hatch_patterns=['', '/', 'x'],
        manual_hatch=True,
        manual_hatch_color='black',
        manual_hatch_linewidth=1.6,
        manual_hatch_slope=1.0,
        manual_hatch_gap=2.5,
        ylabel='Execution Time (ms)',
        title='(a) Grouped Bar: Custom Color Scheme (Y/B/R)',
        bar_text_format='{:.2f}',
        bar_text_fontweight='bold',
        grid_y=True,
        legend_outside=True,
        title_y=-0.25,
        show=False
    )

    # -------------------------------------------------------------------------
    # 2. Breakdown (Stacked) Bar Chart
    # -------------------------------------------------------------------------
    print("Generating Breakdown Bar Chart...")
    save_plot(
        "02_breakdown_bar",
        bc.create_breakdown_bar_chart,
        y_data_list=[[30, 40, 30], [20, 25, 55], [10, 15, 75]],
        x_data=['System X', 'System Y', 'System Z'],
        labels=['CPU', 'Memory', 'I/O'],
        ylabel='Resource Usage (%)',
        title='(b) Breakdown Bar: Component Analysis',
        bar_text_format='{:.0f}%',
        **common_args
    )

    # -------------------------------------------------------------------------
    # 3. Simple Bar Chart
    # -------------------------------------------------------------------------
    print("Generating Simple Bar Chart...")

    simple_args = dict(common_args)
    # Use a different color for each bar (more vivid & higher contrast)
    simple_args['colors'] = ["#248600", "#005289", "#ff4c35", "#f18120"]
    # Make hatch truly sparse (Matplotlib built-in hatch is too dense)
    simple_args['manual_hatch'] = True
    simple_args['manual_hatch_n_lines'] = 4
    simple_args['manual_hatch_linewidth'] = 1.6
    simple_args['manual_hatch_color'] = 'black'
    simple_args['manual_hatch_slope'] = 2.0

    save_plot(
        "03_simple_bar",
        bc.create_simple_bar_chart,
        y_data_list=[85.4, 92.1, 78.5, 96.2],
        x_data=['A', 'B', 'C', 'D'],
        ylabel='Accuracy (%)',
        title='(c) Simple Bar: Model Accuracy Comparison',
        show_xticks=True,
        bar_text_format='{:.1f}%',
        **simple_args
    )

    print(f"\nRefined Bar Gallery generated in: {output_dir}")

if __name__ == "__main__":
    main()
