import streamlit as st

st.set_page_config(
    page_title="Green Guard Pay Beta",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #F7FAFF 0%, #EEF4FF 100%);
}

.main-card {
    background: white;
    padding: 36px;
    border-radius: 28px;
    box-shadow: 0 16px 40px rgba(37, 99, 235, 0.12);
    border: 1px solid rgba(37, 99, 235, 0.12);
}

.logo-box {
    width: 72px;
    height: 72px;
    border-radius: 24px;
    background: linear-gradient(135deg, #2F80ED, #1D4ED8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #0F172A;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 18px;
    color: #475569;
    line-height: 1.7;
    margin-bottom: 28px;
}

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #0F172A;
    margin-top: 28px;
    margin-bottom: 12px;
}

.small-text {
    color: #64748B;
    font-size: 14px;
}

.result-box {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 20px;
    padding: 24px;
    margin-top: 18px;
}

.warning-box {
    background: #FFF7ED;
    border: 1px solid #FED7AA;
    border-radius: 20px;
    padding: 20px;
    margin-top: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-card">
    <div class="logo-box">🛡️</div>
    <div class="hero-title">Green Guard Pay Beta</div>
    <div class="hero-subtitle">
        시몽키 팀의 금융 비서 프로토타입입니다.<br>
        소비, 공과금, 절약 가능 금액을 빠르게 분석합니다.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("이번 달 소비", "520,000원", "-8%")

with col2:
    st.metric("공과금 예상", "143,000원", "+12%")

with col3:
    st.metric("절약 가능 금액", "68,000원", "+22%")

st.markdown('<div class="section-title">소비 정보 입력</div>', unsafe_allow_html=True)
st.markdown('<div class="small-text">현재는 베타 데모라서 직접 입력한 값으로 간단 분석합니다.</div>', unsafe_allow_html=True)

income = st.number_input("월 소득", min_value=0, step=10000)
food = st.number_input("식비", min_value=0, step=10000)
transport = st.number_input("교통비", min_value=0, step=10000)
utility = st.number_input("공과금", min_value=0, step=10000)
etc = st.number_input("기타 지출", min_value=0, step=10000)

total = food + transport + utility + etc

if st.button("분석하기", use_container_width=True):
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("분석 결과")
    st.write(f"총 지출은 **{total:,}원**입니다.")

    if income > 0:
        ratio = total / income * 100
        st.write(f"소득 대비 지출 비율은 **{ratio:.1f}%**입니다.")

        if ratio >= 70:
            st.warning("지출 비율이 높은 편입니다. 식비, 공과금, 기타 지출을 먼저 확인해보세요.")
        elif ratio >= 40:
            st.info("지출 비율이 보통 수준입니다. 고정비와 공과금 변화를 관리하면 좋아요.")
        else:
            st.success("지출 비율이 안정적인 편입니다.")
    else:
        st.info("월 소득을 입력하면 지출 비율까지 계산할 수 있습니다.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="warning-box">
    <b>Beta Notice</b><br>
    이 화면은 기능 검증용 Streamlit 베타입니다. 최종 서비스 화면은 React로 구현할 예정입니다.
</div>
""", unsafe_allow_html=True)
