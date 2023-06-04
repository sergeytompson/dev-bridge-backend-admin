# Generated by Django 4.2.1 on 2023-06-04 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=150, verbose_name="название вложения"),
                ),
                (
                    "attachment",
                    models.FileField(
                        max_length=200,
                        upload_to="emails/attachment/",
                        verbose_name="вложение",
                    ),
                ),
            ],
            options={
                "verbose_name": "вложение",
                "verbose_name_plural": "вложения",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Template",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=150, verbose_name="название шаблона"),
                ),
                (
                    "template",
                    models.FileField(
                        max_length=200,
                        upload_to="emails/templates/",
                        verbose_name="HTML шаблон письма",
                    ),
                ),
            ],
            options={
                "verbose_name": "шаблон",
                "verbose_name_plural": "шаблоны",
                "ordering": ("name",),
                "indexes": [models.Index(fields=["name"], name="template_name_idx")],
            },
        ),
        migrations.CreateModel(
            name="EmailToSend",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "confirm_url",
                    models.URLField(
                        blank=True, verbose_name="ссылка для подтверждения"
                    ),
                ),
                (
                    "is_high_priority",
                    models.BooleanField(
                        default=False, verbose_name="высокий приоритет"
                    ),
                ),
                (
                    "attachments",
                    models.ManyToManyField(
                        related_name="emails_to_send",
                        to="emails.attachment",
                        verbose_name="вложения",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="email_to_send",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="автор",
                    ),
                ),
                (
                    "recipients",
                    models.ManyToManyField(
                        related_name="recipient_emails_to_send",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="получатели",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="emails_to_send",
                        to="emails.template",
                        verbose_name="шаблон",
                    ),
                ),
            ],
            options={
                "verbose_name": "письмо для отправки",
                "verbose_name_plural": "письма для отправки",
                "ordering": ("is_high_priority",),
            },
        ),
        migrations.AddIndex(
            model_name="attachment",
            index=models.Index(fields=["name"], name="attachment_name_idx"),
        ),
    ]
