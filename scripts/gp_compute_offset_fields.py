import math
import arcpy
import os

def get_slope(start, end):
    dy = end.Y - start.Y
    dx = end.X - start.X
    return dx, dy


def find_point_before(polyline, position_along):
    part = polyline.getPart(0)
    location = 0
    for p in part:
        new_location = polyline.measureOnLine(p, False)
        if new_location >= position_along:
            return location
        location = new_location
        return location


def get_normal(polyline, dist, left=True, perpandicular_distance=0.05):
    line_part = polyline.getPart(0)
    distance = dist
    start_point_position = find_point_before(polyline, dist)
    start_point = polyline.positionAlongLine(start_point_position, False)
    point = polyline.positionAlongLine(dist, False)
    dx, dy = get_slope(start_point.centroid, point.centroid)
    segment_angle = math.degrees(math.atan2(dy, dx))
    delta_x = math.cos(math.radians(segment_angle - 90)) * perpandicular_distance
    delta_y = math.sin(math.radians(segment_angle - 90)) * perpandicular_distance
    if left == False:
        delta_x = delta_x * -1
        delta_y = delta_y * -1
    x = point.centroid.X + delta_x
    y = point.centroid.Y + delta_y
    return [x, y]


def parse_line_features(line_fc, points_fc, ratio, perpendicular_distance=0.5, left=True):
    """

    :param line_fc:
    :param points_fc:
    :param ratio:
    :param left:
    :return:
    """

    if arcpy.Exists(points_fc):
        arcpy.Delete_management(points_fc)

    workspace_split = points_fc.split(os.path.sep)
    workspace = os.path.sep.join(workspace_split[:-1])
    arcpy.AddMessage('Output Workspace: {}'.format(workspace))
    arcpy.CreateFeatureclass_management(workspace, workspace_split[-1], 'POINT', spatial_reference=line_fc)
    arcpy.AddField_management(points_fc, 'ORIG_FID', 'DOUBLE')
    with arcpy.da.SearchCursor(line_fc, ['OID@', 'SHAPE@'], where_clause='1=1') as search_cursor:
        with arcpy.da.InsertCursor(points_fc, ['ORIG_FID', 'SHAPE@']) as insert_cursor:
            for line_rows in search_cursor:
                polyline = line_rows[1]
                if polyline.partCount > 1:
                    arcpy.AddError(
                        'The polyline with id {} is a multipart ({}), which is not supported. This feature will be skipped.'.format(
                            line_rows[0],
                            polyline.partCount
                        ))
                    continue
                point = get_normal(polyline, ratio, left, perpendicular_distance)
                insert_cursor.insertRow((line_rows[0], point))


if __name__ == '__main__':
    input_lines_features = arcpy.GetParameterAsText(0)
    output_points_features = arcpy.GetParameterAsText(1)
    ratio = float(arcpy.GetParameterAsText(2))
    perpendicular_distance = float(arcpy.GetParameterAsText(3))
    use_left = arcpy.GetParameter(4)
    parse_line_features(input_lines_features, output_points_features, ratio, perpendicular_distance, use_left)