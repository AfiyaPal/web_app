from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decouple import config
import requests
import logging

logger = logging.getLogger(__name__)

def generate_ai_response(user_msg: str) -> str:
    """Return AI response or a helpful error message.
    This centralises Gemini usage so both views can call it and receive
    consistent, user-friendly error text when the key is missing or the
    API call fails.
    """
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
        return "Sorry, I'm having trouble connecting right now. Please try again or consult a healthcare professional if it's urgent."

def home(request):
    """Home page view."""
    context = {
        "title": "Home",
        "user": request.user,
    }
    return render(request, "frontend/index.html", context)

from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt

def chatbot(request):
    """
    Simple chat interface rendering a standalone page.
    Messages are kept in the session so a conversation can persist while the user
    keeps the browser window open. The POST payload should contain a single
    "message" field which is sent to Gemini; the AI response is appended to the
    chat history immediately.
    """
    logger.info(f"chatbot called with method: {request.method}")
    # get or initialise conversation history
    # handle a manual clear request
    if request.GET.get('clear') == '1':
        messages = []
        request.session['chat_messages'] = messages
        logger.info("Chat cleared")

    messages = request.session.get('chat_messages', [])

    if request.method == "POST":
        user_msg = request.POST.get("message", "").strip()
        logger.info(f"POST received with message: '{user_msg}'")
        if user_msg:
            # add user message
            messages.append({'sender': 'user', 'text': user_msg})
            logger.info(f"User message appended. Total messages: {len(messages)}")
            # use centralized helper for AI response (handles missing key and errors)
            ai_resp = generate_ai_response(user_msg)
            logger.info(f"AI response generated (chars): {len(ai_resp)}")

            messages.append({'sender': 'ai', 'text': ai_resp})
            request.session['chat_messages'] = messages
            logger.info(f"AI response appended. Total messages now: {len(messages)}")

    template = 'frontend/chatbot_frame.html' if request.GET.get('embedded') == '1' else 'frontend/chatbot.html'
    return render(request, template, {
        'messages': messages,
    })


@xframe_options_exempt
def chatbot_frame(request):
    """
    Dedicated view for iframe embedding. Always renders the minimal frame template.
    Handles chat message persistence and AI responses, same as chatbot() but guaranteed
    to return no header/footer/nav.
    """
    logger.info(f"chatbot_frame called with method: {request.method}")
    # handle a manual clear request
    if request.GET.get('clear') == '1':
        messages = []
        request.session['chat_messages'] = messages
        logger.info("Chat cleared")

    messages = request.session.get('chat_messages', [])

    if request.method == "POST":
        user_msg = request.POST.get("message", "").strip()
        logger.info(f"POST received with message: '{user_msg}'")
        if user_msg:
            # add user message
            messages.append({'sender': 'user', 'text': user_msg})
            logger.info(f"User message appended. Total messages: {len(messages)}")
            # use centralized helper for AI response (handles missing key and errors)
            ai_resp = generate_ai_response(user_msg)
            logger.info(f"AI response generated (chars): {len(ai_resp)}")

            messages.append({'sender': 'ai', 'text': ai_resp})
            request.session['chat_messages'] = messages
            logger.info(f"AI response appended. Total messages now: {len(messages)}")

    # Always use frame template (no header/footer/nav)
    return render(request, 'frontend/chatbot_frame.html', {
        'messages': messages,
    })


def gemini_test(request):
    """Simple diagnostic view to verify Gemini availability and a sample response.
    Returns JSON: { available: bool, sample: str }
    """
    sample = None
    available = False
    try:
        sample = generate_ai_response('Say hello in one short sentence.')
        is_unavailable = "AI unavailable" in sample
        is_error = "Sorry, I'm having trouble" in sample
        available = not (is_unavailable or is_error)

    except Exception as e:
        logger.error(f"gemini_test exception: {e}")
        sample = f"error: {e}"
        available = False

    return JsonResponse({
        'available': available,
        'sample': sample,
    })
