import os, json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_pattern(prompt: str, model="gpt-5-mini", layer: str = "melody", key: str = "C minor", bpm: int = 120, bars: int = 8) -> dict:
    """Generate a pattern using OpenAI API or return a mock pattern for testing."""
    
    # Check if we have an API key, if not return a mock pattern
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  No OPENAI_API_KEY found, using mock pattern for testing...")
        return {
            "metadata": {
                "layer": layer,
                "bpm": bpm,
                "key": key,
                "bars": bars
            },
            "pattern": [
                {"note": 60, "velocity": 90, "duration": 480, "bar": 1, "beat": 1.0},
                {"note": 62, "velocity": 85, "duration": 240, "bar": 1, "beat": 2.0},
                {"note": 64, "velocity": 88, "duration": 240, "bar": 1, "beat": 3.0},
                {"note": 65, "velocity": 92, "duration": 480, "bar": 1, "beat": 4.0},
                {"note": 67, "velocity": 87, "duration": 480, "bar": 2, "beat": 1.0},
                {"note": 69, "velocity": 90, "duration": 240, "bar": 2, "beat": 2.0},
                {"note": 67, "velocity": 85, "duration": 240, "bar": 2, "beat": 3.0},
                {"note": 65, "velocity": 88, "duration": 480, "bar": 2, "beat": 4.0}
            ]
        }
    
    # Use actual OpenAI API if key is available
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)