#!/usr/bin/env python3
"""
Sistema A2A MCP - Ponto de entrada principal
Permite executar o sistema usando: python -m a2a_mcp
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

from start_a2a_mcp import main

if __name__ == "__main__":
    main() 