import subprocess
import asyncio

async def get_llm_response(prompt: str) -> str:
    try:
        # Run Ollama synchronously
        process = await asyncio.create_subprocess_exec(
            "ollama", "run", "llama3.1",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await process.communicate(input=prompt.encode("utf-8"))

        if process.returncode != 0:
            return f"Ollama error: {stderr.decode()}"

        # Ollama streams responses → just return the text
        response = stdout.decode("utf-8", errors="ignore").strip()
        if not response:
            return "⚠️ No response from LLM."
        return response

    except Exception as e:
        return f"⚠️ LLM Exception: {e}"
