// verify_api.js

const verifyEndpoint = process.env.VERIFY_ENDPOINT;
const apiKey = process.env.VERIFY_API_KEY;
const pollInterval = process.env.VERIFY_POLL_INTERVAL || 300000; // Default to 300s
const maxRetries = process.env.VERIFY_MAX_RETRIES || 5;

async function fetchManifest() {
    let retries = 0;

    while (retries < maxRetries) {
        try {
            const response = await fetch(verifyEndpoint, {
                method: 'GET',
                headers: {
                    'Authorization': apiKey ? `Bearer ${apiKey}` : undefined,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Error fetching manifest: ${response.statusText}`);
            }

            const manifest = await response.json();
            return manifest;
        } catch (error) {
            retries++;
            if (retries >= maxRetries) {
                showToast(`Failed to fetch manifest after ${maxRetries} attempts: ${error.message}`, 'error');
                throw error;
            }
            await new Promise(resolve => setTimeout(resolve, Math.pow(2, retries) * 1000)); // Exponential backoff
        }
    }
}

function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerText = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

document.getElementById('reverifyButton').addEventListener('click', async () => {
    try {
        const manifest = await fetchManifest();
        // Process the manifest and update the UI accordingly
        showToast('Manifest fetched successfully!', 'success');
    } catch (error) {
        console.error('Error during verification:', error);
    }
});

// Polling function to automatically fetch the manifest at intervals
setInterval(async () => {
    try {
        await fetchManifest();
    } catch (error) {
        console.error('Error during scheduled verification:', error);
    }
}, pollInterval);