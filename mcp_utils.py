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