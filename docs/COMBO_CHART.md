# ComboChart Reference Guide

The `ComboChart` class allows you to create complex visualizations by combining different chart types, such as Bar and Line charts, typically sharing a common X-axis but using dual Y-axes.

## Table of Contents
- [Initialization](#initialization)
- [Combo-Specific Parameters](#combo-specific-parameters)
- [Methods](#methods)
  - [create_bar_line_combo_chart](#create_bar_line_combo_chart)
- [Usage Considerations](#usage-considerations)

---

## Initialization

```python
from hachimiku import ComboChart

cc = ComboChart(figsize=(10, 6))
```

- **`figsize`**: Default figure size (width, height) in inches.

---

## Combo-Specific Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `bar_values` | `list` | 2D list of bar heights: `[groups][bars_per_group]`. |
| `line_values` | `list` | 2D list of line points aligning with each bar: `[groups][points_per_group]`. |
| `ylabel_left` | `str` | Label for the primary (left) Y-axis (Bars). |
| `ylabel_right`| `str` | Label for the secondary (right) Y-axis (Lines). |
| `ylim_left` | `tuple` | Y-axis limits for the left axis. |
| `ylim_right` | `tuple` | Y-axis limits for the right axis. |
| `line_colors` | `list` | Colors for the line series. |
| `bar_spacing` | `float` | Spacing between the centers of group labels. |
| `combine_legends` | `bool` | Whether to combine bar and line legends into one (default: `True`). |
| `linewidth` | `float` | Thickness of the line (default: `2.5`). |

---

## Methods

### `create_bar_line_combo_chart`
Creates a chart with grouped bars on the left axis and lines on the right axis. The lines connect points that correspond exactly to the position of each individual bar within the groups.

![Bar-Line Combo Chart](images/combo/01_bar_line_combo.png)

---

## Usage Considerations

### Data Alignment
The `line_values` should have the same structure as `bar_values`. Each point in `line_values[group_idx][bar_idx]` will be plotted at the exact horizontal center of the corresponding bar.

### Combined Legends
By default, `combine_legends=True` will merge the bar and line legends into a single horizontal row at the top (if `legend_outside_bar=True`). This is often cleaner for academic papers.

```python
cc.create_bar_line_combo_chart(
    ...,
    combine_legends=True,
    legend_ncol_bar=3
)
```

### Line Style
The default line style is now thicker (`linewidth=2.5`) and uses solid markers for better visibility when combined with bars.

---

## Examples

See `examples/combo_chart_gallery.py` for the complete source code used to generate the gallery above.
