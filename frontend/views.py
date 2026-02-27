
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from decouple import config
import logging

logger = logging.getLogger(__name__)

def generate_ai_response(user_msg: str) -> str:
    """Return AI response or a helpful error message."""
    try:
        import google.generativeai as genai
        api_key = config('GEMINI_API_KEY', default=None)
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment or .env file")
            return "AI unavailable: GEMINI_API_KEY is not configured on the server."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        system_prompt = ("You are Afiyapal, a compassionate AI health assistant for underserved "
                         "communities in Mombasa, Kenya. Focus on mental health, myth-busting, "
                         "and first aid. Be concise and actionable.")
        user_prompt = f"User: {user_msg}\n\nProvide a helpful, evidence-based response using your specialties above."
        result = model.generate_content(system_prompt + "\n\n" + user_prompt)
        return result.text.strip()
    except ImportError:
        logger.error("Gemini API library not available.")
        return "AI unavailable: The necessary libraries are not installed on the server."
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
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
