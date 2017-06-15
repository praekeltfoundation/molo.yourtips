from django import forms

from molo.yourtips.models import YourTipsEntry


class YourTipsEntryForm(forms.ModelForm):
    terms_or_conditions_approved = forms.BooleanField(required=True)

    class Meta:
        model = YourTipsEntry
        fields = ['tip_name', 'tip_text', 'terms_or_conditions_approved',
                  'hide_real_name']
