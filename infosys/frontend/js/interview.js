const API_URL = 'http://localhost:5000/api';

const token = localStorage.getItem('token');
if (!token) {
    window.location.href = 'login.html';
}

let mediaRecorder;
let recordedChunks = [];
let stream;
let questions = [];
let currentQuestionIndex = 0;

// Get video stream
async function initCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: true, 
            audio: true 
        });
        document.getElementById('video-preview').srcObject = stream;
    } catch (error) {
        alert('Camera/microphone access denied. Please enable permissions.');
        console.error('Media error:', error);
    }
}

// Load questions
async function loadQuestions() {
    try {
        const response = await fetch(API_URL + '/interview/questions', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        const data = await response.json();
        questions = data.questions;
        
        document.getElementById('total-questions').textContent = questions.length;
        displayQuestion();
    } catch (error) {
        console.error('Error loading questions:', error);
    }
}

function displayQuestion() {
    if (currentQuestionIndex < questions.length) {
        document.getElementById('question-number').textContent = currentQuestionIndex + 1;
        document.getElementById('current-question').textContent = questions[currentQuestionIndex];
    }
}

// Recording controls
document.getElementById('start-btn').addEventListener('click', () => {
    recordedChunks = [];
    
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    
    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            recordedChunks.push(event.data);
        }
    };
    
    mediaRecorder.start();
    
    document.getElementById('start-btn').style.display = 'none';
    document.getElementById('stop-btn').style.display = 'inline-block';
    document.getElementById('recording-indicator').style.display = 'block';
});

document.getElementById('stop-btn').addEventListener('click', () => {
    mediaRecorder.stop();
    
    document.getElementById('stop-btn').style.display = 'none';
    document.getElementById('recording-indicator').style.display = 'none';
    
    if (currentQuestionIndex < questions.length - 1) {
        document.getElementById('next-btn').style.display = 'inline-block';
    } else {
        document.getElementById('submit-btn').style.display = 'inline-block';
    }
});

document.getElementById('next-btn').addEventListener('click', () => {
    currentQuestionIndex++;
    displayQuestion();
    
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('start-btn').style.display = 'inline-block';
});

document.getElementById('submit-btn').addEventListener('click', async () => {
    const statusMessage = document.getElementById('status-message');
    statusMessage.textContent = 'Uploading interview...';
    
    const blob = new Blob(recordedChunks, { type: 'video/webm' });
    const formData = new FormData();
    formData.append('video', blob, 'interview.webm');
    
    try {
        const response = await fetch(API_URL + '/interview/submit', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + token },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('interview_id', data.interview_id);
            statusMessage.textContent = 'Interview submitted! Redirecting...';
            setTimeout(() => {
                window.location.href = 'feedback.html';
            }, 2000);
        } else {
            statusMessage.textContent = 'Upload failed. Please try again.';
        }
    } catch (error) {
        statusMessage.textContent = 'Server error. Please try again.';
        console.error('Upload error:', error);
    }
});

// Initialize
initCamera();
loadQuestions();
