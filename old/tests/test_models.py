import django_currentuser
from django.contrib.auth.models import User
from django.test import TestCase

from portfolio.models import Account


class TestModels(TestCase):
    def test_userdata(self):
        user = self._stub_user_login()

        account = Account()
        account.name = "blah:"
        account.save()

        self.assertEquals(account.user, user)

    def _stub_user_login(self):
        user = User.objects.create(username="test")
        self.client.force_login(user)
        setattr(
            django_currentuser.middleware._thread_locals,
            django_currentuser.middleware.USER_ATTR_NAME,
            user,
        )
        return user
