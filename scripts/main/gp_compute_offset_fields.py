import math
import arcpy
import os


def get_slope(start, end):
    """
    Return a tuple that contains the x and y delta between two points.
    :param start: The start point. Must have X and Y attributes.
    :param end: The end point. Must have X and Y attributes.
    :return: A 2 elements tuple. The first element is the x-delta, the second is the y-delta.
    """
    dy = end.Y - start.Y
    dx = end.X - start.X
    return dx, dy


def find_point_before(polyline, position_along):
    """
    Find the point on the polyline ahead of the position passed as parameter.
    :param polyline: The polyline
    :param position_along: The position along the segment to query.
    :return: a number between 0 and 1
    """
    if position_along < 0 or position_along > 1:
        raise Exception('parameter position_along should have a value between 0 and 1')

    parts_count = polyline.partCount
    location = 0
    for part_index in range(0, parts_count):
        part = polyline.getPart(part_index)
        for p in part:
            new_location = polyline.measureOnLine(p, True)
            if new_location >= position_along:
                return location
            location = new_location
    return location


def get_offset_point(polyline, ratio, left=True, perpendicular_distance=0.05):
    """
    Returns the point along the line with an offset. This the point used to draw the normal line to a polyline.
    :param polyline: The input polyline
    :param ratio: The ratio. A value between 0 and 1.
    :param left: If true, the offset will be drawn on the left side of the input line. Other wise, the offset point will be on the right.
    :param perpendicular_distance: The distance from the line on which the input point will be. Uses the input feature class projection unit.
    :return: An array representing the offset point. The first element represents the X value, the second the Y value.
    """
    start_point_position = find_point_before(polyline, ratio)
    start_point = polyline.positionAlongLine(start_point_position, False)
    point = polyline.positionAlongLine(ratio, True)
    dx, dy = get_slope(start_point.centroid, point.centroid)
    segment_angle = math.degrees(math.atan2(dy, dx))
    delta_x = math.cos(math.radians(segment_angle - 90)) * perpendicular_distance
    delta_y = math.sin(math.radians(segment_angle - 90)) * perpendicular_distance
    if left == False:
        delta_x = delta_x * -1
        delta_y = delta_y * -1
    x = point.centroid.X + delta_x
    y = point.centroid.Y + delta_y
    return [x, y]


def parse_line_features(line_fc, points_fc, ratio, perpendicular_distance=0.5, left=True, ratio_field=None):
    """
    Generates an output feature class of offet points based on the input line feature class.
    :param line_fc: The input line feature class
    :param points_fc: The output offset points feature class
    :param ratio: The ratio on which each point will be drawn on the feature class.
    :param perpendicular_distance: The offset distance.
    :param left: If true, the offset will be drawn on the left of the line. It will be drawn on the right otherwise.
    :param ratio_field: The field that contains the ratio along line for the segment. Will override the ratio value for each feature if provided.
    :return:
    """

    if arcpy.Exists(points_fc):
        arcpy.Delete_management(points_fc)

    workspace_split = points_fc.split(os.path.sep)
    workspace = os.path.sep.join(workspace_split[:-1])
    arcpy.AddMessage('Output Workspace: {}'.format(workspace))
    arcpy.CreateFeatureclass_management(workspace, workspace_split[-1], 'POINT', spatial_reference=line_fc)
    arcpy.AddField_management(points_fc, 'ORIG_FID', 'DOUBLE')

    # Leverage the ratio field if provided.
    search_fields = ['OID@', 'SHAPE@']
    if ratio_field is not None:
        search_fields.append(ratio_field)

    with arcpy.da.SearchCursor(line_fc, search_fields, where_clause='1=1') as search_cursor:
        with arcpy.da.InsertCursor(points_fc, ['ORIG_FID', 'SHAPE@']) as insert_cursor:
            for line_rows in search_cursor:
                polyline = line_rows[1]
                feature_ratio = line_rows[2] if ratio_field is not None else ratio
                if feature_ratio is None:
                    arcpy.AddWarning(
                        'Set to use ratio field but no value provided for id {}. Default ratio used.'.format(line_rows[0])
                    )
                point = get_offset_point(polyline, feature_ratio, left, perpendicular_distance)
                insert_cursor.insertRow((line_rows[0], point))


if __name__ == '__main__':
    input_lines_features = arcpy.GetParameterAsText(0)
    output_points_features = arcpy.GetParameterAsText(1)
    ratio = float(arcpy.GetParameterAsText(2))
    perpendicular_distance = float(arcpy.GetParameterAsText(3))
    use_left = arcpy.GetParameter(4)
    ratio_field = None if arcpy.GetParameterAsText(5) in ["#", ''] else arcpy.GetParameterAsText(5)

    parse_line_features(
        input_lines_features,
        output_points_features,
        ratio,
        perpendicular_distance,
        use_left,
        ratio_field
    )