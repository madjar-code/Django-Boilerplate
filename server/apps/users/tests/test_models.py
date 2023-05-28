from django.test import TestCase
from users.models import User


class TestUsers(TestCase):
    def test_user_model(self):
        user: User = User.objects.create_user(
            username='test', email='test@test.com', password='testpassword')
        query: User = User.objects.first()

        self.assertIsInstance(user, User)
        self.assertEqual(query, user)
        self.assertFalse(query.is_verified)
        self.assertFalse(query.is_superuser)
        self.assertFalse(query.is_staff)

    def test_user_model_as_superuser(self):
        user: User = User.objects.create_superuser(
            username='test', email='test@test.com', password='testpassword')
        query: User = User.objects.first()
        self.assertIsInstance(user, User)
        self.assertEqual(user, query)
        self.assertTrue(query.is_verified)
        self.assertTrue(query.is_superuser)
        self.assertTrue(query.is_staff)
