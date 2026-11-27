from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import FridgeItemForm, RegistrationForm
from .models import FridgeItem


class FridgeItemCoreTests(TestCase):
    def setUp(self):
        self.member = get_user_model().objects.create_user(
            username='member',
            email='member@example.com',
            password='TestPass123!',
            role='member',
        )
        self.other_member = get_user_model().objects.create_user(
            username='other',
            email='other@example.com',
            password='TestPass123!',
            role='member',
        )
        self.manager = get_user_model().objects.create_user(
            username='manager',
            email='manager@example.com',
            password='TestPass123!',
            role='manager',
        )
        self.item = FridgeItem.objects.create(
            owner=self.member,
            name='Milk',
            category='Dairy',
            zone=FridgeItem.StorageZone.FRIDGE,
            quantity=2,
            unit='cartons',
        )

    def valid_item_data(self, **overrides):
        data = {
            'name': 'Eggs',
            'category': 'Dairy',
            'zone': FridgeItem.StorageZone.FRIDGE,
            'quantity': '12',
            'unit': 'pcs',
            'expiry_date': '',
        }
        data.update(overrides)
        return data

    def test_valid_input_creates_record(self):
        self.client.force_login(self.member)
        response = self.client.post(reverse('fridge_item_create'), self.valid_item_data())
        self.assertRedirects(response, reverse('fridge_item_list'))
        self.assertTrue(FridgeItem.objects.filter(owner=self.member, name='Eggs').exists())

    def test_invalid_quantity_is_rejected(self):
        form = FridgeItemForm(
            data=self.valid_item_data(quantity='0'),
            owner=self.member,
        )
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_missing_required_name_is_rejected(self):
        form = FridgeItemForm(
            data=self.valid_item_data(name=''),
            owner=self.member,
        )
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_duplicate_item_is_rejected(self):
        form = FridgeItemForm(
            data=self.valid_item_data(name='milk', quantity='1', unit='cartons'),
            owner=self.member,
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.non_field_errors())

    def test_unauthenticated_user_cannot_access_core_views(self):
        protected_urls = [
            reverse('fridge_item_list'),
            reverse('fridge_item_create'),
            reverse('fridge_item_update', args=[self.item.pk]),
            reverse('fridge_item_delete', args=[self.item.pk]),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 302)

    def test_member_cannot_view_another_members_record(self):
        self.client.force_login(self.other_member)
        response = self.client.get(reverse('fridge_item_update', args=[self.item.pk]))
        self.assertEqual(response.status_code, 404)

    def test_member_cannot_edit_another_members_record(self):
        self.client.force_login(self.other_member)
        response = self.client.post(
            reverse('fridge_item_update', args=[self.item.pk]),
            self.valid_item_data(name='Changed'),
        )
        self.assertEqual(response.status_code, 404)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Milk')

    def test_member_cannot_delete_another_members_record(self):
        self.client.force_login(self.other_member)
        response = self.client.post(
            reverse('fridge_item_delete', args=[self.item.pk])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(FridgeItem.objects.filter(pk=self.item.pk).exists())

    def test_authorized_member_can_update_own_record(self):
        self.client.force_login(self.member)
        response = self.client.post(
            reverse('fridge_item_update', args=[self.item.pk]),
            self.valid_item_data(name='Fresh Milk'),
        )
        self.assertRedirects(response, reverse('fridge_item_list'))
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Fresh Milk')

    def test_authorized_member_can_delete_own_record(self):
        self.client.force_login(self.member)
        response = self.client.post(
            reverse('fridge_item_delete', args=[self.item.pk])
        )
        self.assertRedirects(response, reverse('fridge_item_list'))
        self.assertFalse(FridgeItem.objects.filter(pk=self.item.pk).exists())

    def test_manager_can_view_and_update_all_inventory(self):
        self.client.force_login(self.manager)
        response = self.client.get(reverse('fridge_item_list'))
        self.assertContains(response, 'Milk')
        response = self.client.post(
            reverse('fridge_item_update', args=[self.item.pk]),
            self.valid_item_data(name='Manager Updated'),
        )
        self.assertRedirects(response, reverse('fridge_item_list'))
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Manager Updated')

    def test_invalid_url_returns_custom_404(self):
        self.client.force_login(self.member)
        response = self.client.get('/fridge-items/999999/delete/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'missing', status_code=404)


class StandardFeatureTests(TestCase):
    def test_registration_validates_duplicate_email(self):
        get_user_model().objects.create_user(
            username='existing',
            email='same@example.com',
            password='TestPass123!',
        )
        form = RegistrationForm(data={
            'username': 'newuser',
            'email': 'SAME@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_member_cannot_access_manager_dashboard(self):
        member = get_user_model().objects.create_user(
            username='member_role',
            email='member_role@example.com',
            password='TestPass123!',
            role='member',
        )
        self.client.force_login(member)
        response = self.client.get(reverse('manager_dashboard'))
        self.assertEqual(response.status_code, 403)
