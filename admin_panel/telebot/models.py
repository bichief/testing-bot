from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CreatedModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    updated = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True
    )

    class Meta:
        abstract = True


class Groups(models.Model):
    group_name = models.CharField(
        verbose_name='Кодировка группы',
        help_text='Кодировка группы',
        max_length=500,
        null=True
    )

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Группу'
        verbose_name_plural = '2. Группы'


class Students(CreatedModel):
    telegram_id = models.BigIntegerField(
        verbose_name='Telegram ID студента',
        help_text='Telegram ID студента'
    )

    username = models.CharField(
        verbose_name='Username студента',
        help_text='Username студента',
        max_length=500,
        null=True
    )

    name = models.CharField(
        verbose_name='Имя студента',
        help_text='Имя студента',
        max_length=5000,
        null=True
    )

    group = models.ForeignKey(
        Groups,
        on_delete=models.CASCADE,
        related_name='student_group',
        blank=True,
        null=True,
        help_text='Группа',
        verbose_name='Группа'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Студента'
        verbose_name_plural = '1. Студенты'


class Lessons(models.Model):
    lesson_name = models.CharField(
        verbose_name='Название дисциплины',
        help_text='Название дисциплины',
        max_length=500000,
        null=True
    )

    def __str__(self):
        return self.lesson_name

    class Meta:
        verbose_name = 'Дисциплину'
        verbose_name_plural = '3. Дисциплины'


class Categories(models.Model):
    category_name = models.CharField(
        verbose_name='Категория вопросов',
        help_text='Категория вопросов',
        max_length=500000,
        null=True
    )

    lesson = models.ForeignKey(
        Lessons,
        on_delete=models.CASCADE,
        related_name='category_lesson',
        blank=True,
        null=True,
        help_text='Дисциплина',
        verbose_name='Дисциплина'
    )

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категорию вопросов'
        verbose_name_plural = '4. Категории вопросов'


class Questions(models.Model):
    question = models.CharField(
        verbose_name='Вопрос',
        help_text='Вопрос',
        max_length=500000,
        null=True
    )

    pool_answers = models.CharField(
        verbose_name='Варианты ответов',
        help_text='Варианты ответов',
        max_length=500000,
        null=True
    )

    correct_answer = models.CharField(
        verbose_name='Правильный ответ',
        help_text='Правильный ответ',
        max_length=500000,
        null=True
    )

    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='category_question',
        blank=True,
        null=True,
        help_text='Категория вопроса',
        verbose_name='Категория вопроса'
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = '5. Вопросы'


class Tests(models.Model):
    group = models.CharField(
        max_length=500,
        null=True
    )

    lesson = models.CharField(
        max_length=500,
        null=True
    )

    categories = models.CharField(
        max_length=1000,
        null=True
    )

    teacher_id = models.BigIntegerField(

    )
