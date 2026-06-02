# CCM AEO Auto Publisher

CryptoCasinoMedia LinkedIn 자동 발행 파이프라인
- 월/수/금 오전 8시 자동 실행
- iGaming/Crypto RSS 피드에서 토픽 수집
- Claude가 오리지널 칼럼 생성
- LinkedIn 회사 페이지에 자동 발행
- GitHub Actions로 서버비 0원 운영

---

## 세팅 방법

### 1. 이 레포를 GitHub에 올리기
```bash
git init
git add .
git commit -m "init"
git remote add origin https://github.com/YOUR_USERNAME/ccm-aeo-publisher
git push -u origin main
```

### 2. GitHub Secrets 등록
레포 → Settings → Secrets and variables → Actions → New repository secret

| Secret 이름 | 값 |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com에서 발급 |
| `LINKEDIN_ACCESS_TOKEN` | 아래 LinkedIn 토큰 발급 참고 |
| `LINKEDIN_ORGANIZATION_ID` | 회사 페이지 URL 숫자 |

### 3. LinkedIn Access Token 발급
1. https://www.linkedin.com/developers/apps 접속
2. Create App → 회사 페이지 연결
3. Products에서 "Share on LinkedIn" + "Marketing Developer Platform" 추가
4. Auth 탭 → OAuth 2.0 토큰 발급
5. 필요 scope: `w_organization_social`, `r_organization_social`

### 4. 수동 테스트 실행
```bash
cp .env.example .env
# .env 파일에 실제 키 입력 후:
python main.py
```

### 5. GitHub Actions 자동화 확인
- 레포 → Actions 탭에서 실행 로그 확인
- 수동 실행: Actions → AEO Auto Publisher → Run workflow

---

## 발행 스케줄
월요일, 수요일, 금요일 오전 8시 (한국 시간)

## 로그 확인
`logs.json` 파일 또는 GitHub Actions → Artifacts에서 확인
