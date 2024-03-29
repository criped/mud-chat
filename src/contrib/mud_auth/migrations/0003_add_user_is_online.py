# Generated by Django 3.2.6 on 2021-08-10 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mud_auth', '0002_add_location_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_online',
            field=models.BooleanField(default=False, help_text='Whether the user is online in the game', verbose_name='Is online'),
        ),
    ]
