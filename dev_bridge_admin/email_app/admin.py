from django.contrib import admin

from .models import Template, Attachment, EmailToSend


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("pk", "name",)
    list_display_links = ("pk", "name")
    search_fields = ("name",)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("pk", "name",)
    list_display_links = ("pk", "name")
    search_fields = ("name",)


@admin.register(EmailToSend)
class EmailToSendAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "is_high_priority",)
    list_display_links = ("pk", "author",)
    list_filter = ("author", "template",)
    list_editable = ("is_high_priority",)
