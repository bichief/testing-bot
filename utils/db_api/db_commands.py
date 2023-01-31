from asgiref.sync import sync_to_async

from admin_panel.telebot.models import Groups, Students, Tests


@sync_to_async()
def create_group(group):
    Groups.objects.get_or_create(group_name=group)


@sync_to_async()
def get_all_groups():
    return Groups.objects.values_list('group_name', flat=True)


@sync_to_async()
def create_student(telegram_id, username, group):
    group = Groups.objects.filter(group_name=group).first()
    Students.objects.get_or_create(telegram_id=telegram_id, username=username, group=group)


@sync_to_async()
def update_student_name(telegram_id, name):
    Students.objects.filter(telegram_id=telegram_id).update(name=name)


@sync_to_async()
def update_tests_group(telegram_id, group):
    Tests.objects.get_or_create(teacher_id=telegram_id, group=group)
