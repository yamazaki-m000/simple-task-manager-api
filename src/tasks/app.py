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
    """
    taskを作成する

    その日、初のtask作成の場合、itemごとDBにputする
    :param event:
    :param context:
    :return:
    """
    tasks_table.put_item(
        Item={
            'name': 'yamazaki',
            'date': 20200130,
            'tasks_list': [
                {
                    'task_id': 1,
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
    tasks_table.update_item(
        Key={
            'uname': event.name,
            'date': event.date
        },
        UpdateExpression='SET tasks_list = :val1',
        ExpressionAttributeValues={
            ':val1': [
                event.update_task
            ]
        }
    )
    return {
        "statusCode": 200,
        "body": {}
    }


def delete_task(event, context):

    return {
        "statusCode": 200,
        "body": {}
    }
