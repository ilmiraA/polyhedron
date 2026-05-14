import unittest

from shadow.polyedr import Polyedr


class TestPolyedr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.polyedr = Polyedr(f"data/test.geom")

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr.facets), 6)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr.edges), 24)

    # Грань видима
    def test_facet_visibility_01(self):
        self.assertTrue(self.polyedr.facet_visibility(self.polyedr.facets[0]))

    # Грань невидима
    def test_facet_visibility_03(self):
        self.assertFalse(self.polyedr.facet_visibility(self.polyedr.facets[5]))

    # Грань видима
    def test_facet_visibility_03(self):
        self.assertTrue(self.polyedr.facet_visibility(self.polyedr.facets[3]))
