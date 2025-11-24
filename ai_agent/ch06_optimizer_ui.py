import streamlit as st
import requests
from utils import llm_call

# 주요 함수 재사용
def summarize_text(text, feedback_history=None):
    if feedback_history:
        prompt = (
            f"아래 내용을 요약해줘.\n"
            f"## {text}\n"
            f"## 이전 요약문 및 피드백 전체 기록\n{feedback_history}\n"
            f"평가 결과가 PASS가 되도록 이전 피드백을 모두 참고해 요약문을 생성해."
        )
    else:
        prompt = f"아래 내용을 요약해줘.\n{text}"
    return llm_call(prompt)

EVALUATOR_PROMPT = """
평가 기준에 따라 다음 요약문을 엄격하게 심사해.

1. 형식:
- 여러 항목으로 된 개조식이어야 하며, 한 문장이라도 개조식이 아니면 무조건 FAIL

2. 내용:
- 정의 또는 원리, 주요 장점, 활용 예 등 3가지 핵심 요소가 모두 포함되면 PASS
- 사소한 세부 내용, 인용, 부연 설명 누락은 FAIL이 아님

3. 표현:
- 모든 항목은 짧고 명확해야 함
- 불필요한 수식, 반복문, 비문, 맞춤법/띄어쓰기 오류가 2개 이상이면 FAIL

위 기준 중 하나라도 미달이면 반드시 FAIL을 부여해.

응답 양식:
- 평가 결과: PASS / FAIL
- 문제점 및 개선 방향: (FAIL인 경우 구체적으로)
"""

def evaluate_summary(content, summary):
    prompt = (
        f"{EVALUATOR_PROMPT}\n\n"
        f"<원문>\n{content}\n\n"
        f"<요약문>\n{summary}"
    )
    return llm_call(prompt)

# 반복 워크플로 함수 수정
def loop_workflow_ui(content, max_retries=5):
    feedback_history = ""
    last_summary = None
    last_evaluation = None

    for retries in range(max_retries):
        summary = summarize_text(content, feedback_history=feedback_history)
        evaluation = evaluate_summary(content, summary)
        last_summary = summary
        last_evaluation = evaluation

        # 중간 요약문과 평가 결과 출력
        with st.expander(f"📝 요약 & 평가 - 시도 {retries+1}", expanded=False):
            st.markdown(f"**[요약문]**\n\n{summary}\n\n**[평가 결과]**\n\n{evaluation}")

        # 평가를 통과한 경우
        if "평가 결과: PASS" in evaluation:
            st.success("✅ 통과! 최종 요약")
            st.markdown(summary)
            with st.expander(f"🔍 평가 결과 - 시도 {retries+1}", expanded=True):
                st.markdown(evaluation)
            return summary
        feedback_history += f"\n\n[시도: {retries+1}]\n- 요약문:\n{summary}\n- 평가 피드백:\n{evaluation}\n"

    # 최대 요약 횟수를 모두 소진한 경우
    st.warning("❌ 최대 시도 도달! 평가를 통과한 요약이 없습니다.")
    with st.expander("⛔ [최종 FAIL 시 요약문 & 마지막 평가 결과]", expanded=True):
        st.markdown(f"**[최종 FAIL 시 요약문]**\n\n{last_summary}\n\n**[마지막 평가 결과]**\n\n{last_evaluation}")
    return last_summary

def main():
    st.title(" 평가-최적화 에이전트")

    # 원문 입력 및 평가 기준 표시
    default_url = "https://raw.githubusercontent.com/dabidstudio/sample_files/refs/heads/main/sample_wiki_text.md"
    default_content = requests.get(default_url).text

    tabs = st.tabs(["원문", "평가 기준(참고용)"])
    with tabs[0]:
        content = st.text_area("📰 원문 입력", height=500, value=default_content)
    with tabs[1]:
        st.write(EVALUATOR_PROMPT)

    # 에이전트 실행
    if st.button("🚀 요약 실행"):
        with st.spinner("에이전트가 반복적으로 요약하는 중입니다..."):
            loop_workflow_ui(content, max_retries=5)

if __name__ == "__main__":
    main()
