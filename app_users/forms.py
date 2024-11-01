from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

username_placeholder = _('Username')
password_placeholder = _('Parol')

class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': username_placeholder})
        self.fields['password'].widget.attrs.update({'placeholder': password_placeholder})
        
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 ps-10 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            })
