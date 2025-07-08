# A2A Hello World Agent

Este repositorio apresenta um agente A2A "Hello World" para fins de demonstracao.

This project demonstrates a minimal Agent-to-Agent (A2A) application. It exposes a single agent that replies "Hello World" and includes a simple client for testing communication.

## Setup

1. **Create a virtual environment** (recommended).
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies** listed in `requirements.txt` and the `httpx` HTTP client.
   ```bash
   pip install -r requirements.txt httpx
   ```

## Adding Dependencies

New libraries should be added to `requirements.txt` so that everyone installs the same versions. After editing `requirements.txt`, update the code to import and use the new package. For instance, to add the `mcp` package:

1. Append `mcp` to `requirements.txt`.
2. Run `pip install -r requirements.txt` again.
3. Import and use `mcp` in your scripts as needed.

### Using Smithery CLI

If you are also working with Node-based tools, the [Smithery CLI](https://smithery.ai/) can be used to pull additional packages. A typical command looks like:

```bash
npx -y @smithery/cli@latest install <package> --client gemini-cli --profile <profile>
```

Replace `<package>` and `<profile>` with your desired package and Smithery profile. Any Python packages obtained this way should still be listed in `requirements.txt` so that the project remains reproducible.

## Entry Point

The agent server is defined in `__main__.py`. Edit this file if you want to change the skills, agent card or server configuration.

Start the server from the repository's parent directory with:
```bash
python -m codex
```

The `agent_executor.py` module contains the `HelloWorldAgentExecutor` class
that implements the logic for handling the agent's skills.

The client script (`client.py`) shows how to connect to the agent and invoke its skills.
