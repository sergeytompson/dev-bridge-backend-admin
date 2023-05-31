from django.contrib.auth.models import User
from django.db import models


class Template(models.Model):
    """Модель шаблона письма"""

    name = models.CharField("название шаблона", max_length=150)
    template = models.FileField(
        "HTML шаблон письма", upload_to="emails/templates/", max_length=200
    )

    def __str__(self):
        return self.name[:20]

    class Meta:
        verbose_name = "шаблон"
        verbose_name_plural = "шаблоны"


class Attachment(models.Model):
    """Модель вложения к письму"""

    name = models.CharField("название вложения", max_length=150)
    attachment = models.FileField(
        "вложение", upload_to="emails/attachment/", max_length=200
    )

    def __str__(self):
        return self.name[:20]

    class Meta:
        verbose_name = "вложение"
        verbose_name_plural = "вложения"


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
    )
    attachments = models.ManyToManyField(
        Attachment,
        verbose_name="вложения",
    )
    confirm_url = models.URLField(
        "ссылка для подтверждения",
        blank=True,
    )
    is_high_priority = models.BooleanField(
        "высокий приоритет",
        default=False,
    )

    def __str__(self):
        return f"Письмо №{self.pk}"

    class Meta:
        verbose_name = "письмо для отправки"
        verbose_name_plural = "письма для отправки"
