# 중간 보고서: 깃허브 원격 저장소 동기화 및 무시 파일 설정 강화

## 1. 개요
* 로컬 환경에서 추가 및 수정된 백엔드, 프론트엔드, API 파이프라인 스크립트, 수집 데이터셋, 중간 보고서 일체를 깃허브 원격 저장소에 반영함.
* 로컬 컴퓨터 고유 설정 및 불필요한 빌드 임시 파일이 원격 저장소에 유출되거나 업로드되지 않도록 무시 파일 설정을 정밀 강화함.

## 2. 무시 파일 주요 정리 내역
* 운영체제 및 로컬 시스템 캐시: .DS_Store, Thumbs.db, Desktop.ini 등
* IDE 및 에디터 설정: .idea/, .vscode/, *.iml, *.suo 등
* 백엔드 빌드 및 로그: backend/.gradle/, backend/build/, backend/*.log, application_local.yml 등
* 프론트엔드 종속성 및 빌드: frontend/node_modules/, frontend/dist/, frontend/.env.*.local, 각종 debug 로그
* 파이썬 임시 캐시 및 가상환경: __pycache__/, *.pyc, .venv/, venv/ 등
* 도커 및 데이터베이스 로컬 데이터: postgres_data/, *.h2.db

## 3. 깃 커밋 및 푸시 결과
* 원격 저장소: https://github.com/LWC000316/pubgesports.git
* 브랜치: main
* 커밋 메시지: Update gitignore and add PUBG esports regional teams, sens calculator, tournament tabs and official API pipeline
* 상태: 65개 파일 변경 및 43,652줄 추가 완료, 원격 저장소 푸시 완료
