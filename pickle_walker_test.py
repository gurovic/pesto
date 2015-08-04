import unittest
from unittest.mock import Mock
from pickle_submits import PickleWriter
from shutil import rmtree
from os import mkdir, listdir
from os.path import exists, join
from model import Submit
from pickle_walker import pickle_walker



class Tester(unittest.TestCase):
    def setUp(self):
        self.pickle_submit = PickleWriter()
        self.pickle_submit.default_path = join(".", "testdata", "pickle_walker")

    def tearDown(self):
        if exists(self.pickle_submit.default_path):
            rmtree(self.pickle_submit.default_path)


    def test_mk_many_pickles(self):
        submit = Submit('0', '0', '179', '0', [], '1', "ACM")
        submit.problem_id = ("17", "0")
        for i in range(103):
            self.pickle_submit.visit(submit)
        self.pickle_submit.write_file()
        for parsed_submit in pickle_walker(self.pickle_submit.default_path):
            self.assertEqual(str(submit), str(parsed_submit))

    def test_empty_dir(self):
        parsed_submits = [parsed_submit for parsed_submit in pickle_walker(self.pickle_submit.default_path)]
        self.assertEqual(len(parsed_submits), 0)

    def test_many_contests(self):
        for i in range(101):
            self.pickle_submit.visit(Submit(str(i), ('17', '0'), '179', '0', [], '1', "ACM"))
        for i in range(103):
            self.pickle_submit.visit(Submit(str(i + 101), ('18', '0'), '179', '0', [], '1', "ACM"))
        for i in range(2):
            self.pickle_submit.visit(Submit(str(i + 204), ('19', '0'), '179', '0', [], '1', "ACM"))
        self.pickle_submit.write_file()

        parsed_submits = [parsed_submit for parsed_submit in pickle_walker(self.pickle_submit.default_path)]
        self.assertEqual(len(parsed_submits), 206)
        check_set = set()
        for submit in parsed_submits:
            check_set.add(submit.problem_id[0])
        self.assertEqual(check_set, set(["17", "18", "19"]))


if __name__ == "__main__":
    unittest.main()