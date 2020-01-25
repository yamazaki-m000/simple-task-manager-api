import json

# import requests


def get_tasks(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "taskList": [
                {
                  "id": 1,
                  "taskName": "aa",
                  "taskDetail": "bbb",
                  "status": 0,
                  "priority": 2,
                },
                {
                  "id": 2,
                  "taskName": "cc",
                  "taskDetail": "",
                  "status": 0,
                  "priority": 3,
                },
                {
                  "id": 3,
                  "taskName": "ddd",
                  "taskDetail": "eee",
                  "status": 0,
                  "priority": 1,
                }
              ]
        }),
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
