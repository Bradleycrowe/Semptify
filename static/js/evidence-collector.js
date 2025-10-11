// Semptify Evidence Collection System
// Comprehensive location, timestamp, voice, and audio recording system

class SemptifyEvidenceCollector {
    constructor() {
        this.location = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.recognition = null;
        this.isListening = false;
        
        this.init();
    }

    async init() {
        this.requestLocation();
        this.initVoiceRecognition();
        this.startTimestampUpdates();
        console.log('Semptify Evidence Collector initialized');
    }

    // ===== LOCATION & TIMESTAMP SYSTEM =====
    async requestLocation() {
        if (!navigator.geolocation) {
            console.warn('Geolocation not supported');
            this.updateLocationDisplay('Geolocation not supported');
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
            console.warn('Location access denied:', error.message);
            this.updateLocationDisplay('Location access denied');
        }
    }

    getCurrentTimestamp() {
        return new Date().toISOString();
    }

    getLocationString() {
        if (!this.location) return 'Location unavailable';
        const lat = this.location.latitude.toFixed(6);
        const lng = this.location.longitude.toFixed(6);
        const acc = Math.round(this.location.accuracy);
        return `${lat}, ${lng} (±${acc}m)`;
    }

    startTimestampUpdates() {
        // Update timestamp display every second
        setInterval(() => {
            this.updateTimestampDisplay();
        }, 1000);
        this.updateTimestampDisplay();
    }

    updateTimestampDisplay() {
        const elements = document.querySelectorAll('.timestamp-display');
        elements.forEach(el => {
            el.textContent = new Date().toLocaleString();
        });
    }

    updateLocationDisplay() {
        const elements = document.querySelectorAll('.location-display');
        const locationText = this.getLocationString();
        elements.forEach(el => {
            el.textContent = locationText;
            if (this.location) {
                el.classList.add('location-acquired');
            }
        });
    }

    // ===== VOICE RECOGNITION SYSTEM =====
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
            this.updateVoiceStatus('Recognition error: ' + event.error);
        };

        this.recognition.onend = () => {
            if (this.isListening) {
                // Restart if we're supposed to be listening
                setTimeout(() => this.recognition.start(), 100);
            }
        };
    }

    startVoiceRecognition() {
        if (!this.recognition) {
            alert('Voice recognition not supported in this browser');
            return;
        }

        this.isListening = true;
        this.recognition.start();
        this.updateVoiceStatus('Listening for commands...');
        console.log('Voice recognition started');
    }

    stopVoiceRecognition() {
        this.isListening = false;
        if (this.recognition) {
            this.recognition.stop();
        }
        this.updateVoiceStatus('Voice recognition stopped');
        console.log('Voice recognition stopped');
    }

    handleVoiceCommand(command) {
        console.log('Voice command received:', command);
        this.updateVoiceStatus(`Command: "${command}"`);

        if (command.includes('start recording') || command.includes('record audio')) {
            this.startAudioRecording();
        } else if (command.includes('stop recording') || command.includes('stop audio')) {
            this.stopAudioRecording();
        } else if (command.includes('get location') || command.includes('update location')) {
            this.requestLocation();
        } else if (command.includes('ask copilot') || command.includes('ask ai') || command.includes('help')) {
            this.askAI();
        } else if (command.includes('save form') || command.includes('submit form')) {
            this.saveCurrentForm();
        } else if (command.includes('timestamp') || command.includes('time stamp')) {
            this.announceTimestamp();
        }
    }

    updateVoiceStatus(status) {
        const elements = document.querySelectorAll('.voice-status');
        elements.forEach(el => {
            el.textContent = status;
        });
    }

    // ===== AUDIO RECORDING SYSTEM =====
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
            this.updateRecordingStatus('Recording... 🔴');

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
        this.updateRecordingStatus('Processing recording...');
    }

    processAudioRecording() {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        const timestamp = this.getCurrentTimestamp();
        const location = this.getLocationString();

        // Create metadata
        const metadata = {
            type: 'audio_evidence',
            timestamp: timestamp,
            location: location,
            duration_chunks: this.audioChunks.length,
            size_bytes: audioBlob.size,
            collected_at: new Date().toLocaleString(),
            user_agent: navigator.userAgent
        };

        // Download files
        this.downloadRecording(audioBlob, metadata);
        this.updateRecordingStatus('Recording saved! 💾');

        // Reset for next recording
        this.audioChunks = [];
    }

    downloadRecording(audioBlob, metadata) {
        const timestamp = this.getCurrentTimestamp().replace(/[:.]/g, '-');
        const filename = `evidence_audio_${timestamp}.wav`;

        // Download audio file
        const audioUrl = URL.createObjectURL(audioBlob);
        this.downloadFile(audioUrl, filename);

        // Download metadata file
        const metadataBlob = new Blob([JSON.stringify(metadata, null, 2)], { type: 'application/json' });
        const metadataUrl = URL.createObjectURL(metadataBlob);
        this.downloadFile(metadataUrl, filename.replace('.wav', '_metadata.json'));

        // Clean up URLs
        setTimeout(() => {
            URL.revokeObjectURL(audioUrl);
            URL.revokeObjectURL(metadataUrl);
        }, 1000);
    }

    downloadFile(url, filename) {
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    updateRecordingStatus(status) {
        const elements = document.querySelectorAll('.recording-status');
        elements.forEach(el => {
            el.textContent = status;
        });
    }

    // ===== AI INTEGRATION =====
    async askAI(customPrompt = null) {
        const formContext = this.getFormContext();
        const prompt = customPrompt || this.buildContextualPrompt(formContext);

        try {
            const response = await this.sendToAI(prompt, formContext);
            this.displayAIResponse(response);
        } catch (error) {
            console.error('AI request failed:', error);
            this.displayAIResponse('AI assistance unavailable. Please try again later.');
        }
    }

    buildContextualPrompt(formContext) {
        let prompt = 'I am collecting evidence for a tenant rights case. ';

        if (this.location) {
            prompt += `I am at location ${this.getLocationString()}. `;
        }

        prompt += `Current time: ${new Date().toLocaleString()}. `;

        if (formContext.formType) {
            prompt += `I am working on a ${formContext.formType.replace('_', ' ')}. `;
        }

        if (formContext.data && Object.keys(formContext.data).length > 0) {
            prompt += `Current form data: ${JSON.stringify(formContext.data)}. `;
        }

        prompt += 'Please provide specific guidance on what evidence to collect, legal considerations, and best practices for documentation.';

        return prompt;
    }

    async sendToAI(prompt, context) {
        const payload = {
            prompt: prompt,
            location: this.location ? this.getLocationString() : 'Unknown',
            timestamp: this.getCurrentTimestamp(),
            form_type: context.formType || 'general',
            form_data: context.data || {}
        };

        const csrfToken = this.getCSRFToken();
        const response = await fetch('/api/copilot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`AI request failed: ${response.status}`);
        }

        const data = await response.json();
        return data.output || data.response || 'No response received';
    }

    displayAIResponse(response) {
        // Remove existing AI panel if present
        const existing = document.querySelector('.ai-response-panel');
        if (existing) {
            existing.remove();
        }

        // Create new AI response panel
        const panel = document.createElement('div');
        panel.className = 'ai-response-panel';
        panel.innerHTML = `
            <div class="ai-response-header">
                <h3>🤖 AI Assistant</h3>
                <button class="ai-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="ai-response-content">
                <p><strong>Time:</strong> ${new Date().toLocaleString()}</p>
                <p><strong>Location:</strong> ${this.getLocationString()}</p>
                <div class="ai-response-text">${response.replace(/\n/g, '<br>')}</div>
            </div>
        `;

        document.body.appendChild(panel);
        panel.scrollIntoView({ behavior: 'smooth' });
    }

    // ===== UTILITY FUNCTIONS =====
    getFormContext() {
        const form = document.querySelector('form');
        const formType = this.detectFormType();
        const data = {};

        if (form) {
            const formData = new FormData(form);
            for (let [key, value] of formData.entries()) {
                if (value && value.trim && value.trim()) {
                    data[key] = value;
                }
            }
        }

        return { formType, data };
    }

    detectFormType() {
        const url = window.location.pathname;
        if (url.includes('witness')) return 'witness_statement';
        if (url.includes('filing_packet') || url.includes('packet')) return 'filing_packet';
        if (url.includes('service_animal')) return 'service_animal_request';
        if (url.includes('move_checklist')) return 'move_checklist';
        return 'general_form';
    }

    getCSRFToken() {
        const tokenInput = document.querySelector('input[name="csrf_token"]');
        return tokenInput ? tokenInput.value : '';
    }

    saveCurrentForm() {
        const submitButton = document.querySelector('button[type="submit"]');
        if (submitButton) {
            this.enhanceFormWithEvidence();
            submitButton.click();
        } else {
            console.log('No submit button found');
        }
    }

    enhanceFormWithEvidence() {
        const form = document.querySelector('form');
        if (!form) return;

        // Add hidden fields with evidence data
        this.addHiddenField(form, 'evidence_timestamp', this.getCurrentTimestamp());
        this.addHiddenField(form, 'evidence_location', this.getLocationString());
        this.addHiddenField(form, 'location_accuracy', this.location ? this.location.accuracy.toString() : 'unknown');
        this.addHiddenField(form, 'evidence_user_agent', navigator.userAgent);
    }

    addHiddenField(form, name, value) {
        // Remove existing field if present
        const existing = form.querySelector(`input[name="${name}"]`);
        if (existing) {
            existing.value = value;
            return;
        }

        // Create new hidden field
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = value;
        form.appendChild(input);
    }

    announceTimestamp() {
        const timestamp = new Date().toLocaleString();
        this.updateVoiceStatus(`Current time: ${timestamp}`);
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(`Current time is ${timestamp}`);
            speechSynthesis.speak(utterance);
        }
    }

    // ===== PUBLIC API =====
    toggleRecording() {
        if (this.isRecording) {
            this.stopAudioRecording();
        } else {
            this.startAudioRecording();
        }
    }

    toggleVoiceCommands() {
        if (this.isListening) {
            this.stopVoiceRecognition();
        } else {
            this.startVoiceRecognition();
        }
    }
}

// Initialize the evidence collector when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.semptifyEvidence = new SemptifyEvidenceCollector();
    console.log('Semptify Evidence Collector ready');
});

// Global functions for UI buttons
function toggleRecording() {
    window.semptifyEvidence?.toggleRecording();
}

function toggleVoiceCommands() {
    window.semptifyEvidence?.toggleVoiceCommands();
}

function askAI() {
    window.semptifyEvidence?.askAI();
}

function updateLocation() {
    window.semptifyEvidence?.requestLocation();
}