# Generated by Django 5.0.6 on 2024-05-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_board', '0003_post_date_change'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_change',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]