from ejudge_contest_xml import ejudge_get_contest_name
from walker import AllFilesWalker
import os


def fill_db_from_contest_xml(contest_xmls_dir, cursor, origin):
    files_walker = AllFilesWalker()
    for extension, filename in files_walker.walk(contest_xmls_dir):
        contest_id = os.path.basename(filename)[:6]
        if contest_id.isdigit():
            contest_name = ejudge_get_contest_name(filename)
        else:
            continue
        print('Filling contest name for contest #{}'.format(contest_id))
        cursor.execute('UPDATE Contests SET name = ? WHERE origin = ? AND contest_id = ?',
                       (contest_name, origin, contest_id.rjust(6, '0')))
