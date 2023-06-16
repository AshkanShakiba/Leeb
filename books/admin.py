from django.contrib import admin

from .models import Category, Book, Borrow, Purchase
from .forms import BorrowCreationForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "max_allowed_count_on_borrow",
        "daily_borrow_cost",
        "daily_borrow_penalty",
    ]


admin.site.register(Category, CategoryAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "available_to_borrow",
        "available_to_purchase",
        "price",
    ]


admin.site.register(Book, BookAdmin)


class BorrowAdmin(admin.ModelAdmin):
    add_form = BorrowCreationForm
    model = Borrow
    list_display = [
        "borrower",
        "book",
        "date",
        "delivery_deadline",
        "delivery_date",
    ]
    fieldsets = ((None, {"fields": ("book", "borrower")}),)
    add_fieldsets = ((None, {"fields": ("book", "borrower")}),)


admin.site.register(Borrow, BorrowAdmin)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "book",
        "date",
    ]


admin.site.register(Purchase, PurchaseAdmin)
