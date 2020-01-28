import json
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
tasks_table = dynamodb.Table('tasks')


def get_tasks(event, context):
    name = event['name']
    date = event['date']
    response = tasks_table.get_item(
        Key={
            'name': name,
            'date': date
        }
    )
    return response['Item']


def create_task(event, context):
    tasks_table.put_item(
        Item={
            'name': 'yamazaki',
            'date': 20200130,
            'tasks_list': [
                {
                    'task_name': 'taskname',
                    'task_detail': 'taskdetail',
                    'status': 0,
                    'priority': 1
                }
            ]
        }
    )
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
