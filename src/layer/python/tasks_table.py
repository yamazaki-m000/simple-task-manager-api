import boto3
from copy import copy

dynamodb = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
tasks_table = dynamodb.Table("tasks")


def get_tasks_list(name, date):
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


def create_task(name, date, new_task):
    print("start: create_task")

    current_tasks_list = tasks_table.get_tasks_list(name, date)
    print(current_tasks_list)

    # 新しいタスクに完了状態を追加
    new_task["done"] = False

    print(new_task)

    # 既にタスク一覧がある場合、新しいタスクを既存のタスク一覧に追加し、
    # DBに、そのタスク一覧で上書きをする
    if len(current_tasks_list) != 0:
        # 新しいタスクIDを選定し、新しいタスクにタスクIDを追加
        current_tasks_id_list = map(lambda current_task: current_task["id"], current_tasks_list)
        last_task_id = max(current_tasks_id_list)
        new_task["id"] = last_task_id + 1

        new_tasks_list = copy(current_tasks_list)
        new_tasks_list.append(new_task)

        tasks_table.update_item(
            Key={
                "name": name,
                "date": date
            },
            UpdateExpression="SET tasks_list = :val",
            ExpressionAttributeValues={
                ":val": new_tasks_list
            }
        )

    # 初回タスク作成の場合、DBに新しくITEMを追加する
    else:
        # 新しいタスクにタスクIDを追加
        new_task["id"] = 1

        tasks_table.put_item(
            Item={
                "name": name,
                "date": date,
                "tasks_list": [new_task]
            }
        )


def update_task(name, date, task):
    print("start: update_task")

    def convert_task(current_task):
        """
        現在のタスク一覧から、更新対象のタスクを割り出し、
        更新するタスクデータに変更する
        """
        if current_task.id == task.id:
            return task
        return current_task

    current_tasks_list = tasks_table.get_tasks_list(name, date)
    new_tasks_list = map(lambda current_task: convert_task(current_task), current_tasks_list)

    tasks_table.update_item(
        Key={
            "name": name,
            "date": date
        },
        UpdateExpression="SET tasks_list = :new_tasks_list",
        ExpressionAttributeValues={
            ":new_tasks_list": new_tasks_list
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
        UpdateExpression="SET tasks_list = :new_tasks_list",
        ExpressionAttributeValues={
            ":new_tasks_list": new_tasks_list
        }
    )
