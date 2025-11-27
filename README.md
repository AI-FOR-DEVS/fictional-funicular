# FastAPI Chat Application

A web-based chat application built with FastAPI that integrates with OpenAI's GPT-4o-mini model and supports function calling with DuckDuckGo search capabilities.

## Features

- 🤖 **AI Chat Interface**: Interactive web-based chat interface powered by OpenAI's GPT-4o-mini
- 🔍 **Tool Calling**: Automatic web search using DuckDuckGo when the AI needs real-time information
- 💬 **Session Management**: Persistent conversation history per user session
- 📊 **MLflow Integration**: Tracing support for observability (optional)
- 🎨 **Modern UI**: Clean and responsive chat interface

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- (Optional) MLflow tracking server for observability

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd fast_api_project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   
   Create a `.env` file or set the following environment variable:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```
   
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   ```

## Running the Application

### Option 1: Run directly with Python
```bash
python server.py
```

### Option 2: Run with uvicorn (for development with auto-reload)
```bash
uvicorn server:app --reload
```

The server will start on `http://localhost:8000`

## Project Structure

```
fast_api_project/
├── app.py              # Core chat logic with OpenAI integration and tool calling
├── server.py            # FastAPI server and routes
├── search_tools.py      # DuckDuckGo search tool definition
├── requirements.txt     # Python dependencies
├── templates/
│   └── chat.html       # Web chat interface
└── README.md           # This file
```

## API Endpoints

### `GET /`
Returns the chat interface HTML page.

### `POST /chat`
Sends a message to the chat bot and receives a response.

**Parameters:**
- `query` (required): The user's message
- `session_id` (optional): Session ID for maintaining conversation history

**Response:**
```json
{
  "response": "AI response text",
  "session_id": "unique-session-id"
}
```

## How It Works

1. **User sends a message** through the web interface
2. **Server generates or retrieves a session ID** to maintain conversation context
3. **Message is sent to OpenAI** with conversation history
4. **If the AI needs real-time information**, it can call the DuckDuckGo search tool
5. **Tool results are returned** to the AI, which generates a final response
6. **Response is sent back** to the user with the session ID

## Tool Calling

The application supports function calling with DuckDuckGo search. When the AI determines it needs current information, it can automatically:

1. Call the `search_duckduckgo` function with a search query
2. Receive search results
3. Incorporate the results into its response

Example queries that trigger tool calls:
- "What's the weather in Tokyo?"
- "Search for the latest news about AI"
- "Find information about Python 3.12"

## Session Management

- Each user gets a unique session ID (generated server-side)
- Session IDs are stored in browser localStorage
- Conversation history is maintained per session
- Sessions persist across page refreshes

## MLflow Integration (Optional)

The project includes MLflow tracing support for observability. **Important: This project requires MLflow version 3.6.0.**

### Starting the MLflow Server

1. **Ensure MLflow 3.6.0 is installed**:
   ```bash
   pip install mlflow==3.6.0 mlflow-tracing==3.6.0
   ```

2. **Start MLflow tracking server**:
   ```bash
   mlflow ui --port 5001
   ```
   
   The server will be available at `http://localhost:5001`

3. **Verify MLflow version** (optional):
   ```bash
   mlflow --version
   ```
   Should output: `mlflow, version 3.6.0`

### Configuring MLflow in the Application

The MLflow configuration is already set up in `app.py`:
   ```python
   import mlflow
   mlflow.set_tracking_uri("http://localhost:5001")
   mlflow.openai.autolog()
   ```

### Viewing Traces

Once the MLflow server is running and the application is using it, you can view traces at `http://localhost:5001`

## Development

### Adding New Tools

To add a new function/tool for the AI to use:

1. **Define the tool in `search_tools.py`**:
   ```python
   tools = [
       {
           "type": "function",
           "function": {
               "name": "your_tool_name",
               "description": "Description of what the tool does",
               "parameters": {
                   "type": "object",
                   "properties": {
                       "param_name": {
                           "type": "string",
                           "description": "Parameter description"
                       }
                   },
                   "required": ["param_name"]
               }
           }
       }
   ]
   ```

2. **Implement the function**:
   ```python
   def your_tool_name(param_name):
       # Your implementation
       return result
   ```

3. **Handle the tool call in `app.py`**:
   ```python
   if tool_name == "your_tool_name":
       results = search_tools.your_tool_name(**tool_args)
       # Process results...
   ```

## Configuration

### Server Configuration

Edit `server.py` to change:
- **Port**: Modify `port=8000` in the `uvicorn.run()` call
- **Host**: Modify `host="0.0.0.0"` (use `127.0.0.1` for localhost only)

### Model Configuration

Edit `app.py` to change:
- **Model**: Modify `model="gpt-4o-mini"` to use a different OpenAI model
- **Temperature**: Add `temperature=0.7` parameter to `chat.completions.create()`

## Troubleshooting

### OpenAI API Errors
- Ensure your `OPENAI_API_KEY` is set correctly
- Check your OpenAI account has sufficient credits
- Verify the API key has access to the model you're using

### Tool Calling Not Working
- Ensure `search_tools.tools` is passed to the OpenAI API call
- Check that tool function names match between definition and handler
- Verify tool arguments are properly parsed from JSON

### Session Issues
- Clear browser localStorage if sessions aren't persisting
- Check that session_id is being sent in POST requests

## Dependencies

Key dependencies:
- **FastAPI**: Web framework
- **OpenAI**: OpenAI API client
- **ddgs**: DuckDuckGo search library
- **uvicorn**: ASGI server
- **MLflow**: Observability and tracing (optional)

See `requirements.txt` for the complete list.

## License

[Add your license here]

## Contributing

[Add contribution guidelines if applicable]

## Author

[Add your name/info here]

