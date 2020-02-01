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


def create_task(name, date, task_name, task_detail):
    tasks_list = get_tasks_list(name, date)
    if tasks_list:
        task = tasks_list[-1]
        new_tasks_list = tasks_list.append({
            'id': task.id
        })
