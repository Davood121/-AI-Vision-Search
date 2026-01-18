document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeBtn = document.getElementById('removeBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsSection = document.getElementById('resultsSection');
    const analysisText = document.getElementById('analysisText');
    const reportContainer = document.getElementById('reportContainer');
    const reportContent = document.getElementById('reportContent');
    const resultsList = document.getElementById('resultsList');

    let currentFile = null;

    // Handle File Selection
    uploadZone.addEventListener('click', (e) => {
        if (e.target !== removeBtn && e.target.parentElement !== removeBtn) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag & Drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // Remove Image
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        currentFile = null;
        fileInput.value = '';
        previewContainer.style.display = 'none';
        document.querySelector('.upload-content').style.display = 'block';
        analyzeBtn.disabled = true;
        resultsSection.style.display = 'none';
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file (JPG, PNG, WEBP).');
            return;
        }

        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            document.querySelector('.upload-content').style.display = 'none';
            previewContainer.style.display = 'flex';
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // Analyze & Search
    analyzeBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        // Reset UI
        resultsSection.style.display = 'none';
        analyzeBtn.classList.add('loading');
        analyzeBtn.disabled = true;

        const formData = new FormData();
        formData.append('image', currentFile);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                alert('Error: ' + data.error);
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        } finally {
            analyzeBtn.classList.remove('loading');
            analyzeBtn.disabled = false;
        }
    });

    function displayResults(data) {
        resultsSection.style.display = 'block';

        // Typewriter effect for analysis
        analysisText.textContent = '';
        reportContainer.style.display = 'none'; // Hide initially

        typeWriter(data.description, analysisText, 0, () => {
            // After analysis typewrite finishes, show report
            if (data.report) {
                reportContainer.style.display = 'block';
                reportContent.innerHTML = marked.parse(data.report);
            }
        });

        // Search Results
        resultsList.innerHTML = '';
        if (data.results && data.results.length > 0) {
            data.results.forEach(result => {
                const card = document.createElement('div');
                card.className = 'result-card';
                card.innerHTML = `
                    <h3><a href="${result.href}" target="_blank">${result.title}</a></h3>
                    <p>${result.body}</p>
                `;
                resultsList.appendChild(card);
            });
        } else {
            resultsList.innerHTML = '<p class="no-results">No web results found.</p>';
        }

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function typeWriter(text, element, index, callback) {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            setTimeout(() => typeWriter(text, element, index + 1, callback), 20);
        } else if (callback) {
            callback();
        }
    }
});
