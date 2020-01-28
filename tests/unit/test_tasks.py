from . import setup_dynamodb


def test_setup():
    table = setup_dynamodb.create_table()

    # Print out some data about the table.
    print(table.item_count)
