# Visualizing the Investment in the Neighborhoods of Toronto

This is a technical test of visualizing the investment in the neighborhoods
of Toronto and the relative Tax Estimation on Residential Properties in
those neighborhoods, using matplotlib/numpy/basemap/descartes in Python.

# WIP

This project is a *work in progress*. The implementation is *incomplete*
and subject to change. The documentation can be inaccurate.

# Open Data used from the City of Toronto

Several geographical data sources of the Open Data initiative of the City
of Toronto are used (taken to the WGS84 coordinate system, which most of
them offer):

[City Wards](http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=b1533f0aacaaa210VgnVCM1000006cd60f89RCRD)

[Priority Investment Neighbourhoods for the Toronto Strong Neighbourhoods 2020](http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=ac0389fe9c18b210VgnVCM1000003dd60f89RCRD)

[Business Improvement Areas](http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=8c5d5f9cd70bb210VgnVCM1000003dd60f89RCRD)

[Current Value Assessment (CVA) Tax Impact Residential Properties](http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=b40a57200ff2f210VgnVCM1000003dd60f89RCRD)

[Capital Budget & Plan By Ward (10 Year Recommended)](http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=1dc340271f8e3310VgnVCM1000003dd60f89RCRD)

The script `download_investm_shapefiles_toronto.sh` is given to download
these GIS shapefiles and Excel budgets, and to prepare the GIS shapefiles
to the WGS84 coordinate system (if necessary).

# The very First Version of the Visualization

This is the very first version of the
![Visualization](/TO_developm_neighborhoods.png?raw=true "First version of the visualization using matplotlib/basemap on ESRI shapefiles").

Further work on this is coming.


# Analysis

As mentioned above, this is just a technical test of visualizing the
investment in the neighborhoods of Toronto and relative Tax Estimation
on Residential Properties: a more throughout Data Mining could be
possible as to visualize why certain neighborhoods are chosen, etc,
but these are social and urban planning projections for the future of
Toronto, so Data Mining on them could be computationally expensive.
(This could be interesting and useful on its own: the City of Toronto
offers many more sources of information in its
[Open Data program](http://www.toronto.ca/open).)

