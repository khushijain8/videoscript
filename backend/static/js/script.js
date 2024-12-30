window.onload = function() {
    if (!sessionStorage.getItem('loadedOnce')) { 
        var messageBox = document.getElementById('message-box');
        if (messageBox) {
            messageBox.style.display = 'none'; 
        }
        document.getElementById('prompt').value = '';
        document.getElementById('external-link').value = '';
        localStorage.removeItem('prompt');
        localStorage.removeItem('external-link');
        sessionStorage.setItem('loadedOnce', 'true');
    } else {
        const savedPrompt = localStorage.getItem('prompt');
        if (savedPrompt) {
            document.getElementById('prompt').value = savedPrompt;
        }

        const savedLink = localStorage.getItem('external-link');
        if (savedLink) {
            document.getElementById('external-link').value = savedLink;
        }
    }
    document.getElementById('prompt').addEventListener('input', function() {
        localStorage.setItem('prompt', this.value);
    });

    document.getElementById('external-link').addEventListener('input', function() {
        localStorage.setItem('external-link', this.value);
    });
};





document.getElementById('prompt').addEventListener('input', function() {
    const promptValue = document.getElementById('prompt').value;
    localStorage.setItem('prompt', promptValue);
});

document.getElementById('external-link').addEventListener('input', function() {
    const linkValue = document.getElementById('external-link').value;
    localStorage.setItem('external-link', linkValue);
});


document.getElementById('file-upload').addEventListener('change', function () {
    const form = document.getElementById('upload-file');
    form.submit(); 
});


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function generateScript() {
    const prompt = document.getElementById('prompt').value;
    const externalLink = document.getElementById('external-link').value;
    if (!prompt) {
        alert('Please provide a prompt');
        return;
    }
    const csrfToken = getCookie('csrftoken');
    fetch('/generate-script/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // Include CSRF token for Django
        },
        body: JSON.stringify({ prompt, external_link: externalLink })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                // Display the generated script dynamically
                const outerDiv=document.getElementById('generated-script');
                const outputDiv = document.getElementById('script-output');
                outputDiv.innerHTML = `
                    <h3>Generated Script:</h3>
                    <pre>${data.script}</pre>
                `;
                outerDiv.classList.remove('hidden');
                const saveButton = document.getElementById('save-script');
                saveButton.classList.remove('hidden');
                saveButton.onclick = function() {
                    saveScriptToFile();
                };
                const downloadButton = document.getElementById('download-script');
                downloadButton.classList.remove('hidden');
                downloadButton.onclick = function() {
                    downloadPDF();
                };
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
}



function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const scriptContent = document.getElementById('script-output').innerText;
    const doc = new jsPDF();
    doc.text(scriptContent, 10, 10);  
    const prompt = document.getElementById('prompt').value;
    const promptWords = prompt.split(/\s+/).slice(0, 3).join(' ');
    const pdfFileName = promptWords ? promptWords + '.pdf' : 'generated-script.pdf';
    doc.save(pdfFileName);
}

function saveScriptToFile(){
    const prompt = document.getElementById('prompt').value;
    const externalLink = document.getElementById('external-link').value;
    const scriptContent = document.getElementById('script-output').innerText;
    const csrfToken = getCookie('csrftoken');
    fetch('/save_script/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, 
        },
        body: JSON.stringify({
            prompt : prompt,
            externalLink : externalLink,
            script:scriptContent,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Script saved successfully!');
        } else {
            alert('Failed to save the script.');
        }
    })
    .catch(error => {
        console.error('Error saving the script:', error);
        alert('An error occurred while saving the script.');
    });

}

function fetchAllScripts() {
    fetch('/get_all_scripts/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display scripts
                console.log(data.scripts);
                // You can update the UI with the list of scripts
            } else {
                alert('Failed to fetch scripts.');
            }
        })
        .catch(error => {
            console.error('Error fetching scripts:', error);
        });
}