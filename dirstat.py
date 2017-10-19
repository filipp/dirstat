#! /usr/bin/env python

import re
import os
import sys
import time
import sqlite3
from os.path import join, getsize, basename

DBPATH = 'dirstat.sqlite3'

if not os.path.exists(DBPATH):
    os.system('sqlite3 ' + DBPATH + ' < schema.sql')

DB = sqlite3.connect(DBPATH)
SKIPNAMES = re.compile(r'^\.')
EXTENSION = re.compile(r'.+\.(\w+)$')

def stats(sql):
    for r in DB.execute(sql):
        print(r)


def scandir(path, overwrite=True):
    if not os.path.exists(path):
        raise Exception('Invalid path: %s' % path)

    if not overwrite:
        DB.execute('SELECT id FROM imports WHERE path = ?', (path,))
        if DB.fetchone():
            raise Exception('Path %s already imported' % path)

    DB.execute('INSERT INTO imports(path) VALUES (?)', (path,))
    cursor = DB.execute('SELECT last_insert_rowid() FROM imports')
    import_id = cursor.fetchone()[0]

    total_size = 0
    total_count = 0
    sql = 'INSERT INTO paths(path, type, mtime, size, import_id) VALUES (?,?,?,?, ?)'

    start_time = time.time()

    for root, subdirs, files in os.walk(path):
        for f in files:
            t = 'DIR'
            fp = unicode(join(root, f), 'UTF-8')
            if SKIPNAMES.match(f):
                continue

            result = EXTENSION.match(f)

            if result and result.group(0):
                t = result.group(1).upper()
            
            s = os.lstat(fp)

            print 'Importing %s' % fp
            DB.execute(sql, (fp, t, s.st_mtime, s.st_size, import_id,))
            total_count += 1
            total_size += s.st_size

    # Convert to timestamps
    DB.execute("UPDATE paths SET mtime = datetime(mtime, 'unixepoch', 'localtime')")
    DB.execute("UPDATE imports SET endtime = datetime('now'), count = ?, size = ? WHERE id = ?",
              (import_id, total_count, total_size,))
    DB.commit()

    print '{0} items imported from {2} ({1} bytes)'.format(total_count, total_size, path)


if __name__ == '__main__':
    if sys.argv[1] == 'import':
        path = sys.argv[2]
        scandir(path)
    elif sys.argv[1] == 'stats':
        query = 'SELECT type, size FROM paths GROUP BY type'
        if len(sys.argv) == 3:
            query = sys.argv[2]
        stats(query)
    elif sys.argv[1] == 'clear':
        DB.execute('DELETE FROM paths')
        DB.commit()
    elif sys.argv[1] == 'shell':
        while True:
            cmd = raw_input()
            try:
                for r in DB.execute(cmd):
                    s = []
                    print(u', '.join(r))
            except sqlite3.OperationalError as e:
                print e
