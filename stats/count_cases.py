from visitor import Visitor


class CasesCounter(Visitor):
    def __init__(self):
        super().__init__()
        self.result = {}
    
    def update_submit(self, submit):
        if str(submit.problem_id) not in self.result or len(submit.case_ids) > self.result[str(submit.problem_id)]:
            self.result[str(submit.problem_id)] = len(submit.case_ids)
    
    def get_stat_data(self):
        for k, v in sorted(self.result.items()):
            result += 'Problem #{}: {} cases.\n'.format(k, v)        
        return result

classname = 'CasesCounter'