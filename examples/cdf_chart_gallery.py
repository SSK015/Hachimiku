#!/usr/bin/env python3
"""
CDF Chart Gallery - A comprehensive demonstration of CDFChart capabilities in Hachimiku.
"""

import os
import sys
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hachimiku import CDFChart

def generate_cdf_data(data):
    """Helper to convert raw data into CDF points."""
    sorted_data = np.sort(data)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1) * 100
    return sorted_data, yvals

def main():
    # Create output directories
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/cdf_gallery')
    docs_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/images/cdf')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(docs_img_dir, exist_ok=True)
    
    # Initialize CDFChart handler
    cc = CDFChart(figsize=(10, 6))

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
    # 1. Standard CDF - Network Latency
    # -------------------------------------------------------------------------
    print("Generating Standard CDF...")
    np.random.seed(42)
    data1 = np.random.lognormal(2, 0.5, 1000)
    data2 = np.random.lognormal(2.5, 0.4, 1000)
    data3 = np.random.lognormal(1.8, 0.6, 1000)
    
    x1, y1 = generate_cdf_data(data1)
    x2, y2 = generate_cdf_data(data2)
    x3, y3 = generate_cdf_data(data3)
    
    save_plot(
        "01_standard_cdf",
        cc.create_cdf_chart,
        x_data_list=[x1, x2, x3],
        y_data_list=[y1, y2, y3],
        labels=['System A', 'System B', 'System C'],
        xlabel='Latency (ms)',
        ylabel='Percentage of Requests (%)',
        grid=True,
        markers=True,  # Enable markers
        markevery=100, # Explicitly set sparse markers
        markersizes=8,
        **common_args
    )

    # -------------------------------------------------------------------------
    # 2. Linear Scale CDF - Uniform Distribution
    # -------------------------------------------------------------------------
    print("Generating Linear Scale CDF...")
    u_data1 = np.random.uniform(0, 100, 1000)
    u_data2 = np.random.uniform(20, 80, 1000)
    
    ux1, uy1 = generate_cdf_data(u_data1)
    ux2, uy2 = generate_cdf_data(u_data2)
    
    save_plot(
        "02_linear_scale_cdf",
        cc.create_cdf_chart,
        x_data_list=[ux1, ux2],
        y_data_list=[uy1, uy2],
        labels=['Uniform [0, 100]', 'Uniform [20, 80]'],
        xlabel='Score',
        ylabel='Cumulative Probability (%)',
        log_scale_x=False,
        grid_y=True,
        # markers=None (default), so no markers here for a clean look
        **common_args
    )

    print(f"\nCDF Gallery generated in:\n - {output_dir}\n - {docs_img_dir}")

if __name__ == "__main__":
    main()
