// Drag & drop функциональность
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    for (let file of files) {
        if (file.name === 'drones.csv' || file.name === 'orders.csv') {
            uploadFile(file);
        }
    }
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('csv', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        showStatus(`✅ ${file.name} uploaded successfully`, 'success');
    })
    .catch(error => {
        showStatus(`❌ Error uploading ${file.name}`, 'error');
    });
}

function generatePlan() {
    showStatus('🔄 Generating plan...', 'info');
    
    fetch('/schedule', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        showStatus('✅ Plan generated successfully!', 'success');
    })
    .catch(error => {
        showStatus('❌ Error generating plan', 'error');
    });
}

function downloadResults() {
    window.open('/results', '_blank');
}

function showStatus(message, type) {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = type;
}

function handleFiles(files) {
    for (let file of files) {
        if (file.name === 'drone.csv' || file.name === 'order.csv') {
            uploadFile(file);
        } else {
            showStatus(`⚠️ Файл ${file.name} не поддерживается. Нужны drone.csv и order.csv`, 'warning');
        }
    }
}