# local import
from authors.base_test_config import TestConfiguration
from ..models import User


class TestRegister(TestConfiguration):
    def test_create_super_user(self):
        """ test create super user """
        my_admin = User.objects.create_superuser(
            'myuser',
            'myemail@test.com',
            'password'
        )
        self.assertEqual(my_admin.is_active, False)
        self.assertEqual(my_admin.is_staff, True)
        self.assertEqual(my_admin.is_superuser, True)
