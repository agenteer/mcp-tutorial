import json
import subprocess
import sys

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
    
    def list_resources(self):
        response = self.send_message({"type": "list_resources"})
        return response.get("resources", [])
    
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
    # Create a client that connects to our weather server
    client = MCPClient(["python", "weather_server.py"])
    
    # List available tools
    print("Available tools:")
    tools = client.list_tools()
    for tool in tools:
        print(f"- {tool['name']}: {tool['description']}")
    
    # List available resources
    print("\nAvailable resources:")
    resources = client.list_resources()
    for resource in resources:
        print(f"- {resource['name']}: {resource['description']}")
    
    # Get all cities resource
    print("\nAll cities with weather data:")
    cities = client.get_resource("all_cities")
    print(cities)
    
    # Call the weather tool for a few cities
    print("\nWeather information:")
    for city in ["San Francisco", "Tokyo", "Unknown City"]:
        print(f"\nWeather for {city}:")
        weather = client.call_tool("get_weather", {"city": city})
        if weather:
            print(f"Temperature: {weather['temp']}°F")
            print(f"Condition: {weather['condition']}")
    
    # Clean up
    client.close()

if __name__ == "__main__":
    main()
