# 초기 설정 및 튜토리얼 가이드

이 도구를 처음 설치한 후 대시보드를 활성화하기 위한 가이드입니다.

## 1. 초기 관리자 계정 생성
서버 터미널에서 다음 명령어를 실행하여 첫 관리자 계정을 생성합니다.

```bash
export MYSQL_USER=insight_user
export MYSQL_PASSWORD=your_secure_password
export MYSQL_DB=community_db
export SECRET_KEY=your_random_secret

PYTHONPATH=. python3 backend/scripts/create_admin.py --username admin --password your_password
```

## 2. 웹 대시보드 로그인
브라우저를 열고 `http://localhost:3000/login` (또는 서버 IP)에 접속하여 위에서 생성한 계정으로 로그인합니다.

## 3. 플랫폼 설정 (Initial Configuration)
대시보드에서 'Platforms' 메뉴를 통해 사용할 커뮤니티 플랫폼을 등록합니다.

### 3.1. Daum 카페 설정
- **Name:** `daum`
- **Config:** 필요한 경우 로그인 세션 유지 관련 설정을 JSON 형태로 입력합니다.

### 3.2. Discord 설정
- **Name:** `discord`

## 4. 수집 대상(Target) 및 채널(Channel) 등록
분석하고자 하는 구체적인 카페나 서버를 등록합니다.

### 4.1. Daum 카페 예시
1. **Target 등록:**
   - Name: `특정 카페 이름`
   - Target URL: `https://cafe.daum.net/cafe_id`
2. **Channel 등록:**
   - 해당 Target 하위에 게시판 ID를 등록합니다.
   - Identifier: `board_id` (예: `free_board`)
   - Language: `ko`

### 4.2. Discord 예시
1. **Target 등록:**
   - Name: `디스코드 서버 이름`
   - Target URL: `guild_id` (숫자로 된 ID)
2. **Channel 등록:**
   - 분석할 채널 ID를 등록합니다.
   - Identifier: `channel_id` (숫자로 된 ID)
   - Language: `ko` (혹은 채널 언어에 맞춰 설정)

## 5. 환경 변수 설정 (.env)
시스템 작동을 위해 `backend/.env` 파일에 아래 API 키들을 반드시 설정해야 합니다.

```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
SLACK_TOKEN=xoxb-...
SLACK_CHANNEL_ID=C...
DAUM_ID=your_daum_id
DAUM_PW=your_daum_password
```

## 6. 서비스 실행
`./run_all.sh` 스크립트를 통해 백엔드, 프론트엔드, 스케줄러를 동시에 실행할 수 있습니다.
스케줄러는 기본적으로 매일 오전 9시에 작동하도록 설정되어 있습니다. (변경 시 `backend/scheduler.py` 수정)
