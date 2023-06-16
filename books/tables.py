from django_tables2 import Table, TemplateColumn

from .models import Book, Borrow, Purchase


class BookTable(Table):
    class Meta:
        model = Book
        fields = ("id", "name", "author", "category", "price", "available_to_borrow", "available_to_purchase")


class BorrowTable(Table):
    delivery_registration = TemplateColumn(
        template_code='<a href="{% url "delivery_registration" record.id %}" class="btn btn-success">Deliver</a>')

    class Meta:
        model = Borrow
        fields = ("book", "borrower", "book__category__daily_borrow_cost", "book__category__daily_borrow_penalty",
                  "date", "delivery_deadline", "delivery_date", "revenue", "penalty")


class PurchaseTable(Table):
    class Meta:
        model = Purchase
        fields = ("book", "book__price", "customer", "date")
