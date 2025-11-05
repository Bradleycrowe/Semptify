// Audio/Video Module JavaScript
// Handles recording, voice-to-text, and multimedia capture

let videoStream = null;
let audioStream = null;
let mediaRecorder = null;
let recordedChunks = [];
let recognition = null;
let transcriptionText = '';
let captureMetadata = {};

// Check browser support
const hasMediaDevices = navigator.mediaDevices && navigator.mediaDevices.getUserMedia;
const hasSpeechRecognition = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;

// Initialize Speech Recognition
function initSpeechRecognition() {
    if (!hasSpeechRecognition) {
        console.warn('Speech recognition not supported in this browser');
        return null;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        transcriptionText += finalTranscript;
        document.getElementById('transcription-text').textContent = 
            transcriptionText + (interimTranscript ? '...' + interimTranscript : '');
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
    };

    return recognition;
}

// Get GPS location
async function getLocation() {
    return new Promise((resolve) => {
        if (!navigator.geolocation) {
            resolve({ error: 'Geolocation not supported' });
            return;
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy,
                    timestamp: new Date(position.timestamp).toISOString()
                });
            },
            (error) => {
                resolve({ error: error.message });
            }
        );
    });
}

// Toggle Video Recording
async function toggleVideoRecording() {
    const btn = document.getElementById('video-record-btn');
    const preview = document.getElementById('video-preview');
    const videoElement = document.getElementById('video-element');
    const uploadBtn = document.getElementById('video-upload-btn');
    const metadataPanel = document.getElementById('video-metadata');

    if (!videoStream) {
        // Start recording
        try {
            videoStream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 1280, height: 720 }, 
                audio: true 
            });
            
            videoElement.srcObject = videoStream;
            videoElement.style.display = 'block';
            videoElement.play();
            
            preview.querySelector('p').style.display = 'none';
            
            recordedChunks = [];
            mediaRecorder = new MediaRecorder(videoStream, { mimeType: 'video/webm' });
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = async () => {
                const blob = new Blob(recordedChunks, { type: 'video/webm' });
                const url = URL.createObjectURL(blob);
                videoElement.srcObject = null;
                videoElement.src = url;
                uploadBtn.style.display = 'block';
                
                // Get metadata
                const location = await getLocation();
                captureMetadata.video = {
                    timestamp: new Date().toISOString(),
                    location: location,
                    size: blob.size,
                    duration: videoElement.duration || 'calculating...',
                    type: 'video/webm'
                };
                
                displayMetadata('video', captureMetadata.video);
                metadataPanel.style.display = 'block';
            };
            
            mediaRecorder.start();
            btn.textContent = '■ Stop Recording';
            btn.classList.add('recording');
            
        } catch (error) {
            alert('Error accessing camera/microphone: ' + error.message);
            console.error(error);
        }
    } else {
        // Stop recording
        mediaRecorder.stop();
        videoStream.getTracks().forEach(track => track.stop());
        videoStream = null;
        btn.textContent = '● Start Video Recording';
        btn.classList.remove('recording');
    }
}

// Toggle Audio Recording with Voice-to-Text
async function toggleAudioRecording() {
    const btn = document.getElementById('audio-record-btn');
    const preview = document.getElementById('audio-preview');
    const audioElement = document.getElementById('audio-element');
    const uploadBtn = document.getElementById('audio-upload-btn');
    const transcriptionPanel = document.getElementById('transcription-panel');
    const metadataPanel = document.getElementById('audio-metadata');

    if (!audioStream) {
        // Start recording
        try {
            audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            recordedChunks = [];
            mediaRecorder = new MediaRecorder(audioStream);
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = async () => {
                const blob = new Blob(recordedChunks, { type: 'audio/webm' });
                const url = URL.createObjectURL(blob);
                audioElement.src = url;
                audioElement.style.display = 'block';
                preview.querySelector('p').style.display = 'none';
                uploadBtn.style.display = 'block';
                
                // Get metadata
                const location = await getLocation();
                captureMetadata.audio = {
                    timestamp: new Date().toISOString(),
                    location: location,
                    size: blob.size,
                    transcription: transcriptionText,
                    type: 'audio/webm'
                };
                
                displayMetadata('audio', captureMetadata.audio);
                metadataPanel.style.display = 'block';
            };
            
            mediaRecorder.start();
            
            // Start speech recognition
            transcriptionText = '';
            if (hasSpeechRecognition && !recognition) {
                initSpeechRecognition();
            }
            if (recognition) {
                recognition.start();
                transcriptionPanel.style.display = 'block';
                document.getElementById('transcription-text').textContent = 'Listening...';
            }
            
            btn.textContent = '■ Stop Recording';
            btn.classList.add('recording');
            
        } catch (error) {
            alert('Error accessing microphone: ' + error.message);
            console.error(error);
        }
    } else {
        // Stop recording
        mediaRecorder.stop();
        audioStream.getTracks().forEach(track => track.stop());
        audioStream = null;
        
        if (recognition) {
            recognition.stop();
        }
        
        btn.textContent = '● Start Audio Recording';
        btn.classList.remove('recording');
    }
}

// Capture Photo
async function capturePhoto() {
    const preview = document.getElementById('photo-preview');
    const canvas = document.getElementById('photo-canvas');
    const uploadBtn = document.getElementById('photo-upload-btn');
    const metadataPanel = document.getElementById('photo-metadata');
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        const video = document.createElement('video');
        video.srcObject = stream;
        video.play();
        
        video.onloadedmetadata = async () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            
            stream.getTracks().forEach(track => track.stop());
            
            canvas.style.display = 'block';
            preview.querySelector('p').style.display = 'none';
            uploadBtn.style.display = 'block';
            
            // Get metadata
            const location = await getLocation();
            captureMetadata.photo = {
                timestamp: new Date().toISOString(),
                location: location,
                width: canvas.width,
                height: canvas.height,
                type: 'image/png'
            };
            
            displayMetadata('photo', captureMetadata.photo);
            metadataPanel.style.display = 'block';
        };
    } catch (error) {
        alert('Error accessing camera: ' + error.message);
        console.error(error);
    }
}

// Display Metadata
function displayMetadata(type, metadata) {
    const content = document.getElementById(`${type}-meta-content`);
    let html = `
        <p>🕒 Timestamp: ${metadata.timestamp}</p>
    `;
    
    if (metadata.location && !metadata.location.error) {
        html += `
            <p>📍 Location: ${metadata.location.latitude.toFixed(6)}, ${metadata.location.longitude.toFixed(6)}</p>
            <p>🎯 Accuracy: ±${metadata.location.accuracy.toFixed(1)}m</p>
        `;
    }
    
    if (metadata.size) {
        html += `<p>💾 Size: ${(metadata.size / 1024 / 1024).toFixed(2)} MB</p>`;
    }
    
    if (metadata.transcription) {
        html += `<p>🔤 Transcription: ${metadata.transcription.length} chars</p>`;
    }
    
    content.innerHTML = html;
}

// Upload Functions
async function uploadVideo() {
    await uploadMedia('video', recordedChunks, captureMetadata.video);
}

async function uploadAudio() {
    await uploadMedia('audio', recordedChunks, captureMetadata.audio);
}

async function uploadPhoto() {
    const canvas = document.getElementById('photo-canvas');
    canvas.toBlob(async (blob) => {
        await uploadMedia('photo', [blob], captureMetadata.photo);
    });
}

async function uploadMedia(type, chunks, metadata) {
    try {
        const blob = chunks.length > 1 ? new Blob(chunks) : chunks[0];
        const formData = new FormData();
        formData.append('file', blob, `${type}_${Date.now()}.${type === 'photo' ? 'png' : 'webm'}`);
        formData.append('metadata', JSON.stringify(metadata));
        formData.append('type', type);
        
        const response = await fetch('/api/vault/upload', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            alert(`✅ ${type.charAt(0).toUpperCase() + type.slice(1)} uploaded successfully!\nFile ID: ${result.file_id || 'N/A'}`);
        } else {
            const error = await response.json();
            alert(`❌ Upload failed: ${error.error || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`❌ Upload error: ${error.message}`);
        console.error(error);
    }
}

// Import Functions
async function handleVoicemailUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    alert(`📞 Voicemail import: ${file.name}\n\nTranscription will be processed server-side.\nImplement backend transcription API.`);
    // TODO: Upload to server and get transcription
}

async function handleTextUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    alert(`💬 Text message import: ${file.name}\n\nParsing and importing...`);
    // TODO: Parse and import text messages
}

async function handleEmailUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    alert(`📧 Email import: ${file.name}\n\nParsing email with attachments...`);
    // TODO: Parse and import emails
}

// Export Function
function exportEvidence() {
    const selectedFormat = document.querySelector('.format-btn.selected').dataset.format;
    const instructions = document.getElementById('export-instructions');
    
    alert(`💾 Generating ${selectedFormat.toUpperCase()} export package...\n\nThis will include:\n• All captured media\n• Transcriptions\n• Metadata & timestamps\n• Location data\n• SHA-256 certificates\n• Filing instructions`);
    
    instructions.style.display = 'block';
    
    // TODO: Generate actual export package
    setTimeout(() => {
        const link = document.createElement('a');
        link.href = '#';
        link.download = `semptify_evidence_${Date.now()}.${selectedFormat}`;
        // link.click();
    }, 500);
}

// Format button handling
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.format-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.format-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
        });
    });
    
    // Drag and drop handlers
    ['voicemail-drop', 'text-drop', 'email-drop'].forEach(id => {
        const zone = document.getElementById(id);
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        });
        zone.addEventListener('dragleave', () => {
            zone.classList.remove('dragover');
        });
        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
            const inputId = id.replace('-drop', '-input');
            const input = document.getElementById(inputId);
            input.files = e.dataTransfer.files;
            input.dispatchEvent(new Event('change'));
        });
    });
});
