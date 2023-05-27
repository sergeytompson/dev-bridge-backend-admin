from django.contrib.auth.models import User
from django.db import models


class Template(models.Model):
    name = models.CharField("Название шаблона")
    template = models.FileField("HTML шаблон письма", upload_to="templates/", max_length=200)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Шаблон"
        verbose_name_plural = "Шаблоны"


class Attachment(models.Model):
    name = models.CharField("Название вложения")
    attachment = models.FileField("Вложение", upload_to="attachment/", max_length=200)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"


class EmailToSend(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Автор",
        related_name="emails"
    )
    recipients = models.ManyToManyField(
        User,
        verbose_name="Получатели",
        related_name="recipient_emails"
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Шаблон",
    )
    attachments = models.ManyToManyField(
        Attachment,
        verbose_name="Вложения"
    )
    confirm_url = models.URLField(
        "Ссылка для подтверждения",
        blank=True,
        null=True
    )
    is_high_priority = models.BooleanField(
        "Высокий приоритет",
        default=False
    )

    def __str__(self) -> str:
        return f"Письмо №{self.pk}"

    class Meta:
        verbose_name = "Письмо для отправки"
        verbose_name_plural = "Письма для отправки"
