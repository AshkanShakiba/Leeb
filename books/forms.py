from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import Borrow, Purchase


class BorrowCreationForm(ModelForm):
    class Meta(ModelForm):
        model = Borrow
        fields = ("book", "borrower")


class PurchaseCreationForm(ModelForm):
    class Meta(ModelForm):
        model = Purchase
        fields = ("book", "customer")


class BookFilterFormHelper(FormHelper):
    form_method = "GET"
    layout = Layout(
        "name", "author", "category",
        Submit("submit", "Apply Filter"),
    )


class BorrowFilterFormHelper(FormHelper):
    form_method = "GET"
    layout = Layout(
        "book", "borrower",
        Submit("submit", "Apply Filter"),
    )


class PurchaseFilterFormHelper(FormHelper):
    form_method = "GET"
    layout = Layout(
        "book", "customer",
        Submit("submit", "Apply Filter"),
    )
