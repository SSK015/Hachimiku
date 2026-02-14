#!/usr/bin/env python3
"""
Combo Chart Gallery - A demonstration of Bar + Line combination charts in Hachimiku.
"""

import os
import sys
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hachimiku import ComboChart

def main():
    # Create output directories
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/combo_gallery')
    docs_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/images/combo')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(docs_img_dir, exist_ok=True)
    
    # Initialize ComboChart handler
    cc = ComboChart(figsize=(10, 6))

    # Common style settings for this gallery
    common_args = {
        'colors': ["#248600", "#005289"], # Green, Blue
        'line_colors': ["#ff4c35"],       # Red for the line
        'legend_outside_bar': True,
        'show': False
    }

    # Helper function to save both PDF and PNG
    def save_plot(filename_base, func, **args):
        # Save high quality PDF
        pdf_path = os.path.join(output_dir, f"{filename_base}.pdf")
        args['save_path'] = pdf_path
        func(**args)
        
        # Save PNG for documentation
        png_path = os.path.join(docs_img_dir, f"{filename_base}.png")
        args['save_path'] = png_path
        func(**args)

    # -------------------------------------------------------------------------
    # 1. Bar + Line Combo - System Performance
    # -------------------------------------------------------------------------
    print("Generating Bar-Line Combo Chart...")
    groups = ['App A', 'App B', 'App C', 'App D']
    bar_vals = [
        [10, 15], # Group 1
        [12, 18], # Group 2
        [8, 14],  # Group 3
        [15, 22]  # Group 4
    ]
    # Line points corresponding to each bar in the groups
    line_vals = [
        [85, 92], # Group 1
        [88, 95], # Group 2
        [82, 90], # Group 3
        [90, 98]  # Group 4
    ]
    
    save_plot(
        "01_bar_line_combo",
        cc.create_bar_line_combo_chart,
        x_data=groups,
        bar_values=bar_vals,
        line_values=line_vals,
        labels=['Throughput (Metric 1)', 'Throughput (Metric 2)'],
        line_labels=['Efficiency (%)'],
        xlabel='Applications',
        ylabel_left='Throughput (req/s)',
        ylabel_right='Efficiency (%)',
        ylim_right=(80, 100),
        grid_y=True,
        combine_legends=True,
        legend_ncol_bar=3,
        **common_args
    )

    print(f"\nCombo Gallery generated in:\n - {output_dir}\n - {docs_img_dir}")

if __name__ == "__main__":
    main()
