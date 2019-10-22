# geoprocessing-compute-points-offsets

## Description

This tool creates offset points along line. Offset points are characterized by:
 - A position along a the source line.
 - A side (left or right of the line)
 - A distance from the line

A position must be a value between 0 and 1, 0 being the first point of the line, and 1 being the end point of the line. The same position along line can be used for all features or a different position can be used for each individual feature by using a field. The logic is similar to using a distance field when working with buffers in ArcGIS.

 ## Requirements

 This tool is designed and tested for ArcGIS Pro.

 ## How to run

Check the description associated with the tool for more information.

 ## Output

 A point feature class. The output feature class will have a field called ORIG_FID that can be used to trace back the source feature it was created from.