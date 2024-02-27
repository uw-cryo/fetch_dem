#! /usr/bin/env python

import os,sys,glob,shutil
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
    download_fn = os.path.splitext(out_fn)[0]+"_temp.tif"
    if demtype in ['SRTMGL3_E','SRTM15Plus_E','NASADEM_E','COP30_E','COP90_E',
                     'EU_DTM_E']:
        base_type = demtype.split('_E')[0]
        print(f"Ellipsoidal versions of {base_type} is not provided automatically...")
        print(f"Will perform vertical datum adjustment downstream.....")
        download_type = base_type
    else:
        download_type = demtype
    if os.path.exists(out_fn):
        print(f"Deleting existing DEM file with same name as {out_fn}")
        os.remove(out_fn)
    if not os.path.exists(download_fn):
        #Prepare API request url
        #Bounds should be [minlon, minlat, maxlon, maxlat]
        url = base_url.format(download_type, *bounds, apikey)
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
        open(download_fn, 'wb').write(response.content)
    
    if (proj != None) | (download_type != demtype):
        #Could avoid writing to disk and direclty reproject with rasterio, using gdalwarp for simplicity
        #proj_fn = os.path.splitext(out_fn)[0]+'_proj.tif'
        
        #output_res = 30 ## allow GDAL to calculate output res on its own (https://github.com/uw-cryo/fetch_dem/issues/3)
        gdalwarp = find_executable('gdalwarp')
        
        if download_type != demtype:
            input_horizontal_crs = horizontal_crs_dict[base_type]
            input_vertical_crs = vertical_geoid_proj_dict[base_type]
            input_crs = f"{input_horizontal_crs}+{input_vertical_crs}"
            
            if proj == None:
                proj = input_horizontal_crs
            output_horizontal_crs = proj
            if (base_type == 'EU_DTM') & (proj == horizontal_crs_dict['EU_DTM']):
                output_vertical_crs = 'EPSG:7912' #GRS80 ellipsoidal heights
            else:
                output_vertical_crs = 'EPSG:4979' #WGS84 ellipsoidal heights
            output_crs = f"{output_horizontal_crs}+{output_vertical_crs}"
            gdal_edit_crs = output_crs
            
        else:
            #this is for vertical height transformation is not required
            input_crs = f"{horizontal_crs_dict[demtype]}"
            output_crs = proj
            gdal_edit_crs = output_crs+f"{vertical_geoid_proj_dict[demtype]}"
            
        gdalwarp_call = f"{gdalwarp} -r cubic -co COMPRESS=LZW -co TILED=YES -co BIGTIFF=IF_SAFER -s_srs '{input_crs}' -t_srs '{output_crs}' {download_fn} {out_fn}"
        print(gdalwarp_call)
        run_bash_command(gdalwarp_call)
    else:
        shutil.copy2(download_fn,out_fn)
        gdal_edit_crs = f"{horizontal_crs_dict[demtype]}"+f"{vertical_geoid_proj_dict[demtype]}"
    os.remove(download_fn)
    gdal_edit_cmd = find_executable('gdal_edit.py')
    gdal_edit_call = f"{gdal_edit_cmd} {out_fn} -a_srs {gdal_edit_crs}"
    run_bash_command(gdal_edit_call)
    return out_fn

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
    'SRTM_GL1_E': 'EPSG:4979',
    'AW3D30_E': 'EPSG:4979',
    'SRTM_GL1': 'EPSG:5773',
    'AW3D30': 'EPSG:5773',
    'SRTMGL3': 'EPSG:5773',
    'SRTM15Plus': 'EPSG:5773',
    'NASADEM': 'EPSG:5773',
    'COP30': 'EPSG:3855',
    'COP90': 'EPSG:3855',
    'EU_DTM': 'EPSG:3855'
}
horizontal_crs_dict = {
    'SRTMGL1': 'EPSG:4326',
    'AW3D30': 'EPSG:4326',
    'SRTMGL1_E': 'EPSG:4326',
    'AW3D30_E': 'EPSG:4326',
    'SRTMGL3': 'EPSG:4326',
    'SRTM15Plus': 'EPSG:4326',
    'NASADEM': 'EPSG:4326',
    'COP30': 'EPSG:4326',
    'COP90': 'EPSG:4326',
    'EU_DTM': 'EPSG:3035'
}

    
