from django.urls import path

from .views import tmp_view, BorrowView, PurchaseView, SearchBookView, SearchBorrowView, SearchPurchaseView, \
    RevenueReportView, delivery_registration

urlpatterns = [
    path("search/books", SearchBookView.as_view(), name="search_books"),
    path("search/borrows", SearchBorrowView.as_view(), name="search_borrows"),
    path("search/purchases", SearchPurchaseView.as_view(), name="search_purchases"),
    path("borrow/", BorrowView.as_view(), name="borrow_registration"),
    path("delivery/<int:pk>", delivery_registration, name="delivery_registration"),
    path("purchase/", PurchaseView.as_view(), name="purchase_registration"),
    path("revenue/", RevenueReportView.as_view(), name="revenue_report"),
    path("fines/", SearchBorrowView.as_view(), name="fines_report"),
]
