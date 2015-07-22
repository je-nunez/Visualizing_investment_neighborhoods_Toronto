#!/usr/bin/env bash

function download_and_unzip() {
     local url="${1?1st arg is the URL to the ZIP Shapefile to download}"
     local local_file="${2?2nd arg is name of the local file to save to}"

     [[ -e "$local_file" ]] && rm -rf "$local_file"
     wget -O "$local_file"   "${url}"
     unzip -o "$local_file"
}

# These URLs below are offered by the Open Data initiative of the City of
# Toronto
# Some of these GIS Shapefiles need to be transformed to the WSG84 coordinate
# system. This code will be added soon.
# I know that these lines are lengthier than 80 characters, sorry

download_and_unzip 'http://www1.toronto.ca/City_Of_Toronto/Information_Technology/Open_Data/Data_Sets/Assets/Files/wards_may2010_wgs84.zip' 'wards_may2010_wgs84.zip'

download_and_unzip 'http://www1.toronto.ca/City_Of_Toronto/Information_Technology/Open_Data/Data_Sets/Assets/Files/priority-invest-neighbourhoods.zip' 'priority-invest-neighbourhoods.zip'

download_and_unzip 'http://opendata.toronto.ca/gcc/business_improvement_areas_wgs84.zip' 'business_improvement_areas_wgs84.zip'

download_and_unzip 'http://www1.toronto.ca/City_Of_Toronto/Information_Technology/Open_Data/Data_Sets/Assets/Files/CVA_Tax_Impact_WGS84_(2011).zip' 'CVA_Tax_Impact_WGS84_(2011).zip'

