import streamlit as st

# MBTI 질문 및 답변에 따른 점수 정의
# 각 질문은 E/I, S/N, T/F, J/P 중 하나의 지표에 영향을 줍니다.
# 'score_type': 'E' 또는 'I' 등 해당 지표의 긍정적인 방향
# 'score_value': 해당 답변 선택 시 부여되는 점수 (양수 또는 음수)
questions = [
    {
        "question": "파티에서 새로운 사람들과 어울리는 것을 즐기시나요?",
        "options": [
            {"text": "네, 매우 즐깁니다.", "score_type": "E", "score_value": 1},
            {"text": "아니요, 주로 아는 사람들과 이야기합니다.", "score_type": "I", "score_value": 1},
        ]
    },
    {
        "question": "활동적인 모임보다 조용한 시간을 선호하시나요?",
        "options": [
            {"text": "네, 조용한 시간이 좋습니다.", "score_type": "I", "score_value": 1},
            {"text": "아니요, 활동적인 것이 좋습니다.", "score_type": "E", "score_value": 1},
        ]
    },
    {
        "question": "실용적이고 현실적인 정보를 선호하시나요?",
        "options": [
            {"text": "네, 구체적인 사실이 중요합니다.", "score_type": "S", "score_value": 1},
            {"text": "아니요, 아이디어나 개념에 관심이 많습니다.", "score_type": "N", "score_value": 1},
        ]
    },
    {
        "question": "미래의 가능성과 아이디어에 더 관심이 많으신가요?",
        "options": [
            {"text": "네, 상상하고 예측하는 것을 좋아합니다.", "score_type": "N", "score_value": 1},
            {"text": "아니요, 현재에 집중하는 편입니다.", "score_type": "S", "score_value": 1},
        ]
    },
    {
        "question": "결정을 내릴 때 논리와 객관성을 중요하게 생각하시나요?",
        "options": [
            {"text": "네, 합리적인 분석이 우선입니다.", "score_type": "T", "score_value": 1},
            {"text": "아니요, 사람들과의 관계나 가치를 고려합니다.", "score_type": "F", "score_value": 1},
        ]
    },
    {
        "question": "타인의 감정과 조화를 고려하여 결정하시나요?",
        "options": [
            {"text": "네, 주변 사람들의 감정을 중요하게 생각합니다.", "score_type": "F", "score_value": 1},
            {"text": "아니요, 원칙과 기준에 따라 결정합니다.", "score_type": "T", "score_value": 1},
        ]
    },
    {
        "question": "계획을 세우고 체계적으로 일을 처리하는 것을 선호하시나요?",
        "options": [
            {"text": "네, 미리 계획하는 것이 편합니다.", "score_type": "J", "score_value": 1},
            {"text": "아니요, 유연하게 상황에 맞춰 움직입니다.", "score_type": "P", "score_value": 1},
        ]
    },
    {
        "question": "자유롭고 유연하게 상황에 맞춰 행동하는 것을 좋아하시나요?",
        "options": [
            {"text": "네, 즉흥적인 것을 즐깁니다.", "score_type": "P", "score_value": 1},
            {"text": "아니요, 정해진 틀 안에서 일하는 것이 좋습니다.", "score_type": "J", "score_value": 1},
        ]
    },
]

# MBTI 유형별 설명 (간단하게)
mbti_descriptions = {
    "ISTJ": "청렴결백한 논리주의자",
    "ISFJ": "용감한 수호자",
    "INFJ": "선의의 옹호자",
    "INTJ": "용의주도한 전략가",
    "ISTP": "만능 재주꾼",
    "ISFP": "호기심 많은 예술가",
    "INFP": "열정적인 중재자",
    "INTP": "논리적인 사색가",
    "ESTP": "모험을 즐기는 사업가",
    "ESFP": "자유로운 영혼의 연예인",
    "ENFP": "재기발랄한 활동가",
    "ENTP": "뜨거운 논쟁을 즐기는 변론가",
    "ESTJ": "엄격한 관리자",
    "ESFJ": "사교적인 외교관",
    "ENFJ": "정의로운 사회운동가",
    "ENTJ": "대담한 통솔자",
}

def calculate_mbti(scores):
    """
    점수를 바탕으로 MBTI 유형을 계산합니다.
    """
    mbti_type = ""

    # E/I 지표
    if scores['E'] >= scores['I']:
        mbti_type += "E"
    else:
        mbti_type += "I"

    # S/N 지표
    if scores['S'] >= scores['N']:
        mbti_type += "S"
    else:
        mbti_type += "N"

    # T/F 지표
    if scores['T'] >= scores['F']:
        mbti_type += "T"
    else:
        mbti_type += "F"

    # J/P 지표
    if scores['J'] >= scores['P']:
        mbti_type += "J"
    else:
        mbti_type += "P"

    return mbti_type

# Streamlit 앱 시작
st.set_page_config(page_title="역동적인 MBTI 분석", layout="centered")

st.title("🌟 역동적인 MBTI 분석 페이지 🌟")
st.markdown("아래 질문에 답하여 당신의 MBTI 유형을 알아보세요!")

# 점수 초기화
# session_state를 사용하여 앱이 새로고침되어도 점수가 유지되도록 합니다.
if 'scores' not in st.session_state:
    st.session_state.scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
if 'answers' not in st.session_state:
    st.session_state.answers = {} # 각 질문의 선택된 답변을 저장

# 각 질문을 표시하고 답변을 받습니다.
for i, q_data in enumerate(questions):
    st.subheader(f"{i+1}. {q_data['question']}")
    
    # 질문에 대한 고유한 키를 생성합니다.
    key = f"question_{i}"
    
    # st.radio를 사용하여 옵션을 표시합니다.
    # default 값을 None으로 설정하여 사용자가 선택하지 않은 상태로 시작합니다.
    # on_change 콜백 함수를 사용하여 선택이 변경될 때마다 점수를 업데이트합니다.
    selected_option_index = st.radio(
        "선택하세요:",
        options=[opt['text'] for opt in q_data['options']],
        key=key,
        index=st.session_state.answers.get(key, None) # 이전에 선택된 값 로드
    )

    # 사용자가 선택한 옵션의 인덱스를 저장합니다.
    if selected_option_index is not None:
        st.session_state.answers[key] = [opt['text'] for opt in q_data['options']].index(selected_option_index)

# 모든 질문에 대한 답변이 완료되었는지 확인
all_answered = all(f"question_{i}" in st.session_state.answers for i in range(len(questions)))

if st.button("✨ 결과 보기 ✨", use_container_width=True):
    if not all_answered:
        st.warning("모든 질문에 답변해주세요!")
    else:
        # 점수를 다시 계산합니다. (on_change에서 실시간으로 업데이트되지만, 버튼 클릭 시 최종 확인)
        st.session_state.scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
        for i, q_data in enumerate(questions):
            key = f"question_{i}"
            selected_idx = st.session_state.answers[key]
            selected_option = q_data['options'][selected_idx]
            st.session_state.scores[selected_option['score_type']] += selected_option['score_value']

        # MBTI 유형 계산
        mbti_result = calculate_mbti(st.session_state.scores)

        st.markdown("---")
        st.header(f"🎉 당신의 MBTI 유형은 바로... **{mbti_result}** 입니다! 🎉")
        st.write(f"**{mbti_result}**: {mbti_descriptions.get(mbti_result, '설명을 찾을 수 없습니다.')}")
        st.markdown("---")

        st.subheader("💡 각 지표별 점수:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="외향(E) vs 내향(I)", value=f"E: {st.session_state.scores['E']}, I: {st.session_state.scores['I']}")
        with col2:
            st.metric(label="감각(S) vs 직관(N)", value=f"S: {st.session_state.scores['S']}, N: {st.session_state.scores['N']}")
        with col3:
            st.metric(label="사고(T) vs 감정(F)", value=f"T: {st.session_state.scores['T']}, F: {st.session_state.scores['F']}")
        with col4:
            st.metric(label="판단(J) vs 인식(P)", value=f"J: {st.session_state.scores['J']}, P: {st.session_state.scores['P']}")
