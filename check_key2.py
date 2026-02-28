import os
from decouple import config
print('start')
print('ENV key present', 'GEMINI_API_KEY' in os.environ)
try:
    val = config('GEMINI_API_KEY')
    print('config returned non-empty' if val else 'config returned empty string')
    print('length', len(val))
except Exception as e:
    print('config error', e)
print('end')