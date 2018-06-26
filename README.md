# coordinateTransform
transform coordinate between wgs84 bj09 and gcj02
有很多工具可以做 wgs84 百度坐标系 以及火星坐标系直接的转换。
但是缺一个可以直接对 shp文件进行整体转换的工具
要是有界面可以操作就更好了。
转换的算法来自
https://github.com/wandergis/coordTransform_py

开发了一个pyt工具箱，可以在arcmap arcgis pro中打开，
选择 要素类
选择 转换方法
得到转换后的 shp文件。
