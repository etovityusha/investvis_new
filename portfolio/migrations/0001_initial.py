# Generated by Django 3.1.5 on 2021-02-27 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker_title', models.CharField(db_index=True, max_length=150, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Брокер',
                'verbose_name_plural': 'Брокеры',
                'ordering': ['broker_title'],
            },
        ),
        migrations.CreateModel(
            name='Replenishment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('count', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Сумма пополнения')),
                ('source', models.CharField(choices=[('I', 'Импорт'), ('F', 'Форма')], default='I', max_length=1, verbose_name='Источник')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.currency', verbose_name='Валюта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пополнение',
                'verbose_name_plural': 'Пополнения',
                'ordering': ['user', 'count', '-date'],
            },
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('transaction_type', models.CharField(choices=[('B', 'Покупка'), ('S', 'Продажа')], max_length=1, verbose_name='Тип сделки')),
                ('price', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True, verbose_name='Цена')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('total_cost', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True, verbose_name='Общая стоимость')),
                ('source', models.CharField(choices=[('I', 'Импорт'), ('F', 'Форма')], default='I', max_length=1, verbose_name='Источник')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.currency', verbose_name='Валюта')),
                ('ticker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.stock', verbose_name='Идентификатор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сделка',
                'verbose_name_plural': 'Сделки',
                'ordering': ['-date', 'total_cost'],
            },
        ),
        migrations.CreateModel(
            name='BrokerReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.FileField(upload_to='imported_reports/')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('broker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='portfolio.broker', verbose_name='Брокер')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отчёт',
                'verbose_name_plural': 'Отчёты',
                'ordering': ['uploaded'],
            },
        ),
        migrations.CreateModel(
            name='PortfolioStateRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('O', 'Открытая'), ('С', 'Закрытая')], max_length=1, verbose_name='Состояние позиции')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('average_buy_price', models.DecimalField(decimal_places=6, max_digits=19, verbose_name='Средняя цена покупки')),
                ('average_sell_price', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True, verbose_name='Средняя цена продажи')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.stock', verbose_name='Идентификатор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Позиция',
                'verbose_name_plural': 'Позиции',
                'ordering': ['user', 'ticker'],
                'unique_together': {('user', 'ticker', 'state')},
            },
        ),
    ]
