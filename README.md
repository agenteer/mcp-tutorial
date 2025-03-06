# MCP Tutorial: Weather Server Example

A practical demonstration of the Model Context Protocol (MCP) using a simple weather server.

## Overview

This tutorial demonstrates the core concepts of MCP:
- **Tools**: Model-controlled functions (get_weather)
- **Resources**: Application-controlled data (all_cities)
- **Prompts**: User-controlled templates (weather_report, packing_list)

## Files

- `weather_server.py`: A simple MCP server that provides weather data
- `mcp_client.py`: A client that connects to the server and demonstrates basic interactions
- `weather_agent.py`: An agent that uses the weather server to suggest activities
- `weather_prompt.py`: A demo focusing on user-controlled prompts

## Getting Started

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install anthropic mcp requests`

## Running the Examples

### Basic MCP Client (`mcp_client.py`)

This example demonstrates all three core MCP components: tools, resources, and prompts.

```bash
python mcp_client.py
```

**What you'll see:**
- List of available tools, resources, and prompts from the server
- Retrieving all cities (resource)
- Getting weather data for different cities (tool)
- Generating a weather report and packing list (prompts)

### Weather Activity Agent (`weather_agent.py`)

This example shows how an agent can use MCP tools to provide intelligent recommendations.

```bash
python weather_agent.py
```

**What you'll see:**
- Interactive prompt asking for a city name
- Agent retrieving weather data using the MCP tool
- Agent suggesting activities based on weather conditions
- Type 'quit' to exit

### User-Controlled Prompts Demo (`weather_prompt.py`)

This example focuses on the "prompts" aspect of MCP, showing how users can directly invoke predefined prompt templates.

```bash
python weather_prompt.py
```

**What you'll see:**
- List of available prompt commands (like slash commands)
- Interactive interface where you can type commands like:
  - `/weather_report tokyo` - Generate a weather report for Tokyo
  - `/packing_list london 3` - Generate a packing list for 3 days in London
- Type 'quit' to exit

## What You'll Learn

### From `mcp_client.py`:
- Basic MCP protocol interactions
- How to discover and call tools
- How to retrieve resources
- How to list and invoke prompts

### From `weather_agent.py`:
- How to build an agent that uses MCP tools
- How tools can provide data for intelligent processing
- How to create interactive agents with MCP

### From `weather_prompt.py`:
- How prompts work as user-controlled templates
- How to implement slash commands with MCP prompts
- How prompts differ from tools (user vs. model control)

## MCP Protocol Details

Each file demonstrates a different aspect of the MCP protocol:

1. **Tools** - Model-controlled functions that the AI can invoke when needed
   - Example: `get_weather` tool that retrieves weather data for a city

2. **Resources** - Application-controlled data exposed to the AI
   - Example: `all_cities` resource that provides a list of available cities

3. **Prompts** - User-controlled templates for common interactions
   - Examples: `weather_report` and `packing_list` prompts that generate formatted output

## Learn More

For more information about MCP, visit [Anthropic's MCP documentation](https://modelcontextprotocol.io/introduction).
