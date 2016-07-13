page, article, journal, post, document, messages

cart

/shop/product/<slug>
/shop/brand
/shop/vendor
/shop/pay
/shop/cart
/shop/bookmark

/poll

* date formatting (posted on, modified on)
* pagination : parameterized

* error page -> 테마/사이트 무관하게 만들 것

* blog theme work

validators

* credit card
* cellphone
* local phone
* postal code
* korean registration code

* Mail
* celery
* Flask-migrate
* Fixtures

auth 블루프린트

* 이메일 인증(Email confirmation)
* 이메일 주소 변경시 인증(change email address with confirmation)
* 회원가입 절차 (약관동의/본인인증/정보입력/이메일 인증/가입완료)
* 로그인 내역 기록 (IP, 일시, user-agent)
* 회원 가입 금지 기능(비회원제)
* 로그인: 이메일 or 아이디 선택가능
* 해시함수 지정 가능

글쓰기

* 파일 업로드 AJAX
* 히스토리, 리비전 관리
* 첨부 파일 관리

이미지 파일업로드

* 동일 파일 이름 중복 문제
* 임의이름으로 변경 /uploads/yyyymmdd_uid/username_random/filename.ext
* 데이터베이스 경로 저장 및 첨부 이미지 파일 관리

댓글 기능

* 댓글에 댓글 달기
* 댓글 소셜
* 가입 후 댓글달기 기능

* 메뉴 구현
* 관리자 대시보드 구현
* WYSIWYG tinymce -> HTML sanitize by Bleach
* 삭제된 태그를 실제로 테이블에서 삭제 처리할 것
* 카테고리 삭제시 기존 게시물의 카테고리 null 지정 문제
* 게시물 진짜로 삭제 (erase) 기능 만들 것
* sidebar 위젯 방식(MVC)으로 구현
* 기본 롤 정보 insert_role_permission 메소드 리팩토링
* babel.localeselector, babel.timezoneselector 구현
* 자신의 게시물만 삭제 (o) -> 관리자는 삭제 가능 처리

고민 사항 (성능 관련)

* 카테고리 가져올 때 n-join eager-loading (prefetch) 처리 여부
* gravatar 매번 필터로 계산하는 것보다 디비에 저장 여부
* 태그 카운트를 post_tag 테이블에 저장하는 방안
* 모델 클래스는 Base 모델을 상속 정의 (블루프린트 공통으로 뽑기)
* Admin/Guest 롤을 매번 DB 질의하는 것에 대한 문제-캐시?
* 카테고리 부모를 자신으로 선택할 경우 validator 작성
