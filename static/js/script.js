document.addEventListener('DOMContentLoaded', function() {
    // Handle form submission
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleFormSubmit);
    }

    // Handle response generation
    const generateResponsesBtn = document.getElementById('generateResponsesBtn');
    if (generateResponsesBtn) {
        generateResponsesBtn.addEventListener('click', generateResponseSuggestions);
    }
});

async function handleFormSubmit(e) {
    e.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    const analysisType = document.getElementById('analysisType');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const errorAlert = document.getElementById('errorAlert');

    // Show loading state
    analyzeBtn.disabled = true;
    loading.style.display = 'block';
    errorAlert.style.display = 'none';

    formData.append('file', fileInput.files[0]);
    formData.append('analysis_type', analysisType.value);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Redirect to results page
            window.location.href = '/results';
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        errorAlert.textContent = error.message;
        errorAlert.style.display = 'block';
    } finally {
        analyzeBtn.disabled = false;
        loading.style.display = 'none';
    }
}

async function generateResponseSuggestions() {
    const btn = document.getElementById('generateResponsesBtn');
    const container = document.getElementById('responseSuggestions');

    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
    container.innerHTML = '<div class="text-center"><div class="spinner-border text-warning"></div><p class="mt-2">Generating response suggestions...</p></div>';

    try {
        // Get negative reviews from the page
        const negativeReviews = [];
        document.querySelectorAll('.border-danger').forEach(element => {
            const reviewText = element.querySelector('p').textContent;
            negativeReviews.push(reviewText);
        });

        const response = await fetch('/generate-responses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ negative_reviews: negativeReviews })
        });

        const data = await response.json();

        if (response.ok) {
            displayResponseSuggestions(data.suggested_responses);
        } else {
            throw new Error(data.error || 'Failed to generate responses');
        }
    } catch (error) {
        container.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-robot me-2"></i>Generate Response Suggestions';
    }
}

function displayResponseSuggestions(suggestions) {
    const container = document.getElementById('responseSuggestions');
    let html = '';

    suggestions.forEach((suggestion, index) => {
        html += `
            <div class="card mb-3">
                <div class="card-body">
                    <h6>Review #${index + 1}:</h6>
                    <p class="text-muted">"${suggestion.original_review}"</p>
                    <div class="bg-light p-3 rounded">
                        <strong>Suggested Response:</strong>
                        <p class="mb-0">${suggestion.suggested_response}</p>
                    </div>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}