#!/usr/bin/env python3
"""
Line Chart Gallery - A comprehensive demonstration of LineChart capabilities in Hachimiku.
"""

import os
import sys
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hachimiku import LineChart

def main():
    # Create output directories
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/line_gallery')
    docs_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/images/line')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(docs_img_dir, exist_ok=True)
    
    # Initialize LineChart handler
    lc = LineChart(figsize=(10, 6))

    # Common style settings for this gallery
    common_args = {
        'colors': ["#248600", "#005289", "#ff4c35"],
        'legend_outside': True,
        'title_y': 1.05,
        'show': False
    }

    # Helper function to save both PDF and PNG
    def save_plot(filename_base, func, **args):
        # Save high quality PDF for reference
        pdf_path = os.path.join(output_dir, f"{filename_base}.pdf")
        args['save_path'] = pdf_path
        func(**args)
        
        # Save PNG for documentation embedding
        png_path = os.path.join(docs_img_dir, f"{filename_base}.png")
        args['save_path'] = png_path
        func(**args)

    # -------------------------------------------------------------------------
    # 1. Multi-Series Line Chart - Performance Over Time
    # -------------------------------------------------------------------------
    print("Generating Multi-Series Line Chart...")
    x = np.linspace(0, 10, 11)
    # Use fixed seed for reproducible gallery
    np.random.seed(42)
    y_data_list = [
        x * 1.5 + np.random.normal(0, 1, 11),
        x * 0.8 + np.random.normal(0, 1, 11) + 2,
        x * 2.1 + np.random.normal(0, 1, 11) - 1
    ]
    labels = ['Algorithm A', 'Algorithm B', 'Algorithm C']
    
    save_plot(
        "01_multi_series_line",
        lc.create_line_chart,
        x_data=x,
        y_data_list=y_data_list,
        labels=labels,
        xlabel='Iterations',
        ylabel='Accuracy (%)',
        grid=True,
        **common_args
    )

    # -------------------------------------------------------------------------
    # 2. Log-Scale Line Chart - Convergence Analysis
    # -------------------------------------------------------------------------
    print("Generating Log-Scale Line Chart...")
    x_log = np.arange(1, 11)
    y_log_list = [
        10**(-x_log*0.5),
        10**(-x_log*0.3),
        10**(-x_log*0.7)
    ]
    
    save_plot(
        "02_log_scale_line",
        lc.create_line_chart,
        x_data=x_log,
        y_data_list=y_log_list,
        labels=['Learning Rate 1e-2', 'Learning Rate 1e-3', 'Learning Rate 5e-2'],
        xlabel='Epochs',
        ylabel='Loss (Log Scale)',
        log_scale_y=True,
        grid_y=True,
        **common_args
    )

    # -------------------------------------------------------------------------
    # 3. Custom Style Line Chart - Linewidths & Markers
    # -------------------------------------------------------------------------
    print("Generating Custom Style Line Chart...")
    save_plot(
        "03_custom_style_line",
        lc.create_line_chart,
        x_data=x,
        y_data_list=[y_data_list[0], y_data_list[1]],
        labels=['Thick Line', 'Large Markers'],
        linewidths=[4.0, 1.5],
        markersizes=[8, 14],
        markers=['o', 's'],
        linestyles=['-', '--'],
        xlabel='Time',
        ylabel='Value',
        **common_args
    )

    print(f"\nLine Gallery generated in:\n - {output_dir}\n - {docs_img_dir}")

if __name__ == "__main__":
    main()
