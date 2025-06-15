"""
Testes para models do app risk
"""

from django.test import TestCase
from django.contrib.auth.models import User


class RiskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_placeholder(self):
        """Teste placeholder"""
        self.assertTrue(True)
