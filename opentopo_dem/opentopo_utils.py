#! /usr/bin/env python

import os,sys,glob
import subprocess

def get_dem(demtype, bounds, apikey, out_fn=None, proj='EPSG:4326',output_res=30):
    """
    download a DEM of choice from OpenTopography World DEM
    ## first written by David Shean
    Parameters
    ------------
    demtype: str
        type of DEM to fetch (e.g., COP30, SRTMGL1, SRTMGL1_E, SRTMGL3 etc)
    bounds: list
        geographic aoi extent in format (minx,miny,maxx,maxy)
    apikey: str
        opentopography api key
    out_fn: str
        path to output filename
    proj: str
        output DEM projection
    output_res: numeric
        resolution of output DEM (default 30 m)
    Returns
    -----------
    out_DEM: str
        path to output DEM (useful if the downloaded DEM is reprojected to custom proj)
    """
    import requests
    from distutils.spawn import find_executable
    ### first written by David Shean (dshean@uw.edu)
    base_url="https://portal.opentopography.org/API/globaldem?demtype={}&west={}&south={}&east={}&north={}&outputFormat=GTiff&API_Key={}"
    if out_fn is None:
        out_fn = '{}.tif'.format(demtype)
    if not os.path.exists(out_fn):
        #Prepare API request url
        #Bounds should be [minlon, minlat, maxlon, maxlat]
        url = base_url.format(demtype, *bounds, apikey)
        print(url)
        #Get
        response = requests.get(url)
        #Check for 200
        if response.ok:
            print ('OK!')
        else:
            print ('Query failed')
            sys.exit()
        #Write to disk
        open(out_fn, 'wb').write(response.content)
    if proj != 'EPSG:4326':
        #Could avoid writing to disk and direclty reproject with rasterio, using gdalwarp for simplicity
        proj_fn = os.path.splitext(out_fn)[0]+'_proj.tif'
        if not os.path.exists(proj_fn):
            output_res = 30
            gdalwarp = find_executable('gdalwarp')
            gdalwarp_call = f"{gdalwarp} -r cubic -co COMPRESS=LZW -co TILED=YES -co BIGTIFF=IF_SAFER -tr {output_res} {output_res} -t_srs '{proj}' {out_fn} {proj_fn}"
            print(gdalwarp_call)
            run_bash_command(gdalwarp_call)
        out_DEM = proj_fn
    else:
        out_DEM = out_fn
    return out_DEM


def run_bash_command(cmd):
    #first written by Scott Henderson
    """Call a system command through the subprocess python module."""
    print(cmd)
    try:
        retcode = subprocess.call(cmd, shell=True)
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    

vertical_geoid_proj_dict = {
    'SRTMGL3': 'EPSG:5773',
    'SRTM15Plus': 'EPSG:5773',
    'NASADEM': 'EPSG:5773',
    'COP30': 'EPSG:3855',
    'COP90': 'EPSG:3855',
    'EU_DTM': 'EPSG:3855'
}
horizontal_crs_dict = {
    'SRTM_GL1': 'EPSG:4326',
    'AW3D30': 'EPSG:4326',
    'SRTM_GL1_E': 'EPSG:4326',
    'AW3D30_E': 'EPSG:4326',
    'SRTMGL3': 'EPSG:4326',
    'SRTM15Plus': 'EPSG:4326',
    'NASADEM': 'EPSG:4326',
    'COP30': 'EPSG:4326',
    'COP90': 'EPSG:4326',
    'EU_DTM': 'EPSG:3035'
}

    
