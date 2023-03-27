from django.test import TestCase
from store.views import listing, search, detail, add_product, confirm_added_product, add_category, confirm_added_category, cart
from django.urls import resolve
from django.http import HttpResponse, HttpRequest
from store.models import Product, Shopkeeper
from django.test import Client


# Create your tests here.
#Vues non testées add_product, add_to_cart, add_category, remove_from_cart, cart

class store_page_test_directions(TestCase):
    """Cette classe vérifie que les urls renvoientsversles bonnes vues"""
    def test_root_url_resolves_to_listing(self):
        found = resolve('/store/')
        self.assertEqual(found.func, listing)

    def test_root_url_resolves_to_search(self):
        found = resolve('/store/search/')
        self.assertEqual(found.func, search)

    def test_root_url_resolves_to_add_product(self):
        found = resolve('/store/add/')
        self.assertEqual(found.func, add_product)

    def test_root_url_resolves_to_confirm_added_product(self):
        found = resolve('/store/added_product/')
        self.assertEqual(found.func, confirm_added_product)

    def test_root_url_resolves_to_detail(self):
        found = resolve(r'/store/2/')
        self.assertEqual(found.func, detail)

    def test_root_url_resolves_to_add_category(self):
        found = resolve(r'/store/add/category/')
        self.assertEqual(found.func, add_category)

    def test_root_url_resolves_to_confirm_added_category(self):
        found = resolve(r'/store/added_category/')
        self.assertEqual(found.func, confirm_added_category)
        
    def test_root_url_resolves_to_cart(self):
        found = resolve(r'/store/cart/')
        self.assertEqual(found.func, cart)



class store_page_test_views(TestCase):
    """Cette classe vérifie que les vues renvoient des html corrects"""
    def test_listing_page_returns_correct_html(self):
        request = HttpRequest()
        response = listing(request)
        html = response.content.decode('utf8')
        self.assertIn('Voici nos produits', html)

    def test_detail_page_returns_correct_html(self):
        #Ajoutons un objet dans la base de données
        Leclerc = Shopkeeper.objects.get_or_create(name='Leclerc')[0] #On crée un commercant s'il n'existe pas
        product = Product.objects.get_or_create(name='Pommes de terres', shopkeeper = Leclerc)[0] #on ajout un produit 'Pommes de terres' chez Leclerc s'il n'existe pas encore
        request = HttpRequest()
        response = detail(request, product.id)
        html = response.content.decode('utf8')
        self.assertIn('Réserver', html)

    def test_search_page_returns_correct_html(self):
        c = Client()
        response = c.get('/store/search/', {'query': 'ru'})
        html = response.content.decode('utf8')
        self.assertIn('produits', html)

    def test_confirm_added_product_page_returns_correct_html(self):
        c = Client()
        Leclerc = Shopkeeper.objects.get_or_create(name='Leclerc')[0] #On crée un commercant s'il n'existe pas
        product = Product.objects.get_or_create(name='Pommes de terres', shopkeeper = Leclerc)[0] #on ajout un produit 'Pommes de terres' chez Leclerc s'il n'existe pas encore
        response = c.post('/store/added_product/', {'name':'Pommes de terres','description':'description','price':1.89,'shopkeeper':'Leclerc','available':'on', 'query':'test'})
        html = response.content.decode('utf8')
        self.assertIn('produit', html)

    def test_cconfirm_added_category_page_returns_correct_html(self):
        c = Client()
        Leclerc = Shopkeeper.objects.get_or_create(name='Leclerc')[0] #On crée un commercant s'il n'existe pas
        response = c.post('/store/added_category/', {'name':'Légumes','shopkeeper':'Leclerc','available':'on', 'query':'test'})
        html = response.content.decode('utf8')
        self.assertIn('produit', html)

