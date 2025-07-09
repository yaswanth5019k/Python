# Universal Chatbot Integration Guide

This chatbot can be integrated into **ANY** website regardless of the framework they use. Here are the integration methods:

## 🔄 Integration Methods

### 1. **REST API Integration** (Universal)
Works with: React, Vue, Angular, PHP, WordPress, Django, Rails, .NET, etc.

For local development, use `http://localhost:8080`. For production, replace this with your server's URL.

```javascript
// Example for any JavaScript framework
async function sendMessage(message) {
    const response = await fetch('http://localhost:8080/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
            conversation_id: localStorage.getItem('conversation_id')
        })
    });
    
    const data = await response.json();
    localStorage.setItem('conversation_id', data.conversation_id);
    return data;
}
```

```php
// Example for PHP websites
function sendMessage($message, $conversationId = null) {
    $data = array(
        'message' => $message,
        'conversation_id' => $conversationId
    );
    
    $options = array(
        'http' => array(
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data)
        )
    );
    
    $context  = stream_context_create($options);
    $result = file_get_contents('http://localhost:8080/api/chat', false, $context);
    return json_decode($result, true);
}
```

### 2. **JavaScript Widget** (Drop-in Solution)
Simply add this script tag to ANY website:

```html
<!-- Add this ONE line to any website -->
<script src="http://localhost:8080/widget.js"></script>
```

### 3. **Iframe Integration** (Zero Coding)
Embed as iframe in any website:

```html
<iframe 
    src="http://localhost:8080/chat-iframe" 
    width="350" 
    height="500"
    style="border: none; border-radius: 10px;">
</iframe>
```

### 4. **Webhook Integration** (For Advanced Users)
Your chatbot can send/receive data via webhooks:

```json
POST /webhook
{
    "event_type": "message",
    "payload": {
        "message": "I need funding for my startup",
        "conversation_id": "uuid-here"
    }
}
```

## 🌐 Framework-Specific Examples

### React/Next.js
```jsx
import { useState, useEffect } from 'react';

function ChatBot() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: input })
        });
        const data = await response.json();
        setMessages(prev => [...prev, { user: input, bot: data.response }]);
        setInput('');
    };

    return (
        <div className="chatbot">
            {/* Chat UI */}
        </div>
    );
}
```

### Vue.js
```vue
<template>
    <div class="chatbot">
        <div v-for="msg in messages" :key="msg.id">
            {{ msg.text }}
        </div>
        <input v-model="input" @keyup.enter="sendMessage" />
    </div>
</template>

<script>
export default {
    data() {
        return {
            messages: [],
            input: ''
        };
    },
    methods: {
        async sendMessage() {
            const response = await this.$http.post('/api/chat', {
                message: this.input
            });
            this.messages.push(response.data);
        }
    }
};
</script>
```

### WordPress
```php
// Add to functions.php
function add_chatbot_widget() {
    echo '<script src="http://localhost:8080/widget.js"></script>';
}
add_action('wp_footer', 'add_chatbot_widget');
```

### Angular
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class ChatbotService {
    constructor(private http: HttpClient) {}

    sendMessage(message: string) {
        return this.http.post('/api/chat', { message });
    }
}
```

### Django
```python
# views.py
import requests
from django.shortcuts import render
from django.http import JsonResponse

def chat_proxy(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = requests.post('http://localhost:8080/api/chat', 
                               json={'message': message})
        return JsonResponse(response.json())
```

### Ruby on Rails
```ruby
# controllers/chat_controller.rb
class ChatController < ApplicationController
  def send_message
    response = HTTParty.post('http://localhost:8080/api/chat',
      body: { message: params[:message] }.to_json,
      headers: { 'Content-Type' => 'application/json' }
    )
    render json: response.parsed_response
  end
end
```

## 🚀 Quick Start for Any Website

### Option 1: Instant Widget (Easiest)
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <!-- Your existing website content -->
    
    <!-- Add chatbot with ONE line -->
    <script src="http://localhost:8080/widget.js"></script>
</body>
</html>
```

### Option 2: Custom Integration
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <!-- Your existing website content -->
    
    <div id="chat-container">
        <div id="messages"></div>
        <input type="text" id="chat-input" placeholder="Ask about investments...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value;
            
            const response = await fetch('http://localhost:8080/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            document.getElementById('messages').innerHTML += 
                `<div>Bot: ${data.response}</div>`;
            input.value = '';
        }
    </script>
</body>
</html>
```

## 🔧 Deployment Options

### 1. Cloud Deployment
- **Heroku**: `git push heroku main`
- **AWS**: Deploy on EC2 or Lambda
- **Google Cloud**: Cloud Run or App Engine
- **DigitalOcean**: Droplets or App Platform

### 2. Self-Hosted
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python chatbot.py

# Access at: http://your-domain.com:8080
```

### 3. Docker Deployment
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "chatbot.py"]
```

## 🎯 Key Benefits

✅ **Universal Compatibility**: Works with ANY website framework
✅ **Easy Integration**: Multiple integration methods
✅ **No Framework Dependencies**: Standalone service
✅ **Scalable**: Can handle multiple websites
✅ **Customizable**: Easy to modify for specific needs
✅ **Modern UI**: Beautiful, responsive design
✅ **Mobile-Friendly**: Works on all devices

## 📞 API Endpoints

- `POST /api/chat` - Send messages to chatbot
- `GET /api/conversation/{id}` - Get conversation history
- `GET /widget.js` - JavaScript widget
- `GET /chat-iframe` - Standalone chat interface
- `POST /webhook` - Webhook for integrations
- `GET /api/health` - Health check

The chatbot automatically handles:
- User type detection (investor/entrepreneur)
- Intent recognition
- Context-aware responses
- Conversation history
- Suggestion generation
- Error handling
