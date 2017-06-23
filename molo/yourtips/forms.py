from django import forms

from molo.yourtips.models import YourTipsEntry


class YourTipsEntryForm(forms.ModelForm):

    class Meta:
        model = YourTipsEntry
        fields = [
            'user_name', 'tip_text', 'terms_or_conditions_approved'
        ]
