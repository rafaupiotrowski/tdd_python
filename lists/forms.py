from django import forms
from lists.models import Item

EMPTY_LIST_ERROR = 'Element listy nie może być pusty'

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Wpisz rzecz do zrobienia',
                'class': 'form-control input-lg',
                'blank': False
            })
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }
        
    def save(self, for_list):
        self.instance.list = for_list
        return super().save()