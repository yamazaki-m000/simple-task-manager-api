import json


def get_tasks(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "taskList": [
                {
                  "id": 1,
                  "taskName": "メールを確認する",
                  "taskDetail": "〇〇さんからメールが来てるか確認する",
                  "status": 0,
                  "priority": 2,
                },
                {
                  "id": 2,
                  "taskName": "タバコを吸う",
                  "taskDetail": "",
                  "status": 0,
                  "priority": 3,
                },
                {
                  "id": 3,
                  "taskName": "会議の資料を作成する",
                  "taskDetail": "3/1の入沢会議に使う資料を作成する",
                  "status": 0,
                  "priority": 1,
                }
              ]
        }, ensure_ascii=False),
    }


def create_task(event, context):
    return {
        "statusCode": 200,
        "body": {}
    }


def update_task(event, context):
    return {
        "statusCode": 200,
        "body": {}
    }


def delete_task(event, context):
    return {
        "statusCode": 200,
        "body": {}
    }
