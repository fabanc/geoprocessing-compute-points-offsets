import arcpy
import os
import sys
import unittest

project_dir = os.path.abspath(os.path.dirname(__file__))
main_dir = os.path.join(os.path.dirname(project_dir), 'main')
print(main_dir)
sys.path.insert(0, main_dir)

import gp_compute_offset_fields as gp_compute_offset_fields

part_1 = [[0, 0], [10, 0]]
part_2 = [[10, 0], [20, 0]]

part_1_array = arcpy.Array([arcpy.Point(*coords) for coords in part_1])
part_2_array = arcpy.Array([arcpy.Point(*coords) for coords in part_2])
single_part = arcpy.Polyline(arcpy.Array([part_1_array, part_2_array]))


class MultiPart(unittest.TestCase):
    def test_left_start(self):
        projected_point = gp_compute_offset_fields.get_offset_point(single_part, 0.1, left=True, perpendicular_distance=0.5)
        self.assertEqual(projected_point[0], 2)
        self.assertEqual(projected_point[1], -0.5)

    def test_right_start(self):
        projected_point = gp_compute_offset_fields.get_offset_point(single_part, 0.1, left=False, perpendicular_distance=0.5)
        self.assertEqual(projected_point[0], 2)
        self.assertEqual(projected_point[1], 0.5)

    def test_left_end(self):
        projected_point = gp_compute_offset_fields.get_offset_point(single_part, 0.9, left=True, perpendicular_distance=0.5)
        self.assertEqual(projected_point[0], 18)
        self.assertEqual(projected_point[1], -0.5)

    def test_right_end(self):
        projected_point = gp_compute_offset_fields.get_offset_point(single_part, 0.9, left=False, perpendicular_distance=0.5)
        self.assertEqual(projected_point[0], 18)
        self.assertEqual(projected_point[1], 0.5)


if __name__ == '__main__':
    unittest.main()
