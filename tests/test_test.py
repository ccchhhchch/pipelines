from pipelines.tasks import *
import os
import sqlite3
import pytest
connection_string = 'database.db'
table = 'data_table'
file = 'tests/test_table.csv'
file_output = 'tests/output'
def test_task_load():
    task = LoadFile(table, file)
    task.run()
    cursor = sqlite3.connect(connection_string).cursor()
    cursor.execute("SELECT COUNT(*) from " + table)
    n = cursor.fetchone()[0]
    assert n == 2
    cursor.close()
    clean()
def test_task_export():
    LoadFile(table, file).run()
    CopyToFile(table, file_output).run()
    if os.path.isfile(file_output + '.csv'):
        check_file = open(file_output + '.csv', 'r')
        reader = csv.reader(check_file)
        n = len(list(reader)) - 1
        assert n == 2
        check_file.close()
        clean()
    else:
        pytest.fail("File was not created")
def clean():
    RunSQL('drop table ' + table, connection_string).run()
    if os.path.isfile(file_output + '.csv'):
        os.remove(file_output + '.csv')
        os.remove(connection_string)