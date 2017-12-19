from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

class QuestionManager(models.Manager):
    def all_new(self):
        return self.order_by('-date_pub').all()

    def all_rate(self):
        return self.order_by('-rating').all()

    def all_questions_by_tag(self, tag_name):
        return self.filter(tags__name = tag_name).all()

class AnswerManager(models.Manager):
    def all_answers_by_question(self, question_id):
        return self.filter(question__pk = question_id).all()

class TagManager(models.Manager):
    def get_popular_tags(self):
        return self.all()[:5]

# Create your models here.


class UserImaged(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', default='uploads/avatar.jpg')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Имя категории')
    objects = TagManager()

    def __str__(self):
        return self.name

class Question(models.Model):
    short = models.CharField(max_length=80, verbose_name='Короткий вопрос')
    text = models.TextField(verbose_name='Полный вопрос')
    date_pub = models.DateTimeField(default=datetime.now, verbose_name='Дата публикации')
    author = models.ForeignKey(UserImaged, related_name='qauthor', verbose_name='Автор вопроса')
    tags = models.ManyToManyField(Tag, related_name='qtags', verbose_name='Связанные тэги')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    manager = QuestionManager()

    def __str__(self):
        return self.author.__str__() + " asks " + self.short

class LikeToQuestion(models.Model):
    who = models.ForeignKey(UserImaged, related_name='who_q_likes', verbose_name='Кто лайкнул')
    id_q = models.ForeignKey(Question, related_name='what_q_likes', verbose_name='ID вопроса')
    value = models.IntegerField(default=1, verbose_name='Value')

    def __str__(self):
        ans = str(self.who)
        ans += " likes " + str(self.whom)
        return ans

class Answer(models.Model):
    text = models.TextField(verbose_name='Текст ответа')
    author = models.ForeignKey(UserImaged, related_name='aauthor', verbose_name='Автор ответа')
    date_pub = models.DateTimeField(default=datetime.now, verbose_name='Дата публикации')
    question = models.ForeignKey(Question, related_name='aquestion', verbose_name='Вопрос')
    correct = models.BooleanField(default=False, verbose_name='Верно?')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    manager = AnswerManager()

    def __str__(self):
        return self.author.__str__() + " answers " + self.text


class LikeToAnswer(models.Model):
    who = models.ForeignKey(UserImaged, related_name='who_a_likes', verbose_name='Кто лайкнул')
    id_a = models.ForeignKey(Answer, related_name='what_a_likes', verbose_name='ID ответа')
    value = models.IntegerField(default=1, verbose_name='Value')

    def __str__(self):
        ans = str(self.who)
        ans += " likes " + str(self.whom)
        return ans