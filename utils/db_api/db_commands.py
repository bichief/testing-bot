from asgiref.sync import sync_to_async

from admin_panel.telebot.models import Groups, Students, Tests, Lessons, Categories


@sync_to_async()
def create_group(group):
    Groups.objects.get_or_create(group_name=group)
    return Groups.objects.filter(group_name=group).first().pk


@sync_to_async()
def get_all_groups():
    return Groups.objects.values_list('group_name', flat=True)


@sync_to_async()
def get_all_groups_pk():
    return Groups.objects.values_list('pk', flat=True)


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


@sync_to_async()
def update_tests_lesson(telegram_id, lesson):
    Tests.objects.filter(teacher_id=telegram_id).update(lesson=lesson)


@sync_to_async()
def update_category(telegram_id, category):
    old_categories = Tests.objects.filter(teacher_id=telegram_id).first().categories

    if old_categories is None:
        old_categories = ''

    needed_category = old_categories + f' {category}'

    Tests.objects.filter(teacher_id=telegram_id).update(categories=needed_category)

    return Tests.objects.filter(teacher_id=telegram_id).first().lesson

@sync_to_async()
def get_categories_test(telegram_id):
    return Tests.objects.filter(teacher_id=telegram_id).first().categories

@sync_to_async()
def get_lessons():
    return Lessons.objects.values_list('lesson_name', flat=True)


@sync_to_async()
def get_categories(lesson):
    return Categories.objects.filter(lesson__lesson_name=lesson).values_list('category_name', flat=True)


@sync_to_async()
def delete_test_row(telegram_id):
    Tests.objects.filter(teacher_id=telegram_id).delete()


@sync_to_async()
def get_test_teacher_id(telegram_id):
    return Tests.objects.filter(teacher_id=telegram_id).first()