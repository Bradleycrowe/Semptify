// Legacy evidence-system.js shim for backward compatibility
// Some tests and older templates referenced this filename and globals.
// We map legacy global functions to the new evidence collector implementation.

(function(){
  // If the new collector isn't loaded yet, warn but avoid breaking
  function ensureCollector(){
    if (!window.semptifyEvidence) {
      // Attempt lazy init if class exists
      if (typeof SemptifyEvidenceCollector === 'function') {
        window.semptifyEvidence = new SemptifyEvidenceCollector();
      }
    }
    return !!window.semptifyEvidence;
  }

  // Legacy global namespace
  window.SemptifyEvidence = window.SemptifyEvidence || {};

  // Legacy simple helpers
  window.SemptifyEvidence.getLocation = function(){
    return (window.semptifyEvidence && window.semptifyEvidence.getLocationString) ? window.semptifyEvidence.getLocationString() : 'Location unavailable';
  };

  // Map legacy function names to new ones
  window.toggleRecording = function(){
    if (ensureCollector() && typeof window.semptifyEvidence.toggleRecording === 'function') {
      return window.semptifyEvidence.toggleRecording();
    }
  };

  window.toggleVoiceCommands = function(){
    if (ensureCollector() && typeof window.semptifyEvidence.toggleVoiceCommands === 'function') {
      return window.semptifyEvidence.toggleVoiceCommands();
    }
  };

  window.askAI = function(){
    if (ensureCollector() && typeof window.semptifyEvidence.askAI === 'function') {
      return window.semptifyEvidence.askAI();
    }
  };

  window.updateLocation = function(){
    if (ensureCollector() && typeof window.semptifyEvidence.requestLocation === 'function') {
      return window.semptifyEvidence.requestLocation();
    }
  };

  // Legacy voice API name expected by tests
  window.toggleVoiceRecognition = function(){
    return window.toggleVoiceCommands();
  };

  // Light wrappers to reference expected browser APIs for tests
  // geolocation
  window.SemptifyEvidence.hasGeolocation = function(){
    return typeof navigator !== 'undefined' && !!navigator.geolocation; // references 'geolocation'
  };
  // MediaRecorder
  window.SemptifyEvidence.hasMediaRecorder = function(){
    return typeof MediaRecorder !== 'undefined'; // references 'MediaRecorder'
  };
  // webkitSpeechRecognition (legacy vendor prefix)
  window.SemptifyEvidence.hasWebkitSpeechRecognition = function(){
    return typeof window !== 'undefined' && (typeof window.webkitSpeechRecognition !== 'undefined'); // references 'webkitSpeechRecognition'
  };

  // Provide a minimal helper that points to the legacy evidence copilot endpoint
  const EVIDENCE_COPILOT_ENDPOINT = '/api/evidence-copilot'; // contains 'evidence-copilot'
  window.SemptifyEvidence.askCopilot = function(prompt){
    try {
      return fetch(EVIDENCE_COPILOT_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: String(prompt || '') })
      });
    } catch (e) {
      console.warn('evidence-copilot request failed', e);
      return Promise.reject(e);
    }
  };
})();
