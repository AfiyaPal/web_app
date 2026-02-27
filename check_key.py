import os
from decouple import config
print('ENV GEMINI_API_KEY present?', 'GEMINI_API_KEY' in os.environ)
try:
    print('config gives:', config('GEMINI_API_KEY'))
except Exception as e:
    print('config error', e)