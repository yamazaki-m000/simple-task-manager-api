import tasks_table
import json
from datetime import datetime
from decimal import Decimal


def expire_encoding(object):
    if isinstance(object, datetime):
        return object.isoformat()
    elif isinstance(object, Decimal):
        return float(object)
    raise TypeError


def get_tasks(event, context):
    query_parameter = event["queryStringParameters"]
    print(query_parameter)

    name = query_parameter["name"]
    date = query_parameter["date"]

    tasks_list = tasks_table.get_tasks_list(name, date)

    body = {"name": name, "date": date, "tasks_list": tasks_list}

    return {
        "statusCode": 200,
        "body": json.dumps(body, default=expire_encoding, ensure_ascii=False)
    }


def create_task(event, context):
    """
    taskを作成する

    その日、初のtask作成の場合、itemごとDBにputする
    :param event:
    :param context:
    :return:
    """
    request_body = json.loads(event["body"])
    print(request_body)

    name = request_body["name"]
    date = int(request_body["date"])
    new_task = request_body["task"]

    current_tasks_list = tasks_table.get_tasks_list(name, date)
    print(current_tasks_list)

    if current_tasks_list is None:
        print("is None")
        tasks_table.add_task(name, date, new_task)
    elif len(current_tasks_list) != 0:
        print("len is 0")
        tasks_table.add_task(name, date, new_task, current_tasks_list)
    else:
        tasks_table.create_new_item(name, date, new_task)

    return {
        "statusCode": 200,
        "body": "{}"
    }


def update_task(event, context):
    """
    taskの内容を更新する

    下記のユーザー操作がされた際に、APIコールされる
    ・taskの名前や詳細等のtaskの情報の更新
    ・taskの完了
    ・taskの優先順を変更

    :param event:
        name: ユーザー名
        date: 日付
        task_id: 更新するtaskのid
    :param context:
    :return:
    """
    request_body = json.loads(event["body"])
    print(request_body)

    name = request_body["name"]
    date = int(request_body["date"])
    task = request_body["update_task"]

    tasks_table.update_item(
        Key={
            "name": name,
            "date": date
        },
        UpdateExpression="SET tasks_list = :val1",
        ExpressionAttributeValues={
            ":val1": [task]
        }
    )
    return {
        "statusCode": 200,
        "body": "{}"
    }


def delete_task(event, context):
    request_body = json.loads(event["body"])
    print(request_body)

    name = request_body["name"]
    date = request_body["date"]
    task_id = request_body["task_id"]

    tasks_list = tasks_table.get_tasks_list(name, date)
    deleted_tasks_list = filter(lambda task: task["id"] != task_id, tasks_list)
    tasks_table.update_tasks_list(name, date, deleted_tasks_list)

    return {
        "statusCode": 200,
        "body": "{}"
    }
