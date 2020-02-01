import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb:8000')
tasks_table = dynamodb.Table('tasks')


def get_tasks_list(name, date):
    """
    指定された日付のタスクリストを取得する

    :param name: ユーザー名
    :param date: 日付
    :return:
    """
    response = tasks_table.get_item(
        Key={
            'name': name,
            'date': date
        }
    )
    print('response----------------')
    print(response)
    if 'Item' in response:
        return response['Item']['tasks_list']
    else:
        return []


def add_task(name, date, current_tasks_list, new_task):
    tasks_table.update_item(
        Key={
            'name': name,
            'date': date
        },
        UpdateExpression='SET tasks_list = :val1',
        ExpressionAttributeValues={
            ':val1': current_tasks_list.append(new_task)
        }
    )


def create_new_item(name, date, task):
    tasks_table.put_item(
        Item={
            'name': name,
            'date': date,
            'tasks_list': [task]
        }
    )


def update_tasks_list(name, date, tasks_list):
    tasks_table.update_item(
        Key={
            'name': name,
            'date': date
        },
        UpdateExpression='SET tasks_list = :val1',
        ExpressionAttributeValues={
            ':val1': tasks_list
        }
    )
