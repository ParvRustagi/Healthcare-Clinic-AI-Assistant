import asyncio
from llm_service import get_llm_response

async def test():
    reply = get_llm_response("Book an appointment with Dr. Singh for Monday 3 PM")
    print("LLM Reply:", reply)

asyncio.run(test())