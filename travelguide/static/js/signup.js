document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');
    const submitBtn = document.getElementById('submitBtn');
    
    // Get all form fields
    const usernameField = document.getElementById('id_username');
    const emailField = document.getElementById('id_email');
    const firstNameField = document.getElementById('id_first_name');
    const lastNameField = document.getElementById('id_last_name');
    const password1Field = document.getElementById('id_password1');
    const password2Field = document.getElementById('id_password2');
    const profilePictureField = document.getElementById('id_profile_picture');
    
    // Validation patterns
    const patterns = {
        username: /^[a-zA-Z0-9_]{3,20}$/,
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        name: /^[a-zA-Z\s]{2,30}$/,
        password: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$/
    };
    
    // Error messages
    const errorMessages = {
        username: {
            required: 'Username is required',
            pattern: 'Username must be 3-20 characters, letters, numbers, and underscores only',
            taken: 'This username is already taken'
        },
        email: {
            required: 'Email is required',
            pattern: 'Please enter a valid email address',
            taken: 'This email is already registered'
        },
        firstName: {
            required: 'First name is required',
            pattern: 'First name must be 2-30 letters only'
        },
        lastName: {
            required: 'Last name is required',
            pattern: 'Last name must be 2-30 letters only'
        },
        password1: {
            required: 'Password is required',
            pattern: 'Password must be at least 8 characters with letters and numbers'
        },
        password2: {
            required: 'Please confirm your password',
            mismatch: 'Passwords do not match'
        }
    };
    
    // Helper function to show field validation
    function showFieldValidation(field, isValid, message = '') {
        const errorDiv = field.parentNode.querySelector('.text-danger');
        
        // Remove existing validation classes
        field.classList.remove('is-valid', 'is-invalid');
        
        if (isValid) {
            field.classList.add('is-valid');
            if (errorDiv) {
                errorDiv.remove();
            }
        } else {
            field.classList.add('is-invalid');
            if (errorDiv) {
                errorDiv.textContent = message;
            } else {
                const newErrorDiv = document.createElement('div');
                newErrorDiv.className = 'text-danger small mt-1';
                newErrorDiv.textContent = message;
                field.parentNode.appendChild(newErrorDiv);
            }
        }
    }
    
    // Real-time validation functions
    function validateUsername() {
        const value = usernameField.value.trim();
        if (!value) {
            showFieldValidation(usernameField, false, errorMessages.username.required);
            return false;
        }
        if (!patterns.username.test(value)) {
            showFieldValidation(usernameField, false, errorMessages.username.pattern);
            return false;
        }
        showFieldValidation(usernameField, true);
        return true;
    }
    
    function validateEmail() {
        const value = emailField.value.trim();
        if (!value) {
            showFieldValidation(emailField, false, errorMessages.email.required);
            return false;
        }
        if (!patterns.email.test(value)) {
            showFieldValidation(emailField, false, errorMessages.email.pattern);
            return false;
        }
        showFieldValidation(emailField, true);
        return true;
    }
    
    function validateFirstName() {
        const value = firstNameField.value.trim();
        if (!value) {
            showFieldValidation(firstNameField, false, errorMessages.firstName.required);
            return false;
        }
        if (!patterns.name.test(value)) {
            showFieldValidation(firstNameField, false, errorMessages.firstName.pattern);
            return false;
        }
        showFieldValidation(firstNameField, true);
        return true;
    }
    
    function validateLastName() {
        const value = lastNameField.value.trim();
        if (!value) {
            showFieldValidation(lastNameField, false, errorMessages.lastName.required);
            return false;
        }
        if (!patterns.name.test(value)) {
            showFieldValidation(lastNameField, false, errorMessages.lastName.pattern);
            return false;
        }
        showFieldValidation(lastNameField, true);
        return true;
    }
    
    function validatePassword1() {
        const value = password1Field.value;
        if (!value) {
            showFieldValidation(password1Field, false, errorMessages.password1.required);
            return false;
        }
        if (!patterns.password.test(value)) {
            showFieldValidation(password1Field, false, errorMessages.password1.pattern);
            return false;
        }
        showFieldValidation(password1Field, true);
        return true;
    }
    
    function validatePassword2() {
        const value = password2Field.value;
        const password1Value = password1Field.value;
        
        if (!value) {
            showFieldValidation(password2Field, false, errorMessages.password2.required);
            return false;
        }
        if (value !== password1Value) {
            showFieldValidation(password2Field, false, errorMessages.password2.mismatch);
            return false;
        }
        showFieldValidation(password2Field, true);
        return true;
    }
    
    function validateProfilePicture() {
        const file = profilePictureField.files[0];
        if (file) {
            // Check file size (max 5MB)
            const maxSize = 5 * 1024 * 1024; // 5MB
            if (file.size > maxSize) {
                showFieldValidation(profilePictureField, false, 'Profile picture must be less than 5MB');
                return false;
            }
            
            // Check file type
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
            if (!allowedTypes.includes(file.type)) {
                showFieldValidation(profilePictureField, false, 'Please upload a valid image file (JPEG, PNG, or GIF)');
                return false;
            }
        }
        showFieldValidation(profilePictureField, true);
        return true;
    }
    
    // Add event listeners for real-time validation
    usernameField.addEventListener('input', validateUsername);
    usernameField.addEventListener('blur', validateUsername);
    
    emailField.addEventListener('input', validateEmail);
    emailField.addEventListener('blur', validateEmail);
    
    firstNameField.addEventListener('input', validateFirstName);
    firstNameField.addEventListener('blur', validateFirstName);
    
    lastNameField.addEventListener('input', validateLastName);
    lastNameField.addEventListener('blur', validateLastName);
    
    password1Field.addEventListener('input', function() {
        validatePassword1();
        // Also validate password2 when password1 changes
        if (password2Field.value) {
            validatePassword2();
        }
    });
    password1Field.addEventListener('blur', validatePassword1);
    
    password2Field.addEventListener('input', validatePassword2);
    password2Field.addEventListener('blur', validatePassword2);
    
    // Profile picture validation (on change)
    profilePictureField.addEventListener('change', validateProfilePicture);
    
    // Form submission handling
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate all fields
        const isUsernameValid = validateUsername();
        const isEmailValid = validateEmail();
        const isFirstNameValid = validateFirstName();
        const isLastNameValid = validateLastName();
        const isPassword1Valid = validatePassword1();
        const isPassword2Valid = validatePassword2();
        
        // Check if all validations pass
        if (isUsernameValid && isEmailValid && isFirstNameValid && 
            isLastNameValid && isPassword1Valid && isPassword2Valid) {
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Creating Account...';
            
            // Submit the form
            form.submit();
        } else {
            // Show error message at the top
            let errorMessage = 'Please correct the following errors:';
            const errors = [];
            
            if (!isUsernameValid) errors.push('Username');
            if (!isEmailValid) errors.push('Email');
            if (!isFirstNameValid) errors.push('First Name');
            if (!isLastNameValid) errors.push('Last Name');
            if (!isPassword1Valid) errors.push('Password');
            if (!isPassword2Valid) errors.push('Password Confirmation');
            
            errorMessage += ' ' + errors.join(', ');
            
            // Show error alert
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger alert-dismissible fade show';
            alertDiv.innerHTML = `
                ${errorMessage}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            // Insert at the top of the form
            const formContainer = form.parentNode;
            formContainer.insertBefore(alertDiv, form);
            
            // Scroll to top to show error
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
    
    // Ensure login link works properly by preventing any interference
    const loginLink = document.querySelector('a[href*="login"]');
    if (loginLink) {
        loginLink.addEventListener('click', function(e) {
            // Stop any form validation or other interference
            e.stopPropagation();
            e.preventDefault();
            // Navigate to login page
            window.location.href = this.href;
        });
    }
    
    // Clear loading state if there are validation errors on page load
    const errorElements = document.querySelectorAll('.text-danger');
    if (errorElements.length > 0) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-person-plus"></i> Create Account';
    }
}); 