# Generated by Django 2.0.6 on 2018-09-10 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20180830_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='description',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
