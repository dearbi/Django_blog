# Generated by Django 5.1.5 on 2025-01-19 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CaptchaModel",
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
                ("eamil", models.EmailField(max_length=254)),
                ("captcha", models.CharField(max_length=4)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
