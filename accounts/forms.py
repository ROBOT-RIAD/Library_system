from django import forms
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model =User
        fields =['username','password1','password2','first_name','last_name','email']

    def save(self,commit = True):
        our_user = super().save(commit=False)
        if commit:
            our_user.save()

            UserAccount.objects.create(
                user = our_user,
                account_no = 100000+our_user.id
            )
        return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })




class DepositForm(forms.ModelForm):

    class Meta:
        model = UserAccount
        fields =['balance']
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

    def clean_balance(self):
        min_dipo =50
        balance  = self.cleaned_data.get('balance')
        if balance < min_dipo :
            raise forms.ValidationError(
                f'You need to deposit at least {min_dipo} $'
            )
        return balance

    

