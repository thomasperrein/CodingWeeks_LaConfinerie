from django.test import TestCase
from homepage.views import welcome, about_us #Importation des vues nécessaires pour les tests
from django.urls import resolve
from django.http import HttpResponse, HttpRequest

# Create your tests here.


class homepageTest(TestCase):
    """La classe homepageTest permet d'introduire ici, deux tests sur les urls et deux tests sur les pages html"""
    def test_root_url_resolves_to_welcome_view(self):
        """Ce test vérifie que l'url '/'mène bien à la vue welcome, il s'agit de vérifier que ce lien mène bien à vue accueillant l'utilisateur"""
        found = resolve('/')
        self.assertEqual(found.func, welcome)

    def test_root_url_resolves_to_about_us_view(self):
        """Ce test vérifie que l'url '/about/' mène bien à la vue about_us"""
        found = resolve('/about/')
        self.assertEqual(found.func, about_us)

    def test_homepage_returns_correct_html(self):
        """Ce test sert à vérifier que la page html renvoyée par la vue welcome est correcte"""
        request = HttpRequest()
        response = welcome(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>La confinerie</title>', html)

    def test_aboutus_page_returns_correct_html(self):
        """Ce test sert à vérifier que la page html renvoyée par la vue about_us est correcte"""
        request = HttpRequest()
        response = about_us(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
