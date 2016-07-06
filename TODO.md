page, article, journal, post, document, messages

cart

/shop/product/<slug>
/shop/brand
/shop/vendor
/shop/pay
/shop/cart
/shop/bookmark

/poll

- date formatting (posted on, modified on)
- pagination : parameterized

- error page -> 테마/사이트 무관하게 만들 것

- blog theme work

- id: username or email (preferences)
- verify_password function must be overridden.

댓글 기능

- 댓글에 댓글 달기
- 댓글 소셜
- 댓글 recaptcha
- 가입 후 댓글달기 기능

auth 블루프린트

- 이메일 인증(Email confirmation)
- 이메일 주소 변경시 인증(change email address with confirmation)
- 회원가입 절차 (약관동의/본인인증/정보입력/이메일 인증/가입완료)
- 로그인 내역 기록 (IP, 일시, user-agent)
- 회원 가입 금지 기능(비회원제)

validators

- credit card
- cellphone
- local phone
- postal code
- korean registration code

- tag
- menu
- attachment management
- history
- dashboard

* Mail
* celery
* Flask-migrate
* Fixtures

상태에 따른 게시물 노출 문제 - 사용자 권한 유무와 같이 처리할 것
공개 게시물만 목록 노출함
게시물 detail 보기는 public 조건 아직 없음
삭제된 태그를 실제로 테이블에서 삭제 처리할 것
게시물 진짜로 삭제 (erase) 기능 만들 것
카테고리 추가시 '-'를 '&nbsp;'로 변경 할지
sidebar 위젯 방식(MVC)으로 구현
글보관함 i18n
카테고리 부모를 자신으로 선택할 경우 validator 작성
메소드별 허용 permission 지정
사용자 추가(회원가입)시 role 지정
기본 롤 정보 insert_role_permission 메소드 리팩토링
babel.localeselector, babel.timezoneselector 구현

고민 사항 (성능 관련)

- 카테고리 가져올 때 n-join eager-loading (prefetch) 처리 여부
- gravatar 매번 필터로 계산하는 것보다 디비에 저장 여부
- 태그 카운트를 post_tag 테이블에 저장하는 방안
- 모델 클래스는 Base 모델을 상속 정의 (블루프린트 공통으로 뽑기)
- Admin/Guest 롤을 매번 DB 질의하는 것에 대한 문제-캐시?
