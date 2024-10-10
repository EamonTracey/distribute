import argparse
import unittest

import SpreadSheet
import SpreadSheetClient


class SpreadSheetTests(unittest.TestCase):
    """
    The SpreadSheetTests class is not a normal unit test. Before invocation,
    the class expects assignment of NAME. Further, each test case
    expects a clean spreadsheet and must return the spreadsheet to cleanliness.

    The reason is simplicity in testing the distributed implementation.
    """

    NAME = None

    def setUp(self):
        # self.spreadsheet = SpreadSheet.SpreadSheet()
        self.assertTrue(SpreadSheetTests.NAME is not None)
        self.spreadsheet = SpreadSheetClient.SpreadSheetClient(SpreadSheetTests.NAME)
        self.assertEqual(self.spreadsheet.size(), (0, 0))

    def test_insert_valid(self):
        self.spreadsheet.insert(1, 1, 1)
        self.assertEqual(self.spreadsheet.lookup(1, 1), 1)
        self.spreadsheet.remove(1, 1)

        self.spreadsheet.insert(1, 1, 2)
        self.assertEqual(self.spreadsheet.lookup(1, 1), 2)
        self.spreadsheet.remove(1, 1)

        self.spreadsheet.insert(1, 1, {"complex": {"data": 3}})
        self.assertEqual(self.spreadsheet.lookup(1, 1),
                         {"complex": {
                             "data": 3
                         }})
        self.spreadsheet.remove(1, 1)

        self.spreadsheet.insert(53, 91, "eamon")
        self.spreadsheet.insert(53, 91, "eamon")
        self.assertEqual(self.spreadsheet.lookup(53, 91), "eamon")
        self.spreadsheet.remove(53, 91)

    def test_lookup_valid(self):
        self.spreadsheet.insert(1, 1, 1)
        self.assertEqual(self.spreadsheet.lookup(1, 1), 1)
        self.assertEqual(self.spreadsheet.lookup(1, 1),
                         self.spreadsheet.lookup(1, 1))
        self.spreadsheet.remove(1, 1)

        self.spreadsheet.insert(999, 999, {})
        self.assertEqual(self.spreadsheet.lookup(999, 999), {})
        self.spreadsheet.remove(999, 999)

    def test_remove_valid(self):
        self.spreadsheet.insert(1, 1, 1)
        self.assertEqual(self.spreadsheet.lookup(1, 1), 1)
        self.spreadsheet.remove(1, 1)

        self.spreadsheet.insert(3131, 1313, [92, 5, 3])
        self.assertEqual(self.spreadsheet.lookup(3131, 1313), [92, 5, 3])
        self.spreadsheet.remove(3131, 1313)
        self.spreadsheet.remove(3131, 1313)

        self.spreadsheet.remove(123456789, 987654321)

    def test_query_valid(self):
        self.spreadsheet.insert(1, 1, 1)
        self.assertEqual(self.spreadsheet.query(1, 1, 1, 1), {(1, 1): 1})
        self.spreadsheet.remove(1, 1)

        self.spreadsheet.insert(5, 5, "string")
        self.assertEqual(self.spreadsheet.query(5, 4, 2, 1),
                         {(5, 5): "string"})
        self.spreadsheet.remove(5, 5)

        self.spreadsheet.insert(8, 7, {"nice": 1})
        self.spreadsheet.insert(7, 8, {"man": 2})
        self.assertEqual(self.spreadsheet.query(3, 3, 5, 6),
                         {(8, 7): {
                              "nice": 1
                          }})
        self.assertEqual(self.spreadsheet.query(3, 3, 6, 5),
                         {(7, 8): {
                              "man": 2
                          }})
        self.assertEqual(self.spreadsheet.query(3, 3, 6, 6), {
            (8, 7): {
                "nice": 1
            },
            (7, 8): {
                "man": 2
            }
        })
        self.spreadsheet.remove(8, 7)
        self.spreadsheet.remove(7, 8)

    def test_size_valid(self):
        self.spreadsheet.insert(1, 1, 1)
        self.assertEqual(self.spreadsheet.size(), (1, 1))
        self.spreadsheet.remove(1, 1)

        self.spreadsheet.insert(1, 5, 1)
        self.assertEqual(self.spreadsheet.size(), (1, 5))
        self.spreadsheet.insert(5, 1, 1)
        self.assertEqual(self.spreadsheet.size(), (5, 5))
        self.spreadsheet.remove(1, 5)
        self.assertEqual(self.spreadsheet.size(), (5, 1))
        self.spreadsheet.remove(5, 1)
        self.assertEqual(self.spreadsheet.size(), (0, 0))

    def test_insert_invalid(self):
        with self.assertRaises(ValueError):
            self.spreadsheet.insert(0, 5, 1)
        with self.assertRaises(ValueError):
            self.spreadsheet.insert(-1, 5, 1)

        with self.assertRaises(ValueError):
            self.spreadsheet.insert(5, 0, 1)
        with self.assertRaises(ValueError):
            self.spreadsheet.insert(5, -1, 1)

    def test_lookup_invalid(self):
        with self.assertRaises(ValueError):
            self.spreadsheet.lookup(0, 0)

        with self.assertRaises(ValueError):
            self.spreadsheet.lookup(-1, 1)

        with self.assertRaises(ValueError):
            self.spreadsheet.lookup(1, -1)

    def test_remove_invalid(self):
        with self.assertRaises(ValueError):
            self.spreadsheet.remove(0, 0)

        with self.assertRaises(ValueError):
            self.spreadsheet.remove(-1, 1)

        with self.assertRaises(ValueError):
            self.spreadsheet.remove(1, -1)

    def test_query_invalid(self):
        with self.assertRaises(ValueError):
            self.spreadsheet.query(0, 0, 1, 1)


def main(args: argparse.Namespace):
    SpreadSheetTests.NAME = args.name

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SpreadSheetTests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    args = parser.parse_args()
    main(args)
