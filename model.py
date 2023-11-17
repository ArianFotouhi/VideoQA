import requests
import base64

# OpenAI API Key
api_key = ""

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

question = "What’s in this image?"
image_path = "path_to_your_image.jpg"
base64_image = encode_image(image_path)


headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": question
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://drsonjabenson.com/wp-content/uploads/2016/02/kids-playing-outside.jpg"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())  