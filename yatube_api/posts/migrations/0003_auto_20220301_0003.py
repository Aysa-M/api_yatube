# Generated by Django 2.2.16 on 2022-02-28 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20220228_2333'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='post',
            name='unique_id_text_group',
        ),
    ]
