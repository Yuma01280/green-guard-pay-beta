from html import escape
import pandas as pd
import streamlit as st


def get_ai_response(prompt: str) -> str:
    # 데이터 연동 필요: 추후 LLM 백엔드와 연결할 위치입니다.
    return f"[데모 답변] 입력하신 '{prompt}'에 대한 정밀 분석 결과입니다. 청구 금액이 평소 납부액 대비 약 10배 폭증했으며, 고지서 상 주소지가 '청계천로 100'이나 청구 기관 등록 주소와 불일치하는 정황이 포착되었습니다. 자동이체 승인 보류를 추천해 드립니다."


BRAND_NAME = "BlueGuard Pay"
BRAND_AI = "BlueGuard Pay AI"

# 프로필 필드 정의
PROFILE_FIELDS = [
    {"label": "이름", "key": "name", "default": "김그린"},
    {"label": "전화번호", "key": "phone", "default": "010-1234-5678"},
    {"label": "이메일", "key": "email", "default": "greenguard@example.com"},
    {"label": "주소", "key": "address", "default": "서울시 중구 청계천로 100"},
]

FEATURE_SUGGESTIONS = [
    "요금 폭증 알림",
    "주소지 불일치 감지",
    "자동이체 보류",
    "고지서 자동 분석",
]

BILL_DATA = {
    "수도요금": {
        "6개월": [38000, 41000, 39500, 44000, 52000, 402000],
        "1년": [35000, 36200, 38000, 41000, 39500, 44000, 46200, 48900, 52000, 54800, 60300, 402000],
    },
    "전기요금": {
        "6개월": [68000, 73000, 89000, 92000, 86000, 108000],
        "1년": [51000, 56000, 62000, 68000, 73000, 89000, 92000, 86000, 94000, 97000, 101000, 108000],
    },
    "가스요금": {
        "6개월": [42000, 39000, 31000, 28000, 35000, 61000],
        "1년": [76000, 69000, 58000, 42000, 39000, 31000, 28000, 35000, 41000, 48000, 55000, 61000],
    },
}

MOCK_BILL_PAYLOAD = {
    "email": "demo@nexus.com",
    "category": "가스비",
    "amount": 150000,
    "address": "서울시 강남구 테헤란로 123",
}


def mock_process_bill(bill_payload: dict | None = None) -> dict:
    # 데이터 연동 필요: 추후 process_bill API 응답으로 대체할 mock 결과입니다.
    payload = bill_payload or MOCK_BILL_PAYLOAD
    return {
        "hold": True,
        "has_anomaly": True,
        "status": "hold",
        "message": "고지서 주소와 등록 주소가 일치하지 않습니다.",
        "bill": payload,
    }


def send_bill_to_backend(bill_payload: dict) -> dict:
    # 데이터 연동 필요: 실제 requests.post 호출은 백엔드 연결 단계에서 구현합니다.
    return mock_process_bill(bill_payload)


st.set_page_config(
    page_title=f"{BRAND_NAME} Beta",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 세련되고 깔끔한 화이트/블루 CSS 테마 + 마이페이지 스타일 + 파일 업로드 & 히스토리 리팩토링 CSS
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800&display=swap');

* {
  font-family: 'Noto Sans KR', sans-serif;
  box-sizing: border-box;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
  background: #FFFFFF !important;
  color: #0D1117;
}

[data-testid="stSidebar"] {
  background: #F8F9FC !important;
  border-right: 1px solid #E8EBF2 !important;
  z-index: 1000 !important;
}

[data-testid="stSidebar"] > div:first-child {
  padding: 0 !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
  min-height: calc(100vh - 24px);
}

[data-testid="stAppViewContainer"] > .main > .block-container {
  max-width: 1160px;
  padding: 2.45rem 2.2rem 12.5rem;
}

#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] {
  visibility: visible !important;
  background: rgba(255, 255, 255, 0.72) !important;
  backdrop-filter: blur(10px);
}
[data-testid="stToolbar"] {
  visibility: visible !important;
  display: flex !important;
}
[data-testid="stAppDeployButton"] {
  display: none !important;
}
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] *,
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapsedControl"] *,
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] * {
  visibility: visible !important;
  opacity: 1 !important;
}

.mini-sidebar-rail {
  position: fixed;
  inset: 0 auto 0 0;
  width: 56px;
  z-index: 900;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 12px 8px 16px;
  background: #FFFFFF;
  border-right: 1px solid #E8EBF2;
  box-shadow: 8px 0 20px rgba(15, 23, 42, 0.04);
}
.mini-rail-top,
.mini-rail-bottom {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.mini-rail-logo,
.mini-rail-icon,
.mini-rail-profile {
  position: relative;
  width: 38px;
  height: 38px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #334155;
  text-decoration: none !important;
  font-size: 18px;
  line-height: 1;
  transition: background 0.18s ease, color 0.18s ease, transform 0.18s ease;
}
.mini-rail-logo {
  border-radius: 50%;
  background: #2563EB;
  color: #FFFFFF;
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.18);
}
.mini-rail-profile {
  border-radius: 50%;
  background: #EEF2FF;
  color: #2563EB;
  border: 1px solid #C7D2FE;
  font-size: 16px;
}
.mini-rail-icon:hover,
.mini-rail-profile:hover {
  background: #EEF4FF;
  color: #2563EB;
  transform: translateY(-1px);
}
.mini-rail-alert {
  color: #D96A5E;
  background: #FFF1EF;
}
.mini-rail-alert::after {
  content: "";
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #D96A5E;
  border: 2px solid #FFFFFF;
}
.mini-rail-alert.blink::after {
  animation: anomalyPulse 1.1s ease-in-out infinite;
}

/* 입력창 디자인 */
[data-testid="stTextInput"] {
  margin-bottom: 0 !important;
}

[data-testid="stTextInput"] [data-baseweb="input"] {
  min-height: 46px !important;
  border: 1px solid #D7E2F5 !important;
  border-radius: 24px !important;
  background: #F8F9FC !important;
  box-shadow: none !important;
  outline: none !important;
  overflow: hidden !important;
}

[data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
  border-color: #BFD0FF !important;
  background: #FFFFFF !important;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08) !important;
  outline: none !important;
}

[data-testid="stTextInput"] [data-baseweb="input"] > div,
[data-testid="stTextInput"] [data-baseweb="input"] > div:focus,
[data-testid="stTextInput"] [data-baseweb="input"] > div:focus-within {
  border: 0 !important;
  border-radius: inherit !important;
  background: transparent !important;
  box-shadow: none !important;
  outline: none !important;
  padding: 0 !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextInput"] input:focus {
  min-height: 44px !important;
  border: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  outline: none !important;
  padding: 0 18px !important;
  color: #0D1117 !important;
  font-size: 15px !important;
}

[data-testid="stSidebar"] [data-testid="stTextInput"] [data-baseweb="input"] {
  border-color: #CFE0FF !important;
  background: #FFFFFF !important;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.06) !important;
}

/* 둥근 아이콘 버튼 스타일 */
[data-testid="stButton"] button,
[data-testid="stButton"] > button,
button {
  border-radius: 24px !important;
  border: 1px solid #C7D2FE !important;
  background: #EEF2FF !important;
  color: #2563EB !important;
  font-weight: 700 !important;
  min-height: 40px;
  box-shadow: none !important;
  outline: none !important;
  transition: all 0.15s !important;
}
[data-testid="stButton"] button:hover,
[data-testid="stButton"] > button:hover,
button:hover {
  background: #E0E7FF !important;
  border-color: #2563EB !important;
}
[data-testid="stButton"] button:focus,
[data-testid="stButton"] > button:focus,
button:focus {
  border-color: #9DB8FF !important;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08) !important;
  outline: none !important;
}

/* 새 채팅 & 돋보이는 동작 전용 블루 버튼 스타일 */
.new-chat-btn [data-testid="stButton"] > button,
.new-chat-btn [data-testid="stButton"] button,
button[kind="primary"] {
  border-radius: 8px !important;
  border: none !important;
  background: #2563EB !important;
  color: #FFFFFF !important;
  font-weight: 600 !important;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
}
.new-chat-btn [data-testid="stButton"] > button:hover,
.new-chat-btn [data-testid="stButton"] button:hover,
button[kind="primary"]:hover {
  background: #1D4ED8 !important;
  color: #FFFFFF !important;
}

/* 돌아가기 및 보조 버튼 */
.back-btn [data-testid="stButton"] > button {
  border-radius: 8px !important;
  background: transparent !important;
  color: #6B7280 !important;
  border: 1px solid #E2E6F0 !important;
  font-size: 13px !important;
}

/* 파일 업로드 기본 위젯은 데모 화면에서 사용하지 않습니다. */
[data-testid="stFileUploader"],
[data-testid="stFileUploadDropzone"],
[data-testid="uploadedFileData"] {
  display: none !important;
}

/* 채팅 하단 고정 바 */
html, body,
[data-testid="stAppViewContainer"] {
  overflow-x: hidden !important;
}

.st-key-chat_input_bar {
  position: fixed !important;
  bottom: 28px !important;
  left: calc(280px + (100vw - 280px - min(1480px, calc(100vw - 360px))) / 2) !important;
  width: min(1480px, calc(100vw - 360px)) !important;
  max-width: min(1480px, calc(100vw - 360px)) !important;
  z-index: 850 !important;
  background: #FFFFFF !important;
  border: 1px solid #D7E2F5 !important;
  border-radius: 28px !important;
  box-shadow: 0 12px 34px rgba(37, 99, 235, 0.10) !important;
  padding: 10px 12px !important;
}

.st-key-chat_input_bar [data-testid="stHorizontalBlock"] {
  align-items: center !important;
  gap: 10px !important;
}

.st-key-chat_input_bar [data-testid="column"] {
  min-width: 0 !important;
  padding: 0 !important;
}

/* + 버튼 크기 고정 */
.st-key-chat_attach_demo [data-testid="stButton"] button,
.st-key-chat_attach_demo [data-testid="stButton"] > button {
  width: 58px !important;
  min-width: 58px !important;
  max-width: 58px !important;
  min-height: 46px !important;
  height: 46px !important;
  padding: 0 !important;
  border-radius: 23px !important;
  background: #EEF4FF !important;
  border-color: #C7D2FE !important;
  color: #2563EB !important;
}

.st-key-chat_input [data-testid="stTextArea"] {
  margin: 0 !important;
  width: 100% !important;
}

.st-key-chat_input [data-baseweb="textarea"],
.st-key-chat_input [data-baseweb="textarea"]:focus,
.st-key-chat_input [data-baseweb="textarea"]:focus-visible,
.st-key-chat_input [data-baseweb="textarea"]:focus-within,
.st-key-chat_input [data-baseweb="textarea"]:active,
.st-key-chat_input [data-baseweb="textarea"] *,
.st-key-chat_input [data-baseweb="textarea"] *:focus,
.st-key-chat_input [data-baseweb="textarea"] *:focus-visible,
.st-key-chat_input [data-baseweb="textarea"] *:focus-within,
.st-key-chat_input [data-baseweb="textarea"] *:active,
.st-key-chat_input [data-testid="stTextArea"] > div,
.st-key-chat_input [data-testid="stTextArea"] > div:focus,
.st-key-chat_input [data-testid="stTextArea"] > div:focus-visible,
.st-key-chat_input [data-testid="stTextArea"] > div:focus-within,
.st-key-chat_input [data-testid="stTextArea"] > div:active {
  border-color: transparent !important;
  background: transparent !important;
  box-shadow: none !important;
  outline: none !important;
  outline-color: transparent !important;
}

.st-key-chat_input [data-testid="stTextArea"] textarea {
  min-height: 46px !important;
  height: auto !important;
  max-height: 132px !important;
  field-sizing: content !important;
  resize: none !important;
  overflow-y: auto !important;
  white-space: pre-wrap !important;
  overflow-wrap: anywhere !important;
  word-break: break-word !important;
  caret-color: #1D4ED8 !important;
  border: 1px solid #D7E2F5 !important;
  border-radius: 22px !important;
  background: #F8F9FC !important;
  box-shadow: none !important;
  outline: none !important;
  outline-color: transparent !important;
  appearance: none !important;
  -webkit-appearance: none !important;
  padding: 12px 16px !important;
  color: #0D1117 !important;
  font-size: 15px !important;
  line-height: 1.5 !important;
}

.st-key-chat_input [data-testid="stTextArea"] textarea:focus,
.st-key-chat_input [data-testid="stTextArea"] textarea:focus-visible,
.st-key-chat_input [data-testid="stTextArea"] textarea:active {
  background: #FFFFFF !important;
  border-color: #BFD0FF !important;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08) !important;
  outline: none !important;
  outline-color: transparent !important;
}

.chat-send-demo-button {
  min-height: 46px;
  height: 46px;
  border-radius: 23px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 18px;
  background: linear-gradient(135deg, #2563EB, #3B82F6);
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 800;
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.20);
  user-select: none;
  white-space: nowrap;
}

.chat-attach-note {
  margin: 0 0 8px 8px !important;
  color: #2563EB !important;
  font-size: 13px !important;
}

/* 작은 화면 대응 */
@media (max-width: 900px) {
  [data-testid="stAppViewContainer"] > .main > .block-container {
    padding-bottom: 12rem !important;
  }

  .st-key-chat_input_bar {
    left: 72px !important;
    width: calc(100vw - 90px) !important;
    max-width: calc(100vw - 90px) !important;
    bottom: 24px !important;
    padding: 8px !important;
  }
}

/* 말풍선 디자인 */
.bubble-ai {
  background: #FFFFFF;
  border: 1px solid #E8EBF2;
  border-radius: 4px 16px 16px 16px;
  padding: 14px 18px;
  font-size: 15px;
  line-height: 1.75;
  color: #1A1A2E;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  margin-bottom: 4px;
  text-align: left;
}
.bubble-user {
  background: #2563EB;
  border-radius: 16px 4px 16px 16px;
  padding: 14px 18px;
  font-size: 15px;
  line-height: 1.75;
  color: #FFFFFF;
  text-align: left;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
}
.user-bubble-wrap {
  display: flex;
  justify-content: flex-end;
  margin: 15px auto;
  width: min(760px, 100%);
}
.ai-bubble-wrap {
  display: flex;
  justify-content: flex-start;
  margin: 15px auto;
  width: min(760px, 100%);
}
.msg-label { font-size: 11px; color: #9CA3AF; font-weight: 600; margin-bottom: 5px; text-align: left; }
.msg-label-right { font-size: 11px; color: #9CA3AF; font-weight: 600; margin-bottom: 5px; text-align: right; }

/* 최근 대화 히스토리 아이템 디자인 스타일링 */
.recent-history-container {
  width: 100% !important;
  padding: 0 18px !important;
  margin-top: 18px !important;
  text-align: left !important;
}

.recent-label {
  width: 100% !important;
  padding: 0 0 12px 0 !important;
  text-align: left !important;
  color: #9CA3AF !important;
  font-size: 12px !important;
  font-weight: 800 !important;
  letter-spacing: 0 !important;
}

.recent-history-container [data-testid="stButton"] {
  width: 100% !important;
  display: block !important;
  text-align: left !important;
}

.recent-history-container [data-testid="stButton"] button,
.recent-history-container [data-testid="stButton"] > button,
[class*="st-key-history_item_"] [data-testid="stButton"] button,
[class*="st-key-history_item_"] [data-testid="stButton"] > button {
  border: none !important;
  background: transparent !important;
  color: #334155 !important;
  font-weight: 650 !important;
  font-size: 14px !important;
  text-align: left !important;
  justify-content: flex-start !important;
  align-items: center !important;
  padding: 8px 0 !important;
  min-height: 34px !important;
  height: 34px !important;
  border-radius: 8px !important;
  box-shadow: none !important;
  width: 100% !important;
  display: flex !important;
  margin: 0 !important;
  transition: all 0.2s !important;
}

.recent-history-container [data-testid="stButton"] button:hover,
.recent-history-container [data-testid="stButton"] > button:hover,
[class*="st-key-history_item_"] [data-testid="stButton"] button:hover,
[class*="st-key-history_item_"] [data-testid="stButton"] > button:hover {
  background: #EEF4FF !important;
  color: #2563EB !important;
}

.recent-history-container [data-testid="stButton"] button p,
[class*="st-key-history_item_"] [data-testid="stButton"] button p {
  width: 100% !important;
  margin: 0 !important;
  text-align: left !important;
  display: block !important;
}
.recent-history-container [data-testid="stButton"] button,
.recent-history-container [data-testid="stButton"] > button,
[class*="st-key-history_item_"] [data-testid="stButton"] button,
[class*="st-key-history_item_"] [data-testid="stButton"] > button {
  border: none !important;
  background: transparent !important;
  color: #334155 !important;
  font-weight: 650 !important;
  font-size: 14px !important;
  text-align: left !important;
  justify-content: flex-start !important;
  padding: 8px 6px !important;
  min-height: 34px !important;
  height: 34px !important;
  border-radius: 8px !important;
  box-shadow: none !important;
  width: 100% !important;
  transition: all 0.2s !important;
}
.recent-history-container [data-testid="stButton"] button:hover,
.recent-history-container [data-testid="stButton"] > button:hover,
[class*="st-key-history_item_"] [data-testid="stButton"] button:hover,
[class*="st-key-history_item_"] [data-testid="stButton"] > button:hover {
  background: #EEF4FF !important;
  color: #2563EB !important;
}
.recent-history-container [data-testid="stButton"] button p,
[class*="st-key-history_item_"] [data-testid="stButton"] button p {
  width: 100%;
  text-align: left;
}
.sidebar-data-note {
  padding: 6px 14px 0;
  color: #C4CAD6;
  font-size: 12px;
  font-weight: 650;
}

/* 웰컴 화면 */
.welcome-screen {
  min-height: 62vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 80px;
  padding-bottom: 20px;
}
.welcome-label { font-size: 13px; color: #2563EB; font-weight: 700; margin-bottom: 16px; letter-spacing: 0.05em; }
.welcome-title { font-size: 42px; font-weight: 800; color: #0D1117; margin-bottom: 12px; text-align: center; letter-spacing: -1px; }
.welcome-sub { font-size: 15px; color: #6B7280; text-align: center; }

/* 프로필 및 마이페이지 카드 */
.card-box {
  background: #FFFFFF;
  border: 1px solid #E8EBF2;
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}
.mypage-name { font-size: 24px; font-weight: 700; color: #0D1117; }
.mypage-role { font-size: 13px; color: #9CA3AF; margin-top: 3px; }
.avatar-lg {
  width: 68px; height: 68px; border-radius: 50%;
  background: #EEF2FF; border: 3px solid #C7D2FE;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px; font-weight: 700; color: #2563EB;
}
.section-title {
  font-size: 12px; font-weight: 700; color: #9CA3AF;
  letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 14px;
}
.info-input {
  width: 100%; border: none; border-bottom: 1.5px solid #E2E6F0;
  padding: 10px 4px; font-size: 15px; color: #374151;
  background: transparent; outline: none; margin-bottom: 8px;
}
.info-input:focus { border-bottom-color: #2563EB; }
.transfer-tag {
  display: flex; align-items: center;
  background: #EEF2FF; border: 1px solid #C7D2FE;
  border-radius: 20px; padding: 8px 18px;
  font-size: 14px; color: #2563EB; font-weight: 500;
  margin-bottom: 8px; cursor: pointer;
}
.add-tag {
  border: 1.5px dashed #C7D2FE; border-radius: 20px;
  padding: 8px 18px; font-size: 13px; color: #9CA3AF;
  text-align: center; cursor: pointer; display: block;
  margin-top: 15px; text-decoration: none !important;
}
.add-tag:hover {
  background: #F8FAFF !important;
  border-color: #AFC4FF !important;
  color: #64748B !important;
}
.st-key-add_bill_utility [data-testid="stButton"] button,
.st-key-add_bill_utility [data-testid="stButton"] > button {
  border: 1.5px dashed #C7D2FE !important;
  border-radius: 20px !important;
  background: transparent !important;
  color: #9CA3AF !important;
  box-shadow: none !important;
  font-size: 13px !important;
  font-weight: 650 !important;
  justify-content: center !important;
  min-height: 38px !important;
  height: 38px !important;
  margin-top: 15px !important;
}
.st-key-add_bill_utility [data-testid="stButton"] button:hover,
.st-key-add_bill_utility [data-testid="stButton"] > button:hover {
  background: #F8FAFF !important;
  border-color: #AFC4FF !important;
  color: #64748B !important;
}

/* 위험 고지(Risk Card) 리디자인 */
.risk-card {
  width: min(760px, 100%);
  margin: 20px auto;
  border: 1px solid #FFCDD2;
  border-radius: 14px;
  background: #FFEBEE;
  padding: 22px;
  box-shadow: 0 8px 24px rgba(211, 47, 47, 0.06);
}
.risk-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.pill {
  display: inline-flex;
  min-height: 28px;
  align-items: center;
  border-radius: 999px;
  padding: 0 12px;
  font-size: 12px;
  font-weight: 700;
}
.risk-level { background: #D32F2F; color: #FFFFFF; }
.risk-status { background: #1976D2; color: #FFFFFF; }
.safe-chip { background: #E3F2FD; color: #1976D2; }
.risk-message {
  margin: 12px 0;
  color: #2C3E50;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.6;
  text-align: left;
}
.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}
.risk-tag {
  border: 1px solid #FFCDD2;
  border-radius: 999px;
  background: #FFFFFF;
  color: #C62828;
  padding: 5px 11px;
  font-size: 12px;
  font-weight: 700;
}
.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 16px;
}
.detail-box {
  border: 1px solid #FFCDD2;
  border-radius: 8px;
  background: #FFFFFF;
  padding: 12px;
  text-align: left;
}
.detail-box strong { display: block; color: #C62828; font-size: 12px; }
.detail-box span { display: block; margin-top: 4px; color: #374151; font-size: 13px; }

.top-notification-spacer {
  min-height: 44px;
}
.st-key-anomaly_bell_idle [data-testid="stButton"] button,
.st-key-anomaly_bell_idle [data-testid="stButton"] > button,
.st-key-anomaly_bell_static [data-testid="stButton"] button,
.st-key-anomaly_bell_static [data-testid="stButton"] > button,
.st-key-anomaly_bell_blink [data-testid="stButton"] button,
.st-key-anomaly_bell_blink [data-testid="stButton"] > button {
  position: relative !important;
  width: 44px !important;
  height: 44px !important;
  min-height: 44px !important;
  padding: 0 !important;
  border-radius: 50% !important;
  box-shadow: none !important;
  overflow: visible !important;
  font-size: 18px !important;
}
.st-key-anomaly_bell_idle [data-testid="stButton"] button,
.st-key-anomaly_bell_idle [data-testid="stButton"] > button {
  border: 1px solid #D7E2F5 !important;
  background: #F8FAFF !important;
  color: #2563EB !important;
}
.st-key-anomaly_bell_static [data-testid="stButton"] button,
.st-key-anomaly_bell_static [data-testid="stButton"] > button,
.st-key-anomaly_bell_blink [data-testid="stButton"] button,
.st-key-anomaly_bell_blink [data-testid="stButton"] > button {
  border: 1px solid #FFC9C2 !important;
  background: #FFF1EF !important;
  color: #D96A5E !important;
}
.st-key-anomaly_bell_static [data-testid="stButton"] button::after,
.st-key-anomaly_bell_static [data-testid="stButton"] > button::after,
.st-key-anomaly_bell_blink [data-testid="stButton"] button::after,
.st-key-anomaly_bell_blink [data-testid="stButton"] > button::after {
  content: "";
  position: absolute;
  top: 7px;
  right: 7px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #D96A5E;
  border: 2px solid #FFFFFF;
}
.st-key-anomaly_bell_blink [data-testid="stButton"] button::after,
.st-key-anomaly_bell_blink [data-testid="stButton"] > button::after {
  animation: anomalyPulse 1.1s ease-in-out infinite;
}
@keyframes anomalyPulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(217, 106, 94, 0.42); }
  50% { transform: scale(1.24); box-shadow: 0 0 0 7px rgba(217, 106, 94, 0); }
}
.anomaly-dialog-card {
  width: 100%;
  min-width: 360px;
  max-width: 420px;
  margin: 4px 0 10px auto;
  border: 1px solid #FFC9C2;
  border-radius: 14px;
  background: #FFFFFF;
  padding: 18px 20px;
  box-shadow: 0 14px 34px rgba(217, 106, 94, 0.1);
  text-align: left;
}
.anomaly-dialog-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 8px;
}
.anomaly-dialog-badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  border-radius: 999px;
  background: #FFF1EF;
  color: #B84C43;
  padding: 0 11px;
  font-size: 12px;
  font-weight: 800;
}
.anomaly-dialog-status {
  color: #D96A5E;
  font-size: 12px;
  font-weight: 800;
}
.anomaly-dialog-title {
  margin: 0 0 6px;
  color: #0D1117;
  font-size: 18px;
  font-weight: 850;
}
.anomaly-dialog-message {
  margin: 0;
  color: #475569;
  font-size: 14px;
  line-height: 1.65;
  font-weight: 600;
}
.anomaly-dialog-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-top: 12px;
}
.anomaly-dialog-field {
  border: 1px solid #F2D6D1;
  border-radius: 8px;
  background: #FFF9F8;
  padding: 8px 10px;
}
.anomaly-dialog-field span {
  display: block;
  color: #94A3B8;
  font-size: 12px;
  font-weight: 650;
}
.anomaly-dialog-field strong {
  display: block;
  margin-top: 2px;
  color: #0D1117;
  font-size: 13px;
  font-weight: 800;
}
.anomaly-dialog-note {
  margin-top: 10px;
  color: #64748B;
  font-size: 12px;
  line-height: 1.55;
  font-weight: 650;
}
.st-key-check_anomaly_alert [data-testid="stButton"] button,
.st-key-check_anomaly_alert [data-testid="stButton"] > button {
  border: 0 !important;
  background: linear-gradient(135deg, #1D4ED8, #3B82F6) !important;
  color: #FFFFFF !important;
  box-shadow: 0 8px 18px rgba(29, 78, 216, 0.18) !important;
}
.st-key-approve_anomaly_alert [data-testid="stButton"] button,
.st-key-approve_anomaly_alert [data-testid="stButton"] > button {
  border: 1px solid #C7D2FE !important;
  background: #FFFFFF !important;
  color: #2563EB !important;
  box-shadow: none !important;
}

/* 지출 리포트 리얼 SVG 그래프 스타일 */
.graph-placeholder {
  position: relative;
  height: 240px;
  margin-top: 18px;
  overflow: hidden;
  border: 1px solid #E8EBF2;
  border-radius: 12px;
  background: linear-gradient(180deg, #FFFFFF 0%, #F8F9FC 100%);
  padding: 16px;
}
.graph-svg { width: 100%; height: 100%; }
.graph-grid-line { stroke: #F0F2F5; stroke-dasharray: 4 6; stroke-width: 1.5; }
.graph-axis-line { stroke: #E2E6F0; stroke-width: 2; }
.graph-dotted-line { fill: none; stroke: #2563EB; stroke-width: 4; stroke-linejoin: round; stroke-linecap: round; }
.graph-point { fill: #FFFFFF; stroke: #2563EB; stroke-width: 4; }
.graph-data-note {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #E2E6F0;
  border-radius: 6px;
  font-size: 11px;
  color: #9CA3AF;
  padding: 2px 8px;
}

/* 미니 프로필 */
.element-container:has(.sidebar-profile-anchor) {
  height: 0 !important;
  min-height: 0 !important;
  margin-top: auto !important;
  padding: 0 !important;
  overflow: hidden !important;
}
.sidebar-profile-anchor {
  display: none;
}
.sidebar-profile-rule {
  height: 1px;
  background: #E5EAF3;
  margin: 14px 12px 14px;
}
.sidebar-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 0 0 2px;
  min-height: 48px;
}
.avatar-sm {
  width: 34px; height: 34px; border-radius: 50%;
  background: #EEF2FF; border: 2px solid #C7D2FE;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: #2563EB; font-weight: 700; flex-shrink: 0;
}
.profile-name { font-size: 15px; font-weight: 800; color: #1F2937; text-align: left; line-height: 1.25; }
.profile-sub { margin-top: 3px; font-size: 12px; color: #9CA3AF; text-align: left; line-height: 1.25; }
.profile-icon-button [data-testid="stButton"] button,
.profile-icon-button [data-testid="stButton"] > button,
.st-key-to_mypage [data-testid="stButton"] button,
.st-key-to_mypage [data-testid="stButton"] > button {
  width: 40px !important;
  height: 40px !important;
  min-height: 40px !important;
  padding: 0 !important;
  border-radius: 50% !important;
  border: 1px solid #C7D2FE !important;
  background: #EEF2FF !important;
  color: #4C3F91 !important;
  box-shadow: none !important;
}
.profile-icon-button [data-testid="stButton"] button:hover,
.profile-icon-button [data-testid="stButton"] > button:hover,
.st-key-to_mypage [data-testid="stButton"] button:hover,
.st-key-to_mypage [data-testid="stButton"] > button:hover {
  background: #E0E7FF !important;
  border-color: #9DB8FF !important;
}

.attached-file-note {
  font-size: 12px;
  color: #2563EB;
  font-weight: 600;
  margin-top: 6px;
  padding-left: 10px;
  text-align: left;
}

/* 메트릭 카드 디자인 */
.metric-card {
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 1px solid #E8EBF2;
  border-radius: 12px;
  background: #FFFFFF;
  padding: 14px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.02);
}
.metric-label { color: #6B7280; font-size: 12px; font-weight: 600; }
.metric-value { margin-top: 4px; color: #0D1117; font-size: 18px; font-weight: 800; }

/* 다이얼로그 모달 스타일 */
div[data-testid="stDialog"] div[role="dialog"] {
  border-radius: 14px;
  background: #FFFFFF !important;
  color: #0D1117 !important;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
  padding: 24px !important;
}
div[data-testid="stDialog"] h2,
div[data-testid="stDialog"] h3,
div[data-testid="stDialog"] p,
div[data-testid="stDialog"] label {
  color: #0D1117 !important;
}
</style>
"""


def init_state() -> None:
    defaults = {
        "page": "chat",
        "submitted_prompt": "",
        "show_risk_result": False,
        "selected_category": "수도요금",
        "selected_period": "6개월",
        "mask_strength": 40,
        "feature_query": "",
        "open_info_dialog": False,
        "open_feature_dialog": False,
        "attached_file": None,
        "ai_response_text": "",
        "anomaly_alert": None,
        "show_anomaly_alert": False,
        "open_anomaly_dialog": False,
        "anomaly_approved": False,
        "anomaly_checked": False,
        "chat_history": ["자동이체 이상 여부", "고지서 확인"]
    }
    for field in PROFILE_FIELDS:
        defaults[field["key"]] = field["default"]

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "profile_fields_initialized" not in st.session_state:
        for field in PROFILE_FIELDS:
            current_value = str(st.session_state.get(field["key"], "")).strip()
            if not current_value:
                st.session_state[field["key"]] = field["default"]
        st.session_state.profile_fields_initialized = True

    if st.session_state.anomaly_alert is None:
        alert = send_bill_to_backend(MOCK_BILL_PAYLOAD)
        st.session_state.anomaly_alert = alert
        st.session_state.show_anomaly_alert = bool(alert.get("hold") or alert.get("has_anomaly"))


def safe_html(value: object) -> str:
    return escape(str(value))


def profile_value(key: str) -> str:
    value = str(st.session_state.get(key, "")).strip()
    return value if value else "(데이터 연동 필요)"


def mask_sensitive_value(value: str, strength: int) -> str:
    characters = list(value)
    maskable_indexes = [index for index, char in enumerate(characters) if char.isalnum()]

    if not maskable_indexes:
        return value

    mask_count = max(1, round(len(maskable_indexes) * (strength / 100)))
    start = max(0, (len(maskable_indexes) - mask_count) // 2)
    masked_indexes = set(maskable_indexes[start : start + mask_count])

    return "".join("*" if index in masked_indexes else char for index, char in enumerate(characters))


def close_dialogs() -> None:
    st.session_state.open_info_dialog = False
    st.session_state.open_feature_dialog = False
    st.session_state.open_anomaly_dialog = False


def close_anomaly_dialog() -> None:
    st.session_state.open_anomaly_dialog = False


def open_dialog(dialog_name: str) -> None:
    close_dialogs()
    if dialog_name == "info":
        st.session_state.open_info_dialog = True
    elif dialog_name == "feature":
        st.session_state.open_feature_dialog = True
    elif dialog_name == "anomaly":
        st.session_state.open_anomaly_dialog = True


def reset_chat_state() -> None:
    st.session_state.page = "chat"
    st.session_state.submitted_prompt = ""
    st.session_state.show_risk_result = False
    st.session_state.ai_response_text = ""
    st.session_state.attached_file = None
    close_dialogs()


def get_query_action() -> str:
    action = st.query_params.get("mini_action", "")
    if isinstance(action, list):
        return str(action[0]) if action else ""
    return str(action)


def clear_query_action() -> None:
    if "mini_action" in st.query_params:
        del st.query_params["mini_action"]


def handle_mini_rail_action() -> None:
    action = get_query_action()
    if not action:
        return

    close_dialogs()

    if action == "new_chat":
        reset_chat_state()
    elif action == "notify":
        alert = st.session_state.get("anomaly_alert") or {}
        alert_active = (
            bool(alert.get("hold") or alert.get("has_anomaly"))
            and st.session_state.show_anomaly_alert
            and not st.session_state.anomaly_approved
        )
        if alert_active:
            open_dialog("anomaly")
    elif action == "profile":
        close_anomaly_dialog()
        st.session_state.page = "mypage"
    elif action in {"open_sidebar", "search", "recent"}:
        close_anomaly_dialog()

    clear_query_action()
    st.rerun()


def get_bill_labels(period: str) -> list[str]:
    if period == "1년":
        return [f"{month}월" for month in range(1, 13)]
    return [f"{month}월" for month in range(1, 7)]


# 동적 SVG 리포트 지출 그래프 드로잉 함수
def render_graph_svg(category: str, period: str) -> str:
    values = BILL_DATA[category][period]
    labels = get_bill_labels(period)
    count = len(values)
    min_value = min(values)
    max_value = max(values)
    span = max(max_value - min_value, 1)
    
    # SVG 캔버스 레이아웃 좌표 매핑
    x_start = 50
    x_end = 670
    x_positions = [x_start + ((x_end - x_start) / (count - 1)) * index for index in range(count)]

    points = []
    for x_pos, value in zip(x_positions, values):
        # 160px 범위 내에서 점 플로팅 (SVG 상단 마진 30px 고려)
        y_pos = 170 - ((value - min_value) / span) * 120
        points.append((round(x_pos, 1), round(y_pos, 1)))

    point_attr = " ".join(f"{x},{y}" for x, y in points)
    circles = "\n".join(f'<circle class="graph-point" cx="{x}" cy="{y}" r="6" />' for x, y in points)
    
    label_step = 1 if period == "6개월" else 2
    label_nodes = "\n".join(
        f'<text x="{x}" y="215" text-anchor="middle" fill="#9CA3AF" font-size="11" font-weight="600">{safe_html(label)}</text>'
        for index, ((x, _), label) in enumerate(zip(points, labels))
        if index % label_step == 0
    )

    return f"""
    <div class="graph-placeholder">
      <div class="graph-data-note">데이터 연동 필요</div>
      <svg class="graph-svg" viewBox="0 0 720 230">
        <line class="graph-grid-line" x1="40" y1="50" x2="680" y2="50" />
        <line class="graph-grid-line" x1="40" y1="110" x2="680" y2="110" />
        <line class="graph-grid-line" x1="40" y1="170" x2="680" y2="170" />
        <line class="graph-axis-line" x1="40" y1="195" x2="680" y2="195" />
        <polyline class="graph-dotted-line" points="{point_attr}" />
        {circles}
        {label_nodes}
      </svg>
    </div>
    """


# ════════════════════════════════════════
# 다이얼로그 모달 내부 UI 렌더링
# ════════════════════════════════════════
def render_info_dialog_body() -> None:
    st.caption("개인정보 보호 설정")
    st.subheader("내 정보 수정")
    st.markdown(
        """
        <div style="background:#F0F4FF; border:1px solid #C7D2FE; border-radius:8px; padding:12px; margin-bottom:15px; color:#2563EB; font-size:13px; line-height:1.5;">
          화면 표시 단계에서 개인정보가 마스킹 처리됩니다. (실제 데이터 저장은 백엔드 연동이 필요합니다.)
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.mask_strength = st.slider(
        "마스킹 강도 (%)",
        min_value=10,
        max_value=80,
        step=10,
        value=st.session_state.mask_strength,
    )

    preview_cols = st.columns(2, gap="small")
    for index, field in enumerate(PROFILE_FIELDS):
        current_value = profile_value(field["key"])
        masked_value = mask_sensitive_value(current_value, st.session_state.mask_strength)
        with preview_cols[index % 2]:
            st.markdown(
                f"""
                <div style="border:1px solid #E2E6F0; border-radius:8px; padding:10px; margin-bottom:10px; background:#F8F9FC;">
                  <span style="font-size:11px; color:#6B7280; font-weight:600;">{safe_html(field["label"])}</span>
                  <strong style="display:block; margin-top:3px; color:#0D1117; font-size:13px;">{safe_html(masked_value)}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

    for field in PROFILE_FIELDS:
        st.text_input(
            field["label"],
            key=field["key"],
        )

    st.caption("(데이터 저장 시 백엔드 DB 연동 필요)")
    if st.button("수정 완료", key="close_info_dialog", use_container_width=True):
        close_dialogs()
        st.rerun()


def render_feature_dialog_body() -> None:
    st.caption(BRAND_NAME)
    st.subheader("새로운 보안 기능 추가")
    with st.form("feature_search_form"):
        st.text_input(
            "기능 검색",
            placeholder="추가하고 싶은 보호 기능을 입력해 보세요.",
            label_visibility="collapsed",
            key="feature_query",
        )
        st.form_submit_button("기능 조회", use_container_width=True)

    query = st.session_state.feature_query.strip()
    filtered = [feature for feature in FEATURE_SUGGESTIONS if query in feature] if query else FEATURE_SUGGESTIONS

    if filtered:
        for feature in filtered:
            st.markdown(
                f"""
                <div style="display:flex; justify-content:between; align-items:center; border:1px solid #E8EBF2; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                  <strong style="color:#0D1117; font-size:14px;">{safe_html(feature)}</strong>
                  <span style="color:#2563EB; font-size:11px; font-weight:600; margin-left:auto;">연동 가능</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<div style="color:#9CA3AF; text-align:center; padding:15px; border:1px dashed #E2E6F0; border-radius:8px;">해당 보호 기능은 아직 개발 중입니다.</div>', unsafe_allow_html=True)

    if st.button("다이얼로그 닫기", key="close_feature_dialog", use_container_width=True):
        close_dialogs()
        st.rerun()


def render_anomaly_dialog_body() -> None:
    alert = st.session_state.get("anomaly_alert") or {}
    bill = alert.get("bill", {})
    status_label = "HOLD" if alert.get("hold") else "ANOMALY"
    amount_value = bill.get("amount", "(데이터 연동 필요)")
    amount_text = f"{amount_value:,}원" if isinstance(amount_value, (int, float)) else str(amount_value)

    st.markdown(
        f"""
        <section class="anomaly-dialog-card" aria-label="이상치 시스템 알림">
          <div class="anomaly-dialog-top">
            <span class="anomaly-dialog-badge">시스템 알림</span>
            <span class="anomaly-dialog-status">{safe_html(status_label)}</span>
          </div>
          <h3 class="anomaly-dialog-title">이상치가 발견되었습니다.</h3>
          <p class="anomaly-dialog-message">
            고지서 주소와 등록 주소가 일치하지 않거나, 청구 금액이 비정상적으로 증가했습니다.
          </p>
          <div class="anomaly-dialog-grid">
            <div class="anomaly-dialog-field">
              <span>카테고리</span>
              <strong>{safe_html(bill.get("category", "(데이터 연동 필요)"))}</strong>
            </div>
            <div class="anomaly-dialog-field">
              <span>청구 금액</span>
              <strong>{safe_html(amount_text)}</strong>
            </div>
            <div class="anomaly-dialog-field">
              <span>이메일</span>
              <strong>{safe_html(bill.get("email", "(데이터 연동 필요)"))}</strong>
            </div>
            <div class="anomaly-dialog-field">
              <span>상태</span>
              <strong>{safe_html(alert.get("status", "(데이터 연동 필요)"))}</strong>
            </div>
          </div>
          <div class="anomaly-dialog-note">
            {safe_html(alert.get("message", "(데이터 연동 필요)"))}<br />
            고지서 주소: {safe_html(bill.get("address", "(데이터 연동 필요)"))}
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    action_col_1, action_col_2 = st.columns([1.25, 1], gap="small")
    with action_col_1:
        if st.button("이상치 확인하기", key="check_anomaly_alert", use_container_width=True):
            close_dialogs()
            st.session_state.anomaly_checked = True
            st.session_state.page = "chat"
            st.session_state.show_risk_result = True
            st.session_state.submitted_prompt = "고지서 이상치 확인"
            st.session_state.ai_response_text = (
                "[데모 답변] mock_process_bill() 응답에서 hold 및 has_anomaly가 감지되었습니다. "
                "등록 주소와 고지서 주소, 청구 금액 변동을 확인한 뒤 납부 보류를 권장합니다."
            )
            st.rerun()
    with action_col_2:
        if st.button("승인하기", key="approve_anomaly_alert", use_container_width=True):
            close_dialogs()
            st.session_state.anomaly_approved = True
            st.session_state.show_anomaly_alert = False
            st.rerun()


def render_dialogs() -> None:
    open_dialogs = [
        bool(st.session_state.open_info_dialog),
        bool(st.session_state.open_feature_dialog),
        bool(st.session_state.open_anomaly_dialog),
    ]
    if sum(open_dialogs) > 1:
        st.session_state.open_feature_dialog = False
        st.session_state.open_anomaly_dialog = False

    if st.session_state.open_info_dialog:
        if hasattr(st, "dialog"):
            @st.dialog("내 정보 수정", on_dismiss=close_dialogs)
            def info_dialog() -> None:
                render_info_dialog_body()
            info_dialog()
        else:
            with st.expander("내 정보 수정", expanded=True):
                render_info_dialog_body()

    if st.session_state.open_feature_dialog:
        if hasattr(st, "dialog"):
            @st.dialog("보안 기능 추가", on_dismiss=close_dialogs)
            def feature_dialog() -> None:
                render_feature_dialog_body()
            feature_dialog()
        else:
            with st.expander("보안 기능 추가", expanded=True):
                render_feature_dialog_body()

    if st.session_state.open_anomaly_dialog:
        if hasattr(st, "dialog"):
            @st.dialog("이상치 알림", on_dismiss=close_dialogs)
            def anomaly_dialog() -> None:
                render_anomaly_dialog_body()
            anomaly_dialog()
        else:
            with st.expander("이상치 알림", expanded=True):
                render_anomaly_dialog_body()


def render_top_notification() -> None:
    alert = st.session_state.get("anomaly_alert") or {}
    has_alert = bool(alert.get("hold") or alert.get("has_anomaly"))
    alert_active = has_alert and st.session_state.show_anomaly_alert and not st.session_state.anomaly_approved
    should_blink = alert_active and not st.session_state.anomaly_checked

    if should_blink:
        bell_key = "anomaly_bell_blink"
    elif alert_active:
        bell_key = "anomaly_bell_static"
    else:
        bell_key = "anomaly_bell_idle"

    _, bell_col = st.columns([11.2, 0.7], vertical_alignment="center")
    with bell_col:
        if st.button("🔔", key=bell_key, help="이상치 알림", use_container_width=True):
            if alert_active:
                open_dialog("anomaly")
                st.rerun()


# ════════════════════════════════════════
# 1번째 파일의 분석 카드 기능 (디자인은 2번째 화이트 테마)
# ════════════════════════════════════════
def render_risk_card() -> None:
    st.markdown(
        """
        <article class="risk-card">
          <div class="risk-card-header">
            <span class="pill risk-level">⚠️ 위험도 매우 높음</span>
            <span class="pill risk-status">자동이체 보류 추천</span>
          </div>
          <p class="risk-message">
            이번 달 수도요금이 <strong>402,000원</strong> 청구되어 최근 5개월 평균 대비 약 10배 폭증하였습니다. 또한 고지서 주소지와 청구처가 일치하지 않는 이상 징후가 확인되어 즉시 확인이 필요합니다.
          </p>
          <div class="tag-row" aria-label="감지된 위협 탐지 목록">
            <span class="risk-tag">📍 주소지 불일치 의심</span>
            <span class="risk-tag">📈 청구 금액 폭증 감지</span>
            <span class="risk-tag">🔒 BlueGuard 분석 차단</span>
          </div>
          <div class="detail-grid">
            <div class="detail-box">
              <strong>분석 탐지 대상</strong>
              <span>자동이체 등록 수도요금 청구서</span>
            </div>
            <div class="detail-box">
              <strong>스마트 추천 수칙</strong>
              <span>고지기관 청구 번호 대조 및 납부 일시 보류</span>
            </div>
          </div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def render_mini_sidebar_rail() -> None:
    alert = st.session_state.get("anomaly_alert") or {}
    alert_active = (
        bool(alert.get("hold") or alert.get("has_anomaly"))
        and st.session_state.show_anomaly_alert
        and not st.session_state.anomaly_approved
    )
    alert_class = " mini-rail-alert"
    if alert_active and not st.session_state.anomaly_checked:
        alert_class += " blink"
    if not alert_active:
        alert_class = ""

    st.markdown(
        f"""
        <nav class="mini-sidebar-rail" aria-label="접힌 사이드바 빠른 메뉴">
          <div class="mini-rail-top">
            <a class="mini-rail-logo" href="?mini_action=open_sidebar" title="사이드바 열기" aria-label="사이드바 열기">🛡</a>
            <a class="mini-rail-icon" href="?mini_action=new_chat" title="새 채팅" aria-label="새 채팅">＋</a>
            <a class="mini-rail-icon" href="?mini_action=search" title="검색 / 사이드바 열기" aria-label="검색">⌕</a>
            <a class="mini-rail-icon" href="?mini_action=recent" title="최근 항목 / 사이드바 열기" aria-label="최근 항목">◷</a>
            <a class="mini-rail-icon{alert_class}" href="?mini_action=notify" title="이상치 알림" aria-label="이상치 알림">🔔</a>
          </div>
          <div class="mini-rail-bottom">
            <a class="mini-rail-profile" href="?mini_action=profile" title="마이페이지" aria-label="마이페이지">닉</a>
          </div>
        </nav>
        """,
        unsafe_allow_html=True,
    )


# ════════════════════════════════════════
# 사이드바 레이아웃 (1번째의 기능 + 2번째의 깔끔한 디자인)
# ════════════════════════════════════════
def render_sidebar() -> None:
    with st.sidebar:
        # 상단 로고 (디자인 2 적용)
        st.markdown("""
        <div style="padding:24px 16px 12px;">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:34px;height:34px;border-radius:50%;background:#2563EB;
                            display:flex;align-items:center;justify-content:center;box-shadow: 0 4px 12px rgba(37,99,235,0.22);">
                    <span style="color:white;font-size:16px;">🛡</span>
                </div>
                <span style="font-size:16px;font-weight:800;color:#0D1117;letter-spacing:-0.5px;">BlueGuard Pay</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 대화 검색 (디자인 2 적용)
        st.text_input("대화 검색", placeholder="🔍 대화 내용 검색", label_visibility="collapsed", key="conversation_search")

        # 새 채팅 버튼 (★1번 구조의 리셋 + 2번의 스타일)
        st.markdown('<div class="new-chat-btn" style="margin: 4px 0 16px;">', unsafe_allow_html=True)
        if st.button("＋  새 채팅", use_container_width=True):
            reset_chat_state()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # 최근 내역 Presets (CSS 커스텀 디자인을 적용하여 app.py 본래의 예쁜 목록형 단추 구현)
        st.markdown('<div class="recent-history-container">', unsafe_allow_html=True)
        st.markdown('<div class="recent-label">최근</div>', unsafe_allow_html=True)
        
        # chat_history에 있는 대화 목록들을 텍스트 형태의 세련된 단추로 렌더링
        for idx, item in enumerate(st.session_state.chat_history):
            if st.button(f"💬 {item}", key=f"history_item_{idx}"):
                close_dialogs()
                close_anomaly_dialog()
                st.session_state.submitted_prompt = item
                st.session_state.show_risk_result = True
                st.session_state.page = "chat"
                with st.spinner("지출 내역을 검증하는 중..."):
                    st.session_state.ai_response_text = get_ai_response(item)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-data-note">(데이터 연동 필요)</div>', unsafe_allow_html=True)

        # 프로필 관리 및 마이페이지 전환 영역
        if st.session_state.page == "mypage":
            st.markdown('<div class="back-btn" style="margin-top: 8px;">', unsafe_allow_html=True)
            if st.button("← 메인 채팅방으로", use_container_width=True):
                close_dialogs()
                close_anomaly_dialog()
                st.session_state.page = "chat"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<span class="sidebar-profile-anchor" aria-hidden="true"></span>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-profile-rule"></div>', unsafe_allow_html=True)
        col_prof, col_btn = st.columns([4, 1.2])
        with col_prof:
            st.markdown(f"""
            <div class="sidebar-profile">
                <div class="avatar-sm">닉</div>
                <div>
                    <div class="profile-name">닉네임 님</div>
                    <div class="profile-sub">데이터 연동 필요</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            # 프로필 아이콘 클릭 시 마이페이지로 즉시 이동
            st.markdown('<div class="profile-icon-button">', unsafe_allow_html=True)
            if st.button("👤", key="to_mypage"):
                close_dialogs()
                close_anomaly_dialog()
                st.session_state.page = "mypage"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════
# 챗 허브 홈 레이아웃 (디자인 2 적용)
# ════════════════════════════════════════
def render_chat_page() -> None:
    if not st.session_state.show_risk_result:
        # 환영 웰컴 화면 (디자인 2 적용)
        st.markdown(
            f"""
            <section class="welcome-screen">
              <div class="welcome-label">{safe_html(BRAND_AI)}</div>
              <h1 class="welcome-title">무엇을 도와드릴까요?</h1>
              <p class="welcome-sub">금융 범죄와 요금 사기, 돈이 빠져나가기 전에 AI가 먼저 완벽 검증합니다.</p>
            </section>
            """,
            unsafe_allow_html=True,
        )
    else:
        # 질문 대화 기록 말풍선 렌더링
        st.markdown(
            f"""
            <div class="user-bubble-wrap">
              <div style="max-width: 75%;">
                <div class="msg-label-right">나</div>
                <div class="bubble-user">{safe_html(st.session_state.submitted_prompt)}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.ai_response_text:
            st.markdown(
                f"""
                <div class="ai-bubble-wrap">
                  <div style="max-width: 75%;">
                    <div class="msg-label">{safe_html(BRAND_NAME)}</div>
                    <div class="bubble-ai">{safe_html(st.session_state.ai_response_text)}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        # 위험 감지 결과 정밀 진단서 카드 로드
        render_risk_card()

    # 입력 컴포넌트 하단 고정 바
    with st.container(key="chat_input_bar"):
        if st.session_state.attached_file:
            st.markdown(
                f'<p class="attached-file-note chat-attach-note">📎 {safe_html(st.session_state.attached_file)} 상태입니다. (데이터 연동 필요)</p>',
                unsafe_allow_html=True,
            )

        col_file, col_text, col_send = st.columns([0.7, 10.2, 1.0], vertical_alignment="center", gap="small")

        with col_file:
            if st.button("＋", key="chat_attach_demo", help="파일 첨부 (데이터 연동 필요)", use_container_width=True):
                # 데이터 연동 필요: 실제 파일 업로드는 추후 백엔드와 연결합니다.
                close_dialogs()
                close_anomaly_dialog()
                st.session_state.attached_file = "파일 첨부 데모"

        with col_text:
            prompt_input = st.text_area(
                "메시지 전송",
                placeholder="이번 달 자동이체 지출 항목 중 의심스러운 고지서가 있어? (엔터키로 입력)",
                label_visibility="collapsed",
                key="chat_input",
            )

        with col_send:
            st.markdown('<div class="chat-send-demo-button">전송</div>', unsafe_allow_html=True)

    # 챗 전송 처리
    if prompt_input:
        close_dialogs()
        close_anomaly_dialog()
        final_prompt = prompt_input.strip()
        if st.session_state.attached_file:
            final_prompt += f" [첨부파일: {st.session_state.attached_file}]"
            st.session_state.attached_file = None
            
        st.session_state.submitted_prompt = final_prompt
        st.session_state.show_risk_result = True
        
        # 최근 항목에 검색어 추가 (중복 방지 및 15자 슬라이싱)
        short_prompt = prompt_input[:15] + ("..." if len(prompt_input) > 15 else "")
        if short_prompt not in st.session_state.chat_history:
            st.session_state.chat_history.insert(0, short_prompt)
            
        with st.spinner("BlueGuard AI 알고리즘 실행 중..."):
            st.session_state.ai_response_text = get_ai_response(final_prompt)
        st.rerun()


# ════════════════════════════════════════
# 마이페이지 레이아웃 (디자인 2 기반 구성)
# ════════════════════════════════════════
def render_mypage() -> None:
    st.markdown('<div style="max-width:860px; margin: 0 auto;">', unsafe_allow_html=True)

    # 마이페이지 헤더 카드 (디자인 2 적용)
    profile_name = profile_value("name")
    display_title = f"{profile_name} 님" if not profile_name.startswith("(") else "마이데이터 프로필"

    st.markdown(f"""
    <div class="card-box">
        <div style="display:flex; align-items:center; gap:18px; margin-bottom:12px;">
            <div class="avatar-lg">🛡</div>
            <div>
                <div class="mypage-name">{safe_html(display_title)}</div>
                <div class="mypage-role">BlueGuard Pay 정회원 안심 지킴이 등급</div>
            </div>
        </div>
        <hr style="border:none; border-top:1px solid #E8EBF2; margin: 15px 0;">
        <div class="section-title">등록 프로필 관리 정보</div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin-bottom:15px;">
            <div>
                <label style="font-size:12px; color:#6B7280; font-weight:600;">성함</label>
                <div style="padding: 8px 0; border-bottom:1.5px solid #E2E6F0; font-size:14px; color:#374151; font-weight:700;">
                    {safe_html(profile_value("name"))}
                </div>
            </div>
            <div>
                <label style="font-size:12px; color:#6B7280; font-weight:600;">연락처</label>
                <div style="padding: 8px 0; border-bottom:1.5px solid #E2E6F0; font-size:14px; color:#374151; font-weight:700;">
                    {safe_html(profile_value("phone"))}
                </div>
            </div>
            <div>
                <label style="font-size:12px; color:#6B7280; font-weight:600;">이메일 주소</label>
                <div style="padding: 8px 0; border-bottom:1.5px solid #E2E6F0; font-size:14px; color:#374151; font-weight:700;">
                    {safe_html(profile_value("email"))}
                </div>
            </div>
            <div>
                <label style="font-size:12px; color:#6B7280; font-weight:600;">배송지 고지 주소</label>
                <div style="padding: 8px 0; border-bottom:1.5px solid #E2E6F0; font-size:14px; color:#374151; font-weight:700;">
                    {safe_html(profile_value("address"))}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 내 정보 수정 클릭 시 1번 모달 호출 기능 유지
    col_mod_btn1, col_mod_btn2, _ = st.columns([1.5, 1.5, 3])
    with col_mod_btn1:
        if st.button("👤 내 정보 마스킹 수정", use_container_width=True):
            open_dialog("info")
            st.rerun()
    with col_mod_btn2:
        if st.button("➕ 더 많은 공과금 등록하기", use_container_width=True):
            open_dialog("feature")
            st.rerun()

    # 지출 현황 및 리포트 (디자인 2 카드 레이아웃 배치)
    col_left, col_right = st.columns([1, 2], gap="medium")

    with col_left:
        st.markdown("""
        <div class="card-box" style="height: 100%;">
            <div class="section-title">스마트 필터 탐지 항목</div>
            <div class="transfer-tag">📋 수도 공과금</div>
            <div class="transfer-tag">⚡ 한국전력공사 전기세</div>
            <div class="transfer-tag">🔥 도시 가스 요금</div>
        """, unsafe_allow_html=True)
        if st.button("⊕ 더 많은 공과금 등록하기", key="add_bill_utility", use_container_width=True):
            open_dialog("feature")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="display:flex; justify-content:between; align-items:center; margin-bottom:10px;">
                  <div>
                    <span style="font-size:12px; color:#9CA3AF; font-weight:700; text-transform:uppercase;">지출 분석 스마트 리포트</span>
                    <h2 style="font-size:20px; font-weight:800; color:#0D1117; margin: 4px 0 0;">{safe_html(st.session_state.selected_category)} 안심 지출 트렌드</h2>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # 카테고리 필터 버튼 렌더링
            cat_cols = st.columns(3)
            categories = ["수도요금", "전기요금", "가스요금"]
            for idx, cat in enumerate(categories):
                with cat_cols[idx]:
                    btn_type = "primary" if st.session_state.selected_category == cat else "secondary"
                    if st.button(cat, use_container_width=True, key=f"cat_selector_{cat}", type=btn_type):
                        close_dialogs()
                        close_anomaly_dialog()
                        st.session_state.selected_category = cat
                        st.rerun()

            # 기간 필터 버튼 렌더링
            p_cols = st.columns([1, 1, 3])
            with p_cols[0]:
                p_type = "primary" if st.session_state.selected_period == "6개월" else "secondary"
                if st.button("6개월", key="btn_p6m", type=p_type, use_container_width=True):
                    close_dialogs()
                    close_anomaly_dialog()
                    st.session_state.selected_period = "6개월"
                    st.rerun()
            with p_cols[1]:
                p_type = "primary" if st.session_state.selected_period == "1년" else "secondary"
                if st.button("1년", key="btn_p1y", type=p_type, use_container_width=True):
                    close_dialogs()
                    close_anomaly_dialog()
                    st.session_state.selected_period = "1년"
                    st.rerun()
            with p_cols[2]:
                st.markdown('<p style="font-size:11px; color:#9CA3AF; text-align:right; margin-top:8px;">(한국공과금협회 실시간 조회 연동)</p>', unsafe_allow_html=True)

            # 정밀 지출 SVG 차트 출력
            st.markdown(
                render_graph_svg(st.session_state.selected_category, st.session_state.selected_period),
                unsafe_allow_html=True,
            )

            # 지출 통계 및 메트릭 데이터 출력
            values = BILL_DATA[st.session_state.selected_category][st.session_state.selected_period]
            previous_average = sum(values[:-1]) / max(len(values[:-1]), 1)
            latest = values[-1]
            change = ((latest - previous_average) / previous_average * 100) if previous_average else 0

            m_cols = st.columns(3)
            with m_cols[0]:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">최근 납부 금액</div><div class="metric-value">{latest:,}원</div></div>',
                    unsafe_allow_html=True,
                )
            with m_cols[1]:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">이전 평균 요금</div><div class="metric-value">{previous_average:,.0f}원</div></div>',
                    unsafe_allow_html=True,
                )
            with m_cols[2]:
                sign = "+" if change > 0 else ""
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">요금 변동률</div><div class="metric-value" style="color:{"#D32F2F" if change > 20 else "#374151"};">{sign}{change:+.1f}%</div></div>',
                    unsafe_allow_html=True,
                )

            # 데이터 테이블 바인딩
            st.markdown("<h4 style='font-size:14px; font-weight:700; color:#0D1117; margin-top:20px;'>안심 납부 요금 내역 명세표</h4>", unsafe_allow_html=True)
            render_bill_table(st.session_state.selected_category, st.session_state.selected_period)

    st.markdown('</div>', unsafe_allow_html=True)


def render_bill_table(category: str, period: str) -> None:
    labels = get_bill_labels(period)
    values = BILL_DATA[category][period]
    table = pd.DataFrame(
        {
            "납부 기준 월": labels,
            "납부 요금 총액": [f"{value:,}원" for value in values],
            "안심 보안 검증": ["안심 등급 정합성 확인" if v < sum(values[:-1])/len(values[:-1])*1.5 else "⚠️ 요금 과다 청구 감지됨" for v in values],
        }
    )
    st.dataframe(table, use_container_width=True, hide_index=True)


def main() -> None:
    init_state()
    handle_mini_rail_action()
    st.markdown(CSS, unsafe_allow_html=True)
    render_mini_sidebar_rail()
    render_sidebar()
    render_top_notification()

    if st.session_state.page == "mypage":
        render_mypage()
    else:
        render_chat_page()

    render_dialogs()


if __name__ == "__main__":
    main()
