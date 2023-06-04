"""Модели сервера Admin"""

from django.contrib.auth.models import User
from django.db import models

NAME_LIMIT = 20
CHAR_FIELD_MAX_LENGTH = 150
FILE_FIELD_MAX_LENGTH = 200


class Template(models.Model):
    """Модель шаблона письма"""

    name = models.CharField("название шаблона", max_length=CHAR_FIELD_MAX_LENGTH)
    template = models.FileField(
        "HTML шаблон письма", upload_to="emails/templates/", max_length=FILE_FIELD_MAX_LENGTH
    )

    class Meta:
        verbose_name = "шаблон"
        verbose_name_plural = "шаблоны"
        ordering = ("name",)

    def __str__(self):
        return self.name[:NAME_LIMIT]


class Attachment(models.Model):
    """Модель вложения к письму"""

    name = models.CharField("название вложения", max_length=CHAR_FIELD_MAX_LENGTH)
    attachment = models.FileField(
        "вложение", upload_to="emails/attachment/", max_length=FILE_FIELD_MAX_LENGTH
    )

    class Meta:
        verbose_name = "вложение"
        verbose_name_plural = "вложения"
        ordering = ("name",)

    def __str__(self):
        return self.name[:NAME_LIMIT]


class EmailToSend(models.Model):
    """Модель письма, подготовленного для отправки"""

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="автор",
        related_name="email_to_send",
    )
    recipients = models.ManyToManyField(
        User,
        verbose_name="получатели",
        related_name="recipient_emails_to_send",
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.PROTECT,
        verbose_name="шаблон",
        related_name="emails_to_send"
    )
    attachments = models.ManyToManyField(
        Attachment,
        verbose_name="вложения",
        related_name="emails_to_send"
    )
    confirm_url = models.URLField(
        "ссылка для подтверждения",
        blank=True,
    )
    is_high_priority = models.BooleanField(
        "высокий приоритет",
        default=False,
    )

    class Meta:
        verbose_name = "письмо для отправки"
        verbose_name_plural = "письма для отправки"
        ordering = ("is_high_priority",)

    def __str__(self):
        return f"Письмо №{self.pk}"
