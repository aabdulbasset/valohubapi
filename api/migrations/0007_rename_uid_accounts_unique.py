# Generated by Django 3.2.9 on 2021-12-02 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20211202_2318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accounts',
            old_name='uid',
            new_name='unique',
        ),
    ]
