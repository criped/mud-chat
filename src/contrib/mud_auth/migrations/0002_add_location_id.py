# Generated by Django 3.2.6 on 2021-08-08 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mud_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location_id',
            field=models.IntegerField(blank=True, help_text='Current location of the user if it is online in the game. Otherwise, location where it was last time it logged out.', null=True, verbose_name='Location ID'),
        ),
    ]
