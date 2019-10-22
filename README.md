# Create Offsets Points

## Description

This tool creates offset points from an input line feature class. Offset points are characterized by:
 - A position along a the source line.
 - A side (left or right of the line)
 - A distance from the line

A position must be a value between 0 and 1, 0 being the first point of the line, and 1 being the end point of the line. The same position along line can be used for all features or a different position can be used for each individual feature by using a field. The logic is similar to using a distance field when working with buffers in ArcGIS.

 ## Requirements

 This tool is designed and tested for ArcGIS Pro.

 ## How to run

Check the description associated with the tool for more information.

## Different position along line per featrure

To be documented. 

The value represented the position on a line at a specific distance can be computed in a field and then used as in input to the tool. Assuming your input feature class uses meters as a distance unit, here is the field calculator expression to get the position along the line at 0.5 meters from the starting node: `!Shape!.measureOnLine(!Shape!.positionAlongLine(0.5, False), True)`

 ## Output

 A point feature class. The output feature class will have a field called ORIG_FID that can be used to trace back the source feature it was created from.