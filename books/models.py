from math import floor
from datetime import date, datetime, timedelta
from django.db import models

from accounts.models import LeebUser


class Category(models.Model):
    name = models.CharField(max_length=255)
    max_allowed_count_on_borrow = models.PositiveIntegerField()
    daily_borrow_cost = models.PositiveIntegerField()
    daily_borrow_penalty = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.ImageField(upload_to="covers", default="covers/image-not-found.jpg", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available_to_borrow = models.PositiveIntegerField()
    available_to_purchase = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def borrows_count(self):
        return Borrow.objects.filter(book=self).count()


class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(LeebUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    delivery_deadline = models.PositiveIntegerField()
    delivery_date = models.DateField(null=True, default=None)

    def f(self, days):
        date = datetime.now() - timedelta(days=days)
        return Borrow.objects.filter(book=self.book, date__gte=date).count()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.delivery_date is None:
            n = self.book.available_to_borrow
            delivery_deadline = floor((30 * n) / (n + self.f(30))) + 1

            if delivery_deadline < 3:
                self.delivery_deadline = 3
            else:
                self.delivery_deadline = delivery_deadline

            self.book.available_to_borrow -= 1
            self.book.save()

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return f"{self.borrower}, {self.book}, {self.date}"

    def revenue(self):
        borrow_date = self.date
        delivery_date = self.delivery_date
        delivery_deadline = self.delivery_deadline
        if delivery_date is None:
            delivery_date = date.today()
        borrow_days = (delivery_date - borrow_date).days
        if borrow_days > delivery_deadline:
            return delivery_deadline * self.book.category.daily_borrow_cost + \
                   (borrow_days - delivery_deadline) * self.book.category.daily_borrow_penalty
        else:
            return borrow_days * self.book.category.daily_borrow_cost

    def penalty(self):
        borrow_date = self.date
        delivery_date = self.delivery_date
        delivery_deadline = self.delivery_deadline
        if delivery_date is None:
            delivery_date = date.today()
        borrow_days = (delivery_date - borrow_date).days
        if borrow_days > delivery_deadline:
            return (borrow_days - delivery_deadline) * self.book.category.daily_borrow_penalty
        else:
            return 0


class Purchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(LeebUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.customer.credit -= self.book.price
        self.customer.save()

        self.book.available_to_purchase -= 1
        self.book.save()

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return f"{self.customer}, {self.book}, {self.date}"
