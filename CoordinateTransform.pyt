import arcpy
import math
# -*- coding: utf-8 -*-
import json
import urllib
import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323


#this code copy  from  https://github.com/wandergis/coordTransform_py
def gcj02_to_bd09(lng, lat):
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

dic={
    u"\u0077\u0067\u0073\u0038\u0034\u005f\u0074\u006f\u005f\u706b\u661f\u5750\u6807\u7cfb\u0028\u8c37\u6b4c\u002c\u9ad8\u5fb7\u002c\u0067\u0065\u006f\u0071\u0029":wgs84_to_gcj02,
    u"\u0077\u0067\u0073\u0038\u0034\u005f\u0074\u006f\u005f\u767e\u5ea6\u5750\u6807\u7cfb":wgs84_to_bd09,
     u"\u706b\u661f\u5750\u6807\u7cfb\u0028\u8c37\u6b4c\u002c\u9ad8\u5fb7\u002c\u0067\u0065\u006f\u0071\u0029\u005f\u0074\u006f\u005f\u0077\u0067\u0073\u0038\u0034":gcj02_to_wgs84,
     u"\u706b\u661f\u5750\u6807\u7cfb\u0028\u8c37\u6b4c\u002c\u9ad8\u5fb7\u002c\u0067\u0065\u006f\u0071\u0029\u005f\u0074\u006f\u005f\u767e\u5ea6\u5750\u6807\u7cfb":gcj02_to_bd09,
     u"\u767e\u5ea6\u5750\u6807\u7cfb\u005f\u0074\u006f\u005f\u0077\u0067\u0073\u0038\u0034":bd09_to_wgs84,
     u"\u767e\u5ea6\u5750\u6807\u7cfb\u005f\u0074\u006f\u005f\u706b\u661f\u5750\u6807\u7cfb\u0028\u8c37\u6b4c\u002c\u9ad8\u5fb7\u002c\u0067\u0065\u006f\u0071\u0029":bd09_to_gcj02
}

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "coordinateTransform"
        self.alias = "coordinateTransform"

        self.tools = [TransformTool]
class TransformTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "coordinate Transform"
        self.description = "transform data between wgs84 bd09 and gcj02"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        in_feature = arcpy.Parameter(name="input_featureclass",
                                   displayName="Input FeatureClass",
                                   direction="Input",
                                   datatype='DEFeatureClass',
                                   parameterType="Required")


        method = arcpy.Parameter(name="transform_mothod",
                                  displayName="transform method",
                                  direction="Input",
                                  datatype='GPString',
                                  parameterType="Required",
                                  multiValue=False)
        out_feature = arcpy.Parameter(name="output_featureclass",
                                       displayName="Output FeatureClass",
                                       direction="Output",
                                       datatype='DEFeatureClass',
                                       parameterType="Required")
        method.filter.list=[i for i in dic.keys()]
        params = [in_feature, method, out_feature]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return parameters

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        in_layer = parameters[0].valueAsText
        method_name = parameters[1].valueAsText
        out_layer = parameters[2].valueAsText
        method=dic[method_name]
        arcpy.Copy_management(in_layer, out_layer)
        cur= arcpy.UpdateCursor(out_layer)
        SR= arcpy.Describe(out_layer).spatialReference
        for r in cur:
            geom = r.getValue("SHAPE")
            r.setValue("SHAPE",offsetGeometry(geom,method,SR))
            cur.updateRow(r)
        arcpy.SetParameterAsText(2, out_layer)
        return

def offsetGeometry(geom,method,SR):
    if geom.type=="point":
        tmp_point=geom.getPart(0)
        xx,yy=method(tmp_point.X,tmp_point.Y)
        new_point = arcpy.Point(xx, yy)
        point_geo=arcpy.PointGeometry(new_point)
        return  point_geo
    parts=geom.partCount
    if geom.partCount==0:
        print("empty part")
        return  geom
    part_array=[]
    for partCount in range(parts):
        new_point = arcpy.Point()
        new_array = arcpy.Array()

        array = geom.getPart(partCount)
        for x in range(0,array.count):
            old_point = array[x]
            if old_point==None:
                print("empty point")
                continue
            xx,yy=method(old_point.X,old_point.Y)
            new_point = arcpy.Point(xx, yy)
            new_array.add(new_point)
        part_array.append(new_array)
    if parts==1:
        part_array=part_array[0]
    new_geo=None
    if geom.type== 'polygon':
        new_geo = arcpy.Polygon(part_array,SR)
    elif geom.type== 'polyline':
        new_geo = arcpy.Polyline(part_array,SR)
    elif geom.type=="point":
        new_geo=arcpy.PointGeometry(part_array,spatial_reference=SR)
    part_array.removeAll()
    return new_geo


