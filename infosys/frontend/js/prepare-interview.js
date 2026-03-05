const API_URL = 'http://localhost:5000/api';

const token = localStorage.getItem('token');
if (!token) {
    window.location.href = 'login.html';
}

const user = JSON.parse(localStorage.getItem('user'));
document.getElementById('user-name').textContent = user.name;

document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
});

document.getElementById('prepare-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submit-btn');
    const statusMessage = document.getElementById('status-message');
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processing...';
    statusMessage.textContent = 'Analyzing documents and generating questions...';
    statusMessage.style.color = '#3498db';
    
    try {
        const formData = new FormData();
        const resumeFile = document.getElementById('resume').files[0];
        const jobDescription = document.getElementById('job-description').value;
        
        if (resumeFile) {
            formData.append('resume', resumeFile);
        }
        formData.append('job_description', jobDescription);
        
        const response = await fetch(API_URL + '/interview/upload-documents', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            statusMessage.style.color = 'green';
            statusMessage.textContent = 'Questions generated successfully!';
            
            // Store interview ID
            localStorage.setItem('current_interview_id', result.interview_id);
            localStorage.setItem('interview_questions', JSON.stringify(result.questions));
            
            // Display questions
            displayQuestions(result.questions);
            
            submitBtn.disabled = false;
            submitBtn.textContent = 'Generate Questions';
        } else {
            statusMessage.style.color = '#e74c3c';
            statusMessage.textContent = result.error || 'Failed to generate questions';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Generate Questions';
        }
    } catch (error) {
        statusMessage.style.color = '#e74c3c';
        statusMessage.textContent = 'Server error. Please try again.';
        console.error('Error:', error);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Generate Questions';
    }
});

function displayQuestions(questions) {
    const questionsPreview = document.getElementById('questions-preview');
    const questionsList = document.getElementById('questions-list');
    
    questionsList.innerHTML = '';
    questions.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-item';
        questionDiv.innerHTML = `<p><strong>Q${index + 1}:</strong> ${q.question}</p>`;
        questionsList.appendChild(questionDiv);
    });
    
    questionsPreview.style.display = 'block';
}

document.getElementById('start-interview-btn').addEventListener('click', () => {
    window.location.href = 'interview-new.html';
});
