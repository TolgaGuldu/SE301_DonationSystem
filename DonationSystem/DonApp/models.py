from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, URLValidator, EmailValidator
from django.core.exceptions import ValidationError
import datetime





# Create your models here.


''' USERS '''



class NGOUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ngo_user')

    org_name = models.CharField(max_length=50)
    description = models.TextField(max_length=600)
    org_phone_num = models.CharField(max_length=15)
    contact_mail = models.CharField(max_length=50, validators=[EmailValidator])
    org_website_link = models.CharField(max_length=50, validators=[URLValidator])
    approved = models.BooleanField(default=False)

    def __str__(self): return self.org_name

class DonatorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donator_user')

    approved = models.BooleanField(default=False)

    def __str__(self): return self.user.username

''' CAMPAIGNS '''

class Campaign(models.Model):

    creator = models.ForeignKey(NGOUser, on_delete=models.CASCADE, related_name='campaigns')

    CAMPAIGN_TYPE = (('Monetary', 'Monetary'), ('Item', 'Item'), ('Both', 'Both'))

    campaign_type = models.CharField(max_length=10, choices=CAMPAIGN_TYPE, default='Item')
    campaign_name = models.CharField(default='Campaign Name', max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(max_length = 600)
    approved = models.BooleanField(default=False)

    def __str__(self): return "{} - {}".format(self.creator.org_name, self.campaign_name)

    def clean(self):
        # Date Validation
        if (self.start_date > self.end_date) or \
                self.start_date < datetime.date.today() or \
                self.end_date < datetime.date.today() + datetime.timedelta(1):
            raise ValidationError("Enter valid start and end dates.")



class MonetaryCampaign(models.Model):

    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE, related_name='monetary_campaign')


class ItemCampaign(models.Model):

    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE, related_name='item_campaign')

    #required_items = models.CharField(max_length=100)


''' DONATIONS '''



class MoneyDonation(models.Model):

    donator = models.ForeignKey(DonatorUser, on_delete=models.CASCADE, related_name='money_donations')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE,\
               related_name='campaign_money_donations', null=True, blank=True, default=None)
    ngo = models.ForeignKey(NGOUser, on_delete=models.CASCADE,\
          related_name='received_money_donations', null=True, blank=True, default=None)

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    amount = models.IntegerField(default=0, validators=[MinValueValidator(1)])

    def __str__(self):
        #return "Donation by {} {}".format(self.donator.profile.name, self.donator.profile.surname)
        return "Donation by " + self.donator.user.username

class ItemDonation(models.Model):

    donator = models.ForeignKey(DonatorUser, on_delete=models.CASCADE, related_name='item_donations')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_item_donations')

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    shipping_code = models.CharField(max_length=20, blank=True)
    tracking_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        #return "Donation by {} {}".format(self.donator.profile.name, self.donator.profile.surname)
        return "Donation by " + self.donator.user.username



class Item(models.Model):

    item_donation = models.ForeignKey(ItemDonation, on_delete=models.CASCADE, related_name='items')
    #campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    item_name = models.CharField(max_length=30)
    item_quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self): return self.item_name + " " + str(self.item_quantity)
