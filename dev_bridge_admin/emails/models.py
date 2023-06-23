"""Модели приложения Emails"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from .validators import MimeTypeValidator

NAME_LIMIT = 20
CHAR_FIELD_MAX_LENGTH = 150
FILE_FIELD_MAX_LENGTH = 200


class Template(models.Model):
    """Модель шаблона письма"""

    name = models.CharField("название шаблона", max_length=CHAR_FIELD_MAX_LENGTH)
    template = models.FileField(
        "HTML шаблон письма",
        upload_to="emails/templates/",
        max_length=FILE_FIELD_MAX_LENGTH,
        validators=[MimeTypeValidator({"html": "text/html"})],
    )

    class Meta:
        verbose_name = "шаблон"
        verbose_name_plural = "шаблоны"
        ordering = ("name",)
        indexes = (models.Index(fields=("name",), name="template_name_idx"),)

    def __str__(self):
        return self.name[:NAME_LIMIT]


class Attachment(models.Model):
    """Модель вложения к письму"""

    name = models.CharField("название вложения", max_length=CHAR_FIELD_MAX_LENGTH)
    attachment = models.FileField(
        "вложение", upload_to="emails/attachment/", max_length=FILE_FIELD_MAX_LENGTH
    )
    is_template = models.BooleanField("является шаблоном", default=False)

    class Meta:
        verbose_name = "вложение"
        verbose_name_plural = "вложения"
        ordering = ("name",)
        indexes = (models.Index(fields=("name",), name="attachment_name_idx"),)

    def __str__(self):
        return self.name[:NAME_LIMIT]


class AbstractEmail(models.Model):
    """Базовая модель письма"""

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="автор",
        related_name="%(class)s_set",
        null=True,
        blank=True,
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.PROTECT,
        verbose_name="шаблон",
        related_name="%(class)s_set",
    )
    attachments = models.ManyToManyField(
        Attachment,
        verbose_name="вложения",
        related_name="%(class)s_set",
        blank=True,
    )
    confirm_url = models.URLField(
        "ссылка для подтверждения",
        blank=True,
    )
    is_high_priority = models.BooleanField(
        "высокий приоритет",
        default=False,
    )
    is_email_to_confirm = models.BooleanField(
        "письмо для подтверждения почты",
        default=False,
    )
    is_email_to_anonym = models.BooleanField(
        "письмо анонимным пользователям",
        default=False,
    )

    class Meta:
        abstract = True


class EmailToSend(AbstractEmail):
    """Модель письма, подготовленного для отправки"""

    recipients = models.ManyToManyField(
        User,
        verbose_name="получатели",
        related_name="recipient_emails_to_send",
        blank=True,
    )
    created = models.DateTimeField(
        "создано",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "письмо для отправки"
        verbose_name_plural = "письма для отправки"
        ordering = ("is_high_priority",)
        constraints = (
            models.CheckConstraint(
                check=Q(
                    confirm_url__exact=""
                ) & Q(
                    is_email_to_confirm__exact=False
                ) | Q(
                    confirm_url__regex=r'.+'
                ) & Q(
                    is_email_to_confirm__exact=True
                ),
                name="url_for_email_to_confirm",
                violation_error_message="Письма для подтверждения почты должны включать ссылку, "
                                        "остальные письма - не должны.",
            ),
            models.CheckConstraint(
                check=Q(
                    author__isnull=True
                ) & (
                    Q(
                        is_email_to_confirm__exact=True
                    ) | Q(
                        is_email_to_anonym=True
                    )
                ) | Q(
                    author__isnull=False
                ) & (
                    Q(
                        is_email_to_confirm__exact=False
                    ) & Q(
                        is_email_to_anonym=False
                    )
                ),
                name="empty_author_for_email_to_confirm_and_to_anonym",
                violation_error_message="В письмах с подтверждением почты и в письмах для анонимных "
                                        "юзеров автор указывться не должен, в остальных письмах его "
                                        "указывать обязательно.",
            ),
            models.CheckConstraint(
                check=Q(
                    is_email_to_anonym__exact=True
                ) & Q(
                    is_email_to_confirm__exact=False
                ) | Q(
                    is_email_to_anonym__exact=False
                ) & Q(
                    is_email_to_confirm__exact=True
                ) | Q(
                    is_email_to_anonym__exact=False
                ) & Q(
                    is_email_to_confirm__exact=False
                ),
                name="email_to_confirm_and_to_anonym_cant_be_true_together",
                violation_error_message="Письмо для анонимных юзеров не может быть письмом для подтвеждения "
                                        "почты (и наоборот).",
            ),
        )

    def __str__(self):
        return f"Письмо №{self.pk}"


class SentEmail(AbstractEmail):
    """Модель отправленного письма"""

    created = models.DateTimeField("создано")
    sent = models.DateTimeField("отправлено", auto_now_add=True)
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="получатель",
        related_name="recipient_sent_emails",
        null=True,
    )

    class Meta:
        verbose_name = "отправленное письмо"
        verbose_name_plural = "отправленные письма"


class NotSentEmail(AbstractEmail):
    """Модель не отправленного письма"""

    created = models.DateTimeField("создано")
    sending_attempt = models.DateTimeField("отправлено", auto_now_add=True)
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="получатель",
        related_name="recipient_not_sent_emails",
        null=True,
    )

    class Meta:
        verbose_name = "неотправленное письмо"
        verbose_name_plural = "неотправленные письма"
