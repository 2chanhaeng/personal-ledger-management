# Personal Ledger Management

원티드 5차 백엔드 프리온보딩 코스 3차 과제

## 목차

- [Personal Ledger Management](#personal-ledger-management)
  - [목차](#목차)
  - [앱 소개](#앱-소개)
    - [users](#users)
    - [ledgers](#ledgers)
  - [API Docs](#api-docs)
    - [회원가입](#회원가입)
    - [로그인](#로그인)
    - [로그아웃](#로그아웃)
    - [가계부 기록 생성](#가계부-기록-생성)
    - [가계부 전체 기록 조회](#가계부-전체-기록-조회)
    - [가계부 개별 기록 조회](#가계부-개별-기록-조회)
    - [가계부 기록 수정](#가계부-기록-수정)
    - [가계부 기록 삭제](#가계부-기록-삭제)
    - [가계부 기록 복원](#가계부-기록-복원)

## 앱 소개

### users

- `User`: 사용자 모델
  - `id`: 사용자의 고유한 식별자
  - `email`: 사용자의 메일 주소, 로그인 시 사용
  - `password`: 사용자의 비밀번호, 로그인 시 사용

### ledgers

- `ledgers`: 가계부 기록 모델
  - `id`: 가계부 기록의 고유한 식별자
  - `amount`: 사용 금액
  - `memo`: 사용 메모
  - `info`: 사용 정보
  - `created_at`: 가계부 기록 생성 시간
  - `deleted_at`: 가계부 기록 삭제 시간, Null 값이면 삭제되지 않은 것

## API Docs

### 회원가입

- Method: `POST`
- Request URL: `api/v1/users/signup`
- Request Body
  - `email`: 사용자의 메일 주소
  - `password`: 사용자의 비밀번호
- Response: 성공시 201, 실패시 400

### 로그인

- Method: `POST`
- Request URL: `api/v1/users/login`
- Request Body
  - `email`: 사용자의 메일 주소
  - `password`: 사용자의 비밀번호
- Response: 성공시 Response Body에 `access_token`을 포함한 200, 실패시 400

### 로그아웃

- Method: `POST`
- Request URL: `api/v1/users/logout`
- Request Body: 없음
- Response: 성공시 200 OK, 실패시 401 Unauthorized

### 가계부 기록 생성

- Method: `POST`
- Request URL: `api/v1/ledgers`
- Request Body:
  ```json
  {
    "amount": 사용 금액,
    "memo": 사용 메모,
    "info": {
        사용 정보1: 세부 내용1,
        ...
    }
  }
  ```
- Response: 성공시 201, 실패시 400

### 가계부 전체 기록 조회

- Method: `GET`
- Request URL: `api/v1/ledgers`
- Reponce Body:
  ```json
  [
    {
      "id": 가계부 기록의 고유한 식별자,
      "amount": 사용 금액,
      "created_at": 가계부 기록 생성 시간,
    },
    ...
  ]
  ```

### 가계부 개별 기록 조회

- Method: `GET`
- Request URL: `api/v1/ledgers/<ledger_id>`
- Reponse Body:
  ```json
  {
    "id": 가계부 기록의 고유한 식별자,
    "amount": 사용 금액,
    "memo": 사용 메모,
    "info": {
        사용 정보1: 세부 내용1,
        ...
    },
    "created_at": 가계부 기록 생성 시간
  }
  ```

### 가계부 기록 수정

- Method: `PATCH`
- Request URL: `api/v1/ledgers/<ledger_id>`
- Request Body:
  ```json
  {
    "id": 가계부 기록의 고유한 식별자,
    "amount": 수정된 사용 금액,
    "memo": 수정된 사용 메모,
    "info": {
        수정된 사용 정보1: 수정된 세부 내용1,
        ...
    }
  }
  ```

### 가계부 기록 삭제

- Method: `GET`
- Request URL: `api/v1/ledgers/<ledger_id>/delete`
- Response: 성공시 204, 실패시 400

### 가계부 기록 복원

- Method: `GET`
- Request URL: `api/v1/ledgers/<ledger_id>/undelete`
- Response: 성공시 204, 실패시 400
