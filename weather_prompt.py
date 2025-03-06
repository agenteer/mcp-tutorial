from mcp_utils import MCPClient


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
