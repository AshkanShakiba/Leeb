from django.urls import path

from .views import tmp_view, BorrowView, PurchaseView, SearchBookView, SearchBorrowView, SearchPurchaseView

urlpatterns = [
    path("search/books", SearchBookView.as_view(), name="search_books"),
    path("search/borrows", SearchBorrowView.as_view(), name="search_borrows"),
    path("search/purchases", SearchPurchaseView.as_view(), name="search_purchases"),
    path("borrow/", BorrowView.as_view(), name="borrow_registration"),
    path("delivery/", tmp_view, name="delivery_registration"),
    path("purchase/", PurchaseView.as_view(), name="purchase_registration"),
    path("revenue/", tmp_view, name="revenue_report"),
    path("fines/", tmp_view, name="fines_report"),
]
