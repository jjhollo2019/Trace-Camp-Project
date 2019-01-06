from django import forms
from service.models import FOAAS

class FOAASForm(forms.ModelForm):
    class Meta:
        model = FOAAS
        fields = [
            'box_1',
            'box_2',
            'box_3'
        ]
    box_1 = forms.CharField( required = False ) 
    box_2 = forms.CharField( required = False )
    box_3 = forms.CharField( required = False )