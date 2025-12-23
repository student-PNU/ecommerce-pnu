from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

""""
بررسی هایی که تابع وَلیدیت پسورد انجام می دهد

    حداقل طول: بررسی می‌کند که طول رمز عبور حداقل به اندازه‌ی مشخصی (که به صورت پیش‌فرض 8 است) باشد.
    وجود حروف کوچک و بزرگ: بررسی می‌کند که رمز عبور حاوی حروف کوچک و حروف بزرگ انگلیسی باشد.
    وجود اعداد: بررسی می‌کند که رمز عبور حاوی اعداد باشد.
    وجود نویسه‌های خاص: بررسی می‌کند که رمز عبور حاوی نویسه‌های خاص (مانند @، #، $ و ...) باشد.
    انتخاب رمز عبور ضعیف: بررسی می‌کند که رمز عبور از یک لیست معمولی از رمزهای ضعیف (مانند "password" یا "123456") نباشد.

"""


class UserManager(BaseUserManager):

    def create_user(self, phone_number=None, name=None, password=None):
        # --- Phone number validation ---
        if not phone_number:
            raise ValueError("Phone number is required.")
        if not phone_number.startswith("09"):
            raise ValueError("Phone number must start with 09.")
        if len(phone_number) != 11:
            raise ValueError("Phone number must be 11 digits.")
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits.")

        # --- Name validation ---
        if not name:
            raise ValueError("Name is required.")
        if any(char.isdigit() for char in name):
            raise ValueError("Name cannot contain numbers.")

        # --- Password validation ---
        if not password:
            raise ValueError("Password is required.")
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValueError(e.messages)

        # --- Create user instance ---
        user = self.model(
            phone_number=phone_number,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone_number=None, name=None, password=None):
        user = self.create_user( phone_number=phone_number, name=name, password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
