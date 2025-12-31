from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.
class ordertest(TestCase):
    def test_user_created(self):
        user=User.objects.create_user(username='testuser',password='testpass')
        self.assertEqual(user.username,'testuser')

