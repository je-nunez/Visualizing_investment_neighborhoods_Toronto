#!/usr/bin/env python

# pylint has issues with the dynamic definition of members by numpy, so
# pylint pbby has to be called with '--extension-pkg-whitelist=numpy'
#
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=no-member

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


def draw_basic_map_of_toronto(axis):
    """Draw a basic map of Toronto.

    :param axis: where to draw the map
    :returns: Basemap with Toronto
    """
    # These are the latitudes of the City of Toronto.
    # (Fiona can be better to find them, e.g., from the 'icitw_wgs84' Shapefile
    #  below.)

    low_left_corner_longitude = -79.75
    low_left_corner_latitude = 43.40
    up_right_corner_longitude = -79.10
    up_right_corner_latitude = 43.95

    to_map = Basemap(llcrnrlon=low_left_corner_longitude,
                     llcrnrlat=low_left_corner_latitude,
                     urcrnrlon=up_right_corner_longitude,
                     urcrnrlat=up_right_corner_latitude,
                     ellps='WGS84',
                     resolution='h', area_thresh=1000,
                     ax=axis)

    to_map.drawmapboundary(fill_color='white')
    return to_map


def draw_toronto_and_city_wards(axis):
    """Draw a basic map of Toronto with also the division among
    its city wards.

    :param axis: where to draw the map
    :returns: Basemap with Toronto
    """

    to_map = draw_basic_map_of_toronto(axis)

    # Plot the City Wards in Toronto. The borders of these polygons are plot as
    # they are in the Shapefile

    dummy = to_map.readshapefile(shapefile='./shp_dir/icitw_wgs84',
                                 name='city_wards',
                                 drawbounds=True, color='green')

    return to_map


def visualize_investment_in_toronto():
    """Function to visualize the investment in the neighborhoods of
    Toronto.

    This function is too big, it will be splitted in several parts according
    to the visualization they do.

    It plots these ESRI Shapefiles from Toronto using matplotlib/basemap/etc.
    (These shapefiles are available as Open Data from the City of Toronto):

     . The City Wards in Toronto;
     . The Neighborhoods defined as Priority Investment by the City of Toronto
     . The Business Improvement Areas defined by the City of Toronto
     . The Current Value Assessment on Tax Impact for Residential Neighborhoods
       in the City of Toronto (last year available, 2011)
    """

    fig = plt.figure()

    axes = [None, None, None]
    # grid of 2x2 rows and colums for the subplots with differ. visualizations
    axes[0] = plt.subplot2grid((2, 2), (0, 0))
    axes[1] = plt.subplot2grid((2, 2), (0, 1))
    axes[2] = plt.subplot2grid((2, 2), (1, 0), colspan=2)

    # axes = fig.add_subplot(111)

    # First map is the Priority investment by the City of Toronto

    axes[0].set_title("Priority investment by the City of Toronto")
    to_map = draw_toronto_and_city_wards(axis=axes[0])

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

    axes[0].add_collection(PatchCollection(patches, facecolor='m',
                                           edgecolor='k', linewidths=1.,
                                           zorder=3))

    # Read the Shapefile of the Business Improvement Areas in Toronto.
    # The Shapefile is read first and its polygons are filled with the color
    # 'facecolor' in a for-loop below

    axes[1].set_title("Business Improvement Areas of Toronto")
    to_map = draw_toronto_and_city_wards(axis=axes[1])

    dummy = to_map.readshapefile(shapefile='./shp_dir/TO_busin_improv_area',
                                 name='busin_improv',
                                 drawbounds=False)

    patches = []

    for info, shape in zip(to_map.busin_improv_info, to_map.busin_improv):
        # print info
        patches.append(Polygon(np.array(shape), True))

    axes[1].add_collection(PatchCollection(patches, facecolor='g',
                                           edgecolor='k', linewidths=1.,
                                           zorder=2))

    # Read the Shapefile of the Estimated Tax Impact in Toronto.
    # The way to plot this Shapefile is different than the previous one, since
    # this shapefile has an Avg Tax Impact value [field 'avgtaximpa']
    # associated to each of its polygons, so the different tonalities of
    # 'facecolor' in its polygons represent the Avg Tax Impact value in each
    # polygon

    axes[2].set_title("Current Value and Assessed Tax Impact per Sub-Ward")
    to_map = draw_basic_map_of_toronto(axis=axes[2])

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
    min_taxes = min(taxes)
    max_taxes = max(taxes)
    norm = Normalize(min_taxes, max_taxes)
    patch_collection.set_facecolor(cmap(norm(taxes)))

    axes[2].add_collection(patch_collection)

    # Add a colour bar
    delta_gradient_taxes = max_taxes - min_taxes
    color_bar_taxes = [min_taxes]
    for i in range(1, 6):
        color_bar_taxes.append(min_taxes + (i/6.0) * delta_gradient_taxes)
    color_bar_taxes.append(max_taxes)

    clor_bar = colorbar_index(ncolors=len(color_bar_taxes), cmap=cmap,
                              shrink=0.7, labels=color_bar_taxes,
                              format='%.2f', ax=axes[2])
    # Set the font-size of the tick labels in the color bar
    clor_bar.ax.tick_params(labelsize=7)
    clor_bar.set_label(label='Tax Impact')

    # Show highest densities, in descending order
    # highest = '\n'.join(
    #    value[1] for _, value in df_map[(df_map['jenks_bins'] == 4)][:10].sort().iterrows())
    # highest = 'Most Dense Wards:\n\n' + highest

    # Subtraction is necessary for precise y coordinate alignment

    # details = clor_bar.ax.text(
    #    -1., 0 - 0.007,
    #    highest,
    #    ha='right', va='bottom',
    #    size=5,
    #    color='#555555')

    # Add a small legend
    # ( http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.text )

    # dummy = axes[2].text(
    #    0.98, 0.05,
    #    'This is a map of taxes and investment per subwards in Toronto\n' +
    #    'Obtained from Open Data of the City of Toronto\n' +
    #    'See README of this project for URLs\n',
    #    horizontalalignment='right', verticalalignment='bottom',
    #    size=6,
    #    color='#555555',
    #    bbox=dict(facecolor='red', alpha=0.2),
    #    transform=axes[2].transAxes)

    # Draw a map scale

    #  to_map.drawmapscale(
    #    coords[0] + 0.08, coords[1] + 0.015,
    #    coords[0], coords[1],
    #    10.,
    #    barstyle='fancy', labelstyle='simple',
    #    fillcolor1='w', fillcolor2='#555555',
    #    fontcolor='#555555',
    #    zorder=5)

    fig.set_tight_layout(True)
    fig.set_size_inches(9, 7)

    # plt.title('Toronto Neighborhoods: Priority Investment, Business ' +
    #          'Improvement Areas,\nand Current Value Assessment of Tax ' +
    #          'Impact on Residential Properties')
    # plt.legend()
    fig.savefig('TO_developm_neighborhoods.png')
    plt.show()


def main():
    """Main function on the program.

    What it does, for now, is just to visualize the investment and taxes
    in the neighborhoods in Toronto,
    """

    visualize_investment_in_toronto()


# The following two functions, colorbar_index() and cmap_discretize()
# are taken from, with some very minor changes:
#   http://sensitivecities.com/so-youd-like-to-make-a-map-using-python-EN.html
# and
#   http://brandonrose.org/pythonmap

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


def cmap_discretize(cmap, num):
    """
    Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet.
        num: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)

    """
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., num), (0., 0., 0., 0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., num + 1)
    cdict = {}
    for c_i, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, c_i], colors_rgba[i, c_i])
                      for i in xrange(num + 1)]
    return LinearSegmentedColormap(cmap.name + "_%d" % num, cdict, 1024)


if __name__ == '__main__':
    main()
