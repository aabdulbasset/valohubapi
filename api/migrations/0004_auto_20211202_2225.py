# Generated by Django 3.2.9 on 2021-12-02 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20211202_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='userName',
            field=models.CharField(default='nothin', max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accounts',
            name='entToken',
            field=models.CharField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='riotAuth',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
