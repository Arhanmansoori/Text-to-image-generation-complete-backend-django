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

    fetch("http://127.0.0.1:8000/api/generate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        loadingText.style.display = "none";
        if (data.image_url) {
            generatedImage.src = `http://127.0.0.1:8000${data.image_url}`;
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
