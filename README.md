# opentopo_dem
Utility to request, download, and process a user-specified region of the global DEMs available via OpenTopography API

## Background
OpenTopography hosts several Global DEM datasets (https://portal.opentopography.org/apidocs/#/Public/getGlobalDem) and offers a simple, intuitive API to subset these products. This python script provides a high-level interface to submit an API request for a user-specified region of interest. This can be run interactively, or called by other scripts.

## Usage
```console
> python download_global_DEM.py -h
usage: download_global_DEM.py [-h] [-demtype DEMTYPE] [-extent EXTENT] [-bound_shp BOUND_SHP] -apikey APIKEY [-out_fn OUT_FN] [-out_proj OUT_PROJ]

utility to download global DEMs from opentopo API for a given extent

optional arguments:
  -h, --help            show this help message and exit
  -demtype DEMTYPE      Select the DEM intended to be downloaded (default: COP30)
  -extent EXTENT        Bounding box extent in single quotes as 'minx miny maxx maxy' in lat and lon
  -bound_shp BOUND_SHP  Shapefile specifying extent, if extent is not provided explictly
  -apikey APIKEY        Opentopgraphy api key
  -out_fn OUT_FN        Output filename
  -out_proj OUT_PROJ    Final projection of output as EPSG code (default: EPSG:4326)
```

### Notes
- Please create a free account with OpenTopography to receive an API key
  - https://opentopography.org/blog/introducing-api-keys-access-opentopography-global-datasets
  - The default `demoapikeyot2022` can be used for testing
- All global DEMs hosted on opentopography can be specified, such as 'COP30','COP90','SRTMGL1_E','SRTMGL1','SRTM_GL3','NASADEM'
- The region of interest can be defined with a vector polygon (e.g., shapefile, geojson) passed to `-bound_shp` keyword argument or rectangular extent in lat/lon (bounds 'minx miny maxx maxy')
- To interactively define a region of interest, we recommend [geojson.io](https://geojson.io/)
  - Draw a rectangular bounding box
  - Copy/paste the output geojson block and save as a .geojson file
  - Pass this .geojson to `-bound_shp`



## Requirements
- python 3.8+
- geopandas
- requests

## Authors

[Shashank Bhushan](https://github.com/ShashankBice), [David Shean](https://github.com/dshean), [Scott Henderson](https://github.com/scottyhq)

