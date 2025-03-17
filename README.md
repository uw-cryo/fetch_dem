# fetch_dem
Utility to request, download, and process a user-specified region of the global DEMs available via OpenTopography API. In the future, we plan to add support to fetch DEMs from other resources. Currently the tools have been tested to run on *nix systems (e.g., Linux, Mac OS X) only.

## Background
OpenTopography hosts several Global DEM datasets in cloud-optimized formats (https://portal.opentopography.org/apidocs/#/Public/getGlobalDem) and offers a simple, intuitive API to subset these products on demand. This python script provides a high-level interface to submit an API request for a user-specified region of interest. This can be run interactively, or called by other scripts.

## Usage
```console
> python download_global_DEM.py -h
usage: download_global_DEM.py [-h]
                              [-demtype {SRTMGL3,SRTMGL3_E,SRTMGL1,SRTMGL1_E,AW3D30,AW3D30_E,SRTM15Plus,SRTM15Plus_E,NASADEM,NASADEM_E,COP30,COP30_E,COP90,COP90_E,EU_DTM,GEDI_L3}]
                              [-extent EXTENT] [-poly_fn POLY_FN] [-apikey APIKEY] [-out_fn OUT_FN] [-out_proj OUT_PROJ]

utility to download global DEMs from opentopo API for a given extent

options:
  -h, --help            show this help message and exit
  -demtype {SRTMGL3,SRTMGL3_E,SRTMGL1,SRTMGL1_E,AW3D30,AW3D30_E,SRTM15Plus,SRTM15Plus_E,NASADEM,NASADEM_E,COP30,COP30_E,COP90,COP90_E,EU_DTM,GEDI_L3}
                        Select the DEM intended to be downloaded, postfix "_E" refers to ellipsiodal heights with respect to the WGS84 datum (default: COP30)
  -extent EXTENT        Bounding box extent in single quotes as 'minx miny maxx maxy' in EPSG:4326 (latitude and longitude)
  -poly_fn POLY_FN      Vector dataset filename containing polygon specifying desired extent.
  -apikey APIKEY        Opentopgraphy API key
  -out_fn OUT_FN        Desired output filename, the program appends output horizontal crs EPSG code at the end
  -out_proj OUT_PROJ    Output EPSG code for horizontal CRS (e.g., EPSG:4326, EPSG:32610); if not provided, will default to opentopography provided
                        horizontal CRS
```

### Notes
- Please create a free account with OpenTopography to receive an API key and pass this to `apikey`
  - https://opentopography.org/blog/introducing-api-keys-access-opentopography-global-datasets
  - The default `demoapikeyot2022` can be used for testing
- `demtype` can be any of the global DEMs hosted on opentopography. See link above for latest list.
  - As of June 2023: `['SRTMGL3', 'SRTMGL1', 'SRTMGL1_E', 'AW3D30', 'AW3D30_E', 'SRTM15Plus', 'NASADEM', 'COP30', 'COP90', 'EU_DTM', 'GEDI_L3']`
  - In addition to the above list, the program can also fetch Ellipsoidal versions of the following demtypes : `['SRTMGL3_E','SRTM15Plus_E','NASADEM_E','COP30_E','COP90_E']`. The ellipsoidal heights are computed locally on the user's machine, downstream of opentopography api functionality. 
- The region of interest `extent` can be defined with a vector polygon (e.g., shapefile, geojson) filename passed to `-bound_shp` or a rectangular bounding box extent in lat/lon coordinates ('minx miny maxx maxy')
- To interactively define a region of interest, we recommend [geojson.io](https://geojson.io/)
  - Draw a rectangular bounding box
  - Copy/paste the output geojson block and save as a .geojson file
  - Pass this .geojson to `-bound_shp`

## Requirements
- python 3.8+
- GDAL 3+
- geopandas
- requests

## Authors

[Shashank Bhushan](https://github.com/ShashankBice), [David Shean](https://github.com/dshean), [Scott Henderson](https://github.com/scottyhq)

