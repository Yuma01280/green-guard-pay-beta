from html import escape

import pandas as pd
import streamlit as st


BRAND_NAME = "GreenGuard Pay"
BRAND_AI = "GreenGuard Pay AI"

# 데이터 연동 필요: 실제 사용자/요금/고지서 데이터는 추후 백엔드와 연결합니다.
PROFILE_FIELDS = [
    {"label": "이름", "value": "김그린"},
    {"label": "전화번호", "value": "010-1234-5678"},
    {"label": "이메일", "value": "greenguard@example.com"},
    {"label": "주소", "value": "서울시 중구 청계천로 100"},
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


st.set_page_config(
    page_title=f"{BRAND_NAME} Beta",
    page_icon="G",
    layout="wide",
    initial_sidebar_state="expanded",
)


CSS = """
<style>
:root {
  --bg: #f3f7fd;
  --surface: #ffffff;
  --surface-soft: #f8fbff;
  --line: #dce7f7;
  --line-strong: #b9cbea;
  --text: #0f172a;
  --muted: #64748b;
  --blue: #1d4ed8;
  --blue2: #3b82f6;
  --green: #2f6f73;
  --safe-bg: #eaf4f3;
  --danger: #b64a42;
  --danger-bg: #fff1ef;
}

.stApp {
  background: linear-gradient(180deg, #f9fbff 0%, #f3f7fd 45%, #eef6f5 100%);
  color: var(--text);
}

[data-testid="stHeader"] {
  background: transparent;
}

[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.94);
  border-right: 1px solid var(--line);
  box-shadow: 10px 0 28px rgba(29, 78, 216, 0.06);
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
  gap: 0.72rem;
}

.block-container {
  max-width: 1160px;
  padding: 2.45rem 2.2rem 5.5rem;
}

[data-testid="stVerticalBlock"] {
  gap: 0.82rem;
}

[data-testid="column"] {
  min-width: 0;
}

div[data-testid="stForm"] {
  border: 0;
  padding: 0;
  background: transparent;
}

div[data-testid="stForm"] [data-testid="stVerticalBlock"] {
  gap: 0;
}

div[data-testid="stTextInput"] {
  margin-bottom: 0;
}

div[data-testid="stMarkdownContainer"] p {
  margin-bottom: 0;
}

.element-container {
  margin-bottom: 0;
}

.stButton,
.stFormSubmitButton {
  width: 100%;
}

.stButton > button,
.stFormSubmitButton > button {
  width: 100%;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px;
  line-height: 1.2 !important;
  padding: 0 0.95rem !important;
}

button[kind="primary"],
button[kind="secondary"],
.stButton > button,
.stFormSubmitButton > button {
  border-radius: 8px !important;
  border: 1px solid var(--line) !important;
  background: #ffffff !important;
  color: var(--text) !important;
  font-weight: 850 !important;
  min-height: 46px;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
  white-space: nowrap;
}

button[kind="primary"] {
  border: 0 !important;
  background: linear-gradient(135deg, var(--blue), var(--blue2)) !important;
  color: #ffffff !important;
  box-shadow: 0 12px 24px rgba(29, 78, 216, 0.18) !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
  border-color: #9fc3f7 !important;
  color: var(--blue) !important;
  box-shadow: 0 12px 24px rgba(29, 78, 216, 0.11);
}

.stButton > button:focus,
.stFormSubmitButton > button:focus {
  border-color: #9fc3f7 !important;
  color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.16), 0 12px 24px rgba(29, 78, 216, 0.11) !important;
}

button[kind="primary"]:focus {
  color: #ffffff !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.18), 0 12px 24px rgba(29, 78, 216, 0.18) !important;
}

[data-testid="stSidebar"] .stButton:first-of-type > button,
.stFormSubmitButton > button {
  border: 0 !important;
  background: linear-gradient(135deg, var(--blue), var(--blue2)) !important;
  color: #ffffff !important;
  box-shadow: 0 12px 24px rgba(29, 78, 216, 0.2);
  transform: translateY(7px);
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
  min-height: 46px;
  border-radius: 8px;
  border-color: var(--line);
  background: var(--surface-soft);
  color: var(--text);
  font-weight: 750;
  padding: 0 14px;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: 11px;
  min-height: 42px;
  margin: 2px 0 16px;
}

.brand-symbol {
  position: relative;
  display: grid;
  width: 38px;
  height: 38px;
  place-items: center;
  border-radius: 16px 16px 16px 6px;
  background: linear-gradient(135deg, var(--blue), var(--blue2));
  box-shadow: 0 10px 20px rgba(29, 78, 216, 0.22);
}

.brand-symbol::after {
  position: absolute;
  right: 7px;
  bottom: 5px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #ffffff;
  content: "";
}

.brand-shield {
  width: 16px;
  height: 19px;
  border: 2px solid rgba(255, 255, 255, 0.95);
  border-top-width: 3px;
  border-radius: 8px 8px 10px 10px;
  transform: translateY(-1px);
}

.brand-name {
  color: var(--text);
  font-size: 17px;
  font-weight: 900;
}

.side-label,
.eyebrow {
  margin: 0 0 8px;
  color: var(--green);
  font-size: 13px;
  font-weight: 900;
}

.recent-note {
  margin: 4px 0 14px;
  color: #7c8ba1;
  font-size: 13px;
}

.hero-wrap {
  display: flex;
  min-height: calc(100vh - 300px);
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hero-card {
  width: min(920px, 100%);
  padding: 22px 16px;
}

.hero-title {
  margin: 8px 0;
  color: var(--text);
  font-size: clamp(38px, 5vw, 58px);
  font-weight: 950;
  letter-spacing: 0;
}

.hero-subtitle {
  margin: 0;
  color: #475569;
  font-size: 18px;
}

.chat-shell {
  width: min(860px, 100%);
  margin: 28px auto 0;
}

.chat-form-card {
  border: 1px solid var(--line);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.96);
  padding: 12px 14px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.12);
}

.chat-form-card [data-testid="stHorizontalBlock"] {
  align-items: center;
  gap: 0.7rem;
}

.chat-form-card [data-testid="stTextInput"] input {
  min-height: 50px;
  border: 0;
  background: transparent;
  font-size: 16px;
}

.chat-form-card .stFormSubmitButton > button {
  min-height: 50px !important;
  border-radius: 16px !important;
}

.user-bubble-wrap {
  display: flex;
  justify-content: flex-end;
  margin: 30px auto 18px;
  width: min(760px, 100%);
}

.user-bubble {
  max-width: min(580px, 88%);
  border-radius: 18px 18px 4px 18px;
  background: var(--blue);
  color: #ffffff;
  padding: 13px 17px;
  box-shadow: 0 12px 20px rgba(29, 78, 216, 0.16);
  font-weight: 800;
}

.risk-card {
  width: min(760px, 100%);
  margin: 0 auto 28px;
  border: 1px solid #f6cbc5;
  border-radius: 8px;
  background: #fffafa;
  padding: 22px;
  box-shadow: 0 16px 34px rgba(217, 106, 94, 0.12);
}

.risk-card-header,
.graph-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.pill {
  display: inline-flex;
  min-height: 30px;
  align-items: center;
  border-radius: 999px;
  padding: 0 12px;
  font-size: 13px;
  font-weight: 900;
}

.risk-level {
  background: var(--danger-bg);
  color: var(--danger);
}

.risk-status {
  background: var(--blue);
  color: #ffffff;
}

.safe-chip {
  background: var(--safe-bg);
  color: var(--green);
}

.risk-message {
  margin: 18px 0;
  color: #172033;
  font-size: 18px;
  font-weight: 850;
  line-height: 1.65;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.risk-tag {
  border: 1px solid #ffd7d1;
  border-radius: 999px;
  background: var(--danger-bg);
  color: #9f413a;
  padding: 7px 11px;
  font-size: 13px;
  font-weight: 850;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.detail-box {
  border: 1px solid #f6e1de;
  border-radius: 8px;
  background: #ffffff;
  padding: 13px;
}

.detail-box strong {
  display: block;
  color: var(--danger);
  font-size: 13px;
}

.detail-box span {
  display: block;
  margin-top: 3px;
  color: #334155;
  font-size: 14px;
}

.profile-header-card {
  min-height: 238px;
  display: flex;
  align-items: center;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #ffffff;
  padding: 30px 34px;
  box-shadow: 0 18px 40px rgba(29, 78, 216, 0.09);
  margin: 0 0 24px;
}

.profile-identity {
  display: flex;
  gap: 18px;
  align-items: center;
  width: 100%;
}

.large-avatar {
  display: grid;
  width: 72px;
  height: 72px;
  flex: 0 0 auto;
  place-items: center;
  border-radius: 50%;
  background: var(--safe-bg);
  color: var(--green);
  font-size: 33px;
  font-weight: 900;
  box-shadow: inset 0 0 0 1px rgba(47, 111, 115, 0.12);
}

.profile-title {
  margin: 2px 0 8px;
  color: var(--text);
  font-size: clamp(30px, 4vw, 44px);
  font-weight: 950;
  letter-spacing: 0;
}

.profile-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 18px;
}

.meta-box {
  min-width: 168px;
  min-height: 68px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-radius: 8px;
  background: var(--bg);
  padding: 11px 13px;
}

.meta-box dt {
  margin: 0;
  color: var(--muted);
  font-size: 12px;
  font-weight: 850;
}

.meta-box dd {
  margin: 3px 0 0;
  color: var(--text);
  font-size: 14px;
  font-weight: 900;
}

.graph-card {
  min-height: 560px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #ffffff;
  padding: 28px;
  box-shadow: 0 18px 40px rgba(29, 78, 216, 0.09);
}

[data-testid="stVerticalBlockBorderWrapper"] {
  border: 1px solid var(--line) !important;
  border-radius: 8px !important;
  background: #ffffff !important;
  box-shadow: 0 18px 40px rgba(29, 78, 216, 0.09);
}

[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
  gap: 0.95rem;
}

.graph-title {
  margin: 4px 0 0;
  color: var(--text);
  font-size: 24px;
  font-weight: 950;
}

.graph-header {
  align-items: center;
  margin-bottom: 16px;
}

.graph-placeholder {
  position: relative;
  height: 310px;
  margin-top: 18px;
  overflow: hidden;
  border: 1px dashed var(--line-strong);
  border-radius: 8px;
  background:
    linear-gradient(#e8f1fc 1px, transparent 1px) 0 0 / 100% 25%,
    linear-gradient(180deg, #fbfdff 0%, #f3f7fd 100%);
  padding: 16px;
}

.graph-svg {
  width: 100%;
  height: 100%;
}

.graph-grid-line {
  stroke: #dce7f7;
  stroke-dasharray: 6 10;
  stroke-linecap: round;
  stroke-width: 2;
}

.graph-axis-line {
  stroke: #c8d8ef;
  stroke-width: 2;
}

.graph-dotted-line {
  fill: none;
  filter: drop-shadow(0 8px 12px rgba(29, 78, 216, 0.15));
  stroke: var(--blue);
  stroke-dasharray: 12 14;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 5;
}

.graph-point {
  fill: #ffffff;
  stroke: var(--green);
  stroke-width: 5;
}

.graph-data-note {
  position: absolute;
  z-index: 2;
  top: 50%;
  left: 50%;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.94);
  color: var(--muted);
  padding: 9px 14px;
  font-weight: 900;
  transform: translate(-50%, -50%);
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
  white-space: nowrap;
}

.metric-card {
  min-height: 92px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #ffffff;
  padding: 16px;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.06);
}

.metric-label {
  color: var(--muted);
  font-size: 13px;
  font-weight: 850;
}

.metric-value {
  margin-top: 4px;
  color: var(--text);
  font-size: 22px;
  font-weight: 950;
}

.notice-box {
  border: 1px dashed var(--line-strong);
  border-radius: 8px;
  background: var(--surface-soft);
  color: var(--muted);
  padding: 14px 16px;
  font-weight: 850;
  text-align: center;
}

.feature-item {
  display: flex;
  min-height: 54px;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #ffffff;
  color: var(--text);
  padding: 0 14px;
  margin: 10px 0;
}

.feature-item strong {
  color: var(--text);
}

.feature-item small {
  color: var(--muted);
  white-space: nowrap;
}

.data-caption {
  color: var(--muted);
  font-size: 13px;
  font-weight: 850;
}

.profile-action-offset {
  height: 54px;
}

div[data-testid="stDialog"] div[role="dialog"] {
  border: 1px solid rgba(159, 195, 247, 0.28);
  border-radius: 14px;
  background:
    radial-gradient(circle at 20% 0%, rgba(59, 130, 246, 0.22), transparent 34%),
    linear-gradient(180deg, #0f172a 0%, #172554 100%);
  color: #eaf2ff;
  box-shadow: 0 34px 90px rgba(15, 23, 42, 0.42);
}

div[data-testid="stDialog"] h2,
div[data-testid="stDialog"] h3,
div[data-testid="stDialog"] p,
div[data-testid="stDialog"] label {
  color: #eaf2ff !important;
}

div[data-testid="stDialog"] small,
div[data-testid="stDialog"] [data-testid="stCaptionContainer"] {
  color: #b8c7e5 !important;
}

div[data-testid="stDialog"] input {
  min-height: 46px;
  border: 1px solid rgba(159, 195, 247, 0.32) !important;
  border-radius: 8px !important;
  background: rgba(15, 23, 42, 0.62) !important;
  color: #eef6ff !important;
  font-weight: 850;
  letter-spacing: 0;
}

div[data-testid="stDialog"] .stButton > button,
div[data-testid="stDialog"] .stFormSubmitButton > button {
  border-color: rgba(159, 195, 247, 0.35) !important;
}

.privacy-status {
  border: 1px solid rgba(159, 195, 247, 0.26);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.08);
  padding: 14px 16px;
  margin: 12px 0 14px;
  color: #dbeafe;
  font-size: 14px;
  line-height: 1.6;
}

.mask-preview-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin: 12px 0 16px;
}

.mask-preview {
  min-height: 68px;
  border: 1px solid rgba(159, 195, 247, 0.24);
  border-radius: 8px;
  background:
    linear-gradient(90deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.05)),
    rgba(15, 23, 42, 0.4);
  padding: 11px 12px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.mask-preview span {
  display: block;
  color: #93a9ce;
  font-size: 12px;
  font-weight: 850;
}

.mask-preview strong {
  display: block;
  margin-top: 5px;
  overflow-wrap: anywhere;
  color: #f8fbff;
  font-size: 15px;
  font-weight: 900;
  filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.16));
}

@media (max-width: 700px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .mask-preview-grid {
    grid-template-columns: 1fr;
  }

  .profile-identity,
  .graph-header {
    flex-direction: column;
  }
}
</style>
"""


def init_state() -> None:
    defaults = {
        "current_view": "chat",
        "submitted_prompt": "",
        "show_risk_result": False,
        "selected_category": "수도요금",
        "selected_period": "6개월",
        "mask_strength": 40,
        "feature_query": "",
        "open_info_dialog": False,
        "open_feature_dialog": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def safe_html(value: object) -> str:
    return escape(str(value))


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


def set_chat(reset: bool = False) -> None:
    st.session_state.current_view = "chat"
    close_dialogs()
    if reset:
        st.session_state.submitted_prompt = ""
        st.session_state.show_risk_result = False


def set_profile() -> None:
    st.session_state.current_view = "profile"
    close_dialogs()


def render_brand() -> None:
    st.markdown(
        f"""
        <div class="brand-row" aria-label="{safe_html(BRAND_NAME)}">
          <span class="brand-symbol" aria-hidden="true"><span class="brand-shield"></span></span>
          <span class="brand-name">{safe_html(BRAND_NAME)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        render_brand()

        st.text_input("대화 검색", placeholder="대화 검색", label_visibility="collapsed", key="conversation_search")

        if st.button("+ 새 채팅", width="stretch"):
            set_chat(reset=True)
            st.rerun()

        st.markdown('<p class="side-label">최근</p>', unsafe_allow_html=True)
        if st.button("자동이체 이상 여부", width="stretch"):
            st.session_state.submitted_prompt = "이번 달 자동이체 중 이상한 거 있어?"
            st.session_state.show_risk_result = True
            set_chat()
            st.rerun()

        if st.button("고지서 확인", width="stretch"):
            st.session_state.submitted_prompt = "최근 고지서에서 위험한 납부 항목을 확인해줘"
            st.session_state.show_risk_result = True
            set_chat()
            st.rerun()

        st.markdown('<p class="recent-note">(데이터 연동 필요)</p>', unsafe_allow_html=True)

        st.divider()

        if st.button("닉네임 님\n(데이터 연동 필요)", width="stretch"):
            set_profile()
            st.rerun()


def render_risk_card() -> None:
    st.markdown(
        """
        <article class="risk-card">
          <div class="risk-card-header">
            <span class="pill risk-level">위험도 높음</span>
            <span class="pill risk-status">이체 보류 권장</span>
          </div>
          <p class="risk-message">
            수도요금 402,000원이 최근 평균보다 높고, 주소지 불일치 가능성이 있어 이체 보류가 필요합니다.
          </p>
          <div class="tag-row" aria-label="감지된 위험 요소">
            <span class="risk-tag">주소지 불일치</span>
            <span class="risk-tag">요금 폭증 감지</span>
            <span class="risk-tag">(데이터 연동 필요)</span>
          </div>
          <div class="detail-grid">
            <div class="detail-box">
              <strong>감지 항목</strong>
              <span>자동이체 예정 고지서</span>
            </div>
            <div class="detail-box">
              <strong>권장 조치</strong>
              <span>납부 전 주소와 청구처 확인</span>
            </div>
          </div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def render_chat_input() -> None:
    st.markdown('<div class="chat-shell"><div class="chat-form-card">', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        input_col, send_col = st.columns([8, 1.2], vertical_alignment="bottom")
        with input_col:
            prompt = st.text_input(
                "질문 입력",
                placeholder="이번 달 자동이체 중 이상한 거 있어?",
                label_visibility="collapsed",
            )
        with send_col:
            submitted = st.form_submit_button("전송", width="stretch")

        if submitted and prompt.strip():
            # 데이터 연동 필요: 추후 분석 API와 연결할 위치입니다.
            st.session_state.submitted_prompt = prompt.strip()
            st.session_state.show_risk_result = True
            st.session_state.current_view = "chat"
            st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_chat_home() -> None:
    if not st.session_state.show_risk_result:
        st.markdown(
            f"""
            <section class="hero-wrap">
              <div class="hero-card">
                <p class="eyebrow">{safe_html(BRAND_AI)}</p>
                <h1 class="hero-title">무엇을 도와드릴까요?</h1>
                <p class="hero-subtitle">돈이 빠져나가기 전, AI가 한 번 더 확인합니다.</p>
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="hero-card" style="text-align:center; margin: 0 auto;">
              <p class="eyebrow">{safe_html(BRAND_AI)}</p>
              <h1 class="hero-title" style="font-size: clamp(32px, 4vw, 48px);">무엇을 도와드릴까요?</h1>
              <p class="hero-subtitle">돈이 빠져나가기 전, AI가 한 번 더 확인합니다.</p>
            </div>
            <div class="user-bubble-wrap">
              <div class="user-bubble">{safe_html(st.session_state.submitted_prompt)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_risk_card()

    render_chat_input()


def render_profile_header() -> None:
    st.markdown(
        """
        <section class="profile-header-card">
          <div class="profile-identity">
            <span class="large-avatar">G</span>
            <div>
              <p class="eyebrow">내 프로필</p>
              <h1 class="profile-title">닉네임 님</h1>
              <dl class="profile-meta">
                <div class="meta-box"><dt>이름</dt><dd>(데이터 연동 필요)</dd></div>
                <div class="meta-box"><dt>전화번호</dt><dd>(데이터 연동 필요)</dd></div>
                <div class="meta-box"><dt>이메일</dt><dd>(데이터 연동 필요)</dd></div>
              </dl>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def get_bill_labels(period: str) -> list[str]:
    if period == "1년":
        return [f"{month}월" for month in range(1, 13)]
    return [f"{month}월" for month in range(1, 7)]


def render_graph_svg(category: str, period: str) -> str:
    values = BILL_DATA[category][period]
    labels = get_bill_labels(period)
    count = len(values)
    min_value = min(values)
    max_value = max(values)
    span = max(max_value - min_value, 1)
    x_start = 72
    x_end = 648
    x_positions = [x_start + ((x_end - x_start) / (count - 1)) * index for index in range(count)]

    points = []
    for x_position, value in zip(x_positions, values):
        y_position = 198 - ((value - min_value) / span) * 122
        points.append((round(x_position, 1), round(y_position, 1)))

    point_attr = " ".join(f"{x},{y}" for x, y in points)
    circles = "\n".join(f'<circle class="graph-point" cx="{x}" cy="{y}" r="8" />' for x, y in points)
    label_step = 1 if period == "6개월" else 2
    label_nodes = "\n".join(
        f'<text x="{x}" y="258" text-anchor="middle" fill="#64748b" font-size="18" font-weight="800">{safe_html(label)}</text>'
        for index, ((x, _), label) in enumerate(zip(points, labels))
        if index % label_step == 0
    )

    return f"""
    <div class="graph-placeholder">
      <svg class="graph-svg" viewBox="0 0 720 280" role="img" aria-label="{safe_html(category)} 지출 그래프">
        <line class="graph-grid-line" x1="48" y1="56" x2="672" y2="56" />
        <line class="graph-grid-line" x1="48" y1="118" x2="672" y2="118" />
        <line class="graph-grid-line" x1="48" y1="180" x2="672" y2="180" />
        <line class="graph-axis-line" x1="48" y1="232" x2="672" y2="232" />
        <polyline class="graph-dotted-line" points="{point_attr}" />
        {circles}
        {label_nodes}
      </svg>
      <span class="graph-data-note">(데이터 연동 필요)</span>
    </div>
    """


def render_bill_table(category: str, period: str) -> None:
    labels = get_bill_labels(period)
    values = BILL_DATA[category][period]
    table = pd.DataFrame(
        {
            "기간": labels,
            "요금": [f"{value:,}원" for value in values],
            "상태": ["데모 데이터"] * len(values),
        }
    )
    st.dataframe(table, width="stretch", hide_index=True)
    st.caption("(데이터 연동 필요)")


def render_profile_page() -> None:
    header_col, action_col = st.columns([5.2, 1.15], gap="medium", vertical_alignment="top")
    with header_col:
        render_profile_header()
    with action_col:
        st.markdown('<div class="profile-action-offset"></div>', unsafe_allow_html=True)
        if st.button("내 정보 수정", key="profile_open_info_dialog", width="stretch"):
            st.session_state.open_feature_dialog = False
            st.session_state.open_info_dialog = True
            st.rerun()

    left_col, right_col = st.columns([1.05, 2.85], gap="large")

    with left_col:
        for category in ["수도요금", "전기요금", "가스요금"]:
            category_type = "primary" if st.session_state.selected_category == category else "secondary"
            if st.button(category, key=f"category_{category}", type=category_type, width="stretch"):
                close_dialogs()
                st.session_state.selected_category = category
                st.rerun()

        if st.button("수정하기", key="profile_open_feature_dialog", width="stretch"):
            st.session_state.open_info_dialog = False
            st.session_state.open_feature_dialog = True
            st.rerun()

    with right_col:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="graph-header">
                  <div>
                    <p class="eyebrow">지출 리포트</p>
                    <h2 class="graph-title">{safe_html(st.session_state.selected_category)} 지출 그래프</h2>
                  </div>
                  <span class="pill safe-chip">분석 대기</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            period_col_1, period_col_2, spacer = st.columns([1, 1, 5])
            with period_col_1:
                period_type = "primary" if st.session_state.selected_period == "6개월" else "secondary"
                if st.button("6개월", key="period_6m", type=period_type, width="stretch"):
                    close_dialogs()
                    st.session_state.selected_period = "6개월"
                    st.rerun()
            with period_col_2:
                period_type = "primary" if st.session_state.selected_period == "1년" else "secondary"
                if st.button("1년", key="period_1y", type=period_type, width="stretch"):
                    close_dialogs()
                    st.session_state.selected_period = "1년"
                    st.rerun()
            with spacer:
                st.markdown('<span class="data-caption">(데이터 연동 필요)</span>', unsafe_allow_html=True)

            st.markdown(
                render_graph_svg(st.session_state.selected_category, st.session_state.selected_period),
                unsafe_allow_html=True,
            )

            values = BILL_DATA[st.session_state.selected_category][st.session_state.selected_period]
            previous_average = sum(values[:-1]) / max(len(values[:-1]), 1)
            latest = values[-1]
            change = ((latest - previous_average) / previous_average * 100) if previous_average else 0

            metric_1, metric_2, metric_3 = st.columns(3)
            with metric_1:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">최근 요금</div><div class="metric-value">{latest:,}원</div></div>',
                    unsafe_allow_html=True,
                )
            with metric_2:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">이전 평균</div><div class="metric-value">{previous_average:,.0f}원</div></div>',
                    unsafe_allow_html=True,
                )
            with metric_3:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">변동률</div><div class="metric-value">{change:+.1f}%</div></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("#### 요금 내역 표")
            render_bill_table(st.session_state.selected_category, st.session_state.selected_period)


def render_info_dialog_body() -> None:
    st.caption("개인정보 보호")
    st.subheader("내 정보 수정")
    st.markdown(
        """
        <div class="privacy-status">
          개인정보는 화면 표시 단계에서만 마스킹됩니다. 실제 저장 기능은 데모에서 비활성화되어 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.mask_strength = st.slider(
        "마스킹 강도",
        min_value=10,
        max_value=80,
        step=10,
        value=st.session_state.mask_strength,
    )

    # 데이터 연동 필요: 실제 개인정보 조회/저장 API 연결 예정
    preview_cards = []
    for field in PROFILE_FIELDS:
        masked_value = mask_sensitive_value(field["value"], st.session_state.mask_strength)
        preview_cards.append(
            f"""
            <div class="mask-preview">
              <span>{safe_html(field["label"])}</span>
              <strong>{safe_html(masked_value)}</strong>
            </div>
            """
        )
    st.markdown(f'<div class="mask-preview-grid">{"".join(preview_cards)}</div>', unsafe_allow_html=True)

    for field in PROFILE_FIELDS:
        masked_value = mask_sensitive_value(field["value"], st.session_state.mask_strength)
        st.text_input(
            field["label"],
            value=masked_value,
            disabled=True,
            key=f"masked_{field['label']}_{st.session_state.mask_strength}",
        )

    st.caption("(데이터 연동 필요)")
    if st.button("확인", key="close_info_dialog", width="stretch"):
        close_dialogs()
        st.rerun()


def render_feature_dialog_body() -> None:
    st.caption(BRAND_NAME)
    st.subheader("기능 추가")
    with st.form("feature_search_form"):
        st.text_input(
            "기능 검색",
            placeholder="추가할 기능을 검색하세요",
            label_visibility="collapsed",
            key="feature_query",
        )
        st.form_submit_button("검색", width="stretch")

    query = st.session_state.feature_query.strip()
    filtered = [feature for feature in FEATURE_SUGGESTIONS if query in feature] if query else FEATURE_SUGGESTIONS

    if filtered:
        for feature in filtered:
            st.markdown(
                f"""
                <div class="feature-item">
                  <strong>{safe_html(feature)}</strong>
                  <small>(데이터 연동 필요)</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<div class="notice-box">(데이터 연동 필요)</div>', unsafe_allow_html=True)

    if st.button("닫기", key="close_feature_dialog", width="stretch"):
        close_dialogs()
        st.rerun()


def render_dialogs() -> None:
    if st.session_state.open_info_dialog:
        if hasattr(st, "dialog"):

            @st.dialog("내 정보 수정")
            def info_dialog() -> None:
                render_info_dialog_body()

            info_dialog()
        else:
            with st.expander("내 정보 수정", expanded=True):
                render_info_dialog_body()

    if st.session_state.open_feature_dialog:
        if hasattr(st, "dialog"):

            @st.dialog("기능 추가")
            def feature_dialog() -> None:
                render_feature_dialog_body()

            feature_dialog()
        else:
            with st.expander("기능 추가", expanded=True):
                render_feature_dialog_body()


def main() -> None:
    init_state()
    st.markdown(CSS, unsafe_allow_html=True)
    render_sidebar()

    if st.session_state.current_view == "profile":
        render_profile_page()
    else:
        render_chat_home()

    render_dialogs()


if __name__ == "__main__":
    main()
