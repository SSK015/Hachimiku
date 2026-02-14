#!/usr/bin/env python3
"""
Area Chart Gallery - A demonstration of AreaChart capabilities in Hachimiku.
"""

import os
import sys
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hachimiku import AreaChart

def main():
    # Create output directories
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/area_gallery')
    docs_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/images/area')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(docs_img_dir, exist_ok=True)
    
    # Initialize AreaChart handler
    ac = AreaChart(figsize=(10, 6))

    # Common style settings for this gallery
    # Using the user's preferred color order: green, blue, red
    common_args = {
        'colors': ["#248600", "#005289", "#ff4c35"],
        'legend_outside': True,
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
    # 1. Stacked Area Chart - Resource Usage
    # -------------------------------------------------------------------------
    print("Generating Stacked Area Chart...")
    x = np.arange(0, 24, 1)
    # Generate some periodic data for 3 services
    y1 = 20 + 10 * np.sin(x/3) + np.random.normal(0, 2, 24)
    y2 = 30 + 15 * np.cos(x/4) + np.random.normal(0, 3, 24)
    y3 = 10 + 5 * np.sin(x/2) + np.random.normal(0, 1, 24)
    
    # Ensure non-negative
    y1 = np.maximum(y1, 5)
    y2 = np.maximum(y2, 5)
    y3 = np.maximum(y3, 5)

    save_plot(
        "01_stacked_area",
        ac.create_stacked_area_chart,
        x_data=x,
        y_data_list=[y1, y2, y3],
        labels=['Service A (Web)', 'Service B (DB)', 'Service C (Cache)'],
        xlabel='Hour of Day',
        ylabel='Memory Usage (GB)',
        alpha=0.7,
        grid_y=True,
        **common_args
    )

    print(f"\nArea Gallery generated in:\n - {output_dir}\n - {docs_img_dir}")

if __name__ == "__main__":
    main()
