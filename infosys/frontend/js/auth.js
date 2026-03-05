const API_URL = 'http://localhost:5000/api';

let isLoginMode = true;

document.getElementById('toggle-link').addEventListener('click', (e) => {
    e.preventDefault();
    isLoginMode = !isLoginMode;
    
    const formTitle = document.getElementById('form-title');
    const submitBtn = document.getElementById('submit-btn');
    const toggleText = document.getElementById('toggle-text');
    const toggleLink = document.getElementById('toggle-link');
    const nameField = document.getElementById('name-field');
    const nameInput = document.getElementById('name');
    const profileFields = document.getElementById('profile-fields');
    
    if (isLoginMode) {
        formTitle.textContent = 'Login';
        submitBtn.textContent = 'Login';
        toggleText.textContent = "Don't have an account?";
        toggleLink.textContent = 'Register';
        nameField.style.display = 'none';
        profileFields.style.display = 'none';
        nameInput.removeAttribute('required');
    } else {
        formTitle.textContent = 'Register';
        submitBtn.textContent = 'Register';
        toggleText.textContent = 'Already have an account?';
        toggleLink.textContent = 'Login';
        nameField.style.display = 'block';
        profileFields.style.display = 'block';
        nameInput.setAttribute('required', 'required');
    }
    
    // Clear error message and form
    document.getElementById('error-message').textContent = '';
    document.getElementById('auth-form').reset();
});

document.getElementById('auth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');
    const submitBtn = document.getElementById('submit-btn');
    
    // Validation
    if (!email || !password) {
        errorMessage.textContent = 'Please fill in all required fields';
        return;
    }
    
    errorMessage.textContent = '';
    submitBtn.disabled = true;
    submitBtn.textContent = isLoginMode ? 'Logging in...' : 'Registering...';
    
    try {
        const endpoint = isLoginMode ? '/auth/login' : '/auth/register';
        const data = { email, password };
        
        if (!isLoginMode) {
            const name = document.getElementById('name').value.trim();
            if (!name) {
                errorMessage.textContent = 'Please enter your name';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Register';
                return;
            }
            data.name = name;
            data.job_role = document.getElementById('job-role').value.trim();
            data.industry = document.getElementById('industry').value.trim();
        }
        
        const response = await fetch(API_URL + endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            localStorage.setItem('token', result.token);
            localStorage.setItem('user', JSON.stringify(result.user));
            errorMessage.style.color = 'green';
            errorMessage.textContent = isLoginMode ? 'Login successful! Redirecting...' : 'Registration successful! Redirecting...';
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        } else {
            errorMessage.style.color = '#e74c3c';
            errorMessage.textContent = result.error || 'Authentication failed';
            submitBtn.disabled = false;
            submitBtn.textContent = isLoginMode ? 'Login' : 'Register';
        }
    } catch (error) {
        errorMessage.style.color = '#e74c3c';
        errorMessage.textContent = 'Server error. Please check if the backend is running.';
        console.error('Auth error:', error);
        submitBtn.disabled = false;
        submitBtn.textContent = isLoginMode ? 'Login' : 'Register';
    }
});
