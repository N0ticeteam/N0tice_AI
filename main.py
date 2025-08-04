from fastapi import FastAPI
from schemas import PredictionRequest, PredictionResponse
from services.gpt_service import generate_prompt, ask_gpt_full

app = app = FastAPI()

@app.post(
    "/predict",
    summary="GPT를 활용한 패소 확률 예측",
    description="유사 판례와 사용자 상황 기반으로 GPT가 패소 확률을 예측합니다.",
    tags=["산재 예측"]
)
def predict(request: PredictionRequest):
    prompt = generate_prompt(request.kindb, request.kindc)
    result = ask_gpt_full(prompt)

    return PredictionResponse(
        kindb=request.kindb,
        kindc=request.kindc,
        predictedLoseRate=result["predicted_rate"],
        similarCaseTotal=result["total_case"],
        similarCaseLost=result["lost_case"]
    )
