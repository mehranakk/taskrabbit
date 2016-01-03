from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    title = models.CharField(max_length=50)
    commend = models.PositiveIntegerField(verbose_name="recommendations")
    def __unicode__(self):
        return self.text


class MyUser(models.Model):
    user = models.OneToOneField(User)
    display_name = models.CharField(max_length=50)
    skills = models.ManyToManyField(Skill, blank=True)
    def __unicode__(self):
        return self.display_name



class Category(models.Model):
    name = models.CharField(verbose_name="name", max_length=250, blank=True, default="")
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    def __unicode__(self):
        return self.name


class Task(models.Model):
    employee = models.ForeignKey(MyUser, null=True, blank=True, related_name='task_employee')
    employer = models.ForeignKey(MyUser, related_name='task_employer')
    title = models.CharField(max_length=50)
    text = models.TextField(verbose_name="Text", default="")
    upload_date = models.DateTimeField("Upload Date")
    category = models.ForeignKey(Category)
    STATUS_STATE_CHOICES = (
        ('N', 'New'),
        ('A', 'Assigned'),
        ('D', 'Done'),
    )

    status = models.CharField(verbose_name="status", max_length=1,
                                             choices=STATUS_STATE_CHOICES, default='N')
    def __unicode__(self):
        return self.title


class TaskRequest(models.Model):
    employee = models.ForeignKey(MyUser)
    task = models.ForeignKey(Task)
    def __unicode__(self):
        return self.employee.display_name

class Comment(models.Model):
    employer = models.ForeignKey(MyUser, verbose_name="employer", related_name='comment_employer')
    employee = models.ForeignKey(MyUser, verbose_name="employee", related_name='comment_employee')
    rate = models.PositiveIntegerField(verbose_name="rate")
    text = models.CharField(verbose_name="text", max_length=300, blank=True, null=True)
    def __unicode__(self):
        return self.text
