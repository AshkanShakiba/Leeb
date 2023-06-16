import django_filters

from .models import Book, Borrow, Purchase


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ["name", "author", "category"]


class BorrowFilter(django_filters.FilterSet):
    class Meta:
        model = Borrow
        fields = ["book", "borrower"]


class PurchaseFilter(django_filters.FilterSet):
    class Meta:
        model = Purchase
        fields = ["book", "customer"]
