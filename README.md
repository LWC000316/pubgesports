# 🎮 PUBG PRO VAULT (PUBG eSports Analytics & Player Gear Archive)

> **배틀그라운드(PUBG) eSports 프로 선수 정보, 인게임 세팅(감도/해상도/FOV), 장비(기어) 아카이브 및 글로벌 대회 통계 분석 플랫폼**

---

## 🌟 프로젝트 소개

**PUBG PRO VAULT**는 PUBG eSports 프로 선수들의 상세 프로필, 인게임 감도 및 장비 세팅을 제공하고, **Twire.gg 스타일의 글로벌 대회 순위표(Leaderboard)와 선수 개인 스탯(Kills, Damage, Twire Rating 등)**을 한눈에 탐색하고 검색할 수 있는 풀스택 웹 애플리케이션입니다.

---

## 🚀 주요 기능

### 1. 🎯 PRO PLAYERS (선수 세팅 & 기어 아카이브)
- **실시간 검색 & 필터**: 선수 닉네임, 본명, 마우스 모델명 및 소속 팀별 즉시 필터링
- **선수 카드 그리드**: 팀 뱃지, 국적, 포지션, 주요 감도/DPI 스펙 및 마우스 정보 퀵 뷰
- **상세 팝업 모달 (Player Detail Modal)**:
  - 📊 **인게임 감도 뷰어**: DPI, 일반/조준/ADS 감도, 수직 배율, FOV, 해상도 및 **계산된 eDPI 게이지**
  - 🎧 **기어 랙 (Gear Rack)**: 마우스, 마우스패드, 키보드, 헤드셋/이어폰, 모니터 등 사용 장비 정보
  - 🎬 **하이라이트 영상 플레이어**: 유튜브 임베드 영상 즉시 재생
  - 🔗 **방송 플랫폼 바로가기**: 치지직, SOOP(아프리카TV), 유튜브 채널 연동

### 2. 🏆 TOURNAMENTS (Twire.gg 스타일 대회 순위표)
- PGS 4 등 글로벌/지역 대회별 상금 규모, 개최지, 기간, 티어 정보 제공
- **SUPER 룰셋 기준 그랜드 파이널 18개 매치 종합 리더보드**:
  - Rank (1~3위 하이라이트), 팀명, 지역, 🍗 WWCD(치킨 수), 킬 포인트, 순위 포인트, 토탈 점수, 획득 상금

### 3. 📊 STATS / LEADERBOARD (선수 개인 스탯 랭킹)
- **MVP 하이라이트**: 대회 최다 킬/딜량 1위 Top Fragger 및 최고 Twire Rating 선수 하이라이트
- **선수 개인 스탯 테이블**: Kills, Damage, Knocks, Assists, 헤드샷 비율(%), Twire Rating 랭킹

### 4. 🔄 LIVE DATA CRAWLER ENGINE (실시간 웹 크롤러)
- ProSettings 및 eSports Wiki 데이터 수집을 위한 Jsoup 기반 크롤링 엔진 내장
- 전체 선수 일괄 최신화 및 개별 선수 크롤링 트리거
- 터미널 스타일의 실시간 로그 뷰어 제공 및 매일 새벽 4시 자동 스케줄러 배치 동작

---

## 🛠️ 기술 스택

### Backend
- **Language**: Java 17
- **Framework**: Spring Boot 3.2.3 (Spring Web, Spring Data JPA)
- **Database**: PostgreSQL 16 (Hibernate ORM)
- **Web Crawler**: Jsoup 1.17.2
- **Scheduling**: Spring @EnableScheduling (매일 새벽 4시 자동 크롤링)

### Frontend
- **Framework / Bundler**: React 18, Vite 5
- **Icons**: lucide-react
- **Styling**: Vanilla CSS (eSports Dark Neon & Cyberpunk Glassmorphism Design System)
- **Proxy**: Vite Dev Server Proxy (/api -> http://localhost:8080)

### Infra & DevOps
- **Docker Compose**: PostgreSQL 16 컨테이너 구성

---

## 📂 프로젝트 구조

`	ext
pubgesportsanti/
├── docker-compose.yml            # PostgreSQL 컨테이너 구성
├── .gitignore                    # Git 제외 파일 설정
├── README.md                     # 프로젝트 문서
├── backend/                      # Spring Boot 3 백엔드
│   ├── build.gradle              # Gradle 빌드 설정
│   └── src/main/java/com/pubg/esports/
│       ├── domain/               # JPA 엔티티 (Player, Setting, Gear, Tournament 등)
│       ├── repository/           # JPA 리포지토리
│       ├── service/              # 비즈니스 로직 & 크롤러 서비스
│       ├── controller/           # REST API 컨트롤러
│       └── config/               # DB 시드 데이터 초기화(DataInitializer) & CORS
└── frontend/                     # React 18 + Vite 프론트엔드
    ├── package.json
    ├── vite.config.js            # 개발 서버 프록시 설정
    └── src/
        ├── App.jsx               # 메인 레이아웃 및 탭 상태 관리
        ├── index.css             # 게이밍 다크 네온 디자인 시스템
        ├── data/mockData.js      # 폴백 모의 데이터
        └── components/           # UI 컴포넌트
            ├── Header.jsx        # 네비게이션 헤더
            ├── PlayerView.jsx    # 선수 목록 & 검색
            ├── PlayerDetailModal.jsx # 상세 모달
            ├── TournamentView.jsx# 대회 순위표
            ├── StatsView.jsx     # 개인 스탯 랭킹
            └── CrawlerPanel.jsx  # 크롤러 관리 패널
`

---

## ⚙️ 로컬 실행 방법

### 1. PostgreSQL 데이터베이스 실행 (Docker)
`ash
docker compose up -d
`
*(포트: 5432 / DB: pubg_esports / 계정: pubg_user / 비밀번호: pubg_password123!)*

### 2. 백엔드 (Spring Boot) 실행
`ash
cd backend
./gradlew bootRun
# Windows: gradlew.bat bootRun
`
*(기동 시 DataInitializer에 의해 주요 프로팀 및 선수(Seoul, Salute, Inonix, Heaven, TGLTN) 시드 데이터가 자동 주입됩니다.)*

### 3. 프론트엔드 (React + Vite) 실행
`ash
cd frontend
npm install
npm run dev
`
브라우저에서 http://localhost:5173으로 접속합니다.

---

## 📡 주요 REST API 엔드포인트

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/players | 선수 목록 조회 (팀별, 닉네임 검색 지원) |
| GET | /api/players/{id} | 특정 선수 상세 정보 (세팅, 기어, 하이라이트 포함) |
| GET | /api/teams | 전체 팀 목록 조회 |
| GET | /api/tournaments | 대회 목록 조회 |
| GET | /api/tournaments/{id}/leaderboard | 특정 대회 종합 순위표 조회 |
| GET | /api/tournaments/{id}/stats | 특정 대회 선수 개인 스탯 랭킹 조회 |
| POST | /api/crawler/trigger/all | 전체 선수 데이터 크롤링 최신화 트리거 |
| POST | /api/crawler/trigger/player/{nickname} | 특정 선수 개별 크롤링 트리거 |

---

## 📄 License
This project is licensed under the MIT License.
PLAYERUNKNOWN'S BATTLEGROUNDS is a registered trademark of KRAFTON, Inc.
