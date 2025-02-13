import os
from dotenv import load_dotenv

def configure():
    load_dotenv()

configure()
print(os.getenv("GEMINI_KEY"))
