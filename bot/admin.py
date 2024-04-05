from django.contrib import admin
from django import forms
from .models import Start, WhyWe, Resume, LaborMarket, Interview, Contact, UserProfile, Offer


class StartAdminForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}))

    class Meta:
        model = Start
        fields = '__all__'

@admin.register(Start)
class StartAdmin(admin.ModelAdmin):
    form = StartAdminForm

class OfferAdmin(admin.ModelAdmin):
    list_display = ('user', 'text',)
    list_filter = ('user',)
    search_fields = ('user__username', 'text',)

admin.site.register(Offer, OfferAdmin)
admin.site.register(WhyWe)
admin.site.register(Resume)
admin.site.register(LaborMarket)
admin.site.register(Interview)
admin.site.register(Contact)
admin.site.register(UserProfile)
