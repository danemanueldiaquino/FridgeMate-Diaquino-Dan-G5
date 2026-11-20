from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.forms import FridgeItemForm
from accounts.models import FridgeItem


class FridgeItemModelFormTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='member1', email='member1@example.com', password='TestPass123!')

    def test_create_fridge_item(self):
        item = FridgeItem.objects.create(owner=self.user, name='Milk', category='Dairy', zone=FridgeItem.ZONE_FRIDGE, quantity='1.00', unit='L')
        self.assertEqual(item.name, 'Milk')
        self.assertEqual(item.owner, self.user)

    def test_form_rejects_non_positive_quantity(self):
        form = FridgeItemForm(data={'name': 'Eggs', 'category': 'Dairy', 'zone': FridgeItem.ZONE_FRIDGE, 'quantity': '0', 'unit': 'pcs', 'expiry_date': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)


class FridgeItemCrudViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='member2', email='member2@example.com', password='TestPass123!')

    def test_fridge_item_list_requires_login(self):
        response = self.client.get('/fridge-items/')
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_and_list_item(self):
        self.client.login(username='member2', password='TestPass123!')
        response = self.client.post('/fridge-items/add/', {'name': 'Butter', 'category': 'Dairy', 'zone': FridgeItem.ZONE_FRIDGE, 'quantity': '2.00', 'unit': 'packs', 'expiry_date': ''})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FridgeItem.objects.filter(owner=self.user, name='Butter').exists())
