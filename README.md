# **AnotherClass101🌷** #

진행기간: 2020년 12월 28일 ~ 2021년 1월 8일

<홈페이지 메인화면 사진>

## 🌷**프로젝트 소개**

> 안녕하세요. 'AnotherClass101'는 WECODE 2차 프로젝트 학습용으로 제작된 '클래스101'클론 프로젝트입니다. 클래스101은 다양한 분야의 크리에이터에서 여러 활동을 영상으로 배울 수 있게 돕는 온라인 클래스 플랫폼입니다. 이번 클론 프로젝트에서는 회원가입과 로그인, 마이페이지를 포함하여 메인화면, 크리에이터 생성등의 내용을 구현했습니다.

## 🌷**프로젝트 시연영상**
https://youtu.be/tagQh4wZ0B4

## 🌷 프로젝트 참가자 (Front & Back)

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/285c96b4-ac3a-40d4-a616-196f2821f194/2.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/285c96b4-ac3a-40d4-a616-196f2821f194/2.jpg)

### **👩‍👧‍👧FrontEnd**

김별이, 박소윤, 한민아

### 👩‍👦‍👦 **BackEnd**

김민철, 석여주(PM), 이재혁

---

## 🌷**기술 스택**

### **FrontEnd**

> HTML(JSX) / JavaScript (ES6) / React (CRA 세팅) / Styled-Component / Hooks(useState / useEffect / useRef) / Redux / React-Router / asiox

### **BackEnd**

> Python / Django / CORS Header / Bcrypt / PyJWT / MySQL / AqueryTool (데이터베이스 모델링) / Postman,Httpie (API 관리) / AWS(서버 및 DATABASE관리) / Django-seed및 Faker

### **협업 도구**

> Slack / Git + GitHub / [Trello](https://trello.com/b/9SEvYOoX/anotherclass101)를 이용, 일정관리 및 작업 현황 확인

---

# **⭐️ 구현한 기능**

## **🌱 Frontend**

### **회원가입 & 로그인 (SignUp & SignIn)**

- 회원 가입 & 로그인 아이디 및 패스워드 유효성 검사
- 문자 인증을 통한 핸드폰 번호 검증
- 카카오 소셜 로그인 구현
- 반복적으로 사용되는 타이틀, 텍스트 필드, 버튼, 라벨 컴포넌트 세분화 및 컨텐츠 data 분리하여 관리

### 마이 페이지

- API로 유저 정보를 받아와 마이페이지 적용
- 마이페이지 유저 정보 클릭시 상세 마이페이지 이동
- 상세 마이페이지 유저 정보 및 프로필 사진 수정 기능 구현
- `history.push` 를 통해 페이지 이동시 props 넘겨주는 방식 구현

### Header

- `Token` 유무에 따라 레이아웃 변경. (로그인성공 ⇒ 주문및배송/내 쿠폰/내 클래스 추가됨)
- `Token` 유무에 따라 페이지 이동 통제.
( 로그인 안되어 있을시 ⇒ 다른 메뉴로  넘어가려면 "로그인 후 이용가능한 서비스 입니다" 라는 알람과 동시에 로그인 페이지로 이동)
- `useHistory`  사용하여 페이지 이동.
- `Styled-Component` 로 스타일을 `props`  로 넘겨주어 `Modal`  통제.
- `on-click` 이벤트로 소메뉴 모달창 띄우기.

### 메인 **페이지**

- 반복적으로 쓰이는 부분 `Component` 로 분리해서 만든후 재사용.
- 레이아웃이 비슷하지만 조금씩만 바뀌는 부분에 대해서는 조건부 랜더링 사용해서 통제.
- $ 단위로 오는 데이터 ⇒ ₩ 단위로 바꿔주기.
- `String`  으로 오는 숫자 데이터 `Number` 로 바꿔주기.
- 좋아요 이모티콘 누를시 숫자도 +1 되도록 로직구현.
- Carousel 슬라이더 라이브러리 안쓰고 직접 구현.
- 상품 이름 클릭시 디테일페이지로 이동

### 크리에이터 센터 페이지

- `FormData` 를 사용하여 이미지 및 텍스트 업로드 구현.
- `Styled-Component`를 사용하여 component 재사용을 활용한
유지보수를 생각하여 구현
- `API` `post & get` 데이타 통신으로 폼데이타 전송구현.
- 페이지당 데이타 값을 하나의 `Component`에 담아 동시 값 출력 구현.
- Redux를 활용하여 `store component` 를 연결로 활성화하여 데이터 값의 setState적용
- Slider 라이브러리 사용하지않고 PrevButton & NextButton 클릭시 슬라이드 이동 구현

## **🌱 Backend**

### **모델링 구축**

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9bc10dd0-209f-486c-b2a3-390ca32b14cd/_2021-01-09_14.41.44.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9bc10dd0-209f-486c-b2a3-390ca32b14cd/_2021-01-09_14.41.44.png)

### **회원가입 & 로그인 (SignUp & SignIn) 페이지**

- bcrypt를 사용한 암호화
- JWT 로그인 구현 및 @decorator를 이용해서 토큰 인증
- Email&닉네임 정규화를 통한 Validation적용
- 회원가입시 문자인증과정 적용
- 소셜로그인 구현완료
- 로그인 및 회원가입 UnitTest 완료

### 유저 마이페이지

- AWS S3와 연동
- S3에 이미지 파일 저장 및 URL생성, 데이터베이스 저장기능 적용
- 유저 정보 변경시 데이터베이스에 적용하기

### **스토어 메인화면 페이지**

- @decorator 적용후 유저별 좋아요 기능 구현
- 인기순 필터링 적용한 강의 리스트 API작성
- 얼리버드(오픈예정인 강의) 필터링 적용한 강의 리스트 API작성
- 최근 업데이트순 필터링 적용한 강의 리스트 API작성완료
- 리스트및 좋아요 관련 UnitTest 완료

### 크리에이터 센터 페이지

- 크리에이터가 생성 중인 강의가 있을 경우 해당 정보를 불러오고, 없을 경우 새로운 강의를 생성하도록 구현
- 임의의 여러 장의 사진을 S3 서버에 올려서 순서에 맞게 처리할 수 있도록 API 구현
- 강의 카테고리, 난이도 등을 지정하여 저장하는 API 구현
- 크리에이터 관련 UnitTest 완료

### DATABASE 관련 적용내용

- Django-seed, Faker를 활용한 테스트용 데이터를 자동 생성하여 API 테스트에 활용
- AWS EC2 서버 연동및 RDS를 통한 데이터베이스 관리

---

# 🌷**후기**

## **👩‍💻Frontend**

- 김별이 [https://velog.io/@byulyikeem](https://velog.io/@byulyikeem)
- 박소윤 [https://velog.io/@ss3152ps](https://velog.io/@ss3152psy)y
- 한민아 [https://velog.io/@mincode_](https://velog.io/@mincode_)

## **🧑‍💻 Backend**

- 김민철 [https://velog.io/@mincheolk](https://velog.io/@mincheolk)
- 석여주 [https://velog.io/@fhwmqkfl](https://velog.io/@fhwmqkfl)
- 이재혁 [https://velog.io/@leejaylight](https://velog.io/@leejaylight)

---

# 🌷**레퍼런스**

- 이 프로젝트는  [클래스101](https://class101.net/)을 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것으로 해당 프로젝트 외부인이 사용할 수 없습니다.
