import google.generativeai as genai
import asyncio
import sys
import os

# Add backend directory to Python path for Vercel compatibility
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test():
    # Try to get API key from environment (Vercel) or local .env
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        # Try local .env file
        try:
            from dotenv import load_dotenv
            load_dotenv()
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
        except ImportError:
            pass
    
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    
    genai.configure(api_key=gemini_api_key)
    
    def dummy_func(a: int) -> int:
        return a + 1
    
    model = genai.GenerativeModel('gemini-3.1-flash-lite', tools=[dummy_func])
    chat = model.start_chat()
    
    resp = await chat.send_message_async("Suma 2 a 3 usando dummy_func con a=2")
    print("AI dice:", resp.parts[0])
    
    if resp.parts[0].function_call:
        fc = resp.parts[0].function_call
        print("Llamó a función:", fc.name)
        
        # Opcion 1: dict directo
        try:
            resp2 = await chat.send_message_async(
                [{"function_response": {"name": fc.name, "response": {"result": 3}}}]
            )
            print("Dict funcionó:", resp2.text)
        except Exception as e:
            print("Dict falló:", e)
            try:
                import google.ai.generativelanguage as gl
                part = gl.Part(function_response=gl.FunctionResponse(name=fc.name, response={"result": 3}))
                resp2 = await chat.send_message_async(part)
                print("gl.Part funcionó:", resp2.text)
            except Exception as e2:
                print("gl.Part falló:", e2)

# Test Vercel API endpoints compatibility
async def test_vercel_endpoints():
    """Test Vercel serverless functions for Angelus Sentinel"""
    import aiohttp
    
    base_url = "https://angelus-sentinel.vercel.app/api"
    
    endpoints = [
        "/admision/emergencia",
        "/chat",
        "/patients/1726354910"
    ]
    
    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints:
            try:
                url = f"{base_url}{endpoint}"
                async with session.get(url) as response:
                    print(f"GET {url}: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        print(f"Response: {data}")
                    else:
                        text = await response.text()
                        print(f"Error: {text}")
            except Exception as e:
                print(f"Error testing {endpoint}: {e}")

if __name__ == "__main__":
    print("=== Testing Gemini AI Function Response ===")
    asyncio.run(test())
    
    print("\n=== Testing Vercel API Endpoints ===")
    asyncio.run(test_vercel_endpoints())
