document.getElementById('generateForm').addEventListener('submit', function (e) {
    e.preventDefault();  // Prevent the form from refreshing the page

    const prompt = document.getElementById('prompt').value;
    if (!prompt) {
        alert("Please enter a prompt.");
        return;
    }

    // Clear previous image
    document.getElementById('imageContainer').innerHTML = '';

    // Show loading text
    const loadingMessage = document.createElement('p');
    loadingMessage.innerText = 'Generating image... Please wait.';
    document.getElementById('imageContainer').appendChild(loadingMessage);

    // API request to generate image
    fetch('https://1f94-34-90-168-245.ngrok-free.app/api/generate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt: prompt
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Show error message if API call fails
            document.getElementById('imageContainer').innerHTML = `<p id="error-message">${data.error}</p>`;
        } else {
            // Create image element and set its source as the base64 data
            const img = new Image();
            img.id = "generatedImage";
            img.src = `data:image/png;base64,${data.image_data}`;

            // Clear loading message and append the image
            document.getElementById('imageContainer').innerHTML = '';
            document.getElementById('imageContainer').appendChild(img);
        }
    })
    .catch(error => {
        document.getElementById('imageContainer').innerHTML = `<p id="error-message">An error occurred. Please try again.</p>`;
        console.error('Error:', error);
    });
});
