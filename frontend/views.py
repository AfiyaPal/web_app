
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from decouple import config
import logging

logger = logging.getLogger(__name__)

def generate_ai_response(user_msg: str) -> str:
    """Return AI response or a helpful error message using the official `google-genai` client."""
    api_key = config('GEMINI_API_KEY', default=None)
    if not api_key:
        logger.warning("GEMINI_API_KEY not found in environment or .env file")
        return "AI unavailable: GEMINI_API_KEY is not configured on the server."

    try:
        from google import genai
    except ImportError:
        logger.error("google-genai library not installed.")
        return "AI unavailable: The google-genai library is not installed on the server."

    try:
        client = genai.Client(api_key=api_key)
        system_prompt = (
            "You are Afiyapal, a multi-agent AI health assistant serving underserved communities in Kenya. "
            "Your core mission is to provide evidence-based first aid, clinical myth-busting, and healthcare navigation. "
            
            "GUIDELINES FOR RESPONSE:"
            "1. FIRST AID: Use the provided FirstAidQA context to give immediate, actionable steps for common injuries (e.g., back pain, RSI). Always suggest a medical professional for persistent symptoms."
            "2. MYTH-BUSTING: Compare user claims (e.g., 'okra water') against verified medical data. Be firm but respectful in debunking. If a claim is unverified, state: 'This has been sent to our medical board for professional review.'"
            "3. CLINIC LOCATOR: If the user reports acute pain or requests a doctor, prompt them for their location to trigger the Clinic Finder tool. Prioritize Afiyapal-registered professionals."
            "4. TONE: Compassionate, culturally relevant, and jargon-free. Use Swahili greetings where appropriate (e.g., 'Habari', 'Pole')."
            
            "SAFETY & RED FLAGS:"
            "If the user describes life-threatening symptoms (heavy bleeding, difficulty breathing, chest pain), "
            "immediately override all advice and provide emergency contact details/nearest hospital location. "
            
            "LEGAL DISCLAIMER:"
            "Always append: 'This is informational guidance. For medical emergencies, visit the nearest facility immediately.'"
        )
        user_prompt = f"User: {user_msg}\n\nProvide a helpful, evidence-based response using your specialties above."

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=system_prompt + "\n\n" + user_prompt,
        )

        text = getattr(response, 'text', None)
        if not text:
            try:
                text = response.candidates[0].content[0].text
            except Exception:
                text = str(response)

        return text.strip()
    except Exception as e:
        logger.error(f"google-genai request failed: {e}")
        return "Sorry, I'm having trouble connecting right now. Please try again later."

def home(request):
    """Home page view."""
    return render(request, "frontend/index.html", {"title": "Home", "user": request.user})

@xframe_options_exempt
def chatbot(request):
    """Handles chat page rendering and AJAX message posting."""
    template = 'frontend/chatbot_frame.html' if request.GET.get('embedded') == '1' else 'frontend/chatbot.html'
    
    if request.GET.get('clear') == '1':
        request.session['chat_messages'] = []
        logger.info("Chat cleared")

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_msg = request.POST.get("message", "").strip()
        if not user_msg:
            return JsonResponse({"error": "Empty message"}, status=400)

        messages = request.session.get('chat_messages', [])
        messages.append({'sender': 'user', 'text': user_msg})
        
        ai_resp = generate_ai_response(user_msg)
        messages.append({'sender': 'ai', 'text': ai_resp})
        
        request.session['chat_messages'] = messages
        return JsonResponse({"text": ai_resp})

    return render(request, template, {
        'messages': request.session.get('chat_messages', []),
    })

@xframe_options_exempt
def chatbot_frame(request):
    """Dedicated view for iframe embedding. Handles chat logic via AJAX."""
    if request.GET.get('clear') == '1':
        request.session['chat_messages'] = []
        logger.info("Chat cleared")
        # No need to return anything special, will just render template with empty messages

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_msg = request.POST.get("message", "").strip()
        if not user_msg:
            return JsonResponse({"error": "Empty message"}, status=400)

        messages = request.session.get('chat_messages', [])
        messages.append({'sender': 'user', 'text': user_msg})

        ai_resp = generate_ai_response(user_msg)
        messages.append({'sender': 'ai', 'text': ai_resp})

        request.session['chat_messages'] = messages
        return JsonResponse({"sender": "ai", "text": ai_resp})

    # For initial GET request, just render the frame.
    return render(request, 'frontend/chatbot_frame.html', {
        'messages': request.session.get('chat_messages', []),
    })

def gemini_test(request):
    """Simple diagnostic view for Gemini."""
    try:
        sample = generate_ai_response('Say hello in one short sentence.')
        available = "AI unavailable" not in sample and "Sorry" not in sample
        return JsonResponse({'available': available, 'sample': sample})
    except Exception as e:
        logger.error(f"gemini_test exception: {e}")
        return JsonResponse({'available': False, 'sample': f"error: {e}"}, status=500)
