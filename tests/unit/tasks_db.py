import boto3

dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")


def create_table():
    # Create the DynamoDB table.
    tasks_table = dynamodb.create_table(
        TableName="tasks",
        KeySchema=[
            {
                "AttributeName": "name",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "date",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "name",
                "AttributeType": "S"
            },
            {
                "AttributeName": "date",
                "AttributeType": "N"
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )

    # Wait until the table exists.
    tasks_table.wait_until_exists()

    return tasks_table


def delete_table():
    tasks_table = dynamodb.Table("tasks")
    tasks_table.delete()
    tasks_table.wait_until_not_exists()
