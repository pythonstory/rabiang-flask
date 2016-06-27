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
- babel select lang html

- widget MVC
- blueprint dynamic import

- error page -> 테마/사이트 무관하게 만들 것

- blog theme work


- id: username or email (preferences)
- verify_password function must be overridden.

- 댓글에 댓글 달기
- 댓글 소셜
- 댓글 recaptcha
- 가입 후 댓글달기 기능

- email confirmation
- reset password
- change email address with confirmation

- config/factory pattern refactoring / 블루프린트 로딩 refactoring
- 회원가입 절차 (약관동의/본인인증/정보입력/이메일 인증/가입완료)

validators

- credit card
- cellphone
- local phone
- postal code
- korean registration code

- tag
삭제된 태그를 실제로 테이블에서 삭제 처리할 것
- category
- menu
- attachment management
- history
- dashboard
- gravatar 매번 필터로 계산하는 것보다 디비에 저장하는 게 나을지 생각할 것

- sidebar 기능 추가
카테고리 미구현
글보관함 i18n

* Mail
* celery
* Flask-migrate
* Fixtures


상태에 따른 게시물 노출 문제 - 사용자 권한 유무와 같이 처리할 것