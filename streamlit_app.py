import streamlit as st

# 1. 웹 페이지 제목 설정
st.set_page_config(page_title="카페인 반감기 계산기", page_icon="☕")
st.title('📚 시험기간 카페인 반감기 계산기')
st.markdown("---")

# 2. 음료 데이터 정의
drinks = ['아메리카노', '몬스터 에너지', '핫식스', '캔커피']
caffeine = [150, 130, 60, 80]
drink_dict = dict(zip(drinks, caffeine))

# 3. 음료 메뉴판 표시
st.subheader('[ ☕ 음료 메뉴 ]')
# 보기 좋게 표(Table) 형태로 대시보드에 출력
menu_table = {"음료명": drinks, "카페인 함량 (mg)": caffeine}
st.table(menu_table)

# 4. 세션 상태(Session State) 초기화
# 사용자가 추가한 음료 목록을 기억하기 위한 저장소입니다.
if 'consumed_drinks' not in st.session_state:
    st.session_state.consumed_drinks = []

st.subheader('🥤 섭취한 음료 기록하기')

# st.selectbox를 활용해 직관적으로 음료 선택
selected_drink = st.selectbox('섭취한 음료를 선택하세요:', drinks)

# 버튼을 한 줄에 배치하기 위한 컬럼 구성
col1, col2 = st.columns([1, 1])

with col1:
    if st.button('➕ 음료 추가하기', use_container_width=True):
        st.session_state.consumed_drinks.append(selected_drink)
        st.toast(f'-> [{selected_drink}] 집계 완료!')

with col2:
    if st.button('🔄 기록 초기화', use_container_width=True):
        st.session_state.consumed_drinks = []
        st.toast('모든 기록이 초기화되었습니다.')

# 5. 총 카페인 계산 및 출력
total_caffeine = sum(drink_dict[drink] for drink in st.session_state.consumed_drinks)

if st.session_state.consumed_drinks:
    st.info(f"**현재까지 마신 음료:** {', '.join(st.session_state.consumed_drinks)}")
else:
    st.caption("아직 추가된 음료가 없습니다.")

# 대시보드 스타일로 총 카페인 표시
st.metric(label="[최종 결과] 섭취한 총 카페인", value=f"{total_caffeine} mg")
st.markdown("---")

# 6. 취침 전 공부 시간 입력 및 반감기 계산
st.subheader('⏰ 취침 전 남은 시간 입력')
sleep = st.number_input('몇 시간 더 공부하다 잠에 들 예정인가요? (정수 입력):', min_value=0, value=0, step=1)

# 시간 경과에 따른 카페인 잔류량 계산 (시간당 13%씩 감소 = 87% 남음)
remaining_caffeine = total_caffeine * (0.87 ** sleep)

# 7. 최종 안전 결과 출력
if total_caffeine > 0:
    st.subheader('📊 체내 카페인 예측 결과')
    st.write(f"⏱️ **{sleep}시간 후** 체내에 남아있는 카페인: **{remaining_caffeine:.2f} mg**")
    
    if remaining_caffeine <= 50:
        st.success('✅ **[안전!]** 체내 카페인 양이 안전수치(50mg 이하)로 떨어집니다. 열공하고 푹 주무세요! :)')
    else:
        st.error('🚨 **[위험!]** 체내 카페인 양이 아직 높습니다. 수면의 질이 떨어지거나 숙면이 어려울 수 있습니다.')