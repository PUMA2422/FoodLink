const baseUrl = window.location.origin;

// Function to show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    
    // Set the message and the type of the toast (success/error)
    toastMessage.textContent = message;
    toast.className = 'toast show ' + type;

    // Automatically hide the toast after 4 seconds
    setTimeout(() => {
        toast.className = 'toast'; // Remove the show class to hide the toast
    }, 4000); // Match this to the animation duration
}

// Function to hide toast notification
function hideToast() {
    const toast = document.getElementById('toast');
    toast.className = 'toast'; // Hide the toast when close button is clicked
}



// Check if the signup form exists and add an event listener to it
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.getElementById('signupUsername').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('signupPassword').value;

        try {
            const response = await fetch(`${baseUrl}/api/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                showToast('Signup successful! Redirecting to Dashboard', 'success');
                setTimeout(() => window.location.href = `${baseUrl}/dashboard`, 2000);
            } else {
                showToast('Signup failed: ' + JSON.stringify(data), 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('An error occurred. Please try again later.', 'error');
        }
    });
}

// Check if the login form exists and add an event listener to it
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await fetch(`${baseUrl}/api/token/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('accessToken', data.access);
                localStorage.setItem('refreshToken', data.refresh);
                showToast('Login successful! Redirecting to Dashboard', 'success');
                setTimeout(() => window.location.href = `${baseUrl}/dashboard`, 2000);
            } else {
                showToast('Login failed: ' + (data.detail || 'Unknown error'), 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('An error occurred. Please try again later.', 'error');
        }
    });
}

// Real-time validation for username availability
document.getElementById('signupUsername').addEventListener('input', async function() {
    const username = this.value;
    const response = await fetch(`${baseUrl}/api/check-username/?username=${username}`);
    const data = await response.json();

    if (data.available) {
        this.classList.remove('error');
        this.classList.add('available');
    } else {
        this.classList.add('error');
        this.classList.remove('available');
    }
});

// Real-time validation for email availability
document.getElementById('email').addEventListener('input', async function() {
    const email = this.value;
    const response = await fetch(`${baseUrl}/api/check-email/?email=${email}`);
    const data = await response.json();

    if (data.available) {
        this.classList.remove('error');
        this.classList.add('available');
    } else {
        this.classList.add('error');
        this.classList.remove('available');
    }
});

// Real-time validation for username availability
const signupUsername = document.getElementById('signupUsername');
if (signupUsername) {
    signupUsername.addEventListener('input', async function() {
        const username = this.value;
        const usernameMessage = document.getElementById('username-message');
        
        if (username.length > 0) {
            const response = await fetch(`${baseUrl}/api/check-username/?username=${username}`);
            const data = await response.json();

            if (data.available) {
                this.classList.remove('error');
                this.classList.add('available');
                usernameMessage.textContent = "Username is available";
                usernameMessage.classList.remove('error');
                usernameMessage.classList.add('success');
            } else {
                this.classList.add('error');
                this.classList.remove('available');
                usernameMessage.textContent = "Username is already taken";
                usernameMessage.classList.remove('success');
                usernameMessage.classList.add('error');
            }
        } else {
            // Reset if input is empty
            this.classList.remove('available', 'error');
            usernameMessage.textContent = "";
        }
    });
}

// Real-time validation for email availability
const signupEmail = document.getElementById('email');
if (signupEmail) {
    signupEmail.addEventListener('input', async function() {
        const email = this.value;
        const emailMessage = document.getElementById('email-message');
        
        if (email.length > 0) {
            const response = await fetch(`${baseUrl}/api/check-email/?email=${email}`);
            const data = await response.json();

            if (data.available) {
                this.classList.remove('error');
                this.classList.add('available');
                emailMessage.textContent = "Email is available";
                emailMessage.classList.remove('error');
                emailMessage.classList.add('success');
            } else {
                this.classList.add('error');
                this.classList.remove('available');
                emailMessage.textContent = "Email is already registered";
                emailMessage.classList.remove('success');
                emailMessage.classList.add('error');
            }
        } else {
            // Reset if input is empty
            this.classList.remove('available', 'error');
            emailMessage.textContent = "";
        }
    });
}