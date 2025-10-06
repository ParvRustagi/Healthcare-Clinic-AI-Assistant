import subprocess

def get_llm_response(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "llama3.1"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding='utf-8',  # force UTF-8 to avoid Windows cp1252 issues
        errors='ignore'
    )
    if result.returncode != 0:
        return f"Ollama error: {result.stderr.strip()}"
    return result.stdout.strip()
