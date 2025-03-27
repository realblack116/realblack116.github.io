from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

import uuid
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def chatbot_proxy(request):
    if request.method != 'POST':
        return JsonResponse({'reply': '허용되지 않은 요청'}, status=405)

    try:
        user_payload = json.loads(request.body)
        user_msg = user_payload.get("messages", [{}])[-1].get("content", "")

        preset_messages = [
            {
                "role": "system",
                "content": "당신은 [TEo] 웹사이트에 탑재된 고객 지원 챗봇입니다.\n\n방문자에게 제공하는 프로그램은 다음과 같습니다:\n1. 유튜브 동영상 다운로더\n2. 모션캡쳐 프로그램\n3. 모션 기반 컴퓨터 제어 프로그램\n\n챗봇은 고객의 질문에 친절하고 정중하게 한국어로 답변하며, 사용 예시, 기능, 설치법 등을 명확하게 설명합니다. 결제 안내도 포함합니다."
            },
            {
                "role": "user",
                "content": user_msg
            }
        ]

        request_data = {
            "messages": preset_messages,
            "topP": 0.6,
            "topK": 0,
            "maxTokens": 200,
            "temperature": 0.5,
            "repeatPenalty": 1.2,
            "stopBefore": [],
            "includeAiFilters": True,
            "seed": 0
        }

        response = requests.post(
            'https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003',
            headers={
                'X-NCP-CLOVASTUDIO-API-KEY': 'NTA0MjU2MWZlZTcxNDJiY5bY1T4wxwbYmo5lUTLoH1UEfCcbR1bGBdz1oSXHTqPl',
                'X-NCP-APIGW-API-KEY': 'ANjxbUjbYwHYtgWVaUOlVUv9Hf1BxCnvRKhVGkEe',
                'X-NCP-CLOVASTUDIO-REQUEST-ID': str(uuid.uuid4()),
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json'
            },
            json=request_data
        )

        try:
            raw_data = response.json()
        except Exception:
            return JsonResponse({"reply": "⚠️ Clova 응답이 올바르지 않습니다."}, status=502)

        result = raw_data.get("result", {})
        messages = result.get("messages") or raw_data.get("messages") or []

        if isinstance(messages, list):
            for msg in reversed(messages):
                if msg.get("role") == "assistant" and msg.get("content"):
                    return JsonResponse({"reply": msg["content"]})

        fallback = result.get("message", {}).get("content") or "답변이 없습니다."
        return JsonResponse({"reply": fallback})

    except Exception as e:
        return JsonResponse({'reply': f'⚠️ 서버 오류: {str(e)}'}, status=500)
