"""
Tests for models
"""
from decimal import Decimal
from core import models
from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email='test@example.com', password='password1234'):
    """
    Helper function to create a user
    """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_success(self):
        """
        Test for creating a user with a valid email
        """
        email = 'test@example.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test email is normalized for new users
        """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@example.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """
        Test new user without email, expect to fail and raise ValueError
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """
        Test for creating a superuser
        """
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """
        Successful creation of recipe
        title should match with the string
        representation of the model
        """
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample Recipe Title",
            time_minutes=10,
            price=Decimal('5.50'),
            description="Sample Recipe Description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """
        The string representation of a Tag object
        should be the same as the assigned name of the tag
        """
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='tag1')

        self.assertEqual(str(tag), tag.name)
