from dataclasses import dataclass
from datetime import datetime

# 도메인 객체를 다루기 쉽도록 dataclass 로 선언
# 만약 유저의 이름과 이메일을 Profile이라는 도메인으로 분리하고 싶다면
# 이렇게 도메인 객체를 나눴다고 테이블을 나눌 필요는 없고 해당 profile 처럼 Id 값이 없는 도메인 객체를 값객체(VO) 라고함
# 도메인 주도 설계 에서는 핵심 도메인과 서브 도메인으로 나눔. -> 하지만 지금은 간단한 모델을 사용
#
# @dataclass
# class Profile:
#     name: str
#     email: str

@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    memo: str | None
    created_at: datetime
    updated_at: datetime