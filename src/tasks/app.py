import tasks_table


def get_tasks(event, context):
    print(event)
    print(event['queryStringParameters'])

    name = event['queryStringParameters']['name']
    date = event['queryStringParameters']['date']

    tasks_list = tasks_table.get_tasks_list(name, date)

    body = {'name': name, 'date': date, 'tasks_list': tasks_list}

    return {
        'statusCode': 200,
        'body': body
    }


def create_task(event, context):
    """
    taskを作成する

    その日、初のtask作成の場合、itemごとDBにputする
    :param event:
    :param context:
    :return:
    """
    request = event['body']
    name = request['name']
    date = request['date']
    task = request['task']

    tasks_list = tasks_table.get_tasks_list(name, date)

    if len(tasks_list) != 0:
        tasks_table.add_task
    else:
        tasks_table.create_new_item(name, date, task)

    return {
        'statusCode': 200,
        'body': {}
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
            'name': event.name,
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
        'statusCode': 200,
        'body': {}
    }


def delete_task(event, context):
    request = event['body']
    name = request['name']
    date = request['date']
    task_id = request['task_id']

    tasks_list = tasks_table.get_tasks_list(name, date)
    deleted_tasks_list = filter(lambda task: task['id'] != task_id, tasks_list)
    tasks_table.update_tasks_list(name, date, deleted_tasks_list)

    return {
        'statusCode': 200,
        'body': {}
    }
