import streamlit as st
import pandas as pd
from html import escape

BRAND_NAME = "GreenGuard Pay"
BRAND_AI = "GreenGuard Pay AI"

st.set_page_config(
    page_title=f"{BRAND_NAME} Beta",
    page_icon="🛡️",
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
  --danger: #b64a42;
  --danger-bg: #fff1ef;
}

.stApp {
  background: linear-gradient(180deg, #f9fbff 0%, #f3f7fd 45%, #eef6f5 100%);
  color: var(--text);
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.94);
  border-right: 1px solid var(--line);
  box-shadow: 10px 0 28px rgba(29, 78, 216, 0.06);
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.75rem; }
.block-container {
  max-width: 1180px;
  padding-top: 2.4rem;
  padding-bottom: 7rem;
}

.brand-row {
  display:flex;
  align-items:center;
  gap:11px;
  min-height:42px;
  margin: 2px 0 14px;
}
.brand-symbol {
  position:relative;
  display:grid;
  width:38px;
  height:38px;
  place-items:center;
  border-radius:16px 16px 16px 6px;
  background:linear-gradient(135deg, var(--blue), var(--blue2));
  box-shadow:0 10px 20px rgba(29, 78, 216, 0.22);
}
.brand-symbol::after {
  position:absolute;
  right:7px;
  bottom:5px;
  width:9px;
  height:9px;
  border-radius:50%;
  background:#fff;
  content:"";
}
.brand-shield {
  width:16px;
  height:19px;
  border:2px solid rgba(255,255,255,.95);
  border-top-width:3px;
  border-radius:8px 8px 10px 10px;
  transform:translateY(-1px);
}
.brand-name {
  font-size:17px;
  font-weight:850;
  color:var(--text);
}
.side-label, .eyebrow {
  color: var(--green);
  font-size: 13px;
  font-weight: 850;
  margin: 0 0 8px;
}
.recent-note {
  color:#7c8ba1;
  font-size:13px;
  margin: 6px 0 14px;
}

.hero-wrap {
  min-height: calc(100vh - 220px);
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  text-align:center;
}
.hero-card {
  width:min(920px, 100%);
  padding: 22px 16px;
}
.hero-title {
  margin: 8px 0;
  color: var(--text);
  font-size: clamp(38px, 5vw, 58px);
  font-weight: 900;
  letter-spacing: -0.04em;
}
.hero-subtitle {
  margin: 0;
  color: #475569;
  font-size: 18px;
}
.user-bubble-wrap {
  display:flex;
  justify-content:flex-end;
  margin: 36px auto 18px;
  width:min(760px, 100%);
}
.user-bubble {
  max-width:min(580px, 88%);
  border-radius:18px 18px 4px 18px;
  background:var(--blue);
  color:white;
  padding:13px 17px;
  box-shadow:0 12px 20px rgba(29, 78, 216, .16);
  font-weight: 700;
}
.risk-card {
  width:min(760px, 100%);
  margin: 0 auto;
  border:1px solid #f6cbc5;
  border-radius:8px;
  background:#fffafa;
  padding:22px;
  box-shadow:0 16px 34px rgba(217, 106, 94, .12);
}
.risk-card-header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:16px;
}
.pill {
  display:inline-flex;
  min-height:30px;
  align-items:center;
  border-radius:999px;
  padding:0 12px;
  font-size:13px;
  font-weight:900;
}
.risk-level { background: var(--danger-bg); color: var(--danger); }
.risk-status { background: var(--blue); color: white; }
.safe-chip { background: #eaf4f3; color: var(--green); }
.risk-message {
  margin:18px 0;
  color:#172033;
  font-size:18px;
  font-weight:800;
  line-height:1.65;
}
.tag-row { display:flex; flex-wrap:wrap; gap:8px; }
.risk-tag {
  border:1px solid #ffd7d1;
  border-radius:999px;
  background:var(--danger-bg);
  color:#9f413a;
  padding:7px 11px;
  font-size:13px;
  font-weight:850;
}
.detail-grid {
  display:grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap:12px;
  margin-top:18px;
}
.detail-box {
  border:1px solid #f6e1de;
  border-radius:8px;
  background:white;
  padding:13px;
}
.detail-box strong { display:block; color:var(--danger); font-size:13px; }
.detail-box span { display:block; margin-top:3px; color:#334155; font-size:14px; }

.profile-header-card {
  border:1px solid var(--line);
  border-radius:8px;
  background:white;
  padding: clamp(22px, 4vw, 34px);
  box-shadow:0 18px 40px rgba(29, 78, 216, .09);
  margin-bottom: 22px;
}
.profile-identity {
  display:flex;
  gap:18px;
  align-items:flex-start;
}
.large-avatar {
  display:grid;
  place-items:center;
  width:72px;
  height:72px;
  border-radius:50%;
  background:#eaf4f3;
  color: var(--green);
  font-size: 33px;
  box-shadow: inset 0 0 0 1px rgba(47, 111, 115, .12);
}
.profile-title {
  margin: 2px 0 8px;
  font-size: clamp(30px, 4vw, 44px);
  font-weight: 900;
  letter-spacing: -0.03em;
}
.profile-meta {
  display:flex;
  flex-wrap:wrap;
  gap:12px;
  margin-top:18px;
}
.meta-box {
  min-width:168px;
  border-radius:8px;
  background:#f3f7fd;
  padding:11px 13px;
}
.meta-box dt { color:var(--muted); font-size:12px; font-weight:850; margin:0; }
.meta-box dd { margin:3px 0 0; color:var(--text); font-size:14px; font-weight:850; }
.graph-card {
  min-height:420px;
  border:1px solid var(--line);
  border-radius:8px;
  background:white;
  padding: clamp(20px, 3vw, 30px);
  box-shadow:0 18px 40px rgba(29, 78, 216, .09);
}
.graph-header {
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:16px;
  margin-bottom: 20px;
}
.graph-title { margin: 4px 0 0; font-size: 24px; font-weight: 900; }
.graph-placeholder {
  position:relative;
  height:310px;
  margin-top:16px;
  overflow:hidden;
  border:1px dashed var(--line-strong);
  border-radius:8px;
  background:
    linear-gradient(#e8f1fc 1px, transparent 1px) 0 0 / 100% 25%,
    linear-gradient(180deg, #fbfdff 0%, #f3f7fd 100%);
  padding: 16px;
}
.graph-svg { width:100%; height:100%; }
.graph-grid-line { stroke:#dce7f7; stroke-dasharray:6 10; stroke-linecap:round; stroke-width:2; }
.graph-axis-line { stroke:#c8d8ef; stroke-width:2; }
.graph-dotted-line {
  fill:none;
  filter:drop-shadow(0 8px 12px rgba(29, 78, 216, .15));
  stroke:var(--blue);
  stroke-dasharray:12 14;
  stroke-linecap:round;
  stroke-linejoin:round;
  stroke-width:5;
}
.graph-point { fill:white; stroke: var(--green); stroke-width:5; }
.graph-data-note {
  position:absolute;
  z-index:2;
  top:50%;
  left:50%;
  border:1px solid var(--line);
  border-radius:999px;
  background:rgba(255,255,255,.94);
  color:var(--muted);
  padding:9px 14px;
  font-weight:900;
  transform:translate(-50%, -50%);
  box-shadow:0 10px 24px rgba(15,23,42,.08);
  white-space:nowrap;
}
.metric-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: white;
  padding: 16px;
  box-shadow: 0 12px 24px rgba(15,23,42,.06);
}
.metric-label { color: var(--muted); font-size: 13px; font-weight: 850; }
.metric-value { color: var(--text); font-size: 22px; font-weight: 950; margin-top: 4px; }
.notice-box {
  border:1px dashed var(--line-strong);
  border-radius:8px;
  background:#f8fbff;
  color:var(--muted);
  padding:14px 16px;
  font-weight:850;
  text-align:center;
}
.feature-item {
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  min-height:54px;
  border:1px solid var(--line);
  border-radius:8px;
  background:white;
  color:var(--text);
  padding: 0 14px;
  margin: 10px 0;
}
.feature-item strong { color: var(--text); }
.feature-item small { color: var(--muted); white-space:nowrap; }
@media (max-width: 700px) {
  .detail-grid { grid-template-columns: 1fr; }
  .profile-identity { flex-direction: column; }
  .graph-header { flex-direction: column; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

PROFILE_FIELDS = [
    {"label": "이름", "value": "김블루"},
    {"label": "전화번호", "value": "010-1234-5678"},
    {"label": "이메일", "value": "blueguard@example.com"},
    {"label": "주소", "value": "서울시 중구 청계천로 100"},
]

FEATURE_SUGGESTIONS = ["요금 폭증 알림", "주소지 불일치 감지", "자동이체 보류", "고지서 자동 분석"]
BILL_CATEGORIES = ["수도요금", "전기요금", "가스요금"]

SAMPLE_BILLS = {
    "수도요금": [38000, 41000, 39500, 44000, 52000, 402000],
    "전기요금": [68000, 73000, 89000, 92000, 86000, 108000],
    "가스요금": [42000, 39000, 31000, 28000, 35000, 61000],
}
MONTHS_6 = ["1월", "2월", "3월", "4월", "5월", "6월"]


def init_state():
    defaults = {
        "current_view": "chat",
        "submitted_prompt": "",
        "show_risk_result": False,
        "selected_category": "수도요금",
        "selected_period": "6개월",
        "mask_strength": 40,
        "feature_query": "",
        "open_info_modal": False,
        "open_feature_modal": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def mask_sensitive_value(value: str, strength: int) -> str:
    characters = list(value)
    maskable_indexes = [index for index, char in enumerate(characters) if char.isalnum()]

    if not maskable_indexes:
        return value

    mask_count = max(1, round(len(maskable_indexes) * (strength / 100)))
    start = max(0, (len(maskable_indexes) - mask_count) // 2)
    masked_indexes = set(maskable_indexes[start : start + mask_count])

    return "".join("*" if index in masked_indexes else char for index, char in enumerate(characters))


def safe_html(text: str) -> str:
    return escape(str(text))


def go_chat(reset: bool = False):
    st.session_state.current_view = "chat"
    if reset:
        st.session_state.submitted_prompt = ""
        st.session_state.show_risk_result = False


def go_profile():
    st.session_state.current_view = "profile"


def render_sidebar():
    with st.sidebar:
        st.markdown(
            f"""
            <div class="brand-row" aria-label="{safe_html(BRAND_NAME)}">
              <span class="brand-symbol" aria-hidden="true"><span class="brand-shield"></span></span>
              <span class="brand-name">{safe_html(BRAND_NAME)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_input("대화 검색", placeholder="대화 검색", label_visibility="collapsed", key="conversation_search")

        if st.button("＋ 새 채팅", use_container_width=True):
            go_chat(reset=True)
            st.rerun()

        st.markdown('<p class="side-label">최근</p>', unsafe_allow_html=True)
        if st.button("💬 자동이체 이상 여부", use_container_width=True):
            st.session_state.submitted_prompt = "이번 달 자동이체 중 이상한 거 있어?"
            st.session_state.show_risk_result = True
            go_chat()
            st.rerun()
        if st.button("💬 고지서 확인", use_container_width=True):
            st.session_state.submitted_prompt = "이번 달 고지서 확인해줘"
            st.session_state.show_risk_result = True
            go_chat()
            st.rerun()
        st.markdown('<p class="recent-note">(데이터 연동 필요)</p>', unsafe_allow_html=True)

        st.divider()
        profile_label = "👤 닉네임 님\n\n(데이터 연동 필요)"
        if st.button(profile_label, use_container_width=True):
            go_profile()
            st.rerun()


def render_risk_card():
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


def render_chat_home():
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

    prompt = st.chat_input("이번 달 자동이체 중 이상한 거 있어?")
    if prompt and prompt.strip():
        st.session_state.submitted_prompt = prompt.strip()
        st.session_state.show_risk_result = True
        st.session_state.current_view = "chat"
        st.rerun()


def render_graph_svg(category: str):
    values = SAMPLE_BILLS.get(category, SAMPLE_BILLS["수도요금"])
    min_v, max_v = min(values), max(values)
    span = max(max_v - min_v, 1)
    x_positions = [72, 188, 304, 420, 536, 648]
    # y 76 is high amount, y 198 is low amount
    points = []
    for x, value in zip(x_positions, values):
        y = 198 - ((value - min_v) / span) * 122
        points.append((x, round(y, 1)))
    point_attr = " ".join(f"{x},{y}" for x, y in points)
    circles = "".join(f'<circle class="graph-point" cx="{x}" cy="{y}" r="8" />' for x, y in points)
    labels = "".join(
        f'<text x="{x}" y="258" text-anchor="middle" fill="#64748b" font-size="18" font-weight="800">{label}</text>'
        for x, label in zip(x_positions, MONTHS_6)
    )
    return f"""
    <div class="graph-placeholder">
      <svg class="graph-svg" viewBox="0 0 720 280" role="img" aria-label="지출 그래프 예시">
        <line class="graph-grid-line" x1="48" y1="56" x2="672" y2="56" />
        <line class="graph-grid-line" x1="48" y1="118" x2="672" y2="118" />
        <line class="graph-grid-line" x1="48" y1="180" x2="672" y2="180" />
        <line class="graph-axis-line" x1="48" y1="232" x2="672" y2="232" />
        <polyline class="graph-dotted-line" points="{point_attr}" />
        {circles}
        {labels}
      </svg>
      <span class="graph-data-note">(데이터 연동 필요)</span>
    </div>
    """


def render_profile_header():
    st.markdown(
        """
        <section class="profile-header-card">
          <div class="profile-identity">
            <span class="large-avatar">👤</span>
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


def render_profile_page():
    top_left, top_right = st.columns([5, 1.35], vertical_alignment="top")
    with top_left:
        render_profile_header()
    with top_right:
        st.write("")
        st.write("")
        if st.button("✏️ 내 정보 수정", use_container_width=True):
            st.session_state.open_info_modal = True
            st.rerun()

    left, right = st.columns([1, 2.65], gap="large")

    with left:
        for category in BILL_CATEGORIES:
            prefix = "✅" if st.session_state.selected_category == category else ""
            if st.button(f"{prefix} {category}  ›", key=f"category_{category}", use_container_width=True):
                st.session_state.selected_category = category
                st.rerun()

        if st.button("➕ 수정하기  ›", use_container_width=True):
            st.session_state.open_feature_modal = True
            st.rerun()

    with right:
        st.markdown(
            f"""
            <article class="graph-card">
              <div class="graph-header">
                <div>
                  <p class="eyebrow">지출 리포트</p>
                  <h2 class="graph-title">{safe_html(st.session_state.selected_category)} 지출 그래프</h2>
                </div>
                <span class="pill safe-chip">보호 분석 대기</span>
              </div>
            </article>
            """,
            unsafe_allow_html=True,
        )

        period = st.radio(
            "기간 선택",
            ["6개월", "1년"],
            horizontal=True,
            key="selected_period",
            label_visibility="collapsed",
        )
        if period == "1년":
            st.info("1년 그래프는 데모용으로 6개월 데이터를 확장 표시합니다. 실제 데이터 연동 필요.")
        st.markdown(render_graph_svg(st.session_state.selected_category), unsafe_allow_html=True)

        values = SAMPLE_BILLS[st.session_state.selected_category]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">최근 금액</div><div class="metric-value">{values[-1]:,}원</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            avg = sum(values[:-1]) / max(len(values[:-1]), 1)
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">이전 평균</div><div class="metric-value">{avg:,.0f}원</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            change = ((values[-1] - avg) / avg * 100) if avg else 0
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">변동률</div><div class="metric-value">{change:+.1f}%</div></div>',
                unsafe_allow_html=True,
            )


def render_info_modal_body():
    st.caption("개인정보 보호")
    st.subheader("내 정보 수정")
    st.session_state.mask_strength = st.slider(
        "마스킹 강도",
        min_value=10,
        max_value=80,
        step=10,
        value=st.session_state.mask_strength,
    )
    for field in PROFILE_FIELDS:
        st.text_input(
            field["label"],
            value=mask_sensitive_value(field["value"], st.session_state.mask_strength),
            disabled=True,
            key=f"masked_{field['label']}_{st.session_state.mask_strength}",
        )
    st.caption("(데이터 연동 필요)")
    if st.button("확인", use_container_width=True):
        st.session_state.open_info_modal = False
        st.rerun()


def render_feature_modal_body():
    st.caption(BRAND_NAME)
    st.subheader("기능 추가")
    st.session_state.feature_query = st.text_input(
        "기능 검색",
        value=st.session_state.feature_query,
        placeholder="추가할 기능을 검색하세요",
        label_visibility="collapsed",
    )
    query = st.session_state.feature_query.strip()
    filtered = [feature for feature in FEATURE_SUGGESTIONS if query in feature] if query else FEATURE_SUGGESTIONS

    if filtered:
        for feature in filtered:
            st.markdown(
                f'<div class="feature-item"><strong>🛡️ {safe_html(feature)}</strong><small>(데이터 연동 필요)</small></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<div class="notice-box">(데이터 연동 필요)</div>', unsafe_allow_html=True)

    if st.button("닫기", use_container_width=True):
        st.session_state.open_feature_modal = False
        st.rerun()


def render_dialogs():
    if st.session_state.open_info_modal:
        if hasattr(st, "dialog"):
            @st.dialog("내 정보 수정")
            def info_dialog():
                render_info_modal_body()
            info_dialog()
        else:
            with st.expander("내 정보 수정", expanded=True):
                render_info_modal_body()

    if st.session_state.open_feature_modal:
        if hasattr(st, "dialog"):
            @st.dialog("기능 추가")
            def feature_dialog():
                render_feature_modal_body()
            feature_dialog()
        else:
            with st.expander("기능 추가", expanded=True):
                render_feature_modal_body()


def main():
    init_state()
    render_sidebar()

    if st.session_state.current_view == "profile":
        render_profile_page()
    else:
        render_chat_home()

    render_dialogs()


if __name__ == "__main__":
    main()
