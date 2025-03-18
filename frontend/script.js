document.getElementById("generateBtn").addEventListener("click", function() {
    let prompt = document.getElementById("promptInput").value;
    if (!prompt) {
        alert("Please enter a prompt!");
        return;
    }

    let loadingText = document.getElementById("loadingText");
    let generatedImage = document.getElementById("generatedImage");

    loadingText.style.display = "block";
    generatedImage.style.display = "none";

    // Replace the URL with your ngrok URL
    let ngrokUrl = "https://1f94-34-90-168-245.ngrok-free.app";  // Your ngrok URL

    fetch(`${ngrokUrl}/api/generate/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        loadingText.style.display = "none";
        if (data.image_url) {
            // Update the image URL with the full ngrok URL path
            generatedImage.src = `${ngrokUrl}${data.image_url}`;
            generatedImage.style.display = "block";
        } else {
            alert("Error generating image!");
        }
    })
    .catch(error => {
        loadingText.style.display = "none";
        alert("Error: " + error);
    });
});
