import unittest
from unittest.mock import patch, mock_open

from shadow.polyedr import Polyedr


class TestPolyedr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        fake_file_content = """200.0	45.0	45.0	30.0
8	4	16
-0.5	-0.5	0.5
-0.5	0.5	0.5
0.5	0.5	0.5
0.5	-0.5	0.5
-0.5	-0.5	-0.5
-0.5	0.5	-0.5
0.5	0.5	-0.5
0.5	-0.5	-0.5
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5"""
        fake_file_path = 'data/holey_box.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr.facets), 4)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr.edges), 16)

class TestPolyedgVisibility(unittest.TestCase):

    def setUp(self):
        self.polyedr = Polyedr.__new__(Polyedr)
        self.polyedr.facets = []
        self.polyedr.facet_visibility = Mock()

    def test_empty_facets_list(self):
        self.assertFalse(self.polyedr.polyedg_visibility())

    # Все грани видимы
    def test_all_facets_visible(self):
        self.polyedr.facets = [Mock() for _ in range(3)]
        self.polyedr.facet_visibility.return_value = True
        self.assertTrue(self.polyedr.polyedg_visibility())

    # Хотя бы одна грань видима
    def test_at_least_one_visible(self):
        self.polyedr.facets = [Mock() for _ in range(4)]
        self.polyedr.facet_visibility.side_effect = [False, False, True, False]
        self.assertTrue(self.polyedr.polyedg_visibility())

    # Ни одна грань не видима
    def test_none_visible(self):
        self.polyedr.facets = [Mock() for _ in range(2)]
        self.polyedr.facet_visibility.return_value = False
        self.assertFalse(self.polyedr.polyedg_visibility())
