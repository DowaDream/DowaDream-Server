# Generated by Django 4.2.3 on 2023-08-08 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_remove_user_age_remove_user_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="resol_msg",
            field=models.CharField(max_length=100, verbose_name="다짐메세지"),
        ),
    ]
