from django.contrib import admin

from admin_panel.telebot.models import Students, Groups, Lessons, Categories, Questions


class StudentsAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id',
        'username',
        'name',
        'group',
        'amount_correct_answers',
    )

    list_display_links = ('name',)
    search_fields = ('name', 'group')

    empty_value_display = '- пусто -'

    class Meta:
        verbose_name_plural = 'Студенты'


class GroupsAdmin(admin.ModelAdmin):
    list_display = (
        'group_name',

    )

    list_display_links = ('group_name',)
    search_fields = ('group_name',)

    empty_value_display = '- пусто -'

    class Meta:
        verbose_name_plural = 'Группы'


class LessonsAdmin(admin.ModelAdmin):
    list_display = (
        'lesson_name',
    )

    list_display_links = ('lesson_name',)
    search_fields = ('lesson_name',)

    empty_value_display = '- пусто -'

    class Meta:
        verbose_name_plural = 'Дисциплины'


class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'category_name',
        'lesson',
    )

    list_display_links = ('category_name', 'lesson',)

    search_fields = ('category_name', 'lesson',)

    empty_value_display = '- пусто -'

    class Meta:
        verbose_name_plural = 'Категории'


class QuestionsAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'pool_answers',
        'correct_answer',
        'category',
        'get_lesson',
    )

    def get_lesson(self, obj):
        return obj.category.lesson.lesson_name

    get_lesson.admin_order_field = 'Дисциплина'
    get_lesson.short_description = 'Дисциплина'

    list_display_links = (
        'question',
        'pool_answers',
        'correct_answer',
        'category',
        'get_lesson'
    )
    empty_value_display = '- пусто -'
    search_fields = ('category', 'question',)


admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Lessons, LessonsAdmin)
admin.site.register(Students, StudentsAdmin)
admin.site.register(Groups, GroupsAdmin)
