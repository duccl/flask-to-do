
TASK_ROOT = '/task'

URLS = {
    'add_task':f'{TASK_ROOT}/add',
    'update_task':f'{TASK_ROOT}/update',
    'delete_task':f'{TASK_ROOT}/delete',
    'list_task':f'{TASK_ROOT}/list',
    'get_task':f'{TASK_ROOT}/<string:uuid>'
}