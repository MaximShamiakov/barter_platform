from django.test import TestCase

from ..forms import AdFilterForm, AdForm


class AdFormTest(TestCase):
    """Тесты форм объявлений"""

    def test_ad_filter_form_valid_data(self):
        """Тест валидной формы фильтрации"""
        form_data = {
            'q': 'test query',
            'category': 'electronics',
            'condition': 'new'
        }
        form = AdFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ad_form_valid_data(self):
        """Тест валидной формы создания объявления"""
        form_data = {
            'title': 'Test Ad',
            'description': 'Test description',
            'category': 'electronics',
            'condition': 'new'
        }
        form = AdForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ad_form_missing_required_fields(self):
        """Тест формы с отсутствующими обязательными полями"""
        form_data = {
            'description': 'Test description'
        }
        form = AdForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('category', form.errors)
