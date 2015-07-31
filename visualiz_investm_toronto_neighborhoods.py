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
from matplotlib.colors import Normalize, LinearSegmentedColormap
import matplotlib.cm as cm
import numpy as np


# The following two functions, colorbar_index() and cmap_discretize()
# are taken from:
#   http://sensitivecities.com/so-youd-like-to-make-a-map-using-python-EN.html
# and
#

# Convenience functions for working with colour ramps and bars
def colorbar_index(ncolors, cmap, labels=None, **kwargs):
    """
    This is a convenience function to stop you making off-by-one errors
    Takes a standard colour ramp, and discretizes it,
    then draws a colour bar with correctly aligned labels
    """
    cmap = cmap_discretize(cmap, ncolors)
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = plt.colorbar(mappable, **kwargs)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
    colorbar.set_ticklabels(range(ncolors))
    if labels:
        colorbar.set_ticklabels(labels)
    return colorbar


def cmap_discretize(cmap, N):
    """
    Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)

    """
    if type(cmap) == str:
        cmap = get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0., 0., 0., 0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, ki], colors_rgba[i, ki]) for i in xrange(N + 1)]
    return LinearSegmentedColormap(cmap.name + "_%d" % N, cdict, 1024)


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

    # Note that the taxes impact (in taxes[]) is different inside a same ward
    # in the city of Toronto. I.e., a same ward can have different subpolygons
    # with different tax-impact. Example, for 'ward' = 2:
    #    {'subdiv': '19041', 'ward': 2.0, 'avgtaximpa': -56.0554, ...}
    #    {'subdiv': '19042', 'ward': 2.0, 'avgtaximpa': -58.6994, ...}

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

    # Add a colour bar
    cb = colorbar_index(ncolors=len(taxes), cmap=cmap, shrink=0.7,
                         labels=taxes)
    # Set the font-size of the label
    cb.ax.tick_params(labelsize=7)

    # Show highest densities, in descending order
    # highest = '\n'.join(
    #    value[1] for _, value in df_map[(df_map['jenks_bins'] == 4)][:10].sort().iterrows())
    # highest = 'Most Dense Wards:\n\n' + highest

    # Subtraction is necessary for precise y coordinate alignment

    # details = cb.ax.text(
    #    -1., 0 - 0.007,
    #    highest,
    #    ha='right', va='bottom',
    #    size=5,
    #    color='#555555')

    # Add a small legend
    # ( http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.text )

    smallprint = axes.text(
       0.98, 0.05,
       'This is a map of taxes and investment per wards in Toronto\nObtained from Open Data of the City of Toronto\nSee README of this project for URLs\n',
       horizontalalignment='right', verticalalignment='bottom',
       size=4,
       color='#555555',
       bbox=dict(facecolor='red', alpha=0.2),
       transform=axes.transAxes)

    # Draw a map scale

    #  to_map.drawmapscale(
    #    coords[0] + 0.08, coords[1] + 0.015,
    #    coords[0], coords[1],
    #    10.,
    #    barstyle='fancy', labelstyle='simple',
    #    fillcolor1='w', fillcolor2='#555555',
    #    fontcolor='#555555',
    #    zorder=5)

    plt.tight_layout()
    fig.set_size_inches(7.22, 5.25)

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
