import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api_keys import create_api_key

name = sys.argv[1] if len(sys.argv) > 1 else "default"
key = create_api_key(name)
print(f"API key for '{name}': {key}")
