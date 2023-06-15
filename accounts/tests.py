from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class SignUpTests(TestCase):
    def test_signup_view(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "testuser@email.com",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.last().username, "testuser")
        self.assertEqual(get_user_model().objects.last().email, "testuser@email.com")
