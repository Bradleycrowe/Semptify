// Service Animal Form AI Helper JavaScript
(function() {
  'use strict';
  
  const aiPromptEl = document.getElementById('ai-prompt');
  const aiGenerateBtn = document.getElementById('ai-generate-btn');
  const aiInsertBtn = document.getElementById('ai-insert-btn');
  const aiResponseDiv = document.getElementById('ai-response');
  const aiOutputEl = document.getElementById('ai-output');
  const needSummaryEl = document.getElementById('need_summary');
  const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
  
  if (!aiPromptEl || !aiGenerateBtn || !aiInsertBtn || !aiResponseDiv || !aiOutputEl || !needSummaryEl || !csrfTokenMeta) {
    // Elements not found, AI helper not enabled
    return;
  }

  const csrfToken = csrfTokenMeta.getAttribute('content');
  let generatedText = '';

  aiGenerateBtn.addEventListener('click', async function() {
    const userInput = aiPromptEl.value.trim();
    if(!userInput){ 
      alert('Please describe your situation first.');
      return; 
    }

    aiGenerateBtn.disabled = true;
    aiGenerateBtn.textContent = 'Generating...';
    aiOutputEl.textContent = 'Thinking...';
    aiResponseDiv.classList.remove('hidden');
    aiInsertBtn.classList.add('hidden');

    const prompt = 'You are helping a tenant write a professional explanation for why they need a service or support animal as a reasonable accommodation under fair housing laws. The tenant says: "' + userInput + '". Write a clear, professional, and respectful 2-3 sentence explanation that could be included in their formal request letter. Focus on the necessity of the accommodation without excessive medical details.';

    try {
      const r = await fetch('/api/copilot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': csrfToken },
        body: JSON.stringify({ prompt: prompt })
      });
      const data = await r.json();
      if(!r.ok){
        aiOutputEl.textContent = 'Error (' + r.status + '): ' + (data && data.error ? data.error : 'Unknown error');
        generatedText = '';
      } else {
        generatedText = data.output || '';
        aiOutputEl.textContent = generatedText;
        aiInsertBtn.classList.remove('hidden');
      }
    } catch(err){
      aiOutputEl.textContent = 'Network error: ' + err;
      generatedText = '';
    } finally {
      aiGenerateBtn.disabled = false;
      aiGenerateBtn.textContent = 'Generate Explanation with AI';
    }
  });

  aiInsertBtn.addEventListener('click', function() {
    if(generatedText){
      needSummaryEl.value = generatedText;
      alert('AI-generated text inserted into the form!');
    }
  });
})();
