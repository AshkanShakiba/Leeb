from django.forms import ModelForm

from .models import Borrow


class BorrowCreationForm(ModelForm):
    class Meta(ModelForm):
        model = Borrow
        fields = ("book", "borrower")
