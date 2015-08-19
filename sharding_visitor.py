from visitor import Visitor


class ShardingVisitor(Visitor):
    def __init__(self, factory):
        super().__init__()
        self.visitors = dict()
        self.factory = factory

    def visit(self, submit):
        key = self.build_key(submit)
        if key not in self.visitors:
            self.visitors[key] = self.factory.create(key)
        self.visitors[key].visit(submit)

    def comparable_key(self, key):
        try:
            return int(key)
        except Exception:
            return key

    def get_stat_data(self):
        result = []
        for key_visitor in sorted(self.visitors.items(), key=lambda key:self.comparable_key(key[0])):
            result.append((key_visitor[0], key_visitor[1].get_stat_data()))
        return result

    def pretty_key(self, key):
        return str(key)

    def pretty_print(self):
        result = ''
        for key in sorted(self.visitors.keys(), key=self.comparable_key):
            child_result = self.visitors[key].pretty_print()
            if child_result in ['', None]:
                continue
            result += '\n' + self.pretty_key(key) + ':\n\t' + child_result.replace('\n', '\n\t')
        return result

    def build_key(self, submit):
        return str(submit)


class ShardingByProblemVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.problem_id

    def comparable_key(self, key):
        return int(key[1])

    def pretty_key(self, key):
        return 'Problem #{}'.format(key[1])


class ShardingByContestVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.problem_id[0]

    def pretty_key(self, key):
        return 'Contest #{}'.format(key)


class ShardingByUserVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.user_id

    def pretty_key(self, key):
        return 'UserID #{}'.format(key)


class ShardingByLangVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.lang_id

    def pretty_key(self, key):
        return 'LangID #{}'.format(key)


class ShardingByScoringVisitor(ShardingVisitor):
    def build_key(self, submit):
        return 'ACM' if submit.scoring == 'ACM' else 'kirov'

    def pretty_key(self, key):
        return 'Scoring type - #{}'.format(key)
