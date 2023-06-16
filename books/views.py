from datetime import date
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .models import Book, Category, Borrow, Purchase
from .forms import BorrowCreationForm, PurchaseCreationForm, \
    BookFilterFormHelper, BorrowFilterFormHelper, PurchaseFilterFormHelper
from .tables import BookTable, BorrowTable, PurchaseTable
from .filters import BookFilter, BorrowFilter, PurchaseFilter


def tmp_view(request):
    return render(request, "home.html", context={"books": Book.objects.all()})


class BorrowView(CreateView):
    form_class = BorrowCreationForm
    template_name = "books/borrow.html"
    success_url = reverse_lazy("home")


class PurchaseView(CreateView):
    form_class = PurchaseCreationForm
    template_name = "books/purchase.html"
    success_url = reverse_lazy("home")


class FilteredSingleTableView(SingleTableMixin, FilterView):
    formhelper_class = None

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)
        filterset = filterset_class(**kwargs)
        filterset.form.helper = self.formhelper_class()
        return filterset


class SearchBookView(FilteredSingleTableView):
    template_name = "search.html"
    table_class = BookTable
    paginate_by = 25
    filterset_class = BookFilter
    formhelper_class = BookFilterFormHelper


class SearchBorrowView(FilteredSingleTableView):
    template_name = "search.html"
    table_class = BorrowTable
    paginate_by = 25
    filterset_class = BorrowFilter
    formhelper_class = BorrowFilterFormHelper


class SearchPurchaseView(FilteredSingleTableView):
    template_name = "search.html"
    table_class = PurchaseTable
    paginate_by = 25
    filterset_class = PurchaseFilter
    formhelper_class = PurchaseFilterFormHelper


class RevenueReportView(TemplateView):
    template_name = "bar_chart.html"

    def get_context_data(self, **kwargs):
        labels = []
        values = []
        for category in Category.objects.all():
            value = 0
            for borrow in Borrow.objects.filter(book__category=category):
                value += borrow.revenue()
            for purchase in Purchase.objects.filter(book__category=category):
                value += purchase.book.price
            labels.append(category.name)
            values.append(value)
        return {
            "labels": labels,
            "values": values,
            "title": "Revenue Report",
        }


def delivery_registration(request, pk):
    borrow = Borrow.objects.get(id=pk)
    if borrow.delivery_date is None:
        borrow.delivery_date = date.today()
        borrow.save()

    return redirect(reverse("search_borrows"))
