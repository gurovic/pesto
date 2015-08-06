import find_similar_problems
import sys

class ProblemsTree:
    def __init__(self, problems):
        self.problems = list(problems)
        self.finder = find_similar_problems.SimilarProblemsFinder(self.problems)
        self.problem_previous = dict()
        for pair in self.finder.get_stat_data():
            if pair[1] not in self.problem_previous:
                self.problem_previous[pair[1]] = pair[0]
            else:
                old_similarity = self.finder.get_similarity(self.problem_previous[pair[1]], pair[1])
                new_similarity = self.finder.get_similarity(pair[0], pair[1])
                if new_similarity >= old_similarity:
                    self.problem_previous[pair[1]] = pair[0]

    def get_previous_problem(self, problem):
        if problem in self.problem_previous:
            return self.problem_previous[problem]
        else:
            return None

    def __str__(self):
        resulting_string = ''
        for problem in self.problems:
            resulting_string += str(problem) + ': '
            if problem not in self.problem_previous:
                resulting_string += 'it is a new problem. Tests: {tests}.\n'.format(tests=len(problem.cases))
            else:
                previous = self.problem_previous[problem]
                same_tests_count = self.finder.get_same_tests_count(previous, problem)
                added_tests_count = self.finder.get_added_tests_count(previous, problem)
                removed_tests_count = self.finder.get_removed_tests_count(previous, problem)
                if added_tests_count == 0 and removed_tests_count == 0:
                    resulting_string += 'it is {previous}. Tests: {tests}.\n'.\
                        format(previous=str(previous), tests=same_tests_count)
                else:
                    resulting_string += 'is based on {previous}. '.format(previous=str(previous))
                    resulting_string += 'Tests: +{added}, -{removed}, {same} not changed.\n'.\
                        format(added=added_tests_count, removed=removed_tests_count, same=same_tests_count)
        return resulting_string

