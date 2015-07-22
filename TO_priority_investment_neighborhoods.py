#!/usr/bin/env python

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
from matplotlib.colors import Normalize
from descartes import PolygonPatch
import numpy as np



LOW_LEFT_CORNR_LONGITUDE = -79.10
LOW_LEFT_CORNER_LATITUDE = 43.40
UP_RIGHT_CORNER_LONGITUDE = -79.75
UP_RIGHT_CORNER_LATITUDE = 43.95

fig = plt.figure()
ax  = fig.add_subplot(111)

m = Basemap(llcrnrlon=LOW_LEFT_CORNR_LONGITUDE,
            llcrnrlat=LOW_LEFT_CORNER_LATITUDE,
            urcrnrlon=UP_RIGHT_CORNER_LONGITUDE,
            urcrnrlat=UP_RIGHT_CORNER_LATITUDE,
            ellps='WGS84',
            resolution='h', area_thresh=1000)


m.drawmapboundary(fill_color='white')

# Plot the City Wards in Toronto

s = m.readshapefile(shapefile='icitw_wgs84',
                   name='city_wards',
                   color='green')


# Plot the Priority Investment Neighborhoods in Toronto

s = m.readshapefile(shapefile='TO_priority_inv_neighb',
                   name='prio_investm',
                   drawbounds=False)

patches   = []

for info, shape in zip(m.prio_investm_info, m.prio_investm):
    # print info
    patches.append( Polygon(np.array(shape), True) )

ax.add_collection(PatchCollection(patches, facecolor= 'm', edgecolor='k',
                  linewidths=1., zorder=3))



# Plot the Business Improvement Areas in Toronto

s = m.readshapefile(shapefile='TO_busin_improv_area',
                   name='busin_improv',
                   drawbounds=False)

patches   = []

for info, shape in zip(m.busin_improv_info, m.busin_improv):
    # print info
    patches.append( Polygon(np.array(shape), True) )

ax.add_collection(PatchCollection(patches, facecolor= 'g', edgecolor='k',
                  linewidths=1., zorder=2))


# Plot the Estimated Tax Impact in Toronto

s = m.readshapefile(shapefile='CVA_2011_Tax_Impact_WGS84',
                   name='tax_assesm_impact',
                   drawbounds=False)

patches   = []
taxes = []

for info, shape in zip(m.tax_assesm_impact_info, m.tax_assesm_impact):
    # print info
    # The estimated taxes in the polygon is the gradient which gives the
    # tonality of red to the polygon
    taxes.append(float(info['avgtaximpa']))

    patches.append( Polygon(np.array(shape), True) )

cmap = plt.get_cmap('Reds')
pc = PatchCollection(patches, match_original=True)
norm = Normalize(vmin=min(taxes), vmax=max(taxes))
pc.set_facecolor(cmap(norm(taxes)))

ax.add_collection(pc)


plt.title('Toronto Neighborhoods: Priority Investment, Business ' +
          'Improvement Areas,\nand Current Value Assessment of Tax ' +
          'Impact on Residential Properties')
# plt.legend()
plt.show()

