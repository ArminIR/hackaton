document.getElementById('start-button').addEventListener('click', function() {
    const language = document.getElementById('language').value;
    
    fetch('/recognize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'language=' + encodeURIComponent(language)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('transcript').textContent = data.words;
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while recognizing speech.');
    });
});
