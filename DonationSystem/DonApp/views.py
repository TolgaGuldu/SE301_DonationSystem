from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import Campaign, NGOUser, ItemDonation, Item
from .forms import UserRegistrationForm, DonatorUserForm, NGOUserForm,\
    EditProfileForm, IndexForm, CampaignForm, MoneyDonationForm, ItemDonationForm, ItemForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.forms import inlineformset_factory

# Create your views here.

def view_campaigns(request):

    campaigns = Campaign.objects.all().order_by('-end_date')
    template = loader.get_template('DonApp/campaigns.html')
    context = {
        'campaigns': campaigns,
    }

    return HttpResponse(template.render(context, request))


def view_campaign_detail(request, pk):

    campaign = Campaign.objects.get(pk=pk)
    latest_money_donations = campaign.campaign_money_donations.order_by('-timestamp')[:5]
    latest_item_donations = campaign.campaign_item_donations.order_by('-timestamp')[:5]

    context = {'campaign': campaign, 'latest_item_donations': latest_item_donations, 'latest_money_donations': latest_money_donations}

    return render(request, 'DonApp/view_campaign.html', context)





def view_ngos(request):

    ngos = NGOUser.objects.all()
    template = loader.get_template('DonApp/ngos.html')
    context = {
        'ngos': ngos,
    }

    return HttpResponse(template.render(context, request))


def view_ngo_detail(request, pk):

    ngo = NGOUser.objects.get(pk=pk)

    context = {'ngo': ngo}

    return render(request, 'DonApp/view_ngo.html', context)






def register(request):
    #template = loader.get_template('DonApp/register.html')

    #if request.method == 'POST':


    context = {}

    return render(request, 'regist/register.html', context)

def registerDonator(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        donator_form = DonatorUserForm(request.POST)

        if user_form.is_valid() and donator_form.is_valid():
            user = user_form.save()
            user.is_active = False
            user.save()
            #user.set_password(user_form.cleaned_data.get("password"))
            donator = donator_form.save(commit=False)
            donator.user = user
            user.save()
            donator.save()
            login(request, user)
            return redirect('view_profile')


    else:
        user_form = UserRegistrationForm()
        donator_form = DonatorUserForm()

    return render(request, 'regist/asDonator.html', {
        'user_form':user_form, 'donator_form':donator_form})

def registerNGO(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        ngo_form = NGOUserForm(request.POST)

        if user_form.is_valid() and ngo_form.is_valid():



            user = user_form.save()
            user.is_active = False
            user.save()
            ngo = ngo_form.save(commit=False)
            ngo.user = user
            user.save()
            ngo.save()
            login(request, user)
            return redirect('view_profile')

    else:
        user_form = UserRegistrationForm()
        ngo_form = NGOUserForm()

    return render(request, 'regist/asNGO.html', {
        'user_form':user_form, 'ngo_form':ngo_form
    } )


def view_profile(request):
    context = {'user': request.user}

    return render(request, 'DonApp/account/view_profile.html', context)


def edit_profile(request):
    ngo_form = None
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if hasattr(request.user,'ngo_user'):
            ngo_form =NGOUserForm(request.POST, instance=request.user.ngo_user)

        if form.is_valid() and hasattr(request.user,'ngo_user'):
            if ngo_form.is_valid():
                form.save()
                ngo_form.save()
                return redirect('/profile')
            else:
                form.save()
                return redirect('/profile')
        else:
            form.save()

            return redirect('/profile')

    else:
        form = EditProfileForm(instance=request.user)
        if hasattr(request.user, 'ngo_user'):
            ngo_form =NGOUserForm(instance=request.user.ngo_user)

        context = {'form': form, 'ngo_form': ngo_form}
        return render(request, 'DonApp/account/edit_profile.html', context)




def edit_my_campaign(request):
    pass

    campaign = None
    if request.method == 'POST' and not request.POST.get("pk"):
        #campaign = get_object_or_404(Campaign, pk=request.POST.get("pk"))
        form = CampaignForm(request.POST, instance=campaign)

        if form.is_valid():

            campaign = form.save(commit=False)
            campaign.creator = request.user.ngo_user
            campaign.save()

    else:
        #campaign = get_object_or_404(Campaign, pk=request.POST.get("pk"))
        campaign = request.user.ngo_user.campaigns.get(pk=request.POST.get("pk"))
        print("id ", campaign.id )
        form = CampaignForm(instance=campaign)


    context = {'form': form, 'campaign': campaign}

    return render(request, 'DonApp/edit_my_campaign.html', context)


def my_campaigns(request):

    my_campaigns = request.user.ngo_user.campaigns.all()


    template = loader.get_template('DonApp/my_campaigns.html')
    context = {'my_campaigns': my_campaigns,}

    return HttpResponse(template.render(context, request))


def index(request):
    context = {}

    return render(request, 'DonApp/index.html', context)


def create_campaign(request):


    if request.method == 'POST':
        campaign_form = CampaignForm(request.POST)

        if campaign_form.is_valid():
            campaign = campaign_form.save(commit=False)
            campaign.creator = request.user.ngo_user
            campaign.save()
            return redirect('my_campaigns')


    else:
        campaign_form = CampaignForm()

    return render(request, 'DonApp/create_campaign.html', {
        'campaign_form':campaign_form})


def view_received_donations(request):

    received_donations = request.user.ngo_user.received_money_donations.all

    #campaign_monetary_donations = request.user.ngo_user.campaigns.all


    context = {'received_donations': received_donations,}
               #'campaign_monetary_donations': campaign_monetary_donations}

    return render(request,'DonApp/my_received_donations.html', context)

def view_my_donations(request):

    money_donations = request.user.donator_user.money_donations.all
    item_donations = request.user.donator_user.item_donations.all

    context = {'money_donations': money_donations,
               'item_donations': item_donations}

    return render(request, 'DonApp/my_donations.html', context)

def money_donation(request, pk):

    campaign = get_object_or_404(Campaign, pk=pk)

    if request.method == 'POST':
        donation_form = MoneyDonationForm(request.POST)

        if donation_form.is_valid():
            money_donation = donation_form.save(commit=False)
            money_donation.donator = request.user.donator_user
            money_donation.campaign = campaign
            money_donation.save()
            return redirect('view_campaign_detail', pk=campaign.pk)


    else:
        donation_form = MoneyDonationForm()

    return render(request, 'DonApp/money_donation.html', {
        'donation_form':donation_form})

def ngo_money_donation(request, pk):

    ngo = get_object_or_404(NGOUser, pk=pk)

    if request.method == 'POST':
        donation_form = MoneyDonationForm(request.POST)

        if donation_form.is_valid():
            money_donation = donation_form.save(commit=False)
            money_donation.donator = request.user.donator_user
            money_donation.ngo = ngo
            money_donation.save()
            return redirect('view_ngos')


    else:
        donation_form = MoneyDonationForm()

    return render(request, 'DonApp/money_donation.html', {
        'donation_form':donation_form})

def code_gen():
    import random
    return ''.join(random.choice('0123456789ABCDEF') for i in range(16))


def item_donation(request, pk):

    item_donation = None
    campaign = get_object_or_404(Campaign, pk=pk)
    #ItemInlineFormSet = inlineformset_factory(ItemDonation, Item, fields=('item_name', 'item_quantity'))

    if request.method == 'POST':
        donation_form = ItemDonationForm(request.POST)
        item_form = ItemForm(request.POST)

        if donation_form.is_valid() and item_form.is_valid():
            item_donation = donation_form.save(commit=False)
            item_donation.campaign = campaign
            item_donation.donator = request.user.donator_user
            item_donation.shipping_code = code_gen()
            item_donation.save()
            item = item_form.save(commit=False)
            item.item_donation = item_donation

            item.save()
            return redirect('view_campaign_detail', pk = campaign.pk)

    else:
        donation_form = ItemDonationForm()
        item_form = ItemForm()


    context = {'donation_form': donation_form, 'item_form': item_form}
    return render(request, 'DonApp/item_donation.html', context)



class IndexView(TemplateView):
    template_name = 'DonApp/index.html'

    def get(self, request):
        form = IndexForm()
        campaigns = Campaign.objects.all()
        ngos = NGOUser.objects.all()
        context = {'form': form, 'campaigns': campaigns, 'ngos': ngos}

        return render(request, self.template_name, context)

    def post(self, request):
        form = IndexForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']

        context = {'form': form, 'text': text}
        return render(request, self.template_name, context)


