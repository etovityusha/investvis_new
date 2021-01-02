# Generated by Django 3.1.4 on 2021-01-01 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_currencycourse'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioStateRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('state', models.CharField(choices=[('O', 'Открытая'), ('С', 'Закрытая')], max_length=1, verbose_name='Состояние позиции')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('average_buy_price', models.DecimalField(decimal_places=4, max_digits=19, verbose_name='Средняя цена покупки')),
                ('change', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Изменение стоимости')),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.stock', verbose_name='Идентификатор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Состояние',
                'verbose_name_plural': 'Состояния',
                'ordering': ['-date', 'user'],
                'unique_together': {('user', 'date', 'ticker', 'state')},
            },
        ),
    ]