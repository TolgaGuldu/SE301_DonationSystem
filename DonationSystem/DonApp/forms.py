from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NGOUser, DonatorUser, Campaign, MoneyDonation, ItemDonation, Item
from django.contrib.auth.models import User


from django.contrib.auth.password_validation import validate_password



class UserRegistrationForm (UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class NGOUserForm (forms.ModelForm):

    class Meta:
        model = NGOUser
        fields = ['org_name', 'org_phone_num', 'org_website_link',
                  'contact_mail', 'description']


class DonatorUserForm (forms.ModelForm):

    class Meta:
        model = DonatorUser
        fields = []

class EditProfileForm (UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

class IndexForm(forms.Form):
    post = forms.CharField()

class CampaignForm (forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ['campaign_name', 'campaign_type', 'start_date', 'end_date', 'description']

class MiniCampaignForm (forms.ModelForm):

    class Meta:
        model = Campaign
        fields = []

class MoneyDonationForm (forms.ModelForm):

    class Meta:
        model = MoneyDonation
        fields = ['amount']


class ItemDonationForm (forms.ModelForm):

    class Meta:
        model = ItemDonation
        fields = []
class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['item_name', 'item_quantity']