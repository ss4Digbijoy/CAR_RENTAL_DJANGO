from django import forms
from .models import User, Car, Rent
import re
import hashlib
class UserForm(forms.ModelForm):
     def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password)<=8:
            raise forms.ValidationError('The password must contain at least 9 characters.')
        hash_value = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return hash_value
     def clean_name(self):
        name=self.cleaned_data['name']
        pattern = r'[^a-zA-Z]'
        if re.search(pattern, name):
            raise forms.ValidationError('The name must contain only letters.')
        return name
     class Meta:
        model = User
        fields = '__all__'  # You can specify the fields you want to include if not all fields are needed
        widgets = {
            'password': forms.PasswordInput(),
        }


class loginf(forms.Form):
    email=forms.EmailField(required=True, label='EMAIL')
    password=forms.CharField(label="password",max_length=40, required=True,widget=forms.PasswordInput())
    #def clean_email(self):
    """   emai=self.cleaned_data['email']
        if not(User.objects.filter(email=emai)):
            raise forms.ValidationError("Not Registered Email!!")
        return emai"""
    
    def clean_password(self):
        pss=self.cleaned_data['password']
        emai=self.cleaned_data['email']
        if not(User.objects.filter(email=emai)):
            raise forms.ValidationError("Not Registered Email!!")
        use=User.objects.filter(email=emai)
        has=hashlib.sha256(pss.encode("utf-8")).hexdigest()
        for ino in use:
            has2=ino.password
        if has!=has2:
            raise forms.ValidationError("PASSWORD WRONG")
        return has
class carc(forms.Form):
    choices=Car.objects.filter(occup=False).values_list('vno', 'model')
    dropdown = forms.ChoiceField(choices=choices,required=True,label='CHOOSE YOUR CAR', widget=forms.Select(attrs={'class': 'form-control'}))
    days=forms.IntegerField(required=True, label='choose days')
    def clean_dropdown(self):
            d=self.cleaned_data['dropdown']
            car=Car.objects.get(vno=d)
            if car.occup==True:
                raise forms.ValidationError('ALREADY OCCUPIED CAR')
            return d


    def clean_days(self):
        days=self.cleaned_data['days']
        if days>15:
            raise forms.ValidationError("YOU CAN NOT RENT A CAR FOR MORE THAN 15 DAYS")
        return days

class paym(forms.Form):
    rentid=forms.IntegerField(required=True, label='give the rent id')
    amount=forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    def clean(self):
        cleaned_data = super().clean()
        rid=cleaned_data['rentid']
        amou=cleaned_data['amount']
        try:
            rent=Rent.objects.get(rid=rid)
        except Rent.DoesNotExist:
            rent = None
        if not(rent):
            raise forms.ValidationError('NO SUCH RENT EXISTS')
        if rent.given>=rent.total:
            raise forms.ValidationError('ALREADY PAID RENT')
        if amou>(rent.total-rent.given):
            raise forms.ValidationError('AMOUNT GREATER THAN DUE AMOUNT')
        return

            
    


    


