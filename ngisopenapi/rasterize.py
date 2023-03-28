# rasterize_vector.py
from osgeo import gdal, ogr, osr
import os

def rasterize_vector(input_vector, output_raster, pixel_size=30, nodata_value=-9999):
    source_ds = ogr.Open(input_vector)
    source_layer = source_ds.GetLayer()
    source_srs = source_layer.GetSpatialRef()

    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    x_res = int((x_max - x_min) / pixel_size)
    y_res = int((y_max - y_min) / pixel_size)

    target_ds = gdal.GetDriverByName('GTiff').Create(output_raster, x_res, y_res, 1, gdal.GDT_Float32)

    if target_ds is None:
        print("Error: Failed to create target dataset")
        return

    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    target_ds.SetProjection(source_srs.ExportToWkt())

    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(nodata_value)
    band.Fill(nodata_value)

    gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[1])

    source_ds = None
    target_ds = None


    #output_raster_path = os.path.join(os.getenv('f_path'), f'{uuid.uuid4()}.tif')
    #rasterize_vector(os.getenv('f_path') + filename, output_raster_path, pixel_size=30, nodata_value=-9999)