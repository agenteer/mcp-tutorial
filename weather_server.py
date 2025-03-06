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
        elif message_type == "list_prompts":
            return self.handle_list_prompts()
        elif message_type == "invoke_prompt":
            return self.handle_invoke_prompt(message)
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
    
    def handle_list_prompts(self):
        return {
            "type": "prompts",
            "prompts": [
                {
                    "name": "weather_report",
                    "description": "Generate a detailed weather report for a city"
                },
                {
                    "name": "packing_list",
                    "description": "Generate a packing list based on weather conditions"
                }
            ]
        }

    def handle_invoke_prompt(self, message):
        prompt_name = message.get("name")
        parameters = message.get("parameters", {})
        
        if prompt_name == "weather_report":
            return self.generate_weather_report(parameters)
        elif prompt_name == "packing_list":
            return self.generate_packing_list(parameters)
        else:
            return {"type": "error", "error": f"Unknown prompt: {prompt_name}"}
    
    def generate_weather_report(self, parameters):
        city = parameters.get("city", "").lower()
        
        if city not in self.cities:
            return {
                "type": "error", 
                "error": f"No weather data available for {city}"
            }
        
        weather = self.cities[city]
        
        template = f"""
    # Weather Report for {city.title()}
    
    ## Current Conditions
    - Temperature: {weather['temp']}°F
    - Conditions: {weather['condition']}
    
    ## Forecast
    The conditions are expected to continue for the next few hours.
    
    ## Weather Advisory
    {"Stay hydrated and use sunscreen!" if weather['condition'] == "Sunny" and weather['temp'] > 75 else
     "Remember to bring an umbrella!" if weather['condition'] == "Rainy" else
     "No special advisories at this time."}
    """
        
        return {
            "type": "prompt_result",
            "result": template
        }
    
    def generate_packing_list(self, parameters):
        city = parameters.get("city", "").lower()
        days = parameters.get("days", 1)
        
        if city not in self.cities:
            return {
                "type": "error", 
                "error": f"No weather data available for {city}"
            }
        
        weather = self.cities[city]
        
        items = ["Wallet", "Phone", "Charger"]
        
        # Add weather-specific items
        if weather['condition'] == "Sunny" and weather['temp'] > 75:
            items.extend(["Sunglasses", "Sunscreen", "Hat", "T-shirts", "Shorts"])
        elif weather['condition'] == "Rainy":
            items.extend(["Umbrella", "Rain jacket", "Waterproof shoes"])
        elif weather['temp'] < 65:
            items.extend(["Jacket", "Sweater", "Long pants"])
        
        # Format the packing list
        packing_list = f"# Packing List for {city.title()} ({days} day{'s' if days > 1 else ''})\n\n"
        for item in items:
            packing_list += f"- {item}\n"
        
        return {
            "type": "prompt_result",
            "result": packing_list
        }

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
