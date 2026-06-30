import streamlit as st

st.set_page_config(
    page_title="Green Guard Pay Beta",
    page_icon="🛡️",
    layout="wide"
)

st.title("Green Guard Pay Beta")
st.caption("시몽키 팀의 금융 비서 베타 프로토타입")

st.divider()

st.subheader("무엇을 분석할까요?")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("이번 달 소비", "520,000원", "-8%")

with col2:
    st.metric("공과금 예상", "143,000원", "+12%")

with col3:
    st.metric("절약 가능 금액", "68,000원", "+22%")

st.divider()

st.subheader("소비 정보 입력")

income = st.number_input("월 소득을 입력하세요", min_value=0, step=10000)
food = st.number_input("식비", min_value=0, step=10000)
transport = st.number_input("교통비", min_value=0, step=10000)
utility = st.number_input("공과금", min_value=0, step=10000)

total = food + transport + utility

if st.button("분석하기"):
    st.success("분석이 완료되었습니다.")

    st.write(f"총 지출: **{total:,}원**")

    if income > 0:
        ratio = total / income * 100
        st.write(f"소득 대비 지출 비율: **{ratio:.1f}%**")

        if ratio >= 70:
            st.warning("지출 비율이 높은 편입니다. 고정비와 식비를 먼저 확인해보세요.")
        elif ratio >= 40:
            st.info("지출 비율이 보통 수준입니다. 공과금 변화만 관리해도 좋아요.")
        else:
            st.success("지출 비율이 안정적인 편입니다.")
    else:
        st.info("월 소득을 입력하면 지출 비율까지 계산할 수 있습니다.")
