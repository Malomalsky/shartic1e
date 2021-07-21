from django.forms import ModelForm, TextInput, Textarea, URLInput
from .models import ShortDescription, Article


class NewShortForm(ModelForm):

    class Meta:
        model = ShortDescription
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={
                'class': "form-control",
                'aria-label': "Short",
                'style': 'height: 100px;'
            })
        }


class NewArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ['header', 'url']
        widgets = {
            'header': TextInput(attrs={
                'class': 'form-control  w-100 mb-2 mt-5',
                'placeholder': 'Article header'
            }),
            'url': URLInput(attrs={
                'class': 'form-control w-100 mb-2',
                'placeholder': 'Article URL'
            })
        }
