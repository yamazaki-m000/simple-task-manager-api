import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
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
    return response['Item']['tasks_list']


# def create_task(name, date, task_name, task_detail):
#     get_tasks_list(name, date)
