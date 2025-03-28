"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# 만들어둔 "secret.json" 파일을 읽어 오고
with open(BASE_DIR / '.secret_config' / 'secret.json') as f:
    config_secret_str = f.read()

# "json" 딕셔너리 형태로 변환해서 사용한다
SECRET = json.loads(config_secret_str)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

OWN_APPS = [
    'todo',
    'member',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'django_summernote',
    'django_cleanup',
]

# 왜 Pillow는 INSTALLED_APPS 에 추가하지 않나요?
# Pillow는 Django 애플리케이션의 구성 요소가 아니므로 `INSTALLED_APPS`에 추가되지 않으며, 단지 이미지 필드나 이미지 처리와 같은 기능을 제공하는 외부 라이브러리로 사용되기 때문입니다.
# app의 구성요소로써 동작하는 라이브러리의 경우에만 INSTALLED_APPS 에 추가하여 장고에게 알려주어야 합니다.

# Application definition

INSTALLED_APPS = DJANGO_APPS + OWN_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_DIR = BASE_DIR / 'static'

STATICFILES_DIRS = [
    STATIC_DIR,
]

STATIC_ROOT = BASE_DIR / '.static_root'

# media
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# login
LOGIN_REDIRECT_URL = '/todo/'
LOGIN_URL = '/accounts/login/'

# logout
LOGOUT_REDIRECT_URL = '/todo/'


# 기본적으로 장고에 있는 유저가 아니라 "AUTH_USER_MODEL"에 적힌 내가 따로 커스텀 한 "member.User"모델을
# 사용할거 라는걸 장고에서 인식을 함
# Auth
AUTH_USER_MODEL = 'member.User' # migrate 하기 전에 항상 migrations 해주고 작업을 해야함

# Email
# from django.core.mail.backends.smtp import EmailBackend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.naver.com'   # 네이버 SMTP 서버명 적기
EMAIL_USE_SSL = True            # 네이버 보안 연결을 하겠다
EMAIL_PORT = 465                # 네이버 SMTP 포트 적기
EMAIL_HOST_USER = SECRET["email"]['HOST_USER']   # "secret.json"에 적어둔 키값 user(이메일)
EMAIL_HOST_PASSWORD = SECRET['email']['PASSWORD']   # "secret.json"에 적어둔 키값 password(비밀번호)

# email login
LOGIN_URL = '/users/login/'
LOGOUT_REDIRECT_URL = '/users/logout/'


# summernote
SUMMERNOTE_CONFIG = {
    # Or, you can set it to `False` to use SummernoteInplaceWidget by default - no iframe mode
    # In this case, you have to load Bootstrap/jQuery sources and dependencies manually.
    # Use this when you're already using Bootstrap/jQuery based themes.
    # HTML 태그 또는 JS를 수정하지 못하도록 iframe 설정
    'iframe': True,

    # You can put custom Summernote settings
    'summernote': {
        # As an example, using Summernote Air-mode
        # airMode 비활성화: 툴바를 항상 표시하도록 설정
        'airMode': False,

        # Change editor size
        # 에디터의 사이즈 정의
        'width': '100%',
        'height': '480',

        # Use proper language setting automatically (default)

        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover

        # 에디터의 툴바 메뉴 정의
        'toolbar': [
            ['style', ['style']],                       # 스타일 설정
            ['font', ['bold', 'underline', 'clear']],   # 글꼴 설정: 굵게, 밑줄, 지우기
            ['color', ['color']],                       # 색상 설정
            ['para', ['ul', 'ol', 'paragraph']],        # 문단 설정: 글머리 기호, 번호 매기기, 문단
            ['table', ['table']],                       # 표 삽입
            ['insert', ['link', 'picture', ]],          # 삽입 기능: 링크, 그림
            ['view', ['fullscreen']],                   # 보기 설정: 전체 화면
        ],

        # Or, explicitly set language/locale for editor
        'lang': 'ko-KR',    # 에디터의 언어를 한국어로 설정


        # You can also add custom settings for external plugins
        # 'print': {
        #     'stylesheetUrl': '/some_static_folder/printable.css',
        # },
        'codemirror': {
            'mode': 'htmlmixed',    # 코드미러의 모드를 htmlmixed로 설정
            'lineNumbers': 'true',  # 코드미러에서 줄 번호를 표시
            # You have to include theme file in 'css' or 'css_for_inplace' before using it.
            'theme': 'monokai',     # 코드미러의 테마를 monokai로 설정
        },
    },

    # Require users to be authenticated for uploading attachments.
    'attachment_require_authentication': True,


    # You can completely disable the attachment feature.
    'disable_attachment': False,

    # Set to `False` to return attachment paths in relative URIs.
    'attachment_absolute_uri': True,

    # test_func in summernote upload view. (Allow upload images only when user passes the test)
    # https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin

    # You can add custom css/js for SummernoteWidget.
}