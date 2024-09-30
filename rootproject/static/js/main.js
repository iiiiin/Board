// main.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    
    // Your JavaScript code here
    
    // Example: Add a click event listener to all buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('Button clicked:', this.textContent);
        });
    });
    
    // Example: Simple form validation
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value) {
                    event.preventDefault();
                    console.error('Required field is empty:', field.name);
                }
            });
        });
    }
});