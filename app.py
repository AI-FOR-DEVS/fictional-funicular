from openai import OpenAI

client = OpenAI()

def chat(query: str, history: list):
  history.append({"role": "user", "content": query})

  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=history
  )
  history.append({"role": "assistant", "content": response.choices[0].message.content})
  return response.choices[0].message.content