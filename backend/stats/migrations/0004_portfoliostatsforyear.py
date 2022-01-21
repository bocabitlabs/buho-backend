# Generated by Django 3.2.8 on 2022-01-19 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolios', '0002_alter_portfolio_options'),
        ('stats', '0003_companystatsforyear_dividends_yield'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioStatsForYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('invested', models.DecimalField(decimal_places=3, max_digits=12)),
                ('dividends', models.DecimalField(decimal_places=3, max_digits=12)),
                ('dividends_yield', models.DecimalField(decimal_places=3, max_digits=12, null=True)),
                ('portfolio_currency', models.CharField(max_length=200)),
                ('accumulated_investment', models.DecimalField(decimal_places=3, max_digits=12)),
                ('accumulated_dividends', models.DecimalField(decimal_places=3, max_digits=12)),
                ('portfolio_value', models.DecimalField(decimal_places=3, max_digits=12)),
                ('return_value', models.DecimalField(decimal_places=3, max_digits=12)),
                ('return_percent', models.DecimalField(decimal_places=3, max_digits=12)),
                ('return_with_dividends', models.DecimalField(decimal_places=3, max_digits=12)),
                ('return_with_dividends_percent', models.DecimalField(decimal_places=3, max_digits=12)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='portfolios.portfolio')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('year', 'portfolio')},
            },
        ),
    ]