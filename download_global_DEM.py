#! /usr/bin/env python

import argparse
import geopandas as gpd
from opentopo_dem import opentopo_utils

def get_parser():
        parser = argparse.ArgumentParser(description="utility to download global DEMs from opentopo API for a given extent")
        dem_options = ['COP30','COP90','SRTMGL1_E','SRTMGL1','SRTM_GL3','NASADEM']
        parser.add_argument('-demtype',type=str,default='COP30',help='Select the DEM intended to be downloaded (default: %(default)s)')
        parser.add_argument('-extent',help="Bounding box extent in single quotes  as 'minx miny maxx maxy' in lat and lon",
            type=str,required=False,default=None)
        parser.add_argument('-bound_shp',help='Shapefile specifying extent, if extent is not provided explictly',
            type=str,required=False,default=None)

        parser.add_argument('-apikey',help='Opentopgraphy api key',type=str,required=True)
        parser.add_argument('-out_fn',help='Output filename',type=str,default=None)
        parser.add_argument('-out_proj',type=str,default='EPSG:4326',help='Final projection of output as EPSG code (default: %(default)s)')
        return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.extent is not None:
        minx,miny,maxx,maxy = args.extent.split(' ')
    else:
        if args.bound_shp is not None:
            bound = gpd.read_file(args.bound_shp).to_crs('EPSG:4326')
            minx,miny,maxx,maxy = bound.total_bounds
        else:
            print("You need to provide either the extent or the bound shp to run this program")
            sys.exit()
    bounds = [float(minx),float(miny),float(maxx),float(maxy)]
    print(bounds)
    opentopo_utils.get_dem(demtype=args.demtype, bounds=bounds, apikey=args.apikey, out_fn=args.out_fn, proj=args.out_proj)
    print("Script is complete")

if __name__=="__main__":
    main()



