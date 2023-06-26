# opentopo_dem
Utility to request, download, and process a user-specified region of the global DEMs available via OpenTopography API

## Background
OpenTopography hosts several Global DEM datasets in cloud-optimized formats (https://portal.opentopography.org/apidocs/#/Public/getGlobalDem) and offers a simple, intuitive API to subset these products on demand. This python script provides a high-level interface to submit an API request for a user-specified region of interest. This can be run interactively, or called by other scripts.

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
- Please create a free account with OpenTopography to receive an API key and pass this to `apikey`
  - https://opentopography.org/blog/introducing-api-keys-access-opentopography-global-datasets
  - The default `demoapikeyot2022` can be used for testing
- `demtype` can be any of the global DEMs hosted on opentopography. See link above for latest list.
  - As of June 2023: `['SRTMGL3', 'SRTMGL1', 'SRTMGL1_E', 'AW3D30', 'AW3D30_E', 'SRTM15Plus', 'NASADEM', 'COP30', 'COP90', 'EU_DTM', 'GEDI_L3']`
- The region of interest `extent` can be defined with a vector polygon (e.g., shapefile, geojson) filename passed to `-bound_shp` or a rectangular bounding box extent in lat/lon coordinates ('minx miny maxx maxy')
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

