from memory_database import MemoryDatabase
from problem import Problem
import os.path
import unittest


class MemoryDatabaseInitTest(unittest.TestCase):
    def test_good(self):
        mem_db = MemoryDatabase(os.path.join('testdata', 'memory_database', 'good', '001'), os.path.join('testdata', 'memory_database', 'good', 'db.csv'))
        self.assertEqual(len(mem_db.submits), 8)
        self.assertEqual(len(mem_db.problems), 4)

    def test_bad_csv(self):
        with self.assertRaises(ValueError):
            mem_db = MemoryDatabase(os.path.join('testdata', 'memory_database', 'csv', '001'), os.path.join('testdata', 'memory_database', 'csv', 'db.csv'))

    def test_bad_xml(self):
        mem_db = MemoryDatabase(os.path.join('testdata', 'memory_database', 'xml', '001'), os.path.join('testdata', 'memory_database', 'xml', 'db.csv'))
        self.assertEqual(len(mem_db.submits), 7)
        self.assertEqual(len(mem_db.problems), 4)

    def test_bad_gz(self):  # Now it raises OSError, must skip wrong .gz.
        mem_db = MemoryDatabase(os.path.join('testdata', 'memory_database', 'gz', '001'), os.path.join('testdata', 'memory_database', 'gz', 'db.csv'))
        self.assertEqual(len(mem_db.submits), 7)
        self.assertEqual(len(mem_db.problems), 3)

    def test_empty_folders(self):
        mem_db = MemoryDatabase(os.path.join('testdata', 'memory_database', 'empty_folders', '001'), os.path.join('testdata', 'memory_database', 'empty_folders', 'db.csv'))
        self.assertEqual(len(mem_db.submits), 6)
        self.assertEqual(len(mem_db.problems), 3)

    def test_name_zeros(self):
        mem_db = MemoryDatabase(os.path.join('testdata', 'memory_database', 'name_zeros', '00name'), os.path.join('testdata', 'memory_database', 'name_zeros', 'db.csv'))
        self.assertEqual(len(mem_db.problems), 4)
        self.assertEqual(list(mem_db.problems)[0][0], '00name')

class MemoryDatabaseDataTest(unittest.TestCase):
    def setUp(self):
        self.mem_db = MemoryDatabase(os.path.join('testdata', 'memory_database', 'good', '001'), os.path.join('testdata', 'memory_database', 'good', 'db.csv'))

    def tearDown(self):
        del self.mem_db

    def test_problem_exists(self):
        self.assertTrue(self.mem_db.problem_exists('1', 2))
        self.assertTrue(self.mem_db.problem_exists('1', '2'))
        self.assertFalse(self.mem_db.problem_exists('1', 1337))
        self.assertFalse(self.mem_db.problem_exists(1337, 1))
        self.assertFalse(self.mem_db.problem_exists(None, None))

    def test_get_problem(self):
        with self.assertRaises(KeyError):
            self.mem_db.get_problem(None, None)
        problem = self.mem_db.get_problem('1', 2)
        self.assertEqual(problem.contest_id, '1')
        self.assertEqual(problem.problem_id, '2')
        self.assertEqual(len(problem.case_ids), 10)

    @unittest.expectedFailure
    def test_add_problem(self):
        p = Problem('1337', '256', ['179', '1'])
        self.mem_db.add_problem(1337, 256, p)
        self.assertEqual(self.mem_db.get_problem('1337', '256').contest_id, '1337')
        self.assertEqual(self.mem_db.get_problem('1337', '256').problem_id, '256')
        self.assertEqual(self.mem_db.get_problem('1337', '256').case_ids, ['179', '1'])
        with self.assertRaises(ValueError):
            self.mem_db.add_problem(None, 1337, None)