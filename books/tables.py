from django_tables2 import Table

from .models import Book, Borrow, Purchase


class BookTable(Table):
    class Meta:
        model = Book
        fields = ("id", "name", "author", "category", "price", "available_to_borrow", "available_to_purchase")


class BorrowTable(Table):
    class Meta:
        model = Borrow
        fields = ("book", "borrower", "date", "delivery_deadline", "delivery_date")


class PurchaseTable(Table):
    class Meta:
        model = Purchase
        fields = ("book", "customer", "date")
