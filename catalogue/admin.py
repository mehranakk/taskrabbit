from django.contrib import admin

from catalogue.models import *

admin.site.register(Task)
admin.site.register(MyUser)
admin.site.register(Comment)
admin.site.register(TaskRequest)
admin.site.register(Category)


