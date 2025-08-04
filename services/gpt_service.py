import openai
import re
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 1. 프롬프트 생성 함수
def generate_prompt(kindb: str, kindc: str) -> str:
    return f"""
당신은 산재 사건 판례 데이터를 바탕으로 판결 예측을 도와주는 법률 보조 AI입니다.

사용자의 상황은 다음과 같습니다:
- 질병 유형: {kindb}
- 근무 형태 및 상황: {kindc}

공공데이터 기반으로 유사한 사건들을 참고하여,
1. 사용자의 사건이 패소할 확률을 수치(%)로 예측해 주세요.
2. 몇 건 중 몇 건이 패소한 것으로 판단되는지도 알려 주세요.

⚠️ 아래 형식으로만 숫자와 간단한 문장으로 응답해 주세요:

패소 확률: 77.6%  
83건 중 56건이 패소한 것으로 확인됨
""".strip()

# 2. GPT 응답 파싱 함수
def parse_gpt_response(text: str) -> dict:
    rate_match = re.search(r"(\d+(\.\d+)?)\s*%", text)
    predicted_rate = float(rate_match.group(1)) if rate_match else None

    case_match = re.search(r"(\d+)\s*건\s*중\s*(\d+)\s*건", text)
    total_case = int(case_match.group(1)) if case_match else None
    lost_case = int(case_match.group(2)) if case_match else None

    return {
        "predicted_rate": predicted_rate,
        "total_case": total_case,
        "lost_case": lost_case,
        "raw": text
    }

# 3. GPT 호출 및 파싱 처리 함수
def ask_gpt_full(prompt: str) -> dict:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 판례 기반 패소 확률 예측 AI입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    content = response['choices'][0]['message']['content'].strip()
    return parse_gpt_response(content)