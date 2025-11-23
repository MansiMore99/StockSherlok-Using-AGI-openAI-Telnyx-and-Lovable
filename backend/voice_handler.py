"""
Voice Handler - Telnyx integration for voice queries
"""
import telnyx
from typing import Dict, Optional


class VoiceHandler:
    """
    Handle voice interactions using Telnyx
    """
    
    def __init__(self, api_key: str, phone_number: str):
        """Initialize Telnyx voice handler"""
        self.api_key = api_key
        self.phone_number = phone_number
        telnyx.api_key = api_key
    
    def handle_webhook(self, webhook_data: Dict) -> Dict:
        """
        Handle incoming Telnyx webhooks
        """
        event_type = webhook_data.get('data', {}).get('event_type', '')
        
        if event_type == 'call.initiated':
            return self._handle_call_initiated(webhook_data)
        elif event_type == 'call.answered':
            return self._handle_call_answered(webhook_data)
        elif event_type == 'call.speak.ended':
            return self._handle_speak_ended(webhook_data)
        else:
            return {'status': 'ignored', 'event_type': event_type}
    
    def _handle_call_initiated(self, data: Dict) -> Dict:
        """Handle call initiated event"""
        call_control_id = data.get('data', {}).get('payload', {}).get('call_control_id')
        
        # Answer the call
        try:
            telnyx.Call.answer(call_control_id)
            return {'status': 'answered', 'call_control_id': call_control_id}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _handle_call_answered(self, data: Dict) -> Dict:
        """Handle call answered event"""
        call_control_id = data.get('data', {}).get('payload', {}).get('call_control_id')
        
        # Greet the caller
        greeting = (
            "Hello! I am Sherlok, your AI-powered stock research assistant. "
            "I can help you analyze mid-cap and early-stage tech companies. "
            "Please say the ticker symbol of the company you'd like to research."
        )
        
        try:
            telnyx.Call.speak(
                call_control_id,
                payload=greeting,
                voice='female',
                language='en-US'
            )
            return {'status': 'greeting_sent', 'call_control_id': call_control_id}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _handle_speak_ended(self, data: Dict) -> Dict:
        """Handle speak ended event - ready to gather input"""
        call_control_id = data.get('data', {}).get('payload', {}).get('call_control_id')
        
        # In a full implementation, we would gather speech input here
        # For now, just acknowledge
        return {'status': 'ready_for_input', 'call_control_id': call_control_id}
    
    def make_outbound_call(self, to_number: str, ticker: str, analysis: str) -> Dict:
        """
        Make an outbound call to deliver stock analysis
        """
        message = f"Here is the analysis for {ticker}: {analysis}"
        
        try:
            call = telnyx.Call.create(
                connection_id=self.phone_number,
                to=to_number,
                from_=self.phone_number
            )
            
            # Speak the analysis
            telnyx.Call.speak(
                call.call_control_id,
                payload=message,
                voice='female',
                language='en-US'
            )
            
            return {
                'status': 'call_initiated',
                'call_id': call.call_control_id
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def send_sms_alert(self, to_number: str, ticker: str, summary: str) -> Dict:
        """
        Send SMS alert with stock insights
        """
        message = f"Sherlok Alert: {ticker}\n\n{summary[:140]}..."
        
        try:
            telnyx.Message.create(
                from_=self.phone_number,
                to=to_number,
                text=message
            )
            
            return {'status': 'sms_sent', 'to': to_number}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
