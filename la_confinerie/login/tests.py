from django.test import TestCase
from login.views import secretpage, signup, successfulpage, profile, add_shopkeeper, logout_view, confirmation_add_shopkeeper
from django.urls import resolve
from django.http import HttpResponse, HttpRequest
# Create your tests here.


class loginTest_urls(TestCase):  # suit l'ordre d'attribution des urls

    def test_root_url_resolves_to_profile(self):
        found = resolve('/accounts/profile/')
        self.assertEqual(found.func, profile)

    def test_root_url_resolves_to_signup(self):
        found = resolve('/accounts/signup/')
        self.assertEqual(found.func, signup)

    def test_root_url_resolves_to_successfulpage(self):
        found = resolve('/accounts/successfulpage/')
        self.assertEqual(found.func, successfulpage)

    def test_root_url_resolves_to_secretpage(self):
        found = resolve('/accounts/secretpage/')
        self.assertEqual(found.func, secretpage)

    def test_root_url_resolves_to_secretpage2(self):
        found = resolve('/accounts/unauthorized/')
        self.assertEqual(found.func, secretpage)

    def test_root_url_resolves_to_add_shopkeeper(self):
        found = resolve('/accounts/add_shopkeeper/')
        self.assertEqual(found.func, add_shopkeeper)

    def test_root_url_resolves_to_add_logout_view(self):
        found = resolve('/accounts/logout/')
        self.assertEqual(found.func, logout_view)

    def test_root_url_resolves_to_add_confirmation_add_shopkeeper(self):
        found = resolve('/accounts/confirmation_add_shopkeeper/')
        self.assertEqual(found.func, confirmation_add_shopkeeper)
