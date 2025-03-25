from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
# from member.models import User # 이렇게 불러와도 되고 User = get_user_model() 이렇게 가져와도 된다

User = get_user_model() # 만든 AUTH_USER_MODEL을 가져오는 내장 함수

# 회원가입 폼
class SignupForm(UserCreationForm):    # 장고에 내장된 "UserCreationForm"을 상속 받고
    def __init__(self, *args, **kwargs):  # 클래스 처음 만들 때 호출 되는 것
        super().__init__(*args, **kwargs)  # 원래 UserCreationForm 있는 init을 호출

        # class_default_fields = ('password1', 'password2')

        # for field in class_update_fields:
        for field in ('password1', 'password2'):  # UserCreationForm 여기 'password1', 'password2' 안에
            self.fields[field].widget.attrs['class'] = 'form-control'  # "field"에 'form-control' 속성을 넣어줌
            self.fields[field].widget.attrs['placeholder'] = 'password'  # "field" 입력칸에 'password' 단어를 넣어줌
            if field == 'password1':  # "password1"면 "비밀번호"라고 해주고
                self.fields[field].label = '비밀번호'
            else:  # 아닐 경우 "비밀번호 확인"이라고 해준다
                self.fields[field].label = '비밀번호 확인'


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'name',)
        labels = {
            'email': '이메일',
            'name': '이름',
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'example@example.com',
                    'class': 'form-control',
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'placeholder': '이름',
                    'class': 'form-control',
                }
            )
        }


# 로그인 폼
class LoginForm(forms.Form):
    email = forms.CharField(
        label = '이메일',  # 인풋(입력 하는칸) 왼쪽에 '이메일' 이라고 표기
        required = True,    # 필수로 입력 해야 한다는 설정
        widget = forms.EmailInput(        # 인풋(입력 하는칸)안에 표기할 내용, 속성
            attrs={
                'placeholder': 'example@example.com',
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        label = '패스워드',
        required = True,
        widget = forms.PasswordInput(       # PasswordInput : 비밀번호를 입력할 떄 "****" 이렇게 안 보이게 하는 것
            attrs={
                'placeholder': 'password',
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None


    def clean(self):    # Form안에 있는 함수 is_valid  사용하면서 clean 메서드가 호출이 된다.
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        self.user = authenticate(email=email, password=password) # authenticate : 데이터를 실제 DB에서 가져옴 / 이메일, 패스워드 인증

        if not self.user.is_active:  # 유저의 이메일, 패스워드가 인증(활성화)이 안됐다면
            raise forms.ValidationError('유저가 인증되지 않았습니다.')  # 오류와 오류 문구를 보여준다.
        return cleaned_data     # 잘 되었다면 유저 데이터를 보내준다.

