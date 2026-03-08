# 서버 실행 및 운영 가이드

이 문서는 본 도구를 서버(Linux/Ubuntu 등) 환경에서 상시 구동하기 위한 상세 절차를 설명합니다.

## 1. 서버 환경 준비

### 1.1. 필수 패키지 설치
서버에 Python 3.12+ 및 Node.js 22+가 설치되어 있어야 합니다.

```bash
# Ubuntu 기준
sudo apt update
sudo apt install -y python3-pip nodejs npm
```

### 1.2. 브라우저 의존성 설치 (Playwright)
Daum 카페 크롤링을 위해 필요한 브라우저 엔진 및 라이브러리를 설치합니다.

```bash
pip install playwright
playwright install-deps
playwright install chromium
```

## 2. 프로젝트 설정

### 2.1. 의존성 설치
```bash
# 백엔드
pip install -r backend/requirements.txt

# 프론트엔드
cd frontend
npm install
npm run build  # 운영 환경용 빌드
cd ..
```

### 2.2. 환경 변수 설정
`backend/.env` 파일을 생성하고 필요한 정보를 입력합니다. (docs/tutorial.md 참고)

## 3. 서버 실행 방법

### 3.1. 개발/테스트 모드 (콘솔 확인용)
콘솔 로그를 직접 확인하며 실행할 때 사용합니다.
```bash
chmod +x run_all.sh
./run_all.sh
```

### 3.2. 운영 모드 (백그라운드 실행)
서버 접속을 종료해도 프로그램이 계속 돌아가도록 설정합니다.

#### 방법 A: `nohup` 사용
```bash
# 백엔드 및 스케줄러 실행
PYTHONPATH=. nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
PYTHONPATH=. nohup python3 backend/scheduler.py > scheduler.log 2>&1 &

# 프론트엔드 실행 (정적 파일 서버 사용 권장)
sudo npm install -g serve
nohup serve -s frontend/build -l 3000 > frontend.log 2>&1 &
```

#### 방법 B: `PM2` 사용 (권장)
프로세스 관리가 용이합니다.
```bash
sudo npm install -g pm2

# 백엔드 등록
pm2 start "PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000" --name "insight-api"
# 스케줄러 등록
pm2 start "PYTHONPATH=. python3 backend/scheduler.py" --name "insight-scheduler"
# 프론트엔드 등록
pm2 serve frontend/build 3000 --name "insight-web" --spa

# 상태 확인
pm2 list
```

## 4. 네트워크 설정
서버의 방화벽(AWS Security Group, ufw 등)에서 다음 포트를 허용해야 합니다:
- **8000:** API 서버
- **3000:** 웹 대시보드

## 5. 로그 확인
```bash
# PM2 사용 시
pm2 logs insight-api
pm2 logs insight-scheduler
```
