from django import forms
from .models import Adicion

class AdicionForm(forms.Form):
    adiciones = forms.ModelMultipleChoiceField(
        queryset=Adicion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
