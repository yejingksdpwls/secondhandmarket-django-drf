# 🛒 중고마켓 웹 서비스 API
사용자가 중고 물품을 등록하고 확인할 수 있는 직관적이고 편리한 중고거래 백엔드 애플리케이션입니다.

----

## 목차
[ 📌 개요 ](#-개요)

[ 📅 개발 기간 ](#-개발-기간)

[ ✨ 기능 ](#-기능)

---

## 📌 개요
**중고마켓 웹 서비스 API** 는 중고 거래를 쉽고 안전하게 진행할 수 있는 환경을 제공합니다.
회원 관리, 물품 게시, 검색, 찜하기 등 중고거래 플랫폼의 주요 기능을 제공하며, 프론트엔드 없이 API 테스트 도구(Postman, Swagger 등)로 사용 및 검증할 수 있도록 구현되었습니다.
JWT 기반 인증으로 사용자의 정보를 안전하게 보호하며, RESTful API를 활용하여 확장성과 유지보수성을 높였습니다.

#### 기술 스택
**Backend :**
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white), 
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

**Database :**
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=SQLite&logoColor=white)

**Authentication :** JWT(Simple JWT)

---

## 📅 개발 기간
프로젝트 기간: 2024년 12월 19일 ~ 2024년 12월 27일

팀 구성: 개인 프로젝트 (1인 개발)

---

## ✨ 기능
#### 1️⃣ 회원 기능
* 회원 가입
  * 사용자명, 비밀번호, 이메일, 닉네임 등 필수 정보 입력
  * 중복 검증 및 패스워드 유효성 검사
* 로그인/로그아웃
  * WT Access/Refresh 토큰 발급
  * 로그아웃 시 Refresh 토큰 블랙리스트 등록
* 프로필 조회/수정
  * 사용자의 프로필을 조회 및 수정 가능
  * 비밀번호 변경 기능 포함

#### 2️⃣ 게시 기능
* 상품 등록
  * 로그인 상태에서만 가능
  * 제목, 내용, 이미지, 가격 등의 정보를 입력하여 상품 등록
* 상품 수정/삭제
  * 작성자 본인만 수정/삭제 가능
* 상품 목록 조회
  * 페이지네이션을 적용한 상품 목록 제공
  * 로그인 없이도 조회 가능
* 상품 검색
  * 제목, 내용, 작성자 기준으로 검색 가능

#### 3️⃣ 기타
* 이미지 업로드
  * 상품 등록 시 이미지를 함께 업로드 가능
  * 업로드된 이미지는 지정된 경로에 저장
* 인증 및 보안
  * JWT 기반 인증으로 사용자 정보 보호
  * 비밀번호 암호화 저장 및 검증

---

## 🔥 추가 구현 계획 (Optional)
* **실제 거래 기능 :** 실제로 등록된 물건을 구매/판매가 되는 기능 추가 
