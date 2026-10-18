from pathlib import Path
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.enums import Resampling
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

RUN_DIR = Path(__file__).resolve().parent
MOSAIC_PATH = RUN_DIR / 'PA_inundation_depth_m.tif'
config = json.loads((RUN_DIR / 'parameters.json').read_text())
CHANNEL_STAGE_M = config['stage_m']
RESOLUTION_M = config['resolution_m']
summary = pd.read_csv(RUN_DIR / 'area_summary.csv').set_index('class')['cells']
coverage_pct = 100 * summary['Modelled'] / summary['PA grid footprint']
required = pd.read_csv(RUN_DIR / 'required_tiles.csv')
processed = pd.read_csv(RUN_DIR / 'processing_log.csv')
complete_tile_set = set(required['tile']) == set(processed['tile'])
prefix = 'PA' if complete_tile_set else 'PA_PARTIAL'
states = gpd.read_file(RUN_DIR.parent / 'boundary/states.zip')
pa_projected = states.loc[states['STUSPS'] == 'PA'].to_crs(config['crs'])
plt.rcParams.update({'figure.figsize': (12, 7), 'font.size': 11})

with rasterio.open(MOSAIC_PATH) as src:
    scale = max(src.width / 2200, src.height / 1400, 1)
    shape = (max(1, round(src.height/scale)), max(1, round(src.width/scale)))
    preview = src.read(1, out_shape=shape, masked=True, resampling=Resampling.nearest)
    extent = (src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top)
fig, ax = plt.subplots(figsize=(13, 8))
pa_projected.plot(ax=ax, facecolor='white', edgecolor='none', zorder=0)
dry = np.ma.masked_where(np.ma.getmaskarray(preview) | (preview.data != 0), np.zeros(shape))
ax.imshow(dry, extent=extent, origin='upper', cmap='Greys', vmin=-1, vmax=2,
          interpolation='nearest', zorder=1)
wet = np.ma.masked_where(np.ma.getmaskarray(preview) | (preview.data <= 0), preview.data)
image = ax.imshow(wet, extent=extent, origin='upper', cmap='Blues',
                  vmin=0, vmax=CHANNEL_STAGE_M, interpolation='nearest', zorder=2)
pa_projected.boundary.plot(ax=ax, color='#263746', linewidth=0.7, zorder=3)
fig.colorbar(image, ax=ax, shrink=0.65, label='Estimated inundation depth (m)')
legend = fig.legend(handles=[Patch(facecolor='#aaa', label='Modelled dry'),
                   Patch(facecolor='white', edgecolor='#777', label='Unknown / not modelled')],
          loc='center left', bbox_to_anchor=(0.78, 0.5), frameon=False)
ax.set(title=f'Pennsylvania HAND inundation scenario — {CHANNEL_STAGE_M:g} m channel stage'
             + ('' if complete_tile_set else ' (PARTIAL RUN)'),
       xlabel='Easting (m) · NAD83 / Conus Albers', ylabel='Northing (m)')
ax.set_aspect('equal')
ax.ticklabel_format(style='plain')
fig.tight_layout(rect=(0, 0, 0.76, 1))
MAP_PATH = RUN_DIR / f'{prefix}_inundation_map.png'
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
legend_box = legend.get_window_extent(renderer)
for plot_ax in fig.axes:
    assert not legend_box.overlaps(plot_ax.get_tightbbox(renderer)), "Legend overlaps the map, colorbar, or axis labels."
for note in fig.texts:
    assert not legend_box.overlaps(note.get_window_extent(renderer)), "Legend overlaps the source note."
fig.savefig(MAP_PATH, dpi=220, bbox_inches='tight')
plt.show()
