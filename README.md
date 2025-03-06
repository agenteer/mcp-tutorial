# MCP Tutorial: Weather Server Example

A practical demonstration of the Model Context Protocol (MCP) using a simple weather server.

## Overview

This tutorial demonstrates the core concepts of MCP:
- Tools: Model-controlled functions (get_weather)
- Resources: Application-controlled data (all_cities)
- Client-Server interaction using the MCP protocol

## Files

- `weather_server.py`: A simple MCP server that provides weather data
- `mcp_client.py`: A client that connects to the server and demonstrates basic interactions
- `weather_agent.py`: An agent that uses the weather server to suggest activities

## Getting Started

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install anthropic mcp requests`
5. Run the examples:
   - Basic client: `python mcp_client.py`
   - Weather agent: `python weather_agent.py`

## Learn More

For more information about MCP, visit [Anthropic's MCP documentation](https://docs.anthropic.com/claude/docs/model-context-protocol).
