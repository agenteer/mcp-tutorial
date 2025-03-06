import json
import subprocess

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
    
    def list_prompts(self):
        response = self.send_message({"type": "list_prompts"})
        return response.get("prompts", [])

    def invoke_prompt(self, name, parameters=None):
        if parameters is None:
            parameters = {}
        
        response = self.send_message({
            "type": "invoke_prompt",
            "name": name,
            "parameters": parameters
        })
        
        if "error" in response:
            print(f"Error: {response['error']}")
            return None
        
        return response.get("result")
    
    def close(self):
        self.process.terminate()

def main():
    client = MCPClient(["python", "weather_server.py"])
    
    print("Welcome to the Weather Assistant!")
    print("This demo shows how prompts in MCP are user-controlled.")
    
    # List available prompts
    prompts = client.list_prompts()
    print("\nAvailable prompt commands:")
    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. /{prompt['name']} - {prompt['description']}")
    
    # Get list of cities
    cities = client.get_resource("all_cities")
    print("\nAvailable cities:", ", ".join(city.title() for city in cities))
    
    while True:
        user_input = input("\nEnter a command (e.g., '/weather_report San Francisco') or 'quit' to exit: ")
        
        if user_input.lower() == 'quit':
            break
        
        # Parse command
        if user_input.startswith('/'):
            parts = user_input.split(' ', 1)
            command = parts[0][1:]  # Remove the leading '/'
            
            if len(parts) > 1:
                args = parts[1]
            else:
                args = ""
            
            # Handle different prompt commands
            if command == "weather_report":
                result = client.invoke_prompt("weather_report", {"city": args.lower()})
                if result:
                    print(result)
            
            elif command == "packing_list":
                # Parse arguments: city and days
                arg_parts = args.rsplit(' ', 1)
                if len(arg_parts) > 1 and arg_parts[1].isdigit():
                    city = arg_parts[0].lower()
                    days = int(arg_parts[1])
                else:
                    city = args.lower()
                    days = 1
                
                result = client.invoke_prompt("packing_list", {"city": city, "days": days})
                if result:
                    print(result)
            
            else:
                print(f"Unknown command: {command}")
        else:
            print("Commands start with '/' (e.g., '/weather_report San Francisco')")
    
    client.close()

if __name__ == "__main__":
    main()
