from mcp_utils import MCPClient


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
    
    # List available prompts
    print("\nAvailable prompts:")
    prompts = client.list_prompts()
    for prompt in prompts:
        print(f"- {prompt['name']}: {prompt['description']}")
    
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
    
    # Invoke prompts
    print("\nWeather Report for Tokyo:")
    report = client.invoke_prompt("weather_report", {"city": "tokyo"})
    if report:
        print(report)
    
    print("\nPacking List for London (3 days):")
    packing_list = client.invoke_prompt("packing_list", {"city": "london", "days": 3})
    if packing_list:
        print(packing_list)
    
    # Clean up
    client.close()

if __name__ == "__main__":
    main()
