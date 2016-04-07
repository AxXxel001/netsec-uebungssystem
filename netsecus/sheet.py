from __future__ import unicode_literals

import collections

Sheet = collections.namedtuple('Sheet', ['id', 'end', 'deleted'])

def get_by_id(database, sheet_id):
    """ Returns the sheet or None if no sheet present """
    database.cursor.execute("SELECT id, end, deleted FROM sheet WHERE id = ?", (sheet_id, ))
    row = database.cursor.fetchone()

    if row:
        return Sheet(*row)
    else:
        return None

def get_all(database):
    database.cursor.execute("SELECT id, end, deleted FROM sheet")
    rows = database.cursor.fetchall()

    for row in rows:
        result.append(Sheet(*row))

    return result

def create(database):
    database.cursor.execute("INSERT INTO sheet (end, deleted) VALUES (NULL, 0)")
    database.commit()

def delete(database, sheet_id):
    database.cursor.execute("""UPDATE sheet SET deleted = 1 WHERE id = ?""",
                               (sheet_id, ))
    database.database.commit()

def restore_sheet(database, sheet_id):
    database.cursor.execute("""UPDATE sheet SET deleted = 0 WHERE id = ?""",
                               (sheet_id, ))
    database.database.commit()

def edit_end(database, sheet_id, end):
    database.cursor.execute("""UPDATE sheet SET end=? WHERE id = ?""",
                               (end, sheet_id))
    database.database.commit()
