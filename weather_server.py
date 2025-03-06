import json
import sys
from http import HTTPStatus

# This is a simple MCP server that provides weather information
class WeatherServer:
    def __init__(self):
        self.cities = {
            "san francisco": {"temp": 65, "condition": "Foggy"},
            "new york": {"temp": 72, "condition": "Partly Cloudy"},
            "london": {"temp": 60, "condition": "Rainy"},
            "tokyo": {"temp": 80, "condition": "Sunny"}
        }
    
    def handle_message(self, message):
        message_type = message.get("type")
        
        if message_type == "list_tools":
            return self.handle_list_tools()
        elif message_type == "call_tool":
            return self.handle_call_tool(message)
        elif message_type == "list_resources":
            return self.handle_list_resources()
        elif message_type == "get_resource":
            return self.handle_get_resource(message)
        else:
            return {"type": "error", "error": f"Unsupported message type: {message_type}"}
    
    def handle_list_tools(self):
        return {
            "type": "tools",
            "tools": [
                {
                    "name": "get_weather",
                    "description": "Get the current weather for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city to get weather for"
                            }
                        },
                        "required": ["city"]
                    }
                }
            ]
        }
    
    def handle_call_tool(self, message):
        tool_name = message.get("name")
        parameters = message.get("parameters", {})
        
        if tool_name == "get_weather":
            return self.get_weather(parameters)
        else:
            return {"type": "error", "error": f"Unknown tool: {tool_name}"}
    
    def get_weather(self, parameters):
        city = parameters.get("city", "").lower()
        
        if city in self.cities:
            return {
                "type": "tool_result",
                "result": self.cities[city]
            }
        else:
            return {
                "type": "error", 
                "error": f"No weather data available for {city}"
            }
    
    def handle_list_resources(self):
        return {
            "type": "resources",
            "resources": [
                {
                    "name": "all_cities",
                    "description": "List of all cities with weather data"
                }
            ]
        }
    
    def handle_get_resource(self, message):
        resource_name = message.get("name")
        
        if resource_name == "all_cities":
            return {
                "type": "resource",
                "data": list(self.cities.keys())
            }
        else:
            return {"type": "error", "error": f"Unknown resource: {resource_name}"}

# Main loop to handle stdin/stdout communication
def main():
    server = WeatherServer()
    
    for line in sys.stdin:
        try:
            message = json.loads(line)
            response = server.handle_message(message)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            print(json.dumps({"type": "error", "error": "Invalid JSON"}), flush=True)
        except Exception as e:
            print(json.dumps({"type": "error", "error": str(e)}), flush=True)

if __name__ == "__main__":
    main()
