# Generated by Django 4.2.3 on 2023-08-16 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0009_remove_review_region_remove_review_tag"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="tag",
            field=models.CharField(blank=True, max_length=60, verbose_name="봉사 태그"),
        ),
    ]