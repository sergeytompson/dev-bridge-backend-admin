"""Админ-модели для сервера Admin"""

from django.contrib import admin

from .models import Attachment, EmailToSend, Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """Представление модели Template в админ-панели"""

    list_display = ("pk", "name")
    list_display_links = ("pk", "name")
    search_fields = ("name",)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """Представление модели Attachment в админ-панели"""

    list_display = ("pk", "name")
    list_display_links = ("pk", "name")
    search_fields = ("name",)


@admin.register(EmailToSend)
class EmailToSendAdmin(admin.ModelAdmin):
    """Представление модели EmailToSend в админ-панели"""

    list_display = ("pk", "author", "is_high_priority", "template")
    list_display_links = ("pk", "author")
    list_filter = ("author", "template")
    list_editable = ("is_high_priority",)
