from django.contrib import admin

from .. import models


@admin.register(models.Quiz.DjangoModel)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Answer.DjangoModel)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Info.DjangoModel)
class UserAdmin(admin.ModelAdmin):
    pass