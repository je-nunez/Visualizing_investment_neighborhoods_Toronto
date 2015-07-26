#!/usr/bin/env python

# pylint has issues with the dynamic definition of members by numpy, so
# pylint pbby has to be called with '--extension-pkg-whitelist=numpy'
#
# pylint: disable=no-name-in-module
# pylint: disable=import-error

"""Visualize in the same geographical map the following information about
the different neighborhoods of Toronto, using the ESRI Shapefiles below
through matplotlib/basemap, etc:

. The City Wards in Toronto;
. The Neighborhoods defined as Priority Investment by the City of Toronto
. The Business Improvement Areas defined by the City of Toronto
. The Current Value Assessment on Tax Impact for Residential Neighborhoods
  in the City of Toronto (last year available, 2011)

All these ESRI Shapefiles are available by the Open Data initiative of
the City of Toronto.

It is possible to do a more proper Data Mining on why certain neighborhoods
of the city have been chosen in the way they have been, from other
information in the Open Data of the City of Toronto:

    http://www.toronto.ca/open

Most of this information seems to be in Excel format (as of 2015).

This visualization is another way to express the development of the City
of Toronto, instead of using words as written media, but with visualization.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import numpy as np


def visualize_investment_in_toronto():
    """Function to visualize the investment in the neighborhoods of
    Toronto.

    It plots these ESRI Shapefiles from Toronto using matplotlib/basemap/etc.
    (These shapefiles are available as Open Data from the City of Toronto):

     . The City Wards in Toronto;
     . The Neighborhoods defined as Priority Investment by the City of Toronto
     . The Business Improvement Areas defined by the City of Toronto
     . The Current Value Assessment on Tax Impact for Residential Neighborhoods
       in the City of Toronto (last year available, 2011)
    """

    # These are the latitudes of the City of Toronto.
    # (Fiona can be better to find them, e.g., from the 'icitw_wgs84' Shapefile
    #  below.)

    low_left_corner_longitude = -79.75
    low_left_corner_latitude = 43.40
    up_right_corner_longitude = -79.10
    up_right_corner_latitude = 43.95
        
    fig = plt.figure()
    axes = fig.add_subplot(111)

    # Prepare the map of Toronto

    to_map = Basemap(llcrnrlon=low_left_corner_longitude,
                     llcrnrlat=low_left_corner_latitude,
                     urcrnrlon=up_right_corner_longitude,
                     urcrnrlat=up_right_corner_latitude,
                     ellps='WGS84',
                     resolution='h', area_thresh=1000)

    to_map.drawmapboundary(fill_color='white')

    # Plot the City Wards in Toronto. The borders of these polygons are plot as
    # they are in the Shapefile

    dummy = to_map.readshapefile(shapefile='./shp_dir/icitw_wgs84',
                                 name='city_wards',
                                 drawbounds=True, color='green')

    # Read the Shapefile of the Priority Investment Neighborhoods in Toronto.
    # The Shapefile is read first and its polygons are filled with the color
    # 'facecolor' in a for-loop below

    dummy = to_map.readshapefile(shapefile='./shp_dir/TO_priority_inv_neighb',
                                 name='prio_investm',
                                 drawbounds=False)

    patches = []

    for info, shape in zip(to_map.prio_investm_info, to_map.prio_investm):
        # print info
        patches.append(Polygon(np.array(shape), True))

    axes.add_collection(PatchCollection(patches, facecolor='m', edgecolor='k',
                                        linewidths=1., zorder=3))

    # Read the Shapefile of the Business Improvement Areas in Toronto.
    # The Shapefile is read first and its polygons are filled with the color
    # 'facecolor' in a for-loop below

    dummy = to_map.readshapefile(shapefile='./shp_dir/TO_busin_improv_area',
                                 name='busin_improv',
                                 drawbounds=False)

    patches = []

    for info, shape in zip(to_map.busin_improv_info, to_map.busin_improv):
        # print info
        patches.append(Polygon(np.array(shape), True))

    axes.add_collection(PatchCollection(patches, facecolor='g', edgecolor='k',
                                        linewidths=1., zorder=2))

    # Read the Shapefile of the Estimated Tax Impact in Toronto.
    # The way to plot this Shapefile is different than the previous one, since
    # this shapefile has an Avg Tax Impact value [field 'avgtaximpa']
    # associated to each of its polygons, so the different tonalities of
    # 'facecolor' in its polygons represent the Avg Tax Impact value in each
    # polygon

    dummy = to_map.readshapefile(shapefile='shp_dir/CVA_2011_Tax_Impact_WGS84',
                                 name='tax_assesm_impact',
                                 drawbounds=False)

    patches = []
    taxes = []

    for info, shape in zip(to_map.tax_assesm_impact_info,
                           to_map.tax_assesm_impact):
        # print info
        # The estimated taxes in the polygon is the gradient which gives the
        # tonality of red to the polygon
        taxes.append(float(info['avgtaximpa']))

        patches.append(Polygon(np.array(shape), True))

    cmap = plt.get_cmap('Reds')
    patch_collection = PatchCollection(patches, match_original=True)
    norm = Normalize(vmin=min(taxes), vmax=max(taxes))
    patch_collection.set_facecolor(cmap(norm(taxes)))

    axes.add_collection(patch_collection)

    plt.title('Toronto Neighborhoods: Priority Investment, Business ' +
              'Improvement Areas,\nand Current Value Assessment of Tax ' +
              'Impact on Residential Properties')
    # plt.legend()
    plt.show()


def main():
    """Main function on the program.

    What it does, for now, is just to visualize the investment and taxes
    in the neighborhoods in Toronto,
    """

    visualize_investment_in_toronto()


if __name__ == '__main__':
    main()
