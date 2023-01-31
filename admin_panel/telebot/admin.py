from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from admin_panel.telebot.models import Students, Groups


class StudentsAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id',
        'username',
        'name',
        'group',
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


admin.site.register(Groups, GroupsAdmin)
admin.site.register(Students, StudentsAdmin)
