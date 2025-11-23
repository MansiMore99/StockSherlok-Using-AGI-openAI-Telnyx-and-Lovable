import telnyx from 'telnyx';

// Placeholder constant for API key configuration
const PLACEHOLDER_API_KEY = 'your_telnyx_api_key_here';

/**
 * TelnyxVoiceService - Handles voice-based queries via Telnyx
 * This enables users to talk to Stock Sherlok like a real financial assistant
 */
class TelnyxVoiceService {
  constructor() {
    this.apiKey = process.env.TELNYX_API_KEY;
    this.phoneNumber = process.env.TELNYX_PHONE_NUMBER;
    
    if (this.apiKey && this.apiKey !== PLACEHOLDER_API_KEY) {
      this.client = telnyx(this.apiKey);
      this.enabled = true;
    } else {
      this.enabled = false;
      console.log('Telnyx voice service is disabled. Configure TELNYX_API_KEY to enable voice features.');
    }
  }

  /**
   * Check if voice service is enabled
   */
  isEnabled() {
    return this.enabled;
  }

  /**
   * Handle incoming voice call
   */
  async handleIncomingCall(callControlId, callbackUrl) {
    if (!this.enabled) {
      return { success: false, message: 'Voice service not configured' };
    }

    try {
      // Answer the call
      await this.client.calls.answer({
        call_control_id: callControlId,
      });

      // Speak greeting
      await this.speakText(
        callControlId,
        'Hello! I am Stock Sherlok, your AI-powered financial detective. How can I help you with stock analysis today?'
      );

      return { success: true, message: 'Call answered successfully' };
    } catch (error) {
      console.error('Error handling incoming call:', error.message);
      return { success: false, message: error.message };
    }
  }

  /**
   * Speak text to caller
   */
  async speakText(callControlId, text) {
    if (!this.enabled) {
      return { success: false, message: 'Voice service not configured' };
    }

    try {
      await this.client.calls.speak({
        call_control_id: callControlId,
        payload: text,
        voice: 'female',
        language: 'en-US',
      });

      return { success: true };
    } catch (error) {
      console.error('Error speaking text:', error.message);
      return { success: false, message: error.message };
    }
  }

  /**
   * Gather speech input from user
   */
  async gatherSpeechInput(callControlId) {
    if (!this.enabled) {
      return { success: false, message: 'Voice service not configured' };
    }

    try {
      // Use Telnyx's gather with speech recognition
      const result = await this.client.calls.gather({
        call_control_id: callControlId,
        speech_model: 'default',
        speech_language: 'en-US',
        speech_timeout: 'auto',
      });

      return { success: true, data: result };
    } catch (error) {
      console.error('Error gathering speech input:', error.message);
      return { success: false, message: error.message };
    }
  }

  /**
   * Make outbound call
   */
  async makeOutboundCall(toNumber, message) {
    if (!this.enabled) {
      return { success: false, message: 'Voice service not configured' };
    }

    try {
      const call = await this.client.calls.create({
        to: toNumber,
        from: this.phoneNumber,
        connection_id: process.env.TELNYX_CONNECTION_ID,
      });

      // Note: Message will be spoken once call is answered via webhook event handler
      return { 
        success: true, 
        callControlId: call.data.call_control_id,
        note: 'Call initiated. Message will be spoken when answered via webhook.'
      };
    } catch (error) {
      console.error('Error making outbound call:', error.message);
      return { success: false, message: error.message };
    }
  }

  /**
   * End call
   */
  async hangup(callControlId) {
    if (!this.enabled) {
      return { success: false, message: 'Voice service not configured' };
    }

    try {
      await this.client.calls.hangup({
        call_control_id: callControlId,
      });

      return { success: true };
    } catch (error) {
      console.error('Error hanging up call:', error.message);
      return { success: false, message: error.message };
    }
  }

  /**
   * Process voice webhook from Telnyx
   */
  processWebhook(event) {
    const eventType = event.data?.event_type;
    const callControlId = event.data?.payload?.call_control_id;

    return {
      eventType,
      callControlId,
      payload: event.data?.payload,
    };
  }
}

export default TelnyxVoiceService;
