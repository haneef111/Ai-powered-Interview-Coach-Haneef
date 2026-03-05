const API_URL = 'http://localhost:5000/api';

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');
    const submitBtn = document.getElementById('submit-btn');
    
    // Validation
    if (!email || !password) {
        errorMessage.textContent = 'Please fill in all fields';
        return;
    }
    
    errorMessage.textContent = '';
    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging in...';
    
    try {
        const response = await fetch(API_URL + '/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            localStorage.setItem('token', result.token);
            localStorage.setItem('user', JSON.stringify(result.user));
            errorMessage.style.color = 'green';
            errorMessage.textContent = 'Login successful! Redirecting...';
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        } else {
            errorMessage.style.color = '#e74c3c';
            errorMessage.textContent = result.error || 'Login failed';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Login';
        }
    } catch (error) {
        errorMessage.style.color = '#e74c3c';
        errorMessage.textContent = 'Server error. Please check if the backend is running.';
        console.error('Login error:', error);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Login';
    }
});
