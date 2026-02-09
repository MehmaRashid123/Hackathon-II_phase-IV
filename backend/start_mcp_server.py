"""
MCP Server Startup Script

This script starts the MCP server that exposes tools for AI agents
to interact with the task management system.

Usage:
    python start_mcp_server.py
"""
import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.mcp.server import run_server


def main():
    """Main entry point for MCP server."""
    print("=" * 60)
    print("Starting MCP Server for Task Management")
    print("=" * 60)
    print("\nServer will expose the following tools:")
    print("  • add_task      - Create new tasks")
    print("  • list_tasks    - List all tasks")
    print("  • complete_task - Mark tasks as complete")
    print("  • delete_task   - Delete tasks")
    print("  • update_task   - Update task details")
    print("\n" + "=" * 60)
    print("Server is running... (Press Ctrl+C to stop)")
    print("=" * 60 + "\n")
    
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\n\nShutting down MCP server...")
        print("Server stopped.")
    except Exception as e:
        print(f"\n✗ Error starting MCP server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
