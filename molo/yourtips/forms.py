from django import forms

from molo.yourtips.models import YourTipsEntry


class YourTipsEntryForm(forms.ModelForm):

    class Meta:
        model = YourTipsEntry
        fields = [
            'user_name', 'tip_text', 'allow_share_on_social_media'
        ]
