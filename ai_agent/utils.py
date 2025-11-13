from openai import AsyncOpenAI, OpenAI

# API Key 입력
OPENAI_API_KEY = "API_key_입력"

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

# 비동기 클라이언트 생성
async_client = AsyncOpenAI(
    api_key = OPENAI_API_KEY,
)

# 비동기 LLM 호출 함수 선언
async def llm_call_async(prompt: str, model: str = "gpt-4o-mini") -> str:
    messages = []
    messages.append({"role": "user", "content": prompt})
    chat_completion = await async_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    print(model,"완료")

    return chat_completion.choices[0].message.content

# 웹 검색 LLM 호출 함수 선언
async def llm_search_async(prompt: str, model: str = "gpt-4.1") -> str:
    response = await async_client.responses.create(
        model = model,
        input = prompt,
        tools = [{"type": "web_search_preview"}],
    )
    return response.output_text

if __name__ == "__main__":
    test = llm_call("한국의 수도는?")
    print(test)