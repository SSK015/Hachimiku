# AreaChart Reference Guide

The `AreaChart` class is used to create stacked area charts, which are effective for visualizing how multiple components contribute to a total value over time or across categories.

## Table of Contents
- [Initialization](#initialization)
- [Area-Specific Parameters](#area-specific-parameters)
- [Methods](#methods)
  - [create_stacked_area_chart](#create_stacked_area_chart)
- [Styling Tips](#styling-tips)

---

## Initialization

```python
from hachimiku import AreaChart

ac = AreaChart(figsize=(10, 6))
```

- **`figsize`**: Default figure size (width, height) in inches.

---

## Area-Specific Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `alpha` | `float/list` | Transparency for the filled areas (default: `0.6`). |
| `edge_linewidth` | `float` | Width of the line between stacked areas. |
| `edge_color` | `str` | Color of the edges between areas. |
| `color_preset` | `str` | Predefined color palette (default: `'academic_vivid'`). |

---

## Methods

### `create_stacked_area_chart`
Creates a standard stacked area chart. Useful for showing cumulative totals and individual contributions.

![Stacked Area Chart](images/area/01_stacked_area.png)

---

## Styling Tips

### Transparency (Alpha)
Since area charts involve large filled regions, using a slightly lower `alpha` (e.g., `0.5` to `0.7`) helps make grid lines visible and softens the visual impact, which is often preferred in modern academic papers.

```python
ac.create_stacked_area_chart(
    ...,
    alpha=0.6,
    grid_y=True
)
```

### Edges
To make individual layers more distinct, you can add a thin edge color:

```python
ac.create_stacked_area_chart(
    ...,
    edge_linewidth=0.5,
    edge_color='white' # or 'black'
)
```

---

## Examples

See `examples/area_chart_gallery.py` for the complete source code used to generate the gallery above.
