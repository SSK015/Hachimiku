#!/usr/bin/env python3
"""
Common Features Gallery - Demonstrating shared parameters across all Hachimiku charts.
"""

import os
import sys
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hachimiku import BarChart, LineChart

def main():
    # Create output directories
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/common_features')
    docs_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/images/common')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(docs_img_dir, exist_ok=True)
    
    bc = BarChart()
    lc = LineChart()

    # Data for demos
    x_data = ['Group 1', 'Group 2', 'Group 3']
    y_data = [[10, 12], [15, 18], [12, 14]] # 3 groups, 2 bars each
    labels = ['Metric A', 'Metric B']
    
    # User preferred "Academic Vivid" Blue and Red
    vivid_blue_red = ["#005289", "#ff4c35"]

    def save_plot(filename_base, func, **args):
        args['show'] = False
        # Save PDF
        args['save_path'] = os.path.join(output_dir, f"{filename_base}.pdf")
        func(**args)
        # Save PNG
        args['save_path'] = os.path.join(docs_img_dir, f"{filename_base}.png")
        func(**args)

    # -------------------------------------------------------------------------
    # 1. Color Presets
    # -------------------------------------------------------------------------
    print("Demonstrating Color Presets...")
    # Default: academic_vivid (using Blue and Red as requested)
    save_plot("01_color_academic_vivid", bc.create_grouped_bar_chart, 
              x_data=x_data, y_data_list=y_data, labels=labels, colors=vivid_blue_red)
    
    # Warm Palette
    save_plot("01_color_opt_warm", bc.create_grouped_bar_chart, 
              x_data=x_data, y_data_list=y_data, labels=labels, color_preset='opt_warm')

    # -------------------------------------------------------------------------
    # 2. Legend Placement
    # -------------------------------------------------------------------------
    print("Demonstrating Legend Placement...")
    # Outside (Default for most)
    save_plot("02_legend_outside", lc.create_line_chart, 
              x_data=[1, 2, 3], y_data_list=[[1, 4, 9], [2, 3, 5]], labels=labels,
              colors=vivid_blue_red, legend_outside=True)
    
    # Inside
    save_plot("02_legend_inside", lc.create_line_chart, 
              x_data=[1, 2, 3], y_data_list=[[1, 4, 9], [2, 3, 5]], labels=labels,
              colors=vivid_blue_red, legend_outside=False, legend_loc='upper left')

    # -------------------------------------------------------------------------
    # 3. Spine Configurations
    # -------------------------------------------------------------------------
    print("Demonstrating Spine Styles...")
    # Standard: Solid gray (Academic)
    save_plot("03_spines_standard", bc.create_grouped_bar_chart, 
              x_data=x_data, y_data_list=y_data, labels=labels, colors=vivid_blue_red)
    
    # Clean: No top/right spines
    save_plot("03_spines_none", bc.create_grouped_bar_chart, 
              x_data=x_data, y_data_list=y_data, labels=labels, colors=vivid_blue_red,
              top_right_spine_style='none')

    # -------------------------------------------------------------------------
    # 4. Padding and Positioning
    # -------------------------------------------------------------------------
    print("Demonstrating Padding Control...")
    # title_y and labelpads
    save_plot("04_padding_custom", bc.create_grouped_bar_chart, 
              x_data=x_data, y_data_list=y_data, labels=labels, colors=vivid_blue_red,
              title='Custom Padding Demo', title_y=-0.2, 
              xlabel='X Axis', ylabel='Y Axis',
              xlabel_pad=20, ylabel_pad=20, tick_pad=10)

    # -------------------------------------------------------------------------
    # 5. Grid Styles
    # -------------------------------------------------------------------------
    print("Demonstrating Grid Styles...")
    save_plot("05_grid_custom", lc.create_line_chart, 
              x_data=[1, 2, 3], y_data_list=[[1, 4, 9]], colors=[vivid_blue_red[0]],
              grid=True, grid_style={'linestyle': ':', 'color': 'red', 'alpha': 0.3})

    print(f"\nCommon Features Gallery generated in:\n - {output_dir}\n - {docs_img_dir}")

if __name__ == "__main__":
    main()
