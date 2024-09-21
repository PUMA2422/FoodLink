// Get the current base URL dynamically
const baseUrl = window.location.origin;

// Event listener for login form submission
document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        // Use dynamic base URL instead of hardcoding it
        const response = await fetch(`${baseUrl}/api/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (response.ok) {
            // Store tokens in localStorage for future use
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            alert('Login successful!');
            // Redirect to a protected page or perform other actions
        } else {
            alert('Login failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    }
});

// Event listener for signup form submission
document.getElementById('signupForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('signupUsername').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('signupPassword').value;

    try {
        // Use dynamic base URL for the signup API
        const response = await fetch(`${baseUrl}/api/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            alert('Signup successful! You can now login.');
            window.location.href = `${baseUrl}/login`; // Redirect to login page
        } else {
            alert('Signup failed: ' + JSON.stringify(data));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    }
});
