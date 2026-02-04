# WhatIF Factory - 기술 상세 문서

**프로젝트명:** WhatIF Factory (AI 콘텐츠 생산 자동화 인프라)  
**역할:** Founder & AI Solutions Architect  
**기간:** 2025년 12월 - 현재  
**Repository:** https://github.com/JuneBay/WhatIF_ContentFactory.git (67+ commits)

---

## 📋 프로젝트 개요

다양한 맞춤 영상제작을 1인의 운영자가 제어할 수 있도록 설계된 AI 기반 엔드투엔드(End-to-End) 자동화 파이프라인으로 구축된 범용 콘텐츠 자동화 플랫폼입니다.

**핵심 가치:**
- 완전 자동화를 맹신하지 않으며, 고비용 단계마다 사람이 개입할 수 있도록 설계
- 품질을 유지하면서 불필요한 AI API 비용 낭비를 방지
- 특정 장르에 종속되지 않은 범용 구조로 설계
- 엔터테인먼트 콘텐츠뿐 아니라 제품 소개 영상이나 사용 매뉴얼과 같은 정보성 콘텐츠에도 동일한 파이프라인 적용 가능

---

## 🎯 핵심 성과 및 지표

### 1. 인력 감축
- **Before:** 기획자, 작가, 성우, 배우, 영상 편집자 등 5인 규모의 1팀
- **After:** 1인 1팀으로 완료 가능
- **절감율:** 98.9% 인건비 절감 (90인-시간 → 1인-시간)

### 2. 시간 단축
- **Before:** 12-24시간/편 (평균 18시간)
- **After:** Shorts의 경우 최대 30분/1편 제작 가능
- **개선율:** 92-96% 작업 시간 단축

### 3. 비용 감소
- **98% 비용 절감:** 영상당 $1,350 → $16 미만 (최적화 모드)
- **현재 최적화 설정:** $0.615/편 (Veo 5컷 + Flux 11장)
- **최저 비용 모드:** $0.01/편 (Pollinations + Veo)
- **기존 수동 작업 대비:** 99%+ 비용 절감

### 4. 플랫폼 다양성
- **범용 콘텐츠 파이프라인:** 단일 아키텍처로 다양한 형식 지원
  - 소셜 미디어: YouTube Shorts, Instagram Reels, TikTok 영상
  - 제품 시연: 화장품 튜토리얼, 산업 부품 쇼케이스
  - 간단 매뉴얼: 사용 가이드, 제품 설명서
  - 소비재 마케팅: 브랜드 스토리텔링, 프로모션 콘텐츠
- **산업 불문 설계:** 개인 크리에이터, 중소기업, 다품종 글로벌 기업 모두 서비스

### 5. 효율 증대
- 각 공정에 사람이 검수 및 롤백 가능하게 하여 제품 퀄리티 상승
- 단계별 진행비용 절약 가능 (실패 시 전체 재시작 불필요)

### 6. 글로벌 확장성
- **다국어 지원:** 단일 소스 → 20개국 다국어 자동화
- **절감 효과:** 1,800인-시간 → 1인-시간 (99.94% 절감)

### 7. 생산성 향상
- **Before:** 1편/수일
- **After:** 최대 24편/일 가능 (24시간 연속 작업 시)
- **향상율:** 24배 이상

---

## 🏗️ 시스템 아키텍처

### 전체 파이프라인 구조

```
[1단계] 주제선정 및 대본 생성
   ↓ (Human-in-the-Loop 체크포인트)
[2단계] TTS 음성 생성 + SRT 자막 생성
   ↓ (Human-in-the-Loop 체크포인트)
[3단계] 이미지 생성 (Flux 2.0 Pro)
   ↓ (Human-in-the-Loop 체크포인트)
[4단계] 비디오 생성 (Runway/Veo/Pollinations)
   ↓ (Human-in-the-Loop 체크포인트)
[5단계] 영상 조립 (FFmpeg)
   ↓ (Human-in-the-Loop 체크포인트)
[6단계] 다국어 번역 (20개국)
   ↓ (Human-in-the-Loop 체크포인트)
[7단계] YouTube 업로드 + 메타데이터
```

### 주요 기술적 구현

#### 1. Hybrid HITL (Human-in-the-Loop) 설계
- 완전 자동화의 오류를 방지하기 위해 공정별 체크포인트 배치
- AI의 속도와 인간의 정밀한 품질 검수를 결합한 워크플로우

#### 2. 단계별 롤백 (Granular Rollback) 시스템
- 전체 프로세스를 재시작하지 않고도 대본, 이미지, 음성 등 개별 단계만 선택적으로 수정 및 재생성
- 비용 낭비 방지 및 빠른 반복 개선 가능

#### 3. 비용 최적화 오케스트레이션
- 중복 API 호출 방지
- 리소스 분산 처리를 통해 시스템 운영비(OpEx) 최소화
- Cost-Aware Execution Checkpoints

#### 4. 멀티모달 AI 통합
- Gemini 1.5 Pro, GPT-4o, Flux, ElevenLabs 등 최신 AI 모델들을 유기적으로 결합
- 각 단계에 최적화된 AI 모델 선택

#### 5. SRT-Driven Timing 아키텍처
- 자막 타이밍을 기준으로 모든 영상/이미지 동기화
- 수동 편집 없이 자동 동기화 달성

---

## 💻 기술 스택 (Tech Stack)

### AI Models & APIs
| 카테고리 | 서비스 | 용도 | 비용 |
|---------|--------|------|------|
| **LLM** | GPT-4o (OpenAI) | 대본/프롬프트 생성 | $0.005/1K tokens |
| **LLM** | Gemini 1.5 Pro (Google) | 주제선정, 대본 | 무료 |
| **LLM** | Gemini Advanced (Veo 3.1) | 비디오 생성 | 무료 (3개/일) |
| **TTS** | ElevenLabs (Adam voice) | 음성 생성 | 무료 (Premade Voice) |
| **이미지** | Flux 2.0 Pro (Black Forest Labs) | 이미지 생성 | $0.055/장 |
| **비디오** | Runway Gen-3/Gen-4 Turbo | 비디오 생성 | $0.15/컷 |
| **자막** | Whisper AI (OpenAI) | 자막 생성 | 무료 (OpenAI 포함) |
| **번역** | OpenAI GPT-4o | 다국어 번역 | $0.005/1K tokens |

### Automation & Orchestration
- **Python 3.x:** 전체 파이프라인 오케스트레이션
- **Streamlit:** Web UI 인터페이스
- **Playwright:** 브라우저 자동화 (Runway, Veo 등)
- **n8n:** 워크플로우 자동화 (선택적)

### Video/Audio Processing
- **FFmpeg:** 비디오/오디오 믹싱, 엔코딩, 자막 삽입
- **MoviePy:** 비디오 편집
- **OpenCV:** 이미지 처리
- **Pillow:** 이미지 조작

### APIs & Services
- **YouTube Data API v3:** 메타데이터, 자막 업로드
- **Google Sheets API:** 상태 관리 (선택적)
- **Google Drive API:** 파일 저장 (선택적)
- **Google OAuth 2.0:** 인증

### Development & Deployment
- **GitHub:** 버전 관리 (67+ commits)
- **Docker:** 컨테이너화 (선택적)
- **Windows 11:** 운영 환경 최적화
- **Python-dotenv:** 환경 변수 관리
- **PyYAML:** 설정 파일

### Libraries & Utilities
- **requests:** HTTP 클라이언트
- **numpy:** 수치 연산
- **tqdm:** 진행 표시
- **colorama:** 터미널 색상
- **deep-translator:** 번역 유틸리티 (선택적)

---

## 💰 비용 구조 및 최적화

### 공정별 상세 비용 산출표

| 공정 | AI/도구 | 단가 | 사용량/편 | 비용/편 | 최적화 전략 |
|-----|---------|------|-----------|---------|------------|
| **1. 주제선정 및 대본** | Gemini 1.5 Pro | $0.00 | ~5K tokens | **$0.00** | 무료 LLM 우선 사용 |
| **2. TTS 음성** | ElevenLabs (Adam) | $0.00 | 1편 (57초) | **$0.00** | Premade voice 활용 |
| **3. SRT 자막** | Whisper AI | $0.00 | 1편 | **$0.00** | OpenAI API 포함 |
| **4. 이미지 생성** | Flux 2.0 Pro | $0.055/장 | 11장 | **$0.605** | 최소 필요 장수만 |
| **5A. 비디오 (고품질)** | Runway Gen-4 Turbo | $0.15/컷 | 11컷 | **$1.65** | 고품질 필요 시만 |
| **5B. 비디오 (무료)** | Gemini Veo 3.1 | $0.00 | 5컷 | **$0.00** | 무료 한도 활용 |
| **5C. 비디오 (최저)** | Pollinations | $0.00 | 무제한 | **$0.00** | 완전 무료 모드 |
| **6. 다국어 번역** | GPT-4o | $0.005/1K | ~2K tokens | **$0.01** | 최소 토큰 사용 |
| **7. 영상 조립** | FFmpeg | $0.00 | 1편 | **$0.00** | 오픈소스 도구 |
| **8. YouTube 업로드** | YouTube Data API | $0.00 | 20개국 | **$0.00** | 무료 할당량 내 |

### 시나리오별 총 비용

| 시나리오 | 비용/편 | 월 비용 (30편) | 특징 |
|---------|---------|---------------|------|
| **최적화 모드** (현재) | **$0.615** | **$18.45** | Veo 5컷 + Flux 11장 |
| **고품질 모드** | **$2.265** | **$67.95** | Runway 11컷 + Flux 11장 |
| **최저 비용 모드** | **$0.01** | **$0.30** | Pollinations + Veo |

### 비용 최적화 전략

#### 1. 무료 리소스 우선 활용
- ✅ Gemini 1.5 Pro 선택: GPT-4o ($0.01) 대신 → **$0.01/편 절감**
- ✅ ElevenLabs Adam voice: 유료 voice ($0.10) 대신 → **$0.10/편 절감**
- ✅ Gemini Veo 3.1 활용: Runway ($1.65) 대신 → **$1.65/편 절감**
- ✅ Whisper AI 포함: 별도 TTS→SRT 변환 비용 없음

#### 2. Cost-Aware Execution 설계
- ✅ Human-in-the-Loop 체크포인트: API 실패 시 재시도로 낭비 방지
- ✅ 단계별 롤백 시스템: 전체 재시작 없이 실패한 단계만 재생성
- ✅ 중복 API 호출 방지: 캐싱 및 상태 관리

#### 3. 품질 vs 비용 균형
- ✅ 유연한 모드 선택: 고품질(Runway) vs 최적화(Veo) vs 최저비용(Pollinations)
- ✅ 이미지 최소화: 불필요한 생성 방지
- ✅ 다국어 번역 최적화: 20개국 번역을 단일 API 호출로 처리

---

## 🔧 해결한 주요 기술적 문제

### 1. Runway ML 크레딧 시스템 분리 문제
**문제:** 웹앱 크레딧과 API 크레딧이 완전히 별개 시스템이라는 것을 몰라 크레딧 낭비  
**해결:** dev.runwayml.com에서 API 전용 크레딧 충전 시스템 구축  
**결과:** 크레딧 낭비 100% 방지, 비용 투명성 확보

### 2. Veo 접근 방법 발견
**문제:** Veo Labs를 독립 사이트로 오인하여 접근 불가  
**해결:** Gemini Advanced 구독을 통해 Veo 3.1 접근 경로 발견  
**결과:** 무료 비디오 생성 5개/일 가능 (하루 3개 × Google One 구독)

### 3. YouTube 다국어 로컬라이징 충돌
**문제:** YouTube API의 defaultLanguage 설정 충돌로 "요건 미충족" 에러 발생  
**해결:** Read-Modify-Write 패턴 및 언어 코드 정규화(BCP-47 표준) 적용  
**결과:** 20개국 자막/메타데이터 업로드 성공률 100%

### 4. 해상도 통일 문제
**문제:** Gemini(2304×4096), Runway(720×1280) 등 다양한 해상도 혼재로 화질 저하  
**해결:** FFmpeg scale+pad(letterbox) 필터로 모든 영상을 1080×1920으로 통일  
**결과:** 일관된 고화질 출력, 비율 유지

### 5. SRT 타이밍 Gap 처리
**문제:** 자막 간 gap 시간에도 영상이 필요한데 처리 누락  
**해결:** 다음 자막 시작 시간까지 이전 영상 연장 로직 구현  
**결과:** 자연스러운 영상 흐름, 수동 편집 불필요

### 6. Human-in-the-Loop 오류 처리
**문제:** API 실패 시 전체 프로세스 중단으로 비용 낭비  
**해결:** 자동 재시도(지수 백오프), 단계별 롤백 시스템, 에러 분류(11가지 카테고리)  
**결과:** 일시적 오류로 인한 프로세스 중단 90% 감소

---

## 🚀 비즈니스 활용 용도 (Use Cases)

### 1. 기업용 솔루션
- **글로벌 제품 메뉴얼 자동화:** 부품, 화장품, 식품 등 다양한 제품 카테고리의 국제 판매용 메뉴얼을 각국 언어(20개국) 및 자막으로 자동 생성
- **기술 문서의 영상화:** CS 비용 절감
- **제품 시연 영상 대량 생산**

### 2. 대량 콘텐츠 생산
- **성경 구절, 교육 자료 등** 방대한 데이터를 시각 자료로 자동 변환
- **YouTube Shorts 등** 단편 콘텐츠 대량 제작

### 3. 글로벌 마케팅
- **한 번의 기획으로 전 세계 20개국 동시 광고 송출** 인프라
- **개인화 마케팅:** 고객별 맞춤형 영상을 수천 명에게 동시 발송하는 자동화 도구

---

## 📊 성과 비교표

| 항목 | 기존 방식 (5인 팀/수동) | 혁신 방식 (1인/자동화) | 개선율 |
|-----|----------------------|---------------------|--------|
| **작업 시간** | 12-24시간/편 (평균 18시간) | **60분 이내** | **92-96% 단축** |
| **필요 인원** | 작가, 성우, 촬영팀, 편집자, 검수 등 **5명 이상** | **아키텍트 1명** (AI 에이전트 활용) | **80% 인력 감소** |
| **총 인-시간** | **90인-시간/편** (5명 × 18시간) | **1인-시간/편** (1명 × 1시간) | **98.9% 절감** |
| **AI 비용** | N/A | **$0.48/편** (최적화 후) | $1.05 → $0.48 (54% 절감) |
| **언어 확장** | 국가별 개별 제작 필요 (20개국 × 90인-시간 = 1,800인-시간) | **20개국 언어** 자동 생성 (1인-시간) | **99.94% 절감** |
| **생산성** | 1편/수일 | **최대 24편/일** (24시간 연속) | **24배 이상 향상** |
| **촬영 비용** | 장소 섭외, 진행비용, 인물/식사비용 등 | **$0** (AI 생성) | **100% 절감** |

---

## 💡 Resume/이력서용 핵심 포인트

### 영문 (English)
- Built and operated a production-grade AI content automation pipeline supporting both human-in-the-loop and full automation modes
- Designed cost-aware execution checkpoints to control output quality and minimize wasted AI API usage during high-cost stages
- Automated the end-to-end workflow from topic ideation and scripting through TTS, subtitles, image/video generation, and publishing
- Implemented an SRT-driven timing system to synchronize narration, scene transitions, and subtitle rendering without manual editing
- Developed a domain-agnostic architecture reusable across entertainment content, educational media, product demos, and instructional manuals
- Designed the system to scale from assisted operation during experimentation to fully automated execution once quality and prompts are stabilized
- Independently architected, implemented, and operated the system as a private production workflow

### 한글 (Korean)
- 부분 자동화와 완전 자동화를 모두 지원하는 프로덕션급 AI 콘텐츠 자동화 파이프라인을 설계하고 운영함
- 고비용 공정에서 결과 품질을 통제하고 불필요한 AI API 비용 낭비를 최소화하기 위한 비용 인식 실행 체크포인트를 설계함
- 주제 기획과 대본 생성부터 TTS, 자막, 이미지·영상 생성, 게시까지 이어지는 전체 제작 워크플로우를 자동화함
- 수작업 편집 없이 나레이션, 장면 전환, 자막 타이밍을 정확히 동기화하기 위해 SRT 기반 타이밍 제어 시스템을 구현함
- 엔터테인먼트, 교육 콘텐츠, 제품 소개 영상, 사용 매뉴얼 등 다양한 도메인에 재사용 가능한 범용 아키텍처를 설계함
- 실험 단계에서는 사람 개입 중심으로, 품질과 프롬프트가 안정화되면 완전 자동 실행으로 전환할 수 있도록 시스템을 설계함
- 개인용 프로덕션 워크플로우로서 시스템 전체를 단독으로 설계, 구현, 운영함

---

## 📁 관련 문서

- **GitHub Repository:** https://github.com/JuneBay/WhatIF_ContentFactory.git
- **로컬 경로:** `c:\JoonBae_Works\ContentFactory\WhatIF\WhatIF_Factory\`
- **비용 산출표:** 본 문서 "비용 구조 및 최적화" 섹션 참조
- **성과 비교표:** 본 문서 "성과 비교표" 섹션 참조

---

**작성일:** 2026-01-26  
**최종 수정:** 2026-01-26
