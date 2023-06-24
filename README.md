# opentopo_dem
Tool to automatically download and process Global DEMs via opentopography api


**Usage**

Please use the below command to download Global DEMs hosted on [opentopography](https://portal.opentopography.org/datasets?minX=-144.3169420909554&minY=63.0617743330481&maxX=-144.2537592884724&maxY=63.09891026182693&group=global) for your region of interest.
- All global DEMs hosted on opentopography can be specified, such as 'COP30','COP90','SRTMGL1_E','SRTMGL1','SRTM_GL3','NASADEM'
- The program currently expects either *a shapefile of the region of interest (bounds_shp)*, or *bounds in lat and lon in format as  'minx miny maxx maxy'*
- for conviniently defining your region of interest as a shapefile, please use [geojson.io](https://geojson.io/), draw a rectangular bounding box, and save the output geojson block locally in a .geojson file
- Users must need to provide their opentopography api key
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

**Requires**
- python 3.8+
- geopandas
- requests
- opentopography apikey

**Authors**

[Shashank Bhushan](https://github.com/ShashankBice), [David Shean](https://github.com/dshean), [Scott Henderson](https://github.com/scottyhq)

