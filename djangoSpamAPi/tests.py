from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from djangoSpamAPi.models import User, Contact, SpamReport


class ApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        
        self.user = User.objects.create_user(
            username='Alice',
            phone_number='1234567890',
            password='testpass'
        )
        response = self.client.post('/api/token/', {'phone_number': '1234567890', 'password': 'testpass'})
        
        self.token = response.data['access']

        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        

        
        self.user2 = User.objects.create_user(
            username='Bob',
            phone_number='8765432109',
            password='testpass2'
        )

        
        self.contact1 = Contact.objects.create(
            owner=self.user,
            name='Travis Walsh',
            phone_number='9876543210'
        )
        self.contact2 = Contact.objects.create(
            owner=self.user,
            name='Bob Marley',
            phone_number='8765432109'
        )

        
        SpamReport.objects.create(
            phone_number='9876543210',
            reported_by=self.user
        )
        SpamReport.objects.create(
            phone_number='1234567899',
            reported_by=self.user
        )

    def test_registration(self):
        
        data = {
            'username': 'newuser',
            'phone_number': '0987654321',
            'password': 'newpass'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        
        data = {
            'phone_number': '1234567890',
            'password': 'testpass'
        }
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_contact(self):
        
        data = {
            'name': 'Charlie Brown',
            'phone_number': '7654321098'
        }
        response = self.client.post(reverse('contacts'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 3)

    def test_search_by_name(self):
        response = self.client.get(reverse('search_name') )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0, "No data returned in response")

    def test_search_by_phone_number(self):
        response = self.client.get(reverse('search_phone') + '?phone_number=0123456789')
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertGreater(len(response.data), 0, "No data returned in response")
        self.assertEqual(response.data[0]['phone_number'], '0123456789')

    def test_spam_report(self):
        data = {
            'phone_number': '7654321098',
            'reported_by': self.user.id
        }
        response = self.client.post(reverse('report_spam'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpamReport.objects.count(), 3)

    def test_spam_likelihood(self):
        response = self.client.get(reverse('search_phone') + '?phone_number=9876543210')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0, "No data returned in response")
        self.assertIn('spam_count', response.data[0], "Spam count not found in response")
        self.assertEqual(response.data[0]['spam_count'], 1, "Spam count should be 1")

    def test_email_privacy(self):
       
        response = self.client.get(reverse('search_phone') + '?phone_number=8765432109')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0, "No data returned in response")
        self.assertNotIn('email', response.data[0], "Email should not be visible")
