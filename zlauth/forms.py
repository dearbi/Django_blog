from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': '用户名不能为空',
        'max_length': '用户名在2-20个字符之间',
        'min_length': '用户名在2-20个字符之间'})
    email = forms.EmailField(error_messages={"required": "邮箱不能为空", "invalid": "邮箱格式不正确"})
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 检查邮箱是否已被注册
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已被注册")
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        # 查找验证码记录
        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("验证码和邮箱不匹配！")
        # 如果找到验证码记录，删除它
        captcha_model.delete()  # 删除验证码记录
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required": "邮箱不能为空", "invalid": "邮箱格式不正确"})
    password = forms.CharField(max_length=20, min_length=6)
    remember=forms.IntegerField(required=False)