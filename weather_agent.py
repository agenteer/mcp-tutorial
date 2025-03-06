import json
import subprocess
from anthropic import Anthropic

class WeatherAgent:
    def __init__(self):
        # Initialize the MCP client
        self.client = MCPClient(["python", "weather_server.py"])
        
        # Initialize the Anthropic client (you'll need your API key)
        # self.anthropic = Anthropic(api_key="your_api_key_here")
        
        # For demo purposes without API key
        self.use_fake_llm = True
    
    def suggest_activities(self, city):
        # Get weather for the city
        weather = self.client.call_tool("get_weather", {"city": city})
        
        if not weather:
            return f"Sorry, I don't have weather data for {city}."
        
        if self.use_fake_llm:
            # Simulate LLM response for demo purposes
            if weather["condition"] == "Sunny" and weather["temp"] > 75:
                return f"It's {weather['temp']}°F and {weather['condition']} in {city}. Great day for the beach or outdoor activities like hiking or picnics!"
            elif weather["condition"] == "Rainy":
                return f"It's {weather['temp']}°F and {weather['condition']} in {city}. Perfect for indoor activities like museums, movies, or cozy cafes."
            else:
                return f"It's {weather['temp']}°F and {weather['condition']} in {city}. Good conditions for sightseeing, shopping, or light outdoor activities."
        else:
            # Use Anthropic API for real suggestions
            prompt = f"""
            The weather in {city} is currently {weather['temp']}°F and {weather['condition']}.
            Based on this weather, suggest 3 suitable activities for someone visiting {city} today.
            """
            
            message = self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=300,
                system="You are a helpful travel assistant.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
    
    def close(self):
        self.client.close()

# Reusing our MCPClient class from before
class MCPClient:
    def __init__(self, server_command):
        # Start the server process
        self.process = subprocess.Popen(
            server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    def send_message(self, message):
        # Send a message to the server
        message_json = json.dumps(message) + "\n"
        self.process.stdin.write(message_json)
        self.process.stdin.flush()
        
        # Read the response
        response_json = self.process.stdout.readline()
        return json.loads(response_json)
    
    def list_tools(self):
        response = self.send_message({"type": "list_tools"})
        return response.get("tools", [])
    
    def call_tool(self, name, parameters=None):
        if parameters is None:
            parameters = {}
        
        response = self.send_message({
            "type": "call_tool",
            "name": name,
            "parameters": parameters
        })
        
        if "error" in response:
            print(f"Error: {response['error']}")
            return None
        
        return response.get("result")
    
    def get_resource(self, name, parameters=None):
        if parameters is None:
            parameters = {}
    
        response = self.send_message({
            "type": "get_resource",
            "name": name,
            "parameters": parameters
        })
    
        if "error" in response:
            print(f"Error: {response['error']}")
            return None
    
        return response.get("data")

    def close(self):
        self.process.terminate()

def main():
    agent = WeatherAgent()
    
    # Get list of cities
    cities = agent.client.get_resource("all_cities")
    
    print("Welcome to the Weather Activity Planner!")
    print("Available cities:", ", ".join(city.title() for city in cities))
    
    while True:
        city = input("\nEnter a city (or 'quit' to exit): ").strip().lower()
        
        if city == 'quit':
            break
        
        suggestion = agent.suggest_activities(city)
        print("\nActivity Suggestions:")
        print(suggestion)
    
    agent.close()

if __name__ == "__main__":
    main()
