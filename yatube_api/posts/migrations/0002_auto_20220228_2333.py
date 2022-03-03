# Generated by Django 2.2.16 on 2022-02-28 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='post',
            constraint=models.UniqueConstraint(fields=('id', 'text', 'group'), name='unique_id_text_group'),
        ),
    ]