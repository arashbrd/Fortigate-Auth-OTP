function updateIcon(step, status) {
    let icon = document.getElementById(`icon${step}`);
    
    // Remove existing classes
    icon.classList.remove('waiting', 'success', 'fail', 'bounce');

    if (status === 'success') {
        icon.textContent = '✅';  // Green tick for success
        icon.classList.add('success', 'bounce');  // Add success and bounce animation
    } else {
        icon.textContent = '❌';  // Red cross for failure
        icon.classList.add('fail', 'bounce');  // Add fail and bounce animation
    }
}

document.getElementById('start-process').addEventListener('click', function() {
    // Reset all icons to waiting
    for (let i = 1; i <= 3; i++) {
        let icon = document.getElementById(`icon${i}`);
        icon.textContent = '⏳';  // Reset to waiting icon
        icon.className = 'icon waiting';  // Reset class to waiting color
    }

    // Clear any previous error message
    document.getElementById('error-message').textContent = '';

    // Send AJAX request to run all steps
    fetch('/steps/run/')
        .then(response => response.json())
        .then(data => {
            // Update icons step by step
            if (data.step >= 1) updateIcon(1, data.status === 'fail' && data.step === 1 ? 'fail' : 'success');
            if (data.step >= 2) updateIcon(2, data.status === 'fail' && data.step === 2 ? 'fail' : 'success');
            if (data.step >= 3) updateIcon(3, data.status === 'fail' && data.step === 3 ? 'fail' : 'success');

            // If there's an error, display the message below the button
            if (data.status === 'fail') {
                document.getElementById('error-message').textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            // Handle network errors or other unexpected issues
            document.getElementById('error-message').textContent = 'An unexpected error occurred.';
            console.error('Error:', error);
        });
});