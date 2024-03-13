"""
Initializes API KEY in the init
"""

import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()
# load API for embeddings voyage
API_KEY = os.environ['API_KEY']
