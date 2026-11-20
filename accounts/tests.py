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
