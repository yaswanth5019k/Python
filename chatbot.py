#!/usr/bin/env python3
"""
Investor-Entrepreneur Platform Chatbot
Supports multiple integration methods for any website framework
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import re
import datetime
from typing import Dict, List, Any
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

class InvestorEntrepreneurChatbot:
    def __init__(self):
        self.conversation_history = {}
        self.user_profiles = {}
        
        # Intent patterns for different user types
        self.intent_patterns = {
            'investor': {
                'seeking_startups': [
                    r'looking for.*startup', r'investment.*opportunit', r'seed.*round',
                    r'series.*funding', r'startup.*invest', r'due.*diligence',
                    r'invest.*in.*startup', r'startup.*investment', r'find.*startup'
                ],
                'portfolio_inquiry': [
                    r'portfolio.*track', r'investment.*performance', r'return.*investment',
                    r'portfolio.*management'
                ],
                'market_analysis': [
                    r'market.*trend', r'industry.*analysis', r'sector.*growth',
                    r'market.*size', r'competition.*analysis'
                ]
            },
            'entrepreneur': {
                'seeking_funding': [
                    r'need.*funding', r'raise.*capital', r'looking.*investor',
                    r'seed.*money', r'venture.*capital', r'angel.*investor',
                    r'seeking.*funding', r'need.*investment'
                ],
                'pitch_help': [
                    r'pitch.*deck', r'business.*plan', r'present.*idea',
                    r'pitch.*help', r'investor.*presentation'
                ],
                'business_advice': [
                    r'business.*advice', r'startup.*help', r'scale.*business',
                    r'growth.*strategy', r'business.*model'
                ]
            },
            'general': {
                'platform_info': [
                    r'how.*platform.*work', r'what.*this.*platform', r'platform.*feature',
                    r'how.*use.*platform'
                ],
                'registration': [
                    r'sign.*up', r'register', r'create.*account', r'join.*platform'
                ],
                'meeting_scheduling': [
                    r'schedule.*meeting', r'book.*appointment', r'arrange.*call',
                    r'set.*meeting'
                ]
            }
        }
        
        # Response templates
        self.responses = {
            'investor': {
                'seeking_startups': self._get_startup_opportunities_response,
                'portfolio_inquiry': self._get_portfolio_response,
                'market_analysis': self._get_market_analysis_response
            },
            'entrepreneur': {
                'seeking_funding': self._get_funding_opportunities_response,
                'pitch_help': self._get_pitch_help_response,
                'business_advice': self._get_business_advice_response
            },
            'general': {
                'platform_info': self._get_platform_info_response,
                'registration': self._get_registration_response,
                'meeting_scheduling': self._get_meeting_scheduling_response
            }
        }

    def identify_user_type(self, message: str, conversation_id: str) -> str:
        """Identify if user is investor, entrepreneur, or unknown"""
        investor_keywords = ['invest', 'portfolio', 'capital', 'funding round', 'due diligence', 'returns']
        entrepreneur_keywords = ['startup', 'raise money', 'pitch', 'business idea', 'need funding', 'scale']
        
        # Check conversation history
        if conversation_id in self.user_profiles:
            return self.user_profiles[conversation_id].get('type', 'unknown')
        
        message_lower = message.lower()
        investor_score = sum(1 for keyword in investor_keywords if keyword in message_lower)
        entrepreneur_score = sum(1 for keyword in entrepreneur_keywords if keyword in message_lower)
        
        if investor_score > entrepreneur_score:
            return 'investor'
        elif entrepreneur_score > investor_score:
            return 'entrepreneur'
        else:
            return 'unknown'

    def identify_intent(self, message: str, user_type: str) -> str:
        """Identify the intent of the user's message"""
        message_lower = message.lower()
        
        # Check user type specific patterns first
        if user_type in self.intent_patterns:
            for intent, patterns in self.intent_patterns[user_type].items():
                for pattern in patterns:
                    if re.search(pattern, message_lower):
                        return intent
        
        # Check general patterns
        for intent, patterns in self.intent_patterns['general'].items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return 'general_inquiry'

    def process_message(self, message: str, conversation_id: str = None) -> Dict[str, Any]:
        """Main method to process incoming messages"""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        # Initialize conversation history
        if conversation_id not in self.conversation_history:
            self.conversation_history[conversation_id] = []
        
        # Add user message to history
        self.conversation_history[conversation_id].append({
            'role': 'user',
            'message': message,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        # Identify user type and intent
        user_type = self.identify_user_type(message, conversation_id)
        intent = self.identify_intent(message, user_type)
        
        # Update user profile
        if conversation_id not in self.user_profiles:
            self.user_profiles[conversation_id] = {}
        self.user_profiles[conversation_id]['type'] = user_type
        self.user_profiles[conversation_id]['last_intent'] = intent
        
        # Generate response
        response = self.generate_response(user_type, intent, message, conversation_id)
        
        # Add bot response to history
        self.conversation_history[conversation_id].append({
            'role': 'bot',
            'message': response,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        return {
            'conversation_id': conversation_id,
            'user_type': user_type,
            'intent': intent,
            'response': response,
            'suggestions': self.get_suggestions(user_type, intent)
        }

    def generate_response(self, user_type: str, intent: str, message: str, conversation_id: str) -> str:
        """Generate appropriate response based on user type and intent"""
        if user_type in self.responses and intent in self.responses[user_type]:
            return self.responses[user_type][intent](message, conversation_id)
        elif intent in self.responses['general']:
            return self.responses['general'][intent](message, conversation_id)
        else:
            return self._get_default_response(user_type, message)

    def get_suggestions(self, user_type: str, intent: str) -> List[str]:
        """Get suggested follow-up questions/actions"""
        suggestions = {
            'investor': [
                "Show me startup opportunities in tech",
                "What's the average ROI in Series A rounds?",
                "Schedule a meeting with promising startups",
                "Analyze market trends in fintech"
            ],
            'entrepreneur': [
                "Help me prepare my pitch deck",
                "Find investors interested in my industry",
                "What funding stage am I ready for?",
                "Connect me with mentors"
            ],
            'unknown': [
                "I'm an investor looking for opportunities",
                "I'm an entrepreneur seeking funding",
                "Tell me about this platform",
                "How do I get started?"
            ]
        }
        return suggestions.get(user_type, suggestions['unknown'])

    # Response methods for different intents
    def _get_startup_opportunities_response(self, message: str, conversation_id: str) -> str:
        return """🚀 **Startup Investment Opportunities**

I can help you discover promising startups! Here's what I can do:

📊 **Current Hot Sectors:**
• AI/Machine Learning (34% of recent deals)
• FinTech (22% of deals)
• HealthTech (18% of deals)
• SaaS/Enterprise (15% of deals)

💰 **Funding Stages Available:**
• Pre-seed: $50K - $500K
• Seed: $500K - $2M
• Series A: $2M - $15M

Would you like me to:
1. Show you startups in a specific industry?
2. Filter by funding stage?
3. Set up meetings with founders?
4. Provide due diligence checklists?

What's your investment focus and ticket size?"""

    def _get_funding_opportunities_response(self, message: str, conversation_id: str) -> str:
        return """💰 **Funding Opportunities for Entrepreneurs**

Great! I can help you connect with the right investors. Let me understand your startup better:

📋 **Quick Assessment:**
• What stage is your startup? (Idea/MVP/Revenue/Growth)
• What industry/sector?
• How much funding do you need?
• What will you use the funds for?

🎯 **Available Investor Types:**
• Angel Investors: $25K - $100K
• Seed VCs: $100K - $1M
• Series A VCs: $1M - $10M+

📈 **I can help you:**
1. Match with relevant investors
2. Prepare your pitch materials
3. Practice your pitch
4. Schedule investor meetings
5. Navigate the funding process

Tell me about your startup and funding needs!"""

    def _get_pitch_help_response(self, message: str, conversation_id: str) -> str:
        return """🎯 **Pitch Deck & Presentation Help**

I'll help you create a compelling pitch! Here's my framework:

📋 **Essential Pitch Deck Slides:**
1. Problem & Solution
2. Market Size & Opportunity
3. Business Model
4. Traction & Metrics
5. Competition Analysis
6. Team
7. Financial Projections
8. Funding Ask & Use of Funds

💡 **Pitch Tips:**
• Keep it to 10-12 slides for presentation
• Tell a story, don't just list facts
• Focus on the problem you're solving
• Show traction and growth metrics
• Be clear about your ask

🔧 **I can help you:**
1. Review your current pitch deck
2. Suggest improvements
3. Practice Q&A sessions
4. Tailor pitches for specific investors

What specific help do you need with your pitch?"""

    def _get_platform_info_response(self, message: str, conversation_id: str) -> str:
        return """🌟 **Welcome to the Investor-Entrepreneur Platform!**

This platform connects investors and entrepreneurs for mutual success:

👥 **For Entrepreneurs:**
• Find and connect with relevant investors
• Get feedback on business ideas and pitches
• Access mentorship and business advice
• Join startup communities and events

💼 **For Investors:**
• Discover promising startups and deals
• Conduct due diligence efficiently
• Build and manage your portfolio
• Connect with other investors

🤖 **I'm your AI assistant and can help with:**
• Matching you with relevant connections
• Providing industry insights and trends
• Scheduling meetings and calls
• Answering questions about the platform

To get started:
1. Tell me if you're an investor or entrepreneur
2. Share your interests/focus areas
3. Let me know what you're looking for

How can I help you today?"""

    def _get_registration_response(self, message: str, conversation_id: str) -> str:
        return """📝 **Platform Registration**

I'd love to help you get registered! Here's what you need:

🔐 **Registration Process:**
1. Choose your role: Investor or Entrepreneur
2. Complete your profile
3. Verify your identity
4. Start connecting!

📋 **What you'll need:**
• Professional email address
• LinkedIn profile (recommended)
• Brief description of your background
• Investment focus or startup details

**Quick Start:**
Are you registering as an:
🔹 **Investor** - Looking for investment opportunities
🔹 **Entrepreneur** - Seeking funding or mentorship

I can guide you through the registration process and help you optimize your profile for better matches!

Which role describes you best?"""

    def _get_meeting_scheduling_response(self, message: str, conversation_id: str) -> str:
        return """📅 **Meeting & Call Scheduling**

I can help you schedule meetings with potential matches!

⏰ **Available Meeting Types:**
• Initial intro calls (15-30 minutes)
• Pitch presentations (30-45 minutes)
• Due diligence meetings (60+ minutes)
• Casual networking calls (15-30 minutes)

📋 **To schedule a meeting, I need:**
1. Who you want to meet with
2. Purpose of the meeting
3. Your preferred time/date options
4. Meeting duration
5. Virtual or in-person preference

🔧 **I can:**
• Check availability for both parties
• Send calendar invites
• Prepare meeting agendas
• Provide relevant background info
• Set up follow-up reminders

Who would you like to schedule a meeting with, and what's the purpose?"""

    def _get_portfolio_response(self, message: str, conversation_id: str) -> str:
        return """📊 **Portfolio Management & Tracking**

I can help you manage and track your investment portfolio!

📈 **Portfolio Analytics:**
• Current portfolio value and performance
• ROI analysis by investment stage
• Sector diversification breakdown
• Timeline of investments and exits

📋 **Portfolio Insights:**
• Top performing investments
• Underperforming assets needing attention
• Upcoming funding rounds from portfolio companies
• Exit opportunities and market timing

🔧 **Portfolio Tools:**
1. Performance dashboards
2. Due diligence tracking
3. Communication logs with founders
4. Financial reporting and tax documents

What specific portfolio information are you looking for?"""

    def _get_market_analysis_response(self, message: str, conversation_id: str) -> str:
        return """📊 **Market Analysis & Trends**

Here's the latest market intelligence:

📈 **Current Market Trends:**
• AI/ML: 40% YoY growth in funding
• Sustainability: Emerging high-growth sector
• Remote work tools: Continued strong demand
• FinTech: Regulatory changes creating opportunities

💰 **Funding Landscape:**
• Average Series A: $8.2M (up 15% from last year)
• Median time to Series A: 18 months
• Success rate: 23% of seed companies raise Series A

🌍 **Geographic Hotspots:**
• Silicon Valley: Still #1 for tech startups
• Austin: Fastest growing startup ecosystem
• Europe: Strong FinTech and SaaS growth

Which specific market segment or trend interests you most?"""

    def _get_business_advice_response(self, message: str, conversation_id: str) -> str:
        return """💡 **Business Advice & Strategy**

I'm here to help with your business challenges!

🎯 **Common Startup Topics:**
• Business model validation
• Go-to-market strategy
• Team building and hiring
• Product development priorities
• Customer acquisition strategies
• Scaling operations

📊 **Strategic Planning:**
• Market positioning
• Competitive analysis
• Financial planning and projections
• Fundraising strategy
• Exit planning

👥 **I can connect you with:**
• Industry mentors and advisors
• Other entrepreneurs who've faced similar challenges
• Subject matter experts
• Potential co-founders or team members

What specific business challenge are you facing? The more details you provide, the better I can help!"""

    def _get_default_response(self, user_type: str, message: str) -> str:
        user_greeting = {
            'investor': "As an investor",
            'entrepreneur': "As an entrepreneur", 
            'unknown': "Welcome! Whether you're an investor or entrepreneur"
        }.get(user_type, "Hello")
        
        return f"""{user_greeting}, I'm here to help you succeed on our platform!

I can assist with:
🔹 Finding relevant connections and opportunities
🔹 Providing industry insights and market data  
🔹 Scheduling meetings and networking
🔹 Business advice and strategic guidance
🔹 Platform navigation and features

Could you tell me more specifically what you're looking for? For example:
• Are you seeking funding or investment opportunities?
• Do you need help with pitch preparation?
• Are you looking for business advice or mentorship?
• Would you like to know more about platform features?

I'm here to help make your journey more successful!"""

# Initialize the chatbot
chatbot = InvestorEntrepreneurChatbot()

# REST API Endpoints
@app.route('/api/chat', methods=['POST'])
def chat_api():
    """REST API endpoint for chat integration"""
    try:
        data = request.json
        message = data.get('message', '')
        conversation_id = data.get('conversation_id')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        response = chatbot.process_message(message, conversation_id)
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation history"""
    history = chatbot.conversation_history.get(conversation_id, [])
    return jsonify({'conversation_id': conversation_id, 'history': history})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})

# JavaScript Widget Endpoint
@app.route('/widget.js')
def chat_widget():
    """JavaScript widget for easy embedding"""
    widget_js = """
(function() {
    // Chatbot Widget for Investor-Entrepreneur Platform
    let chatbotConfig = {
        apiUrl: window.location.origin + '/api/chat',
        position: 'bottom-right',
        theme: 'modern'
    };
    
    function createChatWidget() {
        // Create chat button
        const chatButton = document.createElement('div');
        chatButton.id = 'ie-chatbot-button';
        chatButton.innerHTML = '💬';
        chatButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
            transition: transform 0.3s ease;
        `;
        
        // Create chat window
        const chatWindow = document.createElement('div');
        chatWindow.id = 'ie-chatbot-window';
        chatWindow.style.cssText = `
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            display: none;
            flex-direction: column;
            z-index: 1001;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;
        
        // Chat header
        const chatHeader = document.createElement('div');
        chatHeader.innerHTML = `
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px 10px 0 0; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold;">💼 Investment Platform Assistant</span>
                <span id="ie-close-chat" style="cursor: pointer; font-size: 18px;">×</span>
            </div>
        `;
        
        // Chat messages area
        const chatMessages = document.createElement('div');
        chatMessages.id = 'ie-chat-messages';
        chatMessages.style.cssText = `
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background: #f8f9fa;
        `;
        
        // Chat input area
        const chatInput = document.createElement('div');
        chatInput.innerHTML = `
            <div style="padding: 15px; border-top: 1px solid #eee; background: white; border-radius: 0 0 10px 10px;">
                <div style="display: flex; gap: 10px;">
                    <input type="text" id="ie-chat-input" placeholder="Ask about investments, funding, or business advice..." 
                           style="flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 20px; outline: none;">
                    <button id="ie-send-button" style="padding: 10px 15px; background: #667eea; color: white; border: none; border-radius: 50%; cursor: pointer;">➤</button>
                </div>
            </div>
        `;
        
        chatWindow.appendChild(chatHeader);
        chatWindow.appendChild(chatMessages);
        chatWindow.appendChild(chatInput);
        
        document.body.appendChild(chatButton);
        document.body.appendChild(chatWindow);
        
        // Add initial welcome message
        addMessage('bot', 'Welcome! I can help investors find opportunities and entrepreneurs secure funding. Are you an investor or entrepreneur?');
        
        // Event listeners
        chatButton.addEventListener('click', () => {
            chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
        });
        
        document.getElementById('ie-close-chat').addEventListener('click', () => {
            chatWindow.style.display = 'none';
        });
        
        const input = document.getElementById('ie-chat-input');
        const sendButton = document.getElementById('ie-send-button');
        
        sendButton.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        // Hover effect
        chatButton.addEventListener('mouseenter', () => {
            chatButton.style.transform = 'scale(1.1)';
        });
        
        chatButton.addEventListener('mouseleave', () => {
            chatButton.style.transform = 'scale(1)';
        });
    }
    
    function addMessage(sender, message) {
        const messagesDiv = document.getElementById('ie-chat-messages');
        const messageDiv = document.createElement('div');
        
        const isBot = sender === 'bot';
        messageDiv.style.cssText = `
            margin-bottom: 15px;
            display: flex;
            ${isBot ? 'justify-content: flex-start' : 'justify-content: flex-end'};
        `;
        
        const messageBubble = document.createElement('div');
        messageBubble.style.cssText = `
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            ${isBot ? 
                'background: white; border: 1px solid #e1e8ed; margin-right: auto;' : 
                'background: #667eea; color: white; margin-left: auto;'
            }
            white-space: pre-wrap;
            line-height: 1.4;
        `;
        
        messageBubble.innerHTML = message;
        messageDiv.appendChild(messageBubble);
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function sendMessage() {
        const input = document.getElementById('ie-chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        addMessage('user', message);
        input.value = '';
        
        // Show typing indicator
        addMessage('bot', '💭 Thinking...');
        
        fetch(chatbotConfig.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_id: localStorage.getItem('ie-conversation-id')
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            const messages = document.getElementById('ie-chat-messages');
            messages.removeChild(messages.lastChild);
            
            // Store conversation ID
            localStorage.setItem('ie-conversation-id', data.conversation_id);
            
            // Add bot response
            addMessage('bot', data.response);
            
            // Add suggestions if available
            if (data.suggestions && data.suggestions.length > 0) {
                const suggestionsDiv = document.createElement('div');
                suggestionsDiv.style.cssText = 'margin-top: 10px;';
                
                data.suggestions.slice(0, 3).forEach(suggestion => {
                    const suggestionBtn = document.createElement('button');
                    suggestionBtn.textContent = suggestion;
                    suggestionBtn.style.cssText = `
                        display: block;
                        width: 100%;
                        margin: 5px 0;
                        padding: 8px 12px;
                        background: #f8f9fa;
                        border: 1px solid #e1e8ed;
                        border-radius: 15px;
                        cursor: pointer;
                        text-align: left;
                        font-size: 13px;
                        transition: background 0.2s;
                    `;
                    
                    suggestionBtn.addEventListener('mouseenter', () => {
                        suggestionBtn.style.background = '#e9ecef';
                    });
                    
                    suggestionBtn.addEventListener('mouseleave', () => {
                        suggestionBtn.style.background = '#f8f9fa';
                    });
                    
                    suggestionBtn.addEventListener('click', () => {
                        document.getElementById('ie-chat-input').value = suggestion;
                        sendMessage();
                    });
                    
                    suggestionsDiv.appendChild(suggestionBtn);
                });
                
                const messages = document.getElementById('ie-chat-messages');
                const lastMessage = messages.lastChild.querySelector('div');
                lastMessage.appendChild(suggestionsDiv);
            }
        })
        .catch(error => {
            // Remove typing indicator
            const messages = document.getElementById('ie-chat-messages');
            messages.removeChild(messages.lastChild);
            
            addMessage('bot', 'Sorry, I encountered an error. Please try again.');
            console.error('Chatbot error:', error);
        });
    }
    
    // Initialize widget when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createChatWidget);
    } else {
        createChatWidget();
    }
})();
"""
    return widget_js, 200, {'Content-Type': 'application/javascript'}

# Iframe Integration
@app.route('/chat-iframe')
def chat_iframe():
    """Standalone chat interface for iframe embedding"""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Investment Platform Chatbot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: #f8f9fa;
        }
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
        }
        .chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
        }
        .message.user {
            justify-content: flex-end;
        }
        .message-bubble {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            line-height: 1.4;
            white-space: pre-wrap;
        }
        .message.bot .message-bubble {
            background: white;
            border: 1px solid #e1e8ed;
        }
        .message.user .message-bubble {
            background: #667eea;
            color: white;
        }
        .chat-input {
            padding: 15px;
            border-top: 1px solid #e1e8ed;
            background: white;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        #messageInput {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
        }
        #sendButton {
            padding: 12px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
        }
        #sendButton:hover {
            background: #5a6fd8;
        }
    </style>
</head>
<body>
    <div class="chat-header">
        💼 Investment Platform Assistant
    </div>
    <div class="chat-messages" id="chatMessages">
    </div>
    <div class="chat-input">
        <div class="input-group">
            <input type="text" id="messageInput" placeholder="Ask about investments, funding, or business advice...">
            <button id="sendButton">Send</button>
        </div>
    </div>

    <script>
        let conversationId = localStorage.getItem('chat-conversation-id');
        
        function addMessage(sender, message) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const messageBubble = document.createElement('div');
            messageBubble.className = 'message-bubble';
            messageBubble.innerHTML = message;
            
            messageDiv.appendChild(messageBubble);
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            addMessage('user', message);
            input.value = '';
            
            addMessage('bot', '💭 Thinking...');
            
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    conversation_id: conversationId
                })
            })
            .then(response => response.json())
            .then(data => {
                const messages = document.getElementById('chatMessages');
                messages.removeChild(messages.lastChild);
                
                conversationId = data.conversation_id;
                localStorage.setItem('chat-conversation-id', conversationId);
                
                addMessage('bot', data.response);
            })
            .catch(error => {
                const messages = document.getElementById('chatMessages');
                messages.removeChild(messages.lastChild);
                addMessage('bot', 'Sorry, I encountered an error. Please try again.');
            });
        }
        
        document.getElementById('sendButton').addEventListener('click', sendMessage);
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
        
        // Initial welcome message
        addMessage('bot', 'Welcome! I can help investors find opportunities and entrepreneurs secure funding. Are you an investor or entrepreneur?');
    </script>
</body>
</html>
"""
    return html

# WebSocket support (basic implementation)
@app.route('/webhook', methods=['POST'])
def webhook_endpoint():
    """Webhook endpoint for external integrations"""
    try:
        data = request.json
        event_type = data.get('event_type')
        payload = data.get('payload', {})
        
        if event_type == 'message':
            response = chatbot.process_message(
                payload.get('message', ''),
                payload.get('conversation_id')
            )
            return jsonify(response)
        
        return jsonify({'status': 'received', 'event_type': event_type})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Investor-Entrepreneur Chatbot Server Starting...")
    print("📡 REST API available at: http://localhost:8080/api/chat")
    print("🔗 JavaScript Widget: http://localhost:8080/widget.js")
    print("🖼️ Iframe Embed: http://localhost:8080/chat-iframe")
    print("🔗 Webhook URL: http://localhost:8080/webhook")
    print("\n📋 Integration Examples:")
    print("• REST API: Use /api/chat endpoint from any framework")
    print("• Widget: Add <script src='http://your-domain.com/widget.js'></script>")
    print("• Iframe: <iframe src='http://your-domain.com/chat-iframe'></iframe>")
    
    app.run(debug=True, host='0.0.0.0', port=8080)   