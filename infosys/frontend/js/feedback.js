const API_URL = 'http://localhost:5000/api';

const token = localStorage.getItem('token');
const urlParams = new URLSearchParams(window.location.search);
const interviewId = urlParams.get('interview_id') || localStorage.getItem('interview_id');

if (!token || !interviewId) {
    window.location.href = 'dashboard.html';
}

async function loadFeedback() {
    try {
        const response = await fetch(API_URL + '/feedback/' + interviewId, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        const feedback = await response.json();
        
        if (response.ok) {
            if (feedback.interview_type === 'multi_question') {
                displayMultiQuestionFeedback(feedback);
            } else {
                displaySingleVideoFeedback(feedback);
            }
        } else {
            document.getElementById('overall-score').textContent = 'Error';
            document.getElementById('speech-feedback').innerHTML = '<p>Error loading feedback</p>';
        }
    } catch (error) {
        console.error('Error loading feedback:', error);
        document.getElementById('overall-score').textContent = 'Error';
    }
}

function displayMultiQuestionFeedback(feedback) {
    // Overall score
    document.getElementById('overall-score').textContent = feedback.overall_score || '--';
    
    // Summary statistics
    const speechFeedback = document.getElementById('speech-feedback');
    speechFeedback.innerHTML = `
        <p><strong>Average Speech Score:</strong> ${feedback.average_scores.speech}/100</p>
        <p><strong>Total Questions:</strong> ${feedback.total_questions}</p>
        <p><strong>Answered:</strong> ${feedback.answered_questions}</p>
    `;
    
    const facialFeedback = document.getElementById('facial-feedback');
    facialFeedback.innerHTML = `
        <p><strong>Average Confidence Score:</strong> ${feedback.average_scores.facial}/100</p>
        ${feedback.best_answer ? `<p><strong>Best Answer:</strong> Question ${feedback.best_answer.question_id} (${feedback.best_answer.score}/100)</p>` : ''}
    `;
    
    const contentFeedback = document.getElementById('content-feedback');
    contentFeedback.innerHTML = `
        <p><strong>Average Content Score:</strong> ${feedback.average_scores.content}/100</p>
        ${feedback.worst_answer ? `<p><strong>Needs Improvement:</strong> Question ${feedback.worst_answer.question_id} (${feedback.worst_answer.score}/100)</p>` : ''}
    `;
    
    // Add per-question breakdown
    if (feedback.answers && feedback.answers.length > 0) {
        addQuestionBreakdown(feedback.answers);
    }
    
    // Add recommendations
    if (feedback.recommendations) {
        addRecommendations(feedback.recommendations);
    }
}

function displaySingleVideoFeedback(feedback) {
    // Overall score
    document.getElementById('overall-score').textContent = feedback.overall_score || '--';
    
    // Speech analysis
    const speechFeedback = feedback.speech_analysis || {};
    document.getElementById('speech-feedback').innerHTML = `
        <p><strong>Speech Rate:</strong> ${speechFeedback.speech_rate || 0} words/min</p>
        <p><strong>Filler Words:</strong> ${speechFeedback.filler_count || 0}</p>
        <p><strong>Clarity Score:</strong> ${speechFeedback.clarity_score || 0}/100</p>
        <div class="feedback-suggestions">
            ${(speechFeedback.feedback || []).map(f => `<p>• ${f}</p>`).join('')}
        </div>
    `;
    
    // Facial analysis
    const facialFeedback = feedback.facial_analysis || {};
    document.getElementById('facial-feedback').innerHTML = `
        <p><strong>Eye Contact:</strong> ${facialFeedback.eye_contact_percentage || 0}%</p>
        <p><strong>Smile Rate:</strong> ${facialFeedback.smile_percentage || 0}%</p>
        <p><strong>Confidence Score:</strong> ${facialFeedback.confidence_score || 0}/100</p>
        <div class="feedback-suggestions">
            ${(facialFeedback.feedback || []).map(f => `<p>• ${f}</p>`).join('')}
        </div>
    `;
    
    // Content analysis
    const contentFeedback = feedback.content_analysis || {};
    document.getElementById('content-feedback').innerHTML = `
        <p><strong>Word Count:</strong> ${contentFeedback.word_count || 0}</p>
        <p><strong>Structure Score:</strong> ${contentFeedback.structure_score || 0}/10</p>
        <p><strong>Relevance Score:</strong> ${contentFeedback.relevance_score || 0}/100</p>
        <div class="feedback-suggestions">
            ${(contentFeedback.feedback || []).map(f => `<p>• ${f}</p>`).join('')}
        </div>
    `;
}

function addQuestionBreakdown(answers) {
    const container = document.querySelector('.feedback-sections');
    
    const breakdownSection = document.createElement('div');
    breakdownSection.className = 'question-breakdown-section';
    breakdownSection.innerHTML = '<h2>Question-by-Question Analysis</h2>';
    
    answers.forEach((answer, index) => {
        if (!answer.analyzed || !answer.analysis) return;
        
        const analysis = answer.analysis;
        const questionCard = document.createElement('div');
        questionCard.className = 'question-analysis-card';
        
        questionCard.innerHTML = `
            <h3>Question ${answer.question_id}</h3>
            <div class="question-score">Score: ${analysis.question_score}/100</div>
            <div class="question-details">
                <div class="detail-item">
                    <strong>Speech:</strong> ${analysis.speech_analysis.clarity_score}/100
                    <small>${analysis.speech_analysis.speech_rate} wpm, ${analysis.speech_analysis.filler_count} fillers</small>
                </div>
                <div class="detail-item">
                    <strong>Confidence:</strong> ${analysis.facial_analysis.confidence_score}/100
                    <small>Eye contact: ${analysis.facial_analysis.eye_contact_percentage}%</small>
                </div>
                <div class="detail-item">
                    <strong>Content:</strong> ${analysis.content_analysis.relevance_score}/100
                    <small>${analysis.content_analysis.word_count} words</small>
                </div>
            </div>
            <div class="transcript-preview">
                <strong>Transcript:</strong>
                <p>${analysis.speech_analysis.transcript.substring(0, 200)}${analysis.speech_analysis.transcript.length > 200 ? '...' : ''}</p>
            </div>
        `;
        
        breakdownSection.appendChild(questionCard);
    });
    
    container.appendChild(breakdownSection);
}

function addRecommendations(recommendations) {
    const container = document.querySelector('.feedback-sections');
    
    const recSection = document.createElement('div');
    recSection.className = 'recommendations-section';
    recSection.innerHTML = '<h2>📋 Recommendations for Improvement</h2>';
    
    const recList = document.createElement('ul');
    recList.className = 'recommendations-list';
    
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recList.appendChild(li);
    });
    
    recSection.appendChild(recList);
    container.appendChild(recSection);
}

loadFeedback();
