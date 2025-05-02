"""
Tests for tucsonmesh.trellotogeojson.get_board
"""

import unittest

from tucsonmesh.trellotogeojson.get_board import get_coordinates


class GetCoordinatesTestCase(unittest.TestCase):
    """Test get_coordinates() function"""

    def test_get_coordinates_maps_link_has_coordinates(self):
        """
        Test that the get_coordinates() function returns coordinates when the
        text includes a Google Maps link that has coordinates in it

        """
        description = """
        # Location\n\n2001 N 7th Ave\n\n[https://www.google.com/maps/place/BICAS/@32.246221,-110.9707685,20.36z/data=!4m6!3m5!1s0x86d6711f35286f23:0xf345ecfca1e8eda2!8m2!3d32.2462729!4d-110.9707784!16s%2Fg%2F1td00y9l?entry=ttu](https://www.google.com/maps/place/BICAS/@32.246221,-110.9707685,20.36z/data=!4m6!3m5!1s0x86d6711f35286f23:0xf345ecfca1e8eda2!8m2!3d32.2462729!4d-110.9707784!16s%2Fg%2F1td00y9l?entry=ttu "smartCard-inline")\n\n# Contact Info\n\n[PHONE](%22%E2%80%8C%22 "‌")\n\n[EMAIL](%22%E2%80%8C%22 "‌")
        """

        lat, lon = get_coordinates(description)
        self.assertEqual(lat, 32.246221)
        self.assertEqual(lon, -110.9707685)

    def test_get_coordinates_raises_no_maps_link(self):
        """
        Test that get_coordinates() raises an exception when no maps link is
        present

        """
        description = "BLAH BLAH BLAH"

        with self.assertRaises(ValueError):
            get_coordinates(description)

    def test_get_coordinates_short_link(self):
        """
        Test that get_coordinates() returns coordinates when the text
        contains a shortened maps link

        """
        description = """
        # Location\n\n437 E Grant Rd, Tucson, AZ 85705, USA\n\n[See on Google Maps](https://goo.gl/maps/EMsxJFREhBpyyF4V6 "‌")\n\n# Contact Info\n\ninfo@everybody.gallery
        """
        lat, lon = get_coordinates(description)
        self.assertEqual(lat, 32.25063)
        self.assertEqual(lon, -110.9643449)
