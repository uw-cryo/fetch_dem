#! /usr/bin/env python

import os, sys
import argparse
import geopandas as gpd
import rasterio 
import rasterio.warp
from fetch_dem import opentopo_utils

def get_parser():
        parser = argparse.ArgumentParser(description="utility to download global DEMs from opentopo API for a given extent")
        dem_options = ['SRTMGL3', 'SRTMGL3_E', 'SRTMGL1', 'SRTMGL1_E', 'AW3D30', 
                       'AW3D30_E', 'SRTM15Plus', 'SRTM15Plus_E', 'NASADEM', 'NASADEM_E', 
                       'COP30', 'COP30_E', 'COP90', 'COP90_E', 'EU_DTM', 'GEDI_L3']
        parser.add_argument('-demtype',type=str,default='COP30', choices=dem_options, \
                help='Select the DEM intended to be downloaded, postfix "_E" refers to ellipsiodal heights with respect to the WGS84 datum (default: %(default)s)')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-extent',help="Bounding box extent in single quotes as 'minx miny maxx maxy' in EPSG:4326 (latitude and longitude)",
            type=str,required=False,default=None)
        group.add_argument('-vector_fn',help='Vector dataset filename specifying desired extent.',
            type=str,required=False,default=None)
        group.add_argument('-raster_fn',help='Raster dataset filename specifying desired extent.',
            type=str,required=False,default=None)
        parser.add_argument('-pad',help='Pad bounds (deg)',type=float,default=0,required=False)
        parser.add_argument('-apikey',help='Opentopgraphy API key',type=str,default='demoapikeyot2022',required=False)
        parser.add_argument('-out_fn',help='Desired output filename, the program appends output horizontal crs EPSG code at the end',type=str,default=None)
        parser.add_argument('-out_proj',type=str,default=None,help='Output EPSG code for horizontal CRS (e.g., EPSG:4326, EPSG:32610); if not provided, will default to opentopography provided horizontal CRS')
        return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.extent is not None:
        minx,miny,maxx,maxy = args.extent.split(' ')
    else:
        #Can likely clean this up to automatically determine if raster or vector fn was provided
        if args.vector_fn is not None:
            if os.path.exists(args.vector_fn):
                bounds = gpd.read_file(args.vector_fn).to_crs('EPSG:4326')
                minx,miny,maxx,maxy = bounds.total_bounds
            else:
                sys.exit(f"Input file not found: {args.vector_fn}")
        elif args.raster_fn is not None:
            if os.path.exists(args.raster_fn):
                with rasterio.open(args.raster_fn) as dataset:
                    bounds = dataset.bounds
                    bounds = rasterio.warp.transform_bounds(dataset.crs, 'EPSG:4326', *bounds)
                    minx,miny,maxx,maxy = bounds
            else:
                sys.exit(f"Input file not found: {args.raster_fn}")
    bounds = [float(minx),float(miny),float(maxx),float(maxy)]
    bounds = [bounds[0] - args.pad, bounds[1] - args.pad, bounds[2] + args.pad, bounds[3] + args.pad]
    print(bounds)
    opentopo_utils.get_dem(demtype=args.demtype, bounds=bounds, apikey=args.apikey, out_fn=args.out_fn, proj=args.out_proj)

if __name__=="__main__":
    main()
