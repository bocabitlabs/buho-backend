# Generated by Django 3.2.8 on 2022-03-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20220206_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='isin',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]