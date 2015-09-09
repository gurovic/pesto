import dao
import logging

class Statistics:
    def __init__(self, connection, filters={}, extra={}):
        self.filters = filters
        self.extra = extra
        self.calc(self.get_input_data(connection))

    def calc(self, data):
        self.result = None

    def get_input_data(self, connection):
        return []

    def as_string(self):
        return str(self.result)

    def save_to_file(self, filename):
        res = self.as_string()
        if filename is None:
            print(res)
        else:
            with open(filename, 'w') as f:
                f.write(res)


class SubmitStatistics(Statistics):

    def _create_query(self):
        query = 'SELECT {}, Contests.contest_id, Problems.problem_id FROM Submits JOIN Problems ON Submits.problem_ref=Prolems.id JOIN Contests ON Prolems.contest_ref = CONTESTS.id'.format(dao.SubmitsDAO.columns)
        cond = []
        if 'scoring' in self.filters:
            cond.append(('Contests.scoring = ?', self.filters['scoring']))
        if 'contest' in self.filters:
            cond.append(('Contests.contest_id = ?', self.filters['contest']))
        if 'problem' in self.filters:
            cond.append(('Problems.problem_id = ?', self.filters['problem']))
        if cond:
            query += ' WHERE ' + ' AND '.join(i[0] for i in cond)
        return (query, [i[1] for i in cond])

    def get_input_data(self, connection):
        cursor = connection.get_cursor()
        query, vals = self._create_query()
        sdao = dao.SubmitsDAO(connection)
        for submit_row in cursor.execute(query, vals):
            yield sdao.deep_load(submit_row, tuple(submit_row[-2:]))


class ProblemStatistics(Statistics):

    def _create_query(self):
        query = 'SELECT {}, Contests.contest_id FROM Problems JOIN Contests ON Problems.contest_ref = Contests.id'.format(dao.ProblemsDAO.columns)
        cond = []
        if 'scoring' in self.filters:
            cond.append(('Contests.scoring = ?', self.filters['scoring']))
        if 'contest' in self.filters:
            cond.append(('Contests.contest_id = ?', self.filters['contest']))
        if 'problem' in self.filters:
            cond.append(('Problems.problem_id = ?', self.filters['problem']))
        if cond:
            query += ' WHERE ' + ' AND '.join(i[0] for i in cond)
        return (query, [i[1] for i in cond])

    def get_input_data(self, connection):
        cursor = connection.get_cursor()
        query, vals = self._create_query()
        pdao = dao.ProblemsDAO(connection)
        for row in cursor.execute(query, vals):
            prob = pdao.deep_load(row, row['contest_id'])
            logging.debug('Processing problem {} from contest {}'.format(prob.problem_id[1], prob.problem_id[0]))
            yield prob
