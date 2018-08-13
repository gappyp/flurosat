from osgeo import osr, gdal
import sys

# to geodesic coords
def to_geo(fn, P, L):
    # get the existing coordinate system
    ds = gdal.Open(str(fn))
    old_cs= osr.SpatialReference()
    old_cs.ImportFromWkt(ds.GetProjectionRef())

    # create the new coordinate system
    wgs84_wkt = """
GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs .ImportFromWkt(wgs84_wkt)

    # create a transform object to convert between coordinate systems
    transform = osr.CoordinateTransformation(old_cs,new_cs)

    #get the point to transform, pixel (0,0) in this case
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()

    Xp = gt[0] + P*gt[1] + L*gt[2];
    Yp = gt[3] + P*gt[4] + L*gt[5];

    #get the coordinates in lat long
    latlong = transform.TransformPoint(Xp, Yp)

    #print(latlong)

    def decdeg2dms(dd):
       is_positive = dd >= 0
       dd = abs(dd)
       minutes,seconds = divmod(dd*3600,60)
       degrees,minutes = divmod(minutes,60)
       degrees = degrees if is_positive else -degrees
       return (degrees,minutes,seconds)

    # takes floats, uses sign of degrees
    def dms2decdeg(d, m, s):
        if d < 0:
            return d-m/60-s/(60*60)
        else:
            return d+m/60+s/(60*60)

    lat, lon, _ = latlong
    return (lat, lon)