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


class ErrorView(TemplateView):
    template_name = "error.html"
    error = {"error_title": "", "error_text": "", "error_button": "", "error_return_url": ""}

    def get_context_data(self, **kwargs):
        error = self.error
        self.error = {"error_title": "", "error_text": "", "error_button": "", "error_return_url": ""}
        return error


class BorrowView(CreateView):
    form_class = BorrowCreationForm
    template_name = "books/borrow.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        if form.instance.book.available_to_borrow < 1:
            ErrorView.error = {
                "error_title": "End of Borrow Inventory",
                "error_text": f"The Borrow Inventory of {form.instance.book} has ended",
                "error_button": "Back",
                "error_return_url": reverse("home"),
            }
            return redirect("error")

        if Borrow.objects.filter(borrower=form.instance.borrower, book__category=form.instance.book.category
                                 ).count() + 1 > form.instance.book.category.max_allowed_count_on_borrow:
            ErrorView.error = {
                "error_title": "Reached Max Allowed Borrow Count of Category",
                "error_text": f"You have Reached Max Allowed Borrow Count of {form.instance.book.category} Category.",
                "error_button": "Back",
                "error_return_url": reverse("home"),
            }
            return redirect("error")

        for borrow in Borrow.objects.filter(borrower=form.instance.borrower):
            if borrow.penalty() > 0:
                ErrorView.error = {
                    "error_title": "Previous Fines",
                    "error_text": f"You borrowed {borrow.book} earlier and haven't delivered it after its deadline",
                    "error_button": "Back",
                    "error_return_url": reverse("home"),
                }
                return redirect("error")

        if form.instance.borrower.credit < 3 * form.instance.book.category.daily_borrow_cost:
            ErrorView.error = {
                "error_title": "Not Enough Credit",
                "error_text": f"You Don't Have Enough Credit to Borrow {form.instance.book.name}. "
                              + f"Required: {3 * form.instance.book.category.daily_borrow_cost}, "
                              + f"Your Credit: {form.instance.borrower.credit}",
                "error_button": "Back",
                "error_return_url": reverse("home"),
            }
            return redirect("error")

        return super().form_valid(form)


class PurchaseView(CreateView):
    form_class = PurchaseCreationForm
    template_name = "books/purchase.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        if form.instance.book.available_to_purchase < 1:
            ErrorView.error = {
                "error_title": "End of Purchase Inventory",
                "error_text": f"The Purchase Inventory of {form.instance.book} has ended",
                "error_button": "Back",
                "error_return_url": reverse("home"),
            }
            return redirect("error")

        if form.instance.customer.credit < form.instance.book.price:
            ErrorView.error = {
                "error_title": "Not Enough Credit",
                "error_text": f"You Don't Have Enough Credit to Purchase {form.instance.book.name}. "
                              + f"Price: {form.instance.book.price}, Your Credit: {form.instance.customer.credit}",
                "error_button": "Back",
                "error_return_url": reverse("home"),
            }
            return redirect("error")

        return super().form_valid(form)


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

        borrow.borrower.credit -= borrow.revenue()
        borrow.borrower.save()

    return redirect(reverse("search_borrows"))
