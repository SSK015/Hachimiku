#!/usr/bin/env python3
"""
Generate all assets used in README.md.
One script to reproduce every visual featured in the documentation.
"""

import os
import sys
import subprocess

def run_script(script_path):
    print(f"Running {script_path}...")
    try:
        # Run in the script's own directory to ensure relative paths work if any
        script_dir = os.path.dirname(script_path)
        script_name = os.path.basename(script_path)
        subprocess.run([sys.executable, script_name], cwd=script_dir, check=True)
        print(f"Successfully finished {script_name}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")

def main():
    # Root directory for examples
    examples_dir = os.path.dirname(os.path.abspath(__file__))
    
    scripts = [
        "bar_chart_gallery.py",     # Generates Grouped Bar & Custom Colors
        "line_chart_gallery.py",    # Generates Multi-Series Line
        "cdf_chart_gallery.py",     # Generates Standard CDF
        "combo_chart_gallery.py",    # Generates Bar + Line Combo
        "area_chart_gallery.py",     # Generates Stacked Area
        "multi_plot_layout_demo.py"  # Generates Mosaic Layout
    ]

    print("=== Hachimiku Asset Generation Started ===\n")
    
    for script in scripts:
        full_path = os.path.join(examples_dir, script)
        if os.path.exists(full_path):
            run_script(full_path)
        else:
            print(f"Warning: Script not found: {full_path}")

    print("=== All README assets have been generated successfully ===")
    print("Check the 'docs/images/' directory for the updated visuals.")

if __name__ == "__main__":
    main()
