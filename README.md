# Create Offsets Points

## Description

This tool creates offset points from an input line feature class. Offset points are characterized by:
 - A position along a the source line.
 - A side (left or right of the line)
 - A distance from the line

A position must be a value between 0 and 1, 0 being the first point of the line, and 1 being the end point of the line. The same position along line can be used for all features or a different position can be used for each individual feature by using a field. The logic is similar to using a distance field when working with buffers in ArcGIS.

 ## Requirements

 This tool is designed and tested for both ArcGIS Pro 2.4 and ArcMap 10.7.1.

 ## How to run This tool is designed and tested for ArcGIS Pro.
 ## Hw to run

Check the description associated with the tool for more information.

## Different position along line per feature
 
### Tool Create Offset Points

This tool is designed and tested for ArcGIS Pro 2.4 and ArcMap 10.7.1.

## How to run

Check the description associated with the tool for more information.

## Different position along line per feature
Check the description associated with the tool for more information. The tool takes parameters:
 - Input Lines: The input line feature classes.
 - Output Points: The output offset points.
 - Ratio: The position along the line used to create the offset. The position must be between 0 and 1. 0 represent the position at the first vertex, and 1 the position at the last vertex.
 - Perpendicular Distance: The distance away from the line at which the offset point will be created.
 - Use Left: If true, the offset will be drawn on the left of the segment. Otherwise, the tool will be drawn on the right.
 - Ratio Field: A field to determine the position along the line. This is optional, and will override the default ration value if provided.
 - Distance Field: A field to determine the distance of the offset point from the line. This is optional, and will override the default perpendicular distance value if provided.


## Different position along line per feature

The value represented the position on a line at a specific distance can be computed for each features. See the sample expressions in the subfolder `sample-calculator-expressions`