const API_URL = 'http://localhost:5000/api';

// Check authentication
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = 'login.html';
}

const user = JSON.parse(localStorage.getItem('user'));
document.getElementById('user-name').textContent = user.name;

// Logout
document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
});

// Load interview history
async function loadInterviews() {
    try {
        const response = await fetch(API_URL + '/interview/history', {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        });
        
        const data = await response.json();
        
        if (response.ok && data.interviews && data.interviews.length > 0) {
            displayInterviews(data.interviews);
        } else {
            document.getElementById('interview-list').innerHTML = '<p>No interviews yet. Start your first mock interview!</p>';
        }
    } catch (error) {
        console.error('Error loading interviews:', error);
        document.getElementById('interview-list').innerHTML = '<p>Error loading interviews. Please try again.</p>';
    }
}

function displayInterviews(interviews) {
    const interviewList = document.getElementById('interview-list');
    interviewList.innerHTML = '';
    
    // Group by interview (in case there are duplicates)
    const uniqueInterviews = {};
    interviews.forEach(interview => {
        uniqueInterviews[interview._id] = interview;
    });
    
    const interviewArray = Object.values(uniqueInterviews);
    
    if (interviewArray.length === 0) {
        interviewList.innerHTML = '<p>No interviews yet. Start your first mock interview!</p>';
        return;
    }
    
    interviewArray.forEach(interview => {
        const card = document.createElement('div');
        card.className = 'interview-card';
        
        const date = new Date(interview.created_at).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const status = interview.status || 'pending';
        const score = interview.overall_score || interview.feedback?.overall_score || 'N/A';
        const questionsCount = interview.questions?.length || 0;
        const answeredCount = interview.answers?.length || 0;
        
        // Determine status badge color
        let statusClass = 'status-pending';
        if (status === 'completed') statusClass = 'status-completed';
        else if (status === 'processing') statusClass = 'status-processing';
        
        card.innerHTML = `
            <div class="interview-card-header">
                <h4>Interview Session</h4>
                <span class="status-badge ${statusClass}">${status}</span>
            </div>
            <div class="interview-card-body">
                <p><strong>Date:</strong> ${date}</p>
                <p><strong>Questions:</strong> ${answeredCount} of ${questionsCount} answered</p>
                <p><strong>Overall Score:</strong> ${score !== 'N/A' ? score + '/100' : 'Not yet analyzed'}</p>
                ${interview.job_description ? '<p><strong>Type:</strong> Personalized Interview</p>' : '<p><strong>Type:</strong> Standard Interview</p>'}
            </div>
            <div class="interview-card-footer">
                ${status === 'completed' || answeredCount > 0 ? 
                    `<button class="btn-primary" onclick="viewFeedback('${interview._id}')">View Feedback</button>` :
                    `<button class="btn-secondary" disabled>No feedback yet</button>`
                }
            </div>
        `;
        
        interviewList.appendChild(card);
    });
    
    // Add summary statistics
    const completedCount = interviewArray.filter(i => i.status === 'completed').length;
    const avgScore = interviewArray
        .filter(i => i.overall_score)
        .reduce((sum, i) => sum + i.overall_score, 0) / completedCount || 0;
    
    if (completedCount > 0) {
        const summaryCard = document.createElement('div');
        summaryCard.className = 'summary-card';
        summaryCard.innerHTML = `
            <h3>📊 Your Progress</h3>
            <p><strong>Total Interviews:</strong> ${interviewArray.length}</p>
            <p><strong>Completed:</strong> ${completedCount}</p>
            <p><strong>Average Score:</strong> ${avgScore.toFixed(1)}/100</p>
        `;
        interviewList.insertBefore(summaryCard, interviewList.firstChild);
    }
}

function viewFeedback(interviewId) {
    localStorage.setItem('view_interview_id', interviewId);
    window.location.href = 'feedback.html';
}

loadInterviews();
