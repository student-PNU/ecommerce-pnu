from django import forms
from .models import User, PostalInfo
from locations.models import Province, City
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز عبور'}))

    class Meta:
        model = User
        fields = ['name', 'phone_number']
        widgets = {
            'phone_number':forms.TextInput(attrs={'placeholder':'شماره همراه '}),
            'name':forms.TextInput(attrs={'placeholder':' نام '})
            }

    def clean_phone_number(self):
        p_number = self.cleaned_data.get('phone_number')
        if len(str(p_number)) != 11:
            self.add_error('phone_number','shomare motabar nist')
        if not str(p_number).startswith('09'):
            self.add_error('phone_number','شماره با 09 شروع نشده است')
        if User.objects.filter(phone_number=p_number).exists():
            self.add_error('phone_number','این شماره از قبل وجود دارد')
        return p_number

    
    def clean_password2(self):
        """بررسی اینکه تعداد کاراکترها ببشتر از 8 باشد
        از حروف کوچک و بزرگ و علاپم مختلف مثل اتساین و غیره استفاده شده باشد
        """
        p1, p2 = self.cleaned_data.get('password1'), self.cleaned_data.get('password2')
        if not p1 or not p2:
            raise ValidationError('lazem ast password 1 , password 2 por shavad')
        
        password1, password2 = str(p1), str(p2)
        if len(password1) < 8:
            self.add_error('password1','password kootah tar az 8 character ast')
        if not any(char.islower() for char in password1):
            self.add_error('password1','dar password az horufe koochak estefade nashode')
        if not any(char.isupper() for char in password1):
            self.add_error('password1','dar password az horufe bozorg estefade nashode')
        if not re.search(r'[!@#$%^&*_+-]', password1):
            self.add_error('password1','nevise haye ! @ $ % ^ & * _ - + dar password vojud nadarad')
        if password1 != password2:
            self.add_error('password1','passwordha hamkhani nadaradrnd')
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user

class CheckPhoneNumberForm(forms.Form):
    # برای بررسی شماره همراه در هنگام ثبت نام کاربر 
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'شماره همراه '}))

    def clean_phone_number(self):
        p_number = self.cleaned_data.get('phone_number')
        if len(str(p_number)) != 11:
            self.add_error('phone_number','شماره معتبر نیست')
        if not str(p_number).startswith('09'):
            self.add_error('phone_number','شماره با 09 شروع نشده است')
        if User.objects.filter(phone_number=p_number).exists():
            self.add_error('phone_number','این شماره از قبل وجود دارد')
        return p_number

class ForgetPasswordPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'شماره همراه '}))

    def clean_phone_number(self):
        p_number = self.cleaned_data.get('phone_number')
        if len(str(p_number)) != 11:
            self.add_error('phone_number','شماره معتبر نیست')
        if not str(p_number).startswith('09'):
            self.add_error('phone_number','شماره با 09 شروع نشده است')
        if not User.objects.filter(phone_number=p_number).exists():
            self.add_error('phone_number','کاربری با این شماره همراه ثبت نشده است')
        return p_number



class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text = 'you can change password using <a href = \'../password/\'>this form</a>')

    class Meta:
        model = User
        fields = ('name', 'phone_number','password', 'is_active', 'is_admin', 'last_login')

class OtpCodeForm(forms.Form):
    otp_code = forms.CharField(max_length=4, widget=forms.NumberInput(attrs={'placeholder':'کد تایید را وارد کنید'}))

    def clean_otp_code(self):
        code = self.cleaned_data.get("otp_code")
        if len(str(code)) != 4:
            self.add_error('otp_code', "کد باید چهار رقم باشد")
        return code
    

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'شماره همراه '}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور'}))

    def clean_phone_number(self):
        p_number= self.cleaned_data.get('phone_number')
        if len(str(p_number)) != 11:
            self.add_error('phone_number','شماره معتبر نیست')
        if not str(p_number).startswith('09'):
            self.add_error('phone_number','شماره با 09 شروع نشده است')
        return p_number

class ChangePasswordForm(forms.Form):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز عبور'}))

    def clean_password2(self):
        """بررسی اینکه تعداد کاراکترها ببشتر از 8 باشد
        از حروف کوچک و بزرگ و علاپم مختلف مثل اتساین و غیره استفاده شده باشد
        """
        p1, p2 = self.cleaned_data.get('password1'), self.cleaned_data.get('password2')
        if not p1 or not p2:
            raise ValidationError('لازم است «رمز عبور» و «تکرار رمز عبور» کامل شود')
        
        password1, password2 = str(p1), str(p2)
        if len(password1) < 8:
            self.add_error('password1','پسورد کوتاه تر از 8 کاراکتر است')
        if not any(char.islower() for char in password1):
            self.add_error('password1','در پسورد باید از حروف کوچک استفاده شود')
        if not any(char.isupper() for char in password1):
            self.add_error('password1','در پسورد باید از حروف بزرگ استفاده شود')
        if not re.search(r'[!@#$%^&*_+-]', password1):
            self.add_error('password1','کاراکترهای خاص مثل @ ! # $ % ^ & * _ - +  در  پسورد استفاده نشده')
        if password1 != password2:
            self.add_error('password1','پسوردها همخوانی ندارند')
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user
    


class PostalInfoForm(forms.ModelForm):
    class Meta:
        model = PostalInfo
        fields = ['first_name', 'last_name', 'postal_code', 'province', 'city', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'... گلستان - گرگان - روبروی ساختمان '}),
        }

