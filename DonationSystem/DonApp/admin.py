from django.contrib import admin
from django.contrib.auth.models import User



from .models import Campaign, DonatorUser, NGOUser, ItemDonation, Item, MoneyDonation
from django.contrib.auth.models import User
'''
class UserInline(admin.StackedInline):
    model = User

class DonatorUserAdmin(admin.ModelAdmin):
    inlines = [UserInline]

class NGOUserAdmin(admin.ModelAdmin):
    inlines = [UserInline]

# Register your models here.

#admin.site.unregister(User)
admin.site.register(NGOUser, NGOUserAdmin)
admin.site.register(DonatorUser, DonatorUserAdmin)
'''

class ItemInlineAdmin (admin.TabularInline):
    model = Item
    extra = 3

class ItemDonationAdmin (admin.ModelAdmin):
    inlines = [ItemInlineAdmin]

def set_as_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
set_as_active.short_description = "Set selected users as active"

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    ordering = ['date_joined']
    actions = [set_as_active]


admin.site.register(Campaign)
admin.site.register(NGOUser)
admin.site.register(DonatorUser)
admin.site.register(ItemDonation, ItemDonationAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(MoneyDonation)


