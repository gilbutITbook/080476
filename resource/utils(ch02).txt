from openai import OpenAI

# API Key 입력
OPENAI_API_KEY = "API_Key_입력"

# 클라이언트 생성 
sync_client = OpenAI(
    api_key = OPENAI_API_KEY,
)

# LLM 호출 함수 선언
def llm_call(prompt: str, model: str = "gpt-4o-mini") -> str:
    messages = []
    messages.append({"role": "user", "content": prompt})
    chat_completion = sync_client.chat.completions.create(
        model = model,
        messages = messages,
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    test = llm_call("한국의 수도는?")
    print(test)