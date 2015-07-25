#!/usr/bin/env bash

function download_and_unzip() {
     local url="${1?1st arg is the URL to the ZIP Shapefile to download}"
     local local_file="${2?2nd arg is name of the local file to save to}"

     [[ -e "$local_file" ]] && rm -rf "$local_file"
     wget --quiet -O "$local_file"   "${url}"
     unzip -qq -o "$local_file"   # -o: don't confirm (shouldn't be needed)
}

function convert_shapefile() {
     local dst_shp="${1?1st arg is the destination Shapefile to obtain}"
     local src_shp="${2?2nd arg is the source Shapefile to transform}"
     local dst_srs="${3}"
     local src_srs="${4}"

     if [[ "$dst_srs" != "" ]]; then dst_srs="-t_srs $dst_srs"; fi
     if [[ "$src_srs" != "" ]]; then src_srs="-s_srs $src_srs"; fi
     ogr2ogr "$dst_shp" "$src_shp" $src_srs  $dst_srs

}

# These URLs below are offered by the Open Data initiative of the City of
# Toronto
# I know that these lines are lengthier than 80 characters, sorry

if [[ -e ./shp_dir ]]; then
   mv ./shp_dir  ./shp_dir.old-at-$( date +%s ).$RANDOM
fi
mkdir -p ./shp_dir
cd ./shp_dir

download_and_unzip 'http://www1.toronto.ca/City_Of_Toronto/Information_Technology/Open_Data/Data_Sets/Assets/Files/wards_may2010_wgs84.zip' \
                   'wards_may2010_wgs84.zip'
mv -f './gcc/Projects/Open Data/Files/Data Upload - May 2010/May2010_WGS84/'icitw_wgs84.*  .
/bin/rm -rf './gcc'

download_and_unzip 'http://www1.toronto.ca/City_Of_Toronto/Information_Technology/Open_Data/Data_Sets/Assets/Files/priority-invest-neighbourhoods.zip' \
                   'priority-invest-neighbourhoods.zip'
convert_shapefile  TO_priority_inv_neighb.shp \
                   'Priority Investment Neighbourhoods.shp' \
                   'EPSG:4326'  'EPSG:26717'

download_and_unzip 'http://opendata.toronto.ca/gcc/business_improvement_areas_wgs84.zip' 'business_improvement_areas_wgs84.zip'
convert_shapefile  TO_busin_improv_area.shp \
                   BUSINESS_IMPROVEMENT_AREA_WGS84.shp \
                   'EPSG:4326'

download_and_unzip 'http://www1.toronto.ca/City_Of_Toronto/Information_Technology/Open_Data/Data_Sets/Assets/Files/CVA_Tax_Impact_WGS84_(2011).zip' \
                   'CVA_Tax_Impact_WGS84_(2011).zip'

# This is the Capital Budget and Plan per City Ward
# http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=1dc340271f8e3310VgnVCM1000003dd60f89RCRD

wget --quiet -O budget_per_city_ward.xlsx \
    'http://www1.toronto.ca/City%20Of%20Toronto/Information%20&%20Technology/Open%20Data/Data%20Sets/Assets/Files/2015%20staff%20recommended%20capital%20projects%20by%20ward.xlsx'
