const API_URL = 'http://localhost:5000/api';

document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const jobRole = document.getElementById('job-role').value.trim();
    const industry = document.getElementById('industry').value.trim();
    const errorMessage = document.getElementById('error-message');
    const submitBtn = document.getElementById('submit-btn');
    
    // Validation
    if (!name || !email || !password) {
        errorMessage.textContent = 'Please fill in all required fields';
        return;
    }
    
    if (password.length < 6) {
        errorMessage.textContent = 'Password must be at least 6 characters';
        return;
    }
    
    errorMessage.textContent = '';
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating account...';
    
    try {
        const response = await fetch(API_URL + '/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name,
                email,
                password,
                job_role: jobRole,
                industry: industry
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            localStorage.setItem('token', result.token);
            localStorage.setItem('user', JSON.stringify(result.user));
            errorMessage.style.color = 'green';
            errorMessage.textContent = 'Account created successfully! Redirecting...';
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        } else {
            errorMessage.style.color = '#e74c3c';
            errorMessage.textContent = result.error || 'Registration failed';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Sign Up';
        }
    } catch (error) {
        errorMessage.style.color = '#e74c3c';
        errorMessage.textContent = 'Server error. Please check if the backend is running.';
        console.error('Signup error:', error);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Sign Up';
    }
});
