from openai import OpenAI
import search_tools
import json
import mlflow

client = OpenAI()

mlflow.set_tracking_uri("http://localhost:5001")
mlflow.openai.autolog()

def chat(query: str, history: list):
  history.append({"role": "user", "content": query})

  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=history,
      tools=search_tools.tools
  )

  message = response.choices[0].message
  
  # If the model wants to call a tool
  if message.tool_calls:
    # Append the assistant message with tool_calls (not content)
    assistant_message = {
      "role": "assistant",
      "content": message.content,  # Can be None when tool_calls are present
      "tool_calls": [
        {
          "id": tool_call.id,
          "type": tool_call.type,
          "function": {
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments
          }
        }
        for tool_call in message.tool_calls
      ]
    }
    history.append(assistant_message)
    
    # Execute each tool call
    for tool_call in message.tool_calls:
      tool_name = tool_call.function.name
      tool_args_str = tool_call.function.arguments
      tool_args = json.loads(tool_args_str)  # Parse JSON string to dict
      
      if tool_name == "search_duckduckgo":
        results = search_tools.search_duckduckgo(**tool_args)  # Unpack arguments
        print("------> RESULTS: ", results)
        # Convert results to string if needed
        if not isinstance(results, str):
          results = json.dumps(results)
        
        # Append tool response with tool_call_id
        history.append({
          "role": "tool",
          "tool_call_id": tool_call.id,
          "content": results
        })

    # Get final response after tool execution
    new_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        tools=search_tools.tools
    )

    final_message = new_response.choices[0].message
    history.append({"role": "assistant", "content": final_message.content})
    return final_message.content

  # No tool calls, just return the response
  history.append({"role": "assistant", "content": message.content})
  return message.content