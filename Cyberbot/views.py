from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import UploadedImage
from .predict import predict_single_image
import json
import openai
import re
from urllib.parse import urlparse

# ---------------- Chatbot API ----------------
def chat_page(request):
    return render(request, "Cyberbot/chat.html")  # your chat template






# ---------------- Image Prediction ----------------
@csrf_exempt
@require_POST
def predict_api(request):
    image_file = request.FILES.get("image")
    if not image_file:
        return JsonResponse({"error": "No image provided"}, status=400)
    try:
        uploaded_instance = UploadedImage.objects.create(image=image_file)
        result = predict_single_image(image_file)
        uploaded_instance.prediction = result["label"]
        uploaded_instance.save()
        result["id"] = uploaded_instance.id
        return JsonResponse({
            "label": result["label"],
            "confidence": f"{result['confidence']:.2f}%",
            "id": uploaded_instance.id
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def fake_real_image_view(request):
    result = None
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        uploaded_instance = UploadedImage.objects.create(image=uploaded_file)
        pred = predict_single_image(uploaded_file)
        uploaded_instance.prediction = pred["label"]
        uploaded_instance.save()
        result = {
            'label': pred["label"],
            'confidence': f"{pred['confidence']:.2f}%",
            'id': uploaded_instance.id,
            'image_url': uploaded_instance.image.url
        }
    return render(request, 'Cyberbot/fakerealimage.html', {'result': result})


# ---------------- Image Upload ----------------
@csrf_exempt
@require_POST
def upload_image(request):
    image_file = request.FILES.get("image")
    if not image_file:
        return JsonResponse({"error": "No image provided"}, status=400)
    try:
        uploaded_instance = UploadedImage.objects.create(image=image_file)
        uploaded_instance.save()
        return JsonResponse({
            "message": "Image uploaded successfully",
            "id": uploaded_instance.id,
            "image_url": uploaded_instance.image.url
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ---------------- Password Strength ----------------
def _password_strength(password: str):
    rules = {
        'length>=12': len(password) >= 12,
        'upper': any(c.isupper() for c in password),
        'lower': any(c.islower() for c in password),
        'digit': any(c.isdigit() for c in password),
        'symbol': any(c in "!@#$%^&*()-_=+[]{};:'\",.<>/?`~|" for c in password),
    }
    score = sum(rules.values())
    if score <= 2:
        label = 'Weak'
    elif score == 3:
        label = 'Fair'
    elif score == 4:
        label = 'Good'
    else:
        label = 'Strong'

    parts = []
    if not rules['length>=12']:
        parts.append('Use at least 12 characters')
    if not rules['upper']:
        parts.append('Add uppercase letters')
    if not rules['lower']:
        parts.append('Add lowercase letters')
    if not rules['digit']:
        parts.append('Add numbers')
    if not rules['symbol']:
        parts.append('Add special symbols')

    recommendation = '; '.join(parts) if parts else 'Great password.'
    return {'score': score, 'label': label, 'recommendation': recommendation}


@csrf_exempt
@require_POST
def check_password_complete(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    password = payload.get('password')
    if not password:
        return JsonResponse({'error': 'Password required'}, status=400)

    strength = _password_strength(password)
    return JsonResponse({
        'strength': {'label': strength['label'], 'score': strength['score']},
        'breach': {'breached': False, 'count': 0},
        'recommendation': strength['recommendation']
    })


# ---------------- URL Safety ----------------
@csrf_exempt
@require_POST
def check_url_safety(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
        url = (payload.get('url') or '').strip()
        if not url:
            return JsonResponse({'error': 'URL required'}, status=400)

        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        threats = []

        if re.search(r'[0-9]', domain):
            threats.append('Possible look-alike domain')
        if domain.count('-') >= 3:
            threats.append('Too many hyphens in domain')
        if re.search(r'[%=&]', url):
            threats.append('Suspicious special characters')
        if domain.count('.') >= 4:
            threats.append('Too many subdomains')
        if len(domain) > 50:
            threats.append('Unusually long domain')

        return JsonResponse({'safe': len(threats) == 0, 'threats': threats})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ---------------- Train Model Stub ----------------
@csrf_exempt
def train_model(request):
    if request.method == "POST":
        return JsonResponse({"status": "success", "message": "Training started"})
    return JsonResponse({"status": "error", "message": "POST request required"})


# ---------------- Simple Static Pages ----------------
def hello_world(request): return render(request, 'Cyberbot/hello.html')
def home(request): return render(request, 'Cyberbot/homepage.html')
def cyber(request): return render(request, 'Cyberbot/cyber.html')
def login_view(request): return render(request, 'Cyberbot/login.html')
def cyberbot(request): return render(request, 'Cyberbot/cyberbot.html')
def chatbot(request): return render(request, 'Cyberbot/chatbot.html')
def my_view(request): return render(request, 'Cyberbot/fakerealimage.html')
def email_view(request): return render(request, 'Cyberbot/email.html')
def verify_view(request): return render(request, 'Cyberbot/verify.html')

# ---------------- Reset Password View ----------------
def reset_password_view(request): 
    return render(request, 'Cyberbot/reset_password.html')
def api_index(request):
    """
    Simple API landing page
    """
    return JsonResponse({"message": "Welcome to the Cyberbot API"})
