# Generated by Django 4.2.3 on 2023-08-14 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0008_rename_category_review_tag_remove_review_actplace_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="review", name="region",),
        migrations.RemoveField(model_name="review", name="tag",),
    ]
