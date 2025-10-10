# Evidence Collection System

Semptify now includes a comprehensive evidence collection system with location tracking, timestamping, voice activation, audio recording, and AI-powered assistance.

## Features

### 📍 Location & Timestamp Tracking
- **Automatic geolocation**: Uses GPS/network location to timestamp evidence
- **Precision tracking**: Records location accuracy for legal verification
- **Consistent timestamps**: All evidence includes ISO-8601 timestamps
- **Privacy-aware**: Location is only used when granted permission

### 🎙️ Audio Recording
- **One-click recording**: Start/stop audio evidence collection
- **Metadata preservation**: Each recording includes timestamp, location, duration
- **Automatic downloads**: Audio files and metadata JSON downloaded automatically
- **Legal formatting**: Files named with timestamps for organization

### 🗣️ Voice Commands
- **Hands-free operation**: Control recording and navigation with voice
- **Natural language**: Say "start recording", "stop recording", "ask copilot"
- **Multi-browser support**: Works with Chrome, Safari, Edge (with Speech API)

### 🤖 AI-Powered Assistance
- **Context-aware guidance**: AI understands your location, form type, and situation
- **Legal advice**: Specific tenant rights information and evidence collection tips
- **Real-time help**: Ask for guidance while filling forms or collecting evidence
- **Enhanced prompts**: Location and timestamp automatically included in AI requests

## How to Use

### Getting Started
1. **Grant permissions**: Allow location and microphone access when prompted
2. **Voice activation**: Click "Voice Commands" to enable voice control
3. **Recording**: Use "Start Recording" button or say "start recording"
4. **AI assistance**: Click "Ask AI" or say "ask copilot" for guidance

### Voice Commands
- `"start recording"` - Begin audio evidence collection
- `"stop recording"` - End recording and download files
- `"ask copilot"` - Get AI assistance for current situation
- `"get location"` - Update current location
- `"save evidence"` - Submit current form

### Evidence Collection Workflow
1. **Open any form** (Witness Statement, Filing Packet, etc.)
2. **Evidence panel appears** with current location and timestamp
3. **Fill form details** as needed
4. **Record audio evidence** if relevant to your case
5. **Ask AI for guidance** on evidence collection or legal considerations
6. **Submit form** - location and timestamp automatically included

## Technical Details

### Location Data
```javascript
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "accuracy": 10,
  "timestamp": "2025-10-10T15:30:00.000Z"
}
```

### Certificate Enhancement
All form certificates now include evidence metadata:
```json
{
  "type": "witness_statement",
  "evidence": {
    "timestamp": "2025-10-10T15:30:00.000Z",
    "location": "40.7128,-74.0060 (±10m)",
    "location_accuracy": "10"
  }
}
```

### Audio Recording Format
- **Format**: WAV audio files
- **Naming**: `evidence_audio_2025-10-10T15-30-00Z.wav`
- **Metadata**: Separate JSON file with timestamp, location, duration

### AI Integration
- **Enhanced endpoint**: `/api/evidence-copilot` with location/context awareness
- **Fallback support**: Gracefully falls back to basic copilot if enhanced fails
- **Context passing**: Current form data, location, and timestamp sent to AI

## Privacy & Security

### Data Handling
- **Location privacy**: Only collected with explicit permission
- **Local storage**: Audio recordings saved locally, not transmitted to server
- **Metadata only**: Only timestamp/location metadata saved with forms
- **User control**: All features can be disabled or permission revoked

### Legal Considerations
- **Admissible evidence**: Timestamps and locations for legal verification
- **Chain of custody**: Automatic SHA-256 hashing of all evidence
- **Consent tracking**: Voice recording permissions tracked
- **Jurisdiction aware**: AI can provide location-specific tenant rights info

## Browser Compatibility

### Full Support
- **Chrome/Chromium**: All features supported
- **Safari**: All features (may require permissions setup)
- **Edge**: All features supported

### Partial Support
- **Firefox**: Location and AI work; Speech API limited
- **Mobile browsers**: Location and AI work; voice/audio may be limited

## Troubleshooting

### Location Issues
- **"Location unavailable"**: Check browser permissions in settings
- **Inaccurate location**: Move to area with better GPS/network signal
- **Privacy concerns**: Location can be disabled - timestamps still work

### Audio Recording Issues
- **No microphone**: Check browser permissions and hardware
- **Recording fails**: Try refreshing page and re-granting permissions
- **File download issues**: Check browser download settings

### Voice Commands
- **Not recognized**: Speak clearly, try different phrasing
- **Wrong commands**: Check supported command list above
- **Privacy mode**: Some browsers block speech recognition in private mode

### AI Assistance
- **No response**: Check if AI provider is configured (admin setting)
- **Generic responses**: Enhanced copilot may fall back to basic mode
- **Rate limiting**: Wait and try again if hitting API limits

## For Administrators

### Configuration
Set environment variables for AI provider:
```bash
AI_PROVIDER=openai  # or azure, ollama
OPENAI_API_KEY=your_key_here
```

### Monitoring
Evidence collection events are logged:
- `evidence_copilot`: AI assistance requests with location context
- `voice_command`: Voice command usage (for feature analytics)
- Standard form saves include evidence metadata

### Privacy Settings
- Location data is never stored on server permanently
- Audio recordings stay on user device
- Only metadata (timestamp, location string) included in certificates