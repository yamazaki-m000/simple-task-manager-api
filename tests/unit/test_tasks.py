from . import tasks_db


def test_setup():
    tasks_table = tasks_db.create_table()
    print(tasks_table.item_count)


def test_clean_db_data():
    tasks_db.delete_table()
    tasks_table = tasks_db.create_table()
    print(tasks_table.item_count)
