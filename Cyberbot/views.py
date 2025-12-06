from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import UploadedImage
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

import numpy as np
import tensorflow as tf
import json
import re
import os
from io import BytesIO
from PIL import Image




# ----- Lazy Load Model -----
model = None
def get_model():
    global model
    if model is None:
        model = tf.keras.models.load_model("fake_real_model.h5")
    return model

# ----- Prediction Function -----
def predict_image(image_file):
    model = get_model()

    # Read file
    image_file.seek(0)
    image_bytes = BytesIO(image_file.read())

    # Load PIL image
    img = Image.open(image_bytes).convert("RGB")
    img = img.resize((128,128))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array, verbose=0)[0]
    label_index = np.argmax(pred)

    label = "FAKE" if label_index == 0 else "REAL"
    confidence = float(pred[label_index] * 100)

    return label, round(confidence, 2)





# -------- API Endpoint --------
@csrf_exempt
def predict_api(request):
    if request.method == "POST":
        image_file = request.FILES.get("image")
        if not image_file:
            return JsonResponse({"error": "No image provided"}, status=400)

        try:
            label, confidence = predict_image(image_file)
            return JsonResponse({
                "label": label,
                "confidence": f"{confidence:.2f}%",
                "id": f"REC-{np.random.randint(100000,999999)}"
            })
        except Exception as e:
            import traceback
            print("ERROR in predict_api:", traceback.format_exc())
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST request required"}, status=400)



# -------- Django Form Page --------
def fake_real_image_view(request):
    result = None
    color = None

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']

        uploaded_instance = UploadedImage.objects.create(image=uploaded_file)

        label, confidence = predict_image(uploaded_file)

        uploaded_instance.prediction = label
        uploaded_instance.save()

        result = {
            'label': label,
            'confidence': f"{confidence:.2f}%",
            'id': uploaded_instance.id,
            'image_url': uploaded_instance.image.url
        }

        color = 'green' if label.lower() == 'real' else 'red'

    return render(request, 'Cyberbot/fakerealimage.html', {
        'result': result,
        'color': color
    })


# -------- Simple Page Views --------

def hello_world(request):
    return render(request, 'Cyberbot/hello.html')

def home(request):
    return render(request, 'Cyberbot/homepage.html')

def cyber(request):
    return render(request, 'Cyberbot/cyber.html')

def login_view(request):
    return render(request, 'Cyberbot/login.html')

def cyberbot(request):
    return render(request, 'Cyberbot/cyberbot.html')

def chatbot(request):
    return render(request, 'Cyberbot/chatbot.html')

def my_view(request):
    return render(request, 'Cyberbot/fakerealimage.html')

def email_view(request):
    return render(request, 'Cyberbot/email.html')

def verify_view(request):
    return render(request, 'Cyberbot/verify.html')

def reset_password_view(request):
    return render(request, 'Cyberbot/reset_password.html')


# -------- API Index --------
def api_index(request):
    return JsonResponse({"message": "API Working"})


# -------- Password Strength Checker --------
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
    if not rules['length>=12']: parts.append('Use at least 12 characters')
    if not rules['upper']: parts.append('Add uppercase letters')
    if not rules['lower']: parts.append('Add lowercase letters')
    if not rules['digit']: parts.append('Add numbers')
    if not rules['symbol']: parts.append('Add special symbols')

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


# -------- URL Safety Checker --------
@csrf_exempt
@require_POST
def check_url_safety(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    url = (payload.get('url') or '').strip()
    if not url:
        return JsonResponse({'error': 'URL required'}, status=400)

    if not re.match(r'^https?://', url):
        url = 'http://' + url

    threats = []
    lowered = url.lower()

    suspicious_keywords = ['login-', 'update-account', 'verify', 'free-gift', 'banking-secure', 'steamcommunity-']
    if any(k in lowered for k in suspicious_keywords):
        threats.append('Suspicious keyword in URL')

    if '@' in lowered:
        threats.append('Contains @ symbol')

    if re.search(r'//\d{1,3}(?:\.\d{1,3}){3}', lowered):
        threats.append('Direct IP address')

    if len(url) > 120:
        threats.append('Unusually long URL')

    return JsonResponse({'safe': len(threats) == 0, 'threats': threats})


# -------- Train Model Endpoint --------
@csrf_exempt
def train_model(request):
    if request.method == "POST":
        print("Training started...")
        return JsonResponse({"status": "success", "message": "Training started"})
    return JsonResponse({"status": "error", "message": "POST request required"})