from django.test import TestCase
from django.urls import reverse


class TestRecanView(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('recan_view'))
        self.assertEqual(response.status_code, 200)
 
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('recan_view'))
        self.assertTemplateUsed(response,
                                 'base.html')


class TestDataSetsView(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/example_datasets/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('datasets'))
        self.assertEqual(response.status_code, 200)
 
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('datasets'))
        self.assertTemplateUsed(response,
                                 'example_datasets.html')


