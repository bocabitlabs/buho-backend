# Generated by Django 3.2.8 on 2022-01-19 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shares_transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sharestransaction',
            options={'ordering': ['-transaction_date']},
        ),
    ]