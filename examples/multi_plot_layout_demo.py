#!/usr/bin/env python3
"""
Multi-Plot Layout Gallery - Demonstrating complex figure arrangements with LayoutManager.
"""

import os
import sys
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hachimiku import LayoutManager

def main():
    # Create output directories
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/layout_gallery')
    docs_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/images/layout')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(docs_img_dir, exist_ok=True)
    
    lm = LayoutManager()

    # Define some shared colors
    colors = ["#248600", "#005289", "#ff4c35"]

    # 1. Configuration for Subplot A (Bar Chart)
    config_a = {
        'type': 'bar',
        'ax_key': 'A',
        'args': {
            'x_data': ['G1', 'G2', 'G3'],
            'y_data_list': [[10, 12], [15, 18], [12, 14]],
            'labels': ['Metric 1', 'Metric 2'],
            'ylabel': 'Throughput',
            'colors': colors[:2],
            'manual_hatch': True,
            'manual_hatch_n_lines': 5
        }
    }

    # 2. Configuration for Subplot B (Line Chart)
    x = np.linspace(0, 10, 11)
    config_b = {
        'type': 'line',
        'ax_key': 'B',
        'args': {
            'x_data': x,
            'y_data_list': [x*1.2, x*0.8],
            'labels': ['Algo A', 'Algo B'],
            'ylabel': 'Accuracy',
            'colors': colors[:2],
            'grid_y': True
        }
    }

    # 3. Configuration for Subplot C (CDF Chart)
    np.random.seed(42)
    data = np.random.lognormal(2, 0.5, 500)
    sorted_data = np.sort(data)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1) * 100
    
    config_c = {
        'type': 'cdf',
        'ax_key': 'C',
        'args': {
            'x_data_list': [sorted_data],
            'y_data_list': [yvals],
            'labels': ['Lat. Dist.'],
            'xlabel': 'Latency (ms)',
            'ylabel': 'CDF (%)',
            'colors': [colors[2]],
            'log_scale_x': True
        }
    }

    # Define Mosaic Layout: A on top, B and C on bottom
    mosaic = [
        ['A', 'A'],
        ['B', 'C']
    ]

    print("Generating Multi-Plot Mosaic Layout...")
    lm.create_multi_plot(
        config=[config_a, config_b, config_c],
        mosaic=mosaic,
        figsize=(12, 10),
        title='System Performance Comprehensive Analysis',
        shared_legend=True,
        legend_ncol=5,
        hspace=0.4,
        wspace=0.3,
        save_path=os.path.join(output_dir, "01_mosaic_layout.pdf"),
        show=False
    )
    
    # Also save as PNG for documentation
    lm.create_multi_plot(
        config=[config_a, config_b, config_c],
        mosaic=mosaic,
        figsize=(12, 10),
        title='System Performance Comprehensive Analysis',
        shared_legend=True,
        legend_ncol=5,
        hspace=0.4,
        wspace=0.3,
        save_path=os.path.join(docs_img_dir, "01_mosaic_layout.png"),
        show=False
    )

    # -------------------------------------------------------------------------
    # 2. Four Subplots in a Row - Comparison across Benchmarks
    # -------------------------------------------------------------------------
    print("Generating 4-in-a-row Comparison Layout...")
    
    benchmarks = ['B1', 'B2', 'B3', 'B4']
    baselines = ['Baseline X', 'Baseline Y', 'Hachimiku']
    row_colors = ["#248600", "#005289", "#ff4c35"]
    
    row_config = []
    for i, b in enumerate(benchmarks):
        # Generate some random data for each benchmark
        data = np.random.randint(50, 100, size=(1, 3)).tolist()
        row_config.append({
            'type': 'bar',
            'ax_key': f'P{i}',
            'args': {
                'x_data': [b],
                'y_data_list': data,
                'labels': baselines,
                'ylabel': 'Throughput' if i == 0 else None,
                # Fully merge Y-axes: hide ticks and labels for subplots 2, 3, 4
                'yticks': [] if i > 0 else None,
                'colors': row_colors,
                'bar_width': 0.35,     # Slim bars
                'bar_spacing': 1.0,
                'manual_hatch': True,
                'manual_hatch_n_lines': 4,
                'ylim': (0, 120),
                'xlim': (-0.8, 0.8)
            }
        })

    row_mosaic = [['P0', 'P1', 'P2', 'P3']]

    lm.create_multi_plot(
        config=row_config,
        mosaic=row_mosaic,
        figsize=(16, 5),
        title=None,
        shared_legend=True,
        legend_ncol=3,
        legend_bbox_to_anchor=(0.5, -0.2), # Lower legend
        wspace=0.3,            # Separate subplots
        save_path=os.path.join(output_dir, "02_row_layout.pdf"),
        show=False
    )
    
    lm.create_multi_plot(
        config=row_config,
        mosaic=row_mosaic,
        figsize=(16, 5),
        title=None,
        shared_legend=True,
        legend_ncol=3,
        legend_bbox_to_anchor=(0.5, -0.2), # Lower legend
        wspace=0.3,            # Separate subplots
        save_path=os.path.join(docs_img_dir, "02_row_layout.png"),
        show=False
    )

    print(f"\nLayout Gallery generated in:\n - {output_dir}\n - {docs_img_dir}")

if __name__ == "__main__":
    main()
