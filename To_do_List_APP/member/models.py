from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    # 입력 받은 파라미터를 바탕으로 유저 모델을 데이터 베이스에 저장하는 메서드
    def create_user(self, email, password):
        if not email:
            raise ValueError('올바른 이메일을 입력하세요')
        # self.model : 아래 User 클래스를 의미함
        user = self.model(
            email=self.normalize_email(email)   # normalize_email : BaseUserManager 안에 있는 함수
        )
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user


    # 입력 받은 파라미터를 바탕으로 어드민 유저 모델을 데이터 베이스에 저장하는 메서드
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    name = models.CharField(max_length=100) # name은 최대 100자 까지
    email = models.EmailField(unique=True)  # email은 유니크(중복x) 속성을 가짐
    is_active = models.BooleanField(default=False)  # email 비활성화
    is_staff = models.BooleanField(default=False)   # admin 사이트 들어갈 수 있는 admin 기능

    objects = UserManager() # 위의 UserManager 클래스
    USERNAME_FIELD = 'email'    # 기본 username 필드 user대신에 email을 사용
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '유저' # 상세 이름
        verbose_name_plural = f'{verbose_name} 목록'  # 상세 이름 복수형


    # property : 함수인데 클래스 변수처럼 사용할 수 있게 해주는 것
    # user.name() => user.name 이렇게 사용할 수 있다
    # AbstractBaseUser에 있는 name 컬럼을 사용하기 위해서
    @property
    def username(self):
        return self.name


