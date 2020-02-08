import boto3
from copy import copy

dynamodb = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
tasks_table = dynamodb.Table("tasks")


def get_tasks_list(name, date):
    """
    指定された日付のタスクリストを取得する

    :param name: ユーザー名
    :param date: 日付
    :return:
    """
    print("start: get_tasks_list")
    response = tasks_table.get_item(
        Key={
            "name": name,
            "date": date
        }
    )
    print(response)

    if "Item" in response:
        return response["Item"]["tasks_list"]
    else:
        return []


def add_task(name, date, new_task, current_tasks_list=None):
    if current_tasks_list is None:
        current_tasks_list = []

    print("start: add_task")

    new_tasks_list = copy(current_tasks_list)
    new_tasks_list.append(new_task)

    tasks_table.update_item(
        Key={
            "name": name,
            "date": date
        },
        UpdateExpression="SET tasks_list = :val1",
        ExpressionAttributeValues={
            ":val1": new_tasks_list
        }
    )


def create_new_item(name, date, task):
    print("start: create_new_item")

    tasks_table.put_item(
        Item={
            "name": name,
            "date": date,
            "tasks_list": [task]
        }
    )


def update_task(name, date, task):
    print("start: update_task")

    def convert_tasks(current_task):
        if current_task.id == task.id:
            return task
        return current_task

    current_tasks_list = tasks_table.get_tasks_list(name, date)
    new_tasks_list = map(lambda current_task: convert_tasks(current_task), current_tasks_list)

    tasks_table.update_item(
        Key={
            "name": name,
            "date": date
        },
        UpdateExpression="SET tasks_list = :val1",
        ExpressionAttributeValues={
            ":val1": new_tasks_list
        }
    )


def delete_task(name, date, task_id):
    print("start: delete_task")
    current_tasks_list = tasks_table.get_tasks_list(name, date)
    new_tasks_list = filter(lambda task: task["id"] != task_id, current_tasks_list)

    tasks_table.update_item(
        Key={
            "name": name,
            "date": date
        },
        UpdateExpression="SET tasks_list = :val1",
        ExpressionAttributeValues={
            ":val1": new_tasks_list
        }
    )
