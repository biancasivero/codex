from a2a_mcp.mcp.server import serve


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, default=10000, help="Port number")
    parser.add_argument("--transport", type=str, default="sse", help="Transport mechanism")
    args = parser.parse_args()

    serve(args.host, args.port, args.transport)

if __name__ == "__main__":
    main()