from django.test import SimpleTestCase
from usrsmgmnt.froms import  UserRegistrationForm
class TestRegForm(SimpleTestCase):
    def test_reg_form_with_valid_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())


