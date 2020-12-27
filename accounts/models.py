from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from stock.models import Currency


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='assets/images',
        default='no-img.jpg',
        blank=True
    )
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='none@email.com')
    birth_date = models.DateField(default='1999-12-31')
    bio = models.TextField(default='')
    city = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    open_portfolio = models.BooleanField(default=False)
    analytics_currency = models.ForeignKey(Currency, default=2, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
