// Semptify Evidence Collection System
// Location, Timestamp, Voice, and Audio Recording utilities

class SemptifyEvidence {
    constructor() {
        this.location = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.recognition = null;
        this.initVoiceRecognition();
        this.requestLocation();
    }

    // Geolocation and Timestamping
    async requestLocation() {
        if (!navigator.geolocation) {
            console.warn('Geolocation not supported');
            return;
        }
        
        try {
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 300000 // 5 minutes
                });
            });
            
            this.location = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                accuracy: position.coords.accuracy,
                timestamp: new Date().toISOString()
            };
            
            console.log('Location acquired:', this.location);
            this.updateLocationDisplay();
        } catch (error) {
            console.warn('Location access denied or unavailable:', error.message);
        }
    }

    getTimestamp() {
        return new Date().toISOString();
    }

    getLocationString() {
        if (!this.location) return 'Location unavailable';
        return `${this.location.latitude.toFixed(6)}, ${this.location.longitude.toFixed(6)} (±${this.location.accuracy}m)`;
    }

    updateLocationDisplay() {
        const locationElements = document.querySelectorAll('.location-display');
        locationElements.forEach(el => {
            el.textContent = this.getLocationString();
            el.classList.add('location-acquired');
        });
    }

    // Voice Recognition for Commands
    initVoiceRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';

        this.recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
            this.handleVoiceCommand(transcript);
        };

        this.recognition.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
        };
    }

    handleVoiceCommand(command) {
        console.log('Voice command:', command);
        
        if (command.includes('start recording') || command.includes('record audio')) {
            this.startAudioRecording();
        } else if (command.includes('stop recording') || command.includes('stop audio')) {
            this.stopAudioRecording();
        } else if (command.includes('get location') || command.includes('update location')) {
            this.requestLocation();
        } else if (command.includes('ask copilot') || command.includes('ask ai')) {
            this.triggerAIAssist();
        } else if (command.includes('save evidence') || command.includes('save form')) {
            this.saveCurrentForm();
        }

        // Update voice command display
        const voiceDisplay = document.querySelector('.voice-command-display');
        if (voiceDisplay) {
            voiceDisplay.textContent = `Last command: "${command}"`;
        }
    }

    startVoiceRecognition() {
        if (this.recognition) {
            this.recognition.start();
            console.log('Voice recognition started');
        }
    }

    stopVoiceRecognition() {
        if (this.recognition) {
            this.recognition.stop();
            console.log('Voice recognition stopped');
        }
    }

    // Audio Recording
    async startAudioRecording() {
        if (this.isRecording) {
            console.log('Already recording');
            return;
        }

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                this.processAudioRecording();
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            
            console.log('Audio recording started');
            this.updateRecordingUI(true);
            
        } catch (error) {
            console.error('Error starting audio recording:', error);
            alert('Could not access microphone. Please check permissions.');
        }
    }

    stopAudioRecording() {
        if (!this.isRecording) {
            console.log('Not currently recording');
            return;
        }

        this.mediaRecorder.stop();
        this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
        this.isRecording = false;
        
        console.log('Audio recording stopped');
        this.updateRecordingUI(false);
    }

    processAudioRecording() {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        const timestamp = this.getTimestamp();
        const location = this.getLocationString();
        
        // Create metadata
        const metadata = {
            timestamp: timestamp,
            location: location,
            duration: this.audioChunks.length,
            type: 'audio_evidence'
        };

        // Create download link
        const url = URL.createObjectURL(audioBlob);
        const filename = `evidence_audio_${timestamp.replace(/[:.]/g, '-')}.wav`;
        
        this.downloadAudio(url, filename, metadata);
        this.sendToAI(audioBlob, metadata);
    }

    downloadAudio(url, filename, metadata) {
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        
        // Also create metadata file
        const metadataBlob = new Blob([JSON.stringify(metadata, null, 2)], { type: 'application/json' });
        const metadataUrl = URL.createObjectURL(metadataBlob);
        const metadataFilename = filename.replace('.wav', '_metadata.json');
        
        const metaLink = document.createElement('a');
        metaLink.href = metadataUrl;
        metaLink.download = metadataFilename;
        metaLink.click();
    }

    updateRecordingUI(isRecording) {
        const recordBtn = document.querySelector('.record-btn');
        const recordStatus = document.querySelector('.record-status');
        
        if (recordBtn) {
            recordBtn.textContent = isRecording ? '⏹️ Stop Recording' : '🎙️ Start Recording';
            recordBtn.classList.toggle('recording', isRecording);
        }
        
        if (recordStatus) {
            recordStatus.textContent = isRecording ? 'Recording...' : 'Ready to record';
            recordStatus.classList.toggle('active', isRecording);
        }
    }

    // AI Integration
    async sendToAI(audioBlob, metadata) {
        // Convert audio to base64 for sending (if needed)
        // For now, just trigger AI with context
        const context = `Audio evidence recorded at ${metadata.timestamp} from location ${metadata.location}`;
        this.triggerAIAssist(context);
    }

    async triggerAIAssist(context = '') {
        const currentForm = this.getCurrentFormContext();
        const prompt = this.buildAIPrompt(currentForm, context);
        
        try {
            const payload = {
                prompt: prompt,
                location: this.getLocationString(),
                timestamp: this.getTimestamp(),
                form_type: this.getFormType(),
                form_data: JSON.stringify(currentForm)
            };

            const response = await fetch('/api/evidence-copilot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                const data = await response.json();
                this.displayAIResponse(data.output, data.context);
            } else {
                console.error('AI request failed:', response.status);
                // Fallback to basic copilot
                this.fallbackAIRequest(prompt);
            }
        } catch (error) {
            console.error('AI request error:', error);
            this.fallbackAIRequest(prompt);
        }
    }

    async fallbackAIRequest(prompt) {
        try {
            const response = await fetch('/api/copilot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ prompt: prompt })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.displayAIResponse(data.output);
            }
        } catch (error) {
            console.error('Fallback AI request failed:', error);
        }
    }

    getCurrentFormContext() {
        const formElement = document.querySelector('form');
        if (!formElement) return 'No form active';
        
        const formData = new FormData(formElement);
        const context = {};
        
        for (let [key, value] of formData.entries()) {
            if (value && value.trim()) {
                context[key] = value;
            }
        }
        
        return context;
    }

    buildAIPrompt(formContext, additionalContext = '') {
        let prompt = 'I am collecting evidence for a tenant rights case. ';
        
        if (additionalContext) {
            prompt += additionalContext + '. ';
        }
        
        if (this.location) {
            prompt += `I am at location ${this.getLocationString()}. `;
        }
        
        prompt += `Current timestamp: ${this.getTimestamp()}. `;
        
        if (formContext && Object.keys(formContext).length > 0) {
            prompt += 'Current form data: ' + JSON.stringify(formContext) + '. ';
        }
        
        prompt += 'Please provide guidance on what evidence to collect, legal considerations, or help me document this properly.';
        
        return prompt;
    }

    displayAIResponse(response, context = null) {
        let aiDisplay = document.querySelector('.ai-response');
        if (!aiDisplay) {
            aiDisplay = document.createElement('div');
            aiDisplay.className = 'ai-response card';
            aiDisplay.innerHTML = '<h3>🤖 Evidence AI Assistant</h3><div class="ai-content"></div><button class="ai-close" onclick="this.parentElement.remove()">×</button>';
            document.body.appendChild(aiDisplay);
        }
        
        const content = aiDisplay.querySelector('.ai-content');
        let contextInfo = '';
        if (context && context.location) {
            contextInfo = `<p><strong>Location:</strong> ${context.location}</p>`;
        }
        
        content.innerHTML = `<p><strong>Timestamp:</strong> ${this.getTimestamp()}</p>
                           ${contextInfo}
                           <div><strong>AI Guidance:</strong></div>
                           <div class="ai-response-text">${response.replace(/\n/g, '<br>')}</div>`;
        
        // Scroll into view
        aiDisplay.scrollIntoView({ behavior: 'smooth' });
    }

    getFormType() {
        const url = window.location.pathname;
        if (url.includes('witness')) return 'witness_statement';
        if (url.includes('filing_packet')) return 'filing_packet';
        if (url.includes('service_animal')) return 'service_animal';
        if (url.includes('move_checklist')) return 'move_checklist';
        return 'general';
    }

    getCSRFToken() {
        const token = document.querySelector('input[name="csrf_token"]');
        return token ? token.value : '';
    }

    saveCurrentForm() {
        const saveBtn = document.querySelector('button[type="submit"]');
        if (saveBtn) {
            saveBtn.click();
        }
    }

    // Enhanced form data with location and timestamp
    enhanceFormData(formElement) {
        // Add hidden fields for location and timestamp
        this.addHiddenField(formElement, 'evidence_timestamp', this.getTimestamp());
        this.addHiddenField(formElement, 'evidence_location', this.getLocationString());
        this.addHiddenField(formElement, 'location_accuracy', this.location ? this.location.accuracy : 'unknown');
    }

    addHiddenField(form, name, value) {
        let existing = form.querySelector(`input[name="${name}"]`);
        if (existing) {
            existing.value = value;
        } else {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = name;
            input.value = value;
            form.appendChild(input);
        }
    }
}

// Initialize the system
window.semptifyEvidence = new SemptifyEvidence();

// Auto-enhance forms when they're submitted
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            window.semptifyEvidence.enhanceFormData(form);
        });
    });
});