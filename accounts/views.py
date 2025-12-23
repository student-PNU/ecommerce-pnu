from django.shortcuts import render, redirect
from django.views import View
from .forms import CheckPhoneNumberForm, OtpCodeForm, UserCreationForm, UserLoginForm
import random
from .models import OtpCode, User
from django.db.transaction import atomic
from utils import send_otp_code
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


class CheckPhoneNumberView(View):  
    # گرفتن شماره همراه کاربر، اعتبار سنجی شماره همراه
    # ارسال کردن کد تایید و هدایت به صفحه ی وارد کردن کد تایید
    form_class = CheckPhoneNumberForm
    def get(self, request):
        phone_number = request.GET.get('phone_number', None)
        if phone_number is None:
            #نشان دادن صفحه ای برای دریافت شماره همراه از کاربر
            return render(request, 'accounts/register_step1.html', {'phone_number_form':self.form_class})
        else:
            #اعتبارسنجی شماره،بررسی و حذف کد تایید هایی که از قبل برای آن شماره وجود دارد و ارسال کد تایید و نشان دادن صفحه ای برای دریافت کد تایید
            p = self.form_class({'phone_number':phone_number})
            if p.is_valid():
                phone_number = p.cleaned_data['phone_number']
                request.session['phone_number'] = phone_number
                random_code = random.randint(1000, 9999)
                if OtpCode.objects.filter(phone_number=phone_number).exists():
                    with atomic():
                        OtpCode.objects.filter(phone_number=phone_number).delete()
                OtpCode.objects.create(code=random_code, phone_number=phone_number)
                send_otp_code(phone_number, random_code)
                OtpCode_form = OtpCodeForm()
                return render(request, 'accounts/register_step1.html', {'OtpCode_form':OtpCode_form,'phone_number':phone_number})
            else:
                return render(request, 'accounts/register_step1.html', {'phone_number_form':p})

    
    def post(self, request):
        #بررسی اعتبار کد تایید وارد شده و هدایت کاربر به کلاس ساخت کاربر
        phone_number = request.session.get('phone_number', None)
        print('*************************************************',request.POST)
        OtpCode_form = OtpCodeForm(request.POST)
        if OtpCode_form.is_valid():
            entered_code = OtpCode_form.cleaned_data.get('otp_code')
            OtpCode_obj = OtpCode.objects.get(phone_number=phone_number)
            Otp_created_at = OtpCode_obj.created
            
            print('*************************************************',int((timezone.now() - Otp_created_at).total_seconds())<120)
            if str(OtpCode_obj.code) == str(entered_code):
                OtpCode_obj.delete()
                return redirect('accounts:register_step2')
            else:
                OtpCode_form.add_error('otp_code',"عدم اعتبار")
                return render(request, 'accounts/register_step1.html', {'OtpCode_form':OtpCode_form, 'phone_number':phone_number})
        else:
            return render(request, 'accounts/register_step1.html', {'OtpCode_form':OtpCode_form, 'phone_number':phone_number})


class UserCreationView(View):
    #نشان دادن صفحه ای برای دریافت نام و پسورد کاربری که قصد ثبت نام دارد
    #ذخیره شماره همراه - نام - پسورد کاربر و هدا یت او به صفحه ی خانه
    form_class = UserCreationForm
    def get(self, request):
        phone_number = request.session.get('phone_number', None)
        del request.session['phone_number']
        if phone_number:
            #اگر شماره همراه کاربر در مرحله ی قبل در سِشِن های کاربر ذخیره شده باشد
            #فرم ساخت کاربر جدید را با آن شماره همراه مقدار دهی میکنیم و
            #فیلد وارد کردن شماره تلفن را برای کاربر مخفی کرده و فرم را به کاربر نشان میدهیم
            from django import forms
            form = self.form_class(initial={'phone_number':phone_number})
            form.fields['phone_number'].widget = forms.HiddenInput()
            return render(request, 'accounts/register_step2.html', {'form':form})
        else:
            return redirect("accounts:register_step1")
    
    def post(self, request):
        #فرم را اعتبار سنجی کرده و اگر اطلاعات معتبر بود یک کاربر جدید ساخته میشود و کاربر به 
        # .صفحه ی خانه هدایت میشود و در صورت معتبر نبود ارور ها به کاربر نشان داده میشود
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(name=cd['name'], phone_number=cd['phone_number'],
                                 password=cd['password1'])
            messages.success(request, 'ثبت نام با موفقیت انجام شد')
            return redirect('home:home')
        else:
            from django import forms
            form.fields['phone_number'].widget = forms.HiddenInput()
            return render(request, 'accounts/register_step2.html', {'form':form})


class UserLoginView(View):
    #نشان دادن صفحه ای برای دریافت شماره تلفن و  پسورد کاربر و  ورود کاربر به سایت پس از اعتبار سنجی اطلاعات
    form = UserLoginForm
    def get(self,request):

        return render(request, 'accounts/login.html', {'form':self.form})
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user=user)
                messages.success(request, "ورود با موفقیت انجام شد")
                return redirect('home:home')
            else:
                if User.objects.filter(phone_number = cd['phone_number']).exists():
                    form.add_error('password', 'رمز عبور صحیح نمی باشد')
                    return render(request, 'accounts/login.html', {'form':form})
                else:
                    form.add_error('phone_number', 'کاربری با این شماره تلفن مجود نیست')
                    return render(request, 'accounts/login.html', {'form':form})
        else:
            return render(request, 'accounts/login.html', {'form':form})



class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:home')