const API_URL = 'http://localhost:5000/api';

const token = localStorage.getItem('token');
if (!token) {
    window.location.href = 'login.html';
}

const interviewId = localStorage.getItem('current_interview_id');
const questionsData = JSON.parse(localStorage.getItem('interview_questions') || '[]');

if (!interviewId || questionsData.length === 0) {
    alert('No interview session found. Please start from the dashboard.');
    window.location.href = 'dashboard.html';
}

let currentQuestionIndex = 0;
let mediaRecorder;
let recordedChunks = [];
let stream;
let timerInterval;
let recordingStartTime;
let answeredQuestions = new Set();

// Initialize camera
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

// Display current question
function displayQuestion() {
    const question = questionsData[currentQuestionIndex];
    const totalQuestions = questionsData.length;
    
    document.getElementById('question-number').textContent = `Question ${currentQuestionIndex + 1} of ${totalQuestions}`;
    document.getElementById('current-question').textContent = question.question;
    document.getElementById('question-type').textContent = `Type: ${question.type} | Category: ${question.category}`;
    document.getElementById('progress-text').textContent = `Question ${currentQuestionIndex + 1} of ${totalQuestions}`;
    
    // Update progress bar
    const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100;
    document.getElementById('progress-fill').style.width = progress + '%';
    
    // Update navigation buttons
    document.getElementById('prev-btn').style.display = currentQuestionIndex > 0 ? 'inline-block' : 'none';
    
    // Check if question already answered
    if (answeredQuestions.has(currentQuestionIndex)) {
        document.getElementById('status-message').textContent = '✓ This question has been answered';
        document.getElementById('status-message').style.color = 'green';
    } else {
        document.getElementById('status-message').textContent = '';
    }
}

// Timer functions
function startTimer() {
    recordingStartTime = Date.now();
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
        const seconds = (elapsed % 60).toString().padStart(2, '0');
        document.getElementById('timer').textContent = `${minutes}:${seconds}`;
    }, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
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
    startTimer();
    
    document.getElementById('start-btn').style.display = 'none';
    document.getElementById('stop-btn').style.display = 'inline-block';
    document.getElementById('recording-indicator').style.display = 'flex';
    document.getElementById('timer').style.display = 'block';
    document.getElementById('prev-btn').style.display = 'none';
    document.getElementById('status-message').textContent = 'Recording... Speak clearly and maintain eye contact.';
    document.getElementById('status-message').style.color = '#e74c3c';
});

document.getElementById('stop-btn').addEventListener('click', async () => {
    mediaRecorder.stop();
    stopTimer();
    
    document.getElementById('stop-btn').style.display = 'none';
    document.getElementById('recording-indicator').style.display = 'none';
    document.getElementById('timer').style.display = 'none';
    document.getElementById('status-message').textContent = 'Uploading answer...';
    document.getElementById('status-message').style.color = '#3498db';
    
    // Wait for recording to finalize
    await new Promise(resolve => {
        mediaRecorder.onstop = resolve;
    });
    
    // Upload answer
    await uploadAnswer();
});

async function uploadAnswer() {
    try {
        const blob = new Blob(recordedChunks, { type: 'video/webm' });
        const formData = new FormData();
        formData.append('video', blob, `answer_q${currentQuestionIndex + 1}.webm`);
        formData.append('question_id', questionsData[currentQuestionIndex].id);
        
        console.log('Uploading answer for question:', questionsData[currentQuestionIndex].id);
        console.log('Interview ID:', interviewId);
        
        const response = await fetch(API_URL + `/interview/${interviewId}/submit-answer`, {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            body: formData
        });
        
        const result = await response.json();
        console.log('Upload response:', result);
        
        if (response.ok) {
            answeredQuestions.add(currentQuestionIndex);
            document.getElementById('status-message').textContent = '✓ Answer uploaded successfully!';
            document.getElementById('status-message').style.color = 'green';
            
            // Show navigation buttons
            if (currentQuestionIndex < questionsData.length - 1) {
                document.getElementById('next-btn').style.display = 'inline-block';
            } else {
                document.getElementById('finish-btn').style.display = 'inline-block';
            }
            
            if (currentQuestionIndex > 0) {
                document.getElementById('prev-btn').style.display = 'inline-block';
            }
        } else {
            document.getElementById('status-message').textContent = 'Upload failed: ' + (result.error || 'Unknown error');
            document.getElementById('status-message').style.color = '#e74c3c';
            document.getElementById('start-btn').style.display = 'inline-block';
        }
    } catch (error) {
        console.error('Upload error:', error);
        document.getElementById('status-message').textContent = 'Upload failed. Please try again.';
        document.getElementById('status-message').style.color = '#e74c3c';
        document.getElementById('start-btn').style.display = 'inline-block';
    }
}

// Navigation
document.getElementById('prev-btn').addEventListener('click', () => {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
        resetControls();
    }
});

document.getElementById('next-btn').addEventListener('click', () => {
    if (currentQuestionIndex < questionsData.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
        resetControls();
    }
});

document.getElementById('finish-btn').addEventListener('click', async () => {
    const unanswered = questionsData.length - answeredQuestions.size;
    
    if (unanswered > 0) {
        const confirm = window.confirm(`You have ${unanswered} unanswered question(s). Are you sure you want to finish?`);
        if (!confirm) return;
    }
    
    document.getElementById('status-message').textContent = 'Processing interview... Please wait.';
    document.getElementById('status-message').style.color = '#3498db';
    document.getElementById('finish-btn').disabled = true;
    
    // Mark interview as ready for analysis
    try {
        const response = await fetch(API_URL + `/interview/${interviewId}/complete`, {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            localStorage.removeItem('current_interview_id');
            localStorage.removeItem('interview_questions');
            window.location.href = `feedback.html?interview_id=${interviewId}`;
        } else {
            // Even if complete endpoint fails, redirect to feedback
            window.location.href = `feedback.html?interview_id=${interviewId}`;
        }
    } catch (error) {
        console.error('Complete error:', error);
        // Redirect anyway
        window.location.href = `feedback.html?interview_id=${interviewId}`;
    }
});

function resetControls() {
    document.getElementById('start-btn').style.display = 'inline-block';
    document.getElementById('stop-btn').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('finish-btn').style.display = 'none';
    document.getElementById('recording-indicator').style.display = 'none';
    document.getElementById('timer').style.display = 'none';
    document.getElementById('timer').textContent = '00:00';
}

// Initialize
initCamera();
displayQuestion();
