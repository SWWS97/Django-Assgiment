from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth import login, get_user_model

from member.forms import SignupForm, LoginForm
from django.conf import settings

from utils.email import send_email


User = get_user_model()


# 회원 가입 뷰(페이지) 만들기
class SignupView(CreateView):
    template_name = 'auth/signup.html'
    form_class = SignupForm


    def form_valid(self, form):
        user = form.save()
        # 이메일 발송
        signer = TimestampSigner()  # TimestampSigner(암호화 기능) : 특정 정보를 암호화(복호화가 가능)해서 사용할 수 있다.
        signed_user_email = signer.sign(user.email)  # 유저 이메일을 받아서 sign(암호화)를 함
        signer_dump = signing.dumps(signed_user_email)  # dump(기억장치의 내용을 전부 또는 일부를 인쇄 하는것)한걸 만든다.

        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/users/verify/?code={signer_dump}'
        if settings.DEBUG:  # 개발 할때만 DEBUG(True) 사용
            print(url)

            subject = '[Pystagram]이메일 인증을 완료 해주세요.'
            message = f'다음 링크를 클릭 해주세요. <br><a href="{url}">{url}</a>'

            send_email(subject, message, user.email)

        return render(
            self.request,
            template_name='auth/signup_done.html',
            context={'user': user}
        )


# 로그인 뷰(페이지) 만들기
class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    # TODO : 나중에 메인 페이지로 Redirect 시키기
    success_url = reverse_lazy('todo:list')

    # "forms.py"에서 받은 폼에 유저의 이메일과 비밀번호가 인증(authenticate)이 되고, 활성화(is_active)가 되고
    # "form"이 valid(유효한 폼인지 판별)하면
    def form_valid(self, form):
        # 유저 데이터를 받아와서
        user = form.user
        # 로그인을 시켜줌
        login(self.request, user)

        # next로 쿼리 스트링(url)이 들어 오면 그 페이지로 보내준다.
        next_page = self.request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)

        # 그다음 "get_success_url"로 "redirect(해당 페이지로 이동)" 시켜줌
        return HttpResponseRedirect(self.get_success_url())


def verify_email(request):
    # 위의 'url' 'verify' 와 '?code='뒤에 오는 url 쿼리 파라미터로 부터 읽어온 signer_dump 받는다.
    # 유저가 접속한 url에 'code'가 있으면 그걸 가져오고 없으면 None => ''(공백)을 가져온다.
    code = request.GET.get('code', '')

    signer = TimestampSigner()
    try:
        # admin9@admin.com:1tweGe:_6Yh9SLoejopzJTIuFxNERshBgLnPUxXkCwm8muWd68(암호화 한게 맞는 건지 체크, 시간, 정보가 들어 있음)
        decoded_user_email = signing.loads(code)
        # 디코드 unsign(복호화) 시켜줌
        email = signer.unsign(decoded_user_email, max_age=60 * 30)  # "max_age" 복호화 유지 시간 설정
        # 복호화 할때 문제가 생기면 except에 걸려서 'auth/not_verified.html'에 렌더링을 시켜서 오류 났으니 다시 하라는 페이지를 보여줌
    except (TypeError, SignatureExpired):
        return render(request, 'auth/verify_failed.html')

    # 비활성화(is_active=False)된 email을 가져오고
    user = get_object_or_404(User, email=email, is_active=False)
    # 활성화(is_active=True)를 해준다
    user.is_active = True
    # 그리고 email을 저장
    user.save()
    # TODO : 나중에 Redirect 시키기   # 나중에 수정할 수 있게 체크 해논 것 : 옆에 사이드바 도구창 안 TODO에서 확인이 가능함
    # 이메일 완료 페이지로 보내준다.
    return render(request, 'auth/verify_success.html', {'user' : user})
