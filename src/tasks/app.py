import tasks_table
import json
from datetime import datetime
from decimal import Decimal


def get_tasks(event, context):
    """
    タスク一覧を取得する

    :param event:
        queryStringParameters(object):
            name(str): ユーザー名
            date(int): 対象日付
    :param context:
    :return:
    """
    print("start lambda_handler get_tasks")

    query_parameter = event["queryStringParameters"]
    print("query_parameter: " + query_parameter)

    name = query_parameter["name"]
    date = query_parameter["date"]

    tasks_list = tasks_table.get_tasks_list(name, date)

    body = {"name": name, "date": date, "tasks_list": tasks_list}
    print("response_body: " + body)

    print("end lambda_handler get_tasks")
    return {
        "statusCode": 200,
        "body": json.dumps(body, default=__expire_encoding, ensure_ascii=False)
    }


def create_task(event, context):
    """
    タスクを作成する

    :param event:
        body(str):
            name(str): ユーザー名
            date(int): 対象日付
            task(object): 作成するタスク
                name(str): タスク名
                detail(str): タスクの詳細
    :param context:
    :return:
    """
    print("start lambda_handler create_task")

    request_body = json.loads(event["body"], object_pairs_hook=evalfn)
    print(request_body)

    name = request_body["name"]
    date = int(request_body["date"])
    task = request_body["task"]

    tasks_table.create_task(name, date, task)

    print("end lambda_handler create_task")
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
        body(str):
            name(str): ユーザー名
            date(int): 対象日付
            task(object): 更新するタスク
                id(int): タスクID
                name(str): タスク名
                detail(str): タスクの詳細
                done(bool): 完了状態
            priority_than(int): [optional] 優先度1つ下のタスクID
    :param context:
    :return:
    """
    print("start lambda_handler update_task")

    request_body = json.loads(event["body"], object_pairs_hook=evalfn)
    print(request_body)

    name = request_body["name"]
    date = int(request_body["date"])
    task = request_body["task"]

    tasks_table.update_task(name, date, task)

    print("end lambda_handler update_task")
    return {
        "statusCode": 200,
        "body": "{}"
    }


def delete_task(event, context):
    """
    タスクを削除する

    :param event:
        body(str):
            name(str): ユーザー名
            date(int): 対象日付
            task_id(int): 更新するタスクのタスクID
    :param context:
    :return:
    """
    print("start lambda_handler delete_task")

    request_body = json.loads(event["body"], object_pairs_hook=evalfn)
    print(request_body)

    name = request_body["name"]
    date = int(request_body["date"])
    task_id = request_body["task_id"]

    tasks_table.delete_task(name, date, task_id)

    print("end lambda_handler delete_task")
    return {
        "statusCode": 200,
        "body": "{}"
    }


def __expire_encoding(target_object):
    if isinstance(target_object, datetime):
        return target_object.isoformat()
    elif isinstance(target_object, Decimal):
        return float(target_object)
    raise TypeError


def evalfn(pairs):
    res = {}
    for key, val in pairs:
        try:
            if val in {'true', 'false'}:
                res[key] = val == 'true'
                continue
            else:
                res[key] = val
        except Exception as e:
            res[key] = val
    return res
