# Generated by Django 3.1.5 on 2021-02-27 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_ticker', models.CharField(max_length=6, unique=True, verbose_name='Идентификатор')),
                ('currency_rus', models.CharField(max_length=150, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
                'ordering': ['currency_ticker'],
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_title', models.CharField(max_length=100, verbose_name='Индустрия')),
                ('industry_rus', models.CharField(blank=True, max_length=100, null=True, verbose_name='Индустрия ru')),
            ],
            options={
                'verbose_name': 'Индустрия',
                'verbose_name_plural': 'Индустрии',
                'ordering': ['industry_title'],
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector_title', models.CharField(max_length=50, unique=True, verbose_name='Сектор')),
                ('sector_rus', models.CharField(default='', max_length=50, verbose_name='Сектор ru')),
            ],
            options={
                'verbose_name': 'Сектор',
                'verbose_name_plural': 'Сектора',
                'ordering': ['sector_title'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Индентификатор')),
                ('ticker_yf', models.CharField(db_index=True, max_length=50, null=True, unique=True, verbose_name='Индентификатор для Yahoo Finance')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название')),
                ('logo', models.ImageField(blank=True, default=None, null=True, upload_to='documents/logos', verbose_name='Логотип')),
                ('decimal_places', models.IntegerField(default=2, verbose_name='Десятичные знаки')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='stock.currency', verbose_name='Валюта')),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='stock.industry', verbose_name='Индустрия')),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='stock.sector', verbose_name='Сектор')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
                'ordering': ['ticker'],
            },
        ),
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, verbose_name='Дата')),
                ('open', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Цена открытия')),
                ('high', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Максимальная цена')),
                ('low', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Минимальная цена')),
                ('close', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Цена закрытия')),
                ('volume', models.IntegerField(verbose_name='Объём торгов')),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.stock', verbose_name='Индентификатор')),
            ],
            options={
                'verbose_name': 'Котировка',
                'verbose_name_plural': 'Котировки',
                'ordering': ['-date', 'ticker'],
            },
        ),
        migrations.AddField(
            model_name='industry',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.sector'),
        ),
        migrations.CreateModel(
            name='Dividend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('dividend_per_share', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Дивиденд на акцию')),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.stock', verbose_name='Акция')),
            ],
            options={
                'verbose_name': 'Дивиденд',
                'verbose_name_plural': 'Дивиденды',
                'ordering': ['-date', 'stock_id'],
            },
        ),
        migrations.CreateModel(
            name='CurrencyCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, verbose_name='Дата')),
                ('open', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Цена открытия')),
                ('high', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Максимальная цена')),
                ('low', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Минимальная цена')),
                ('close', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Цена закрытия')),
                ('currency1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_currency', to='stock.currency', verbose_name='Валюта 1')),
                ('currency2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_currency', to='stock.currency', verbose_name='Валюта 2')),
            ],
            options={
                'verbose_name': 'Курс валют',
                'verbose_name_plural': 'Курсы валют',
                'ordering': ['-date', 'currency1', 'currency2'],
            },
        ),
    ]
