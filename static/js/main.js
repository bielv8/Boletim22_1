// Main JavaScript file for SENAI Bulletin System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Auto-hide flash messages
    autoHideFlashMessages();
    
    // Form validation enhancements
    enhanceFormValidation();
    
    // Grade calculation helpers
    setupGradeCalculation();
    
    // Confirm delete actions
    setupDeleteConfirmations();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Auto-hide flash messages after 5 seconds
 */
function autoHideFlashMessages() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Enhance form validation with real-time feedback
 */
function enhanceFormValidation() {
    // Grade input validation (0-100)
    const gradeInputs = document.querySelectorAll('input[type="number"][step="0.1"]');
    gradeInputs.forEach(input => {
        if (input.min === '0' && input.max === '100') {
            input.addEventListener('input', function() {
                validateGradeInput(this);
            });
        }
    });
    
    // Registration number validation
    const regNumberInput = document.querySelector('input[name="registration_number"]');
    if (regNumberInput) {
        regNumberInput.addEventListener('input', function() {
            validateRegistrationNumber(this);
        });
    }
    
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });
}

/**
 * Validate grade input (0-100)
 */
function validateGradeInput(input) {
    const value = parseFloat(input.value);
    const isValid = !isNaN(value) && value >= 0 && value <= 100;
    
    input.classList.remove('is-valid', 'is-invalid');
    
    if (input.value === '') {
        // Empty is okay for optional fields
        return;
    }
    
    if (isValid) {
        input.classList.add('is-valid');
        showFieldFeedback(input, 'Nota válida', 'valid');
    } else {
        input.classList.add('is-invalid');
        showFieldFeedback(input, 'Nota deve estar entre 0 e 100', 'invalid');
    }
}

/**
 * Validate registration number format
 */
function validateRegistrationNumber(input) {
    const value = input.value.trim();
    const isValid = value.length >= 3 && /^[A-Za-z0-9]+$/.test(value);
    
    input.classList.remove('is-valid', 'is-invalid');
    
    if (value === '') {
        return;
    }
    
    if (isValid) {
        input.classList.add('is-valid');
        showFieldFeedback(input, 'Número de matrícula válido', 'valid');
    } else {
        input.classList.add('is-invalid');
        showFieldFeedback(input, 'Deve conter pelo menos 3 caracteres alfanuméricos', 'invalid');
    }
}

/**
 * Validate email format
 */
function validateEmail(input) {
    const value = input.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(value);
    
    input.classList.remove('is-valid', 'is-invalid');
    
    if (value === '') {
        // Email is optional
        return;
    }
    
    if (isValid) {
        input.classList.add('is-valid');
        showFieldFeedback(input, 'Email válido', 'valid');
    } else {
        input.classList.add('is-invalid');
        showFieldFeedback(input, 'Formato de email inválido', 'invalid');
    }
}

/**
 * Show field validation feedback
 */
function showFieldFeedback(input, message, type) {
    // Remove existing feedback
    const existingFeedback = input.parentNode.querySelector('.valid-feedback, .invalid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    // Create new feedback element
    const feedback = document.createElement('div');
    feedback.className = type === 'valid' ? 'valid-feedback' : 'invalid-feedback';
    feedback.textContent = message;
    
    // Insert after input
    input.parentNode.insertBefore(feedback, input.nextSibling);
}

/**
 * Setup grade calculation helpers
 */
function setupGradeCalculation() {
    const gradeForm = document.querySelector('form');
    if (!gradeForm) return;
    
    const gradeInputs = gradeForm.querySelectorAll('input[name^="grade_"]');
    const absencesInput = gradeForm.querySelector('input[name="absences"]');
    
    if (gradeInputs.length > 0 || absencesInput) {
        // Create approval status indicator
        const statusDiv = document.createElement('div');
        statusDiv.id = 'approval-status';
        statusDiv.className = 'alert mt-3';
        statusDiv.style.display = 'none';
        
        const lastGradeInput = gradeForm.querySelector('input[name="final_grade"]');
        if (lastGradeInput) {
            lastGradeInput.parentNode.parentNode.appendChild(statusDiv);
        }
        
        // Add event listeners
        gradeInputs.forEach(input => {
            input.addEventListener('input', updateApprovalStatus);
        });
        
        if (absencesInput) {
            absencesInput.addEventListener('input', updateApprovalStatus);
        }
    }
}

/**
 * Update approval status based on current values
 */
function updateApprovalStatus() {
    const finalGradeInput = document.querySelector('input[name="final_grade"]');
    const absencesInput = document.querySelector('input[name="absences"]');
    const statusDiv = document.getElementById('approval-status');
    
    if (!finalGradeInput || !absencesInput || !statusDiv) return;
    
    const finalGrade = parseFloat(finalGradeInput.value);
    const absences = parseInt(absencesInput.value);
    
    if (isNaN(finalGrade) && isNaN(absences)) {
        statusDiv.style.display = 'none';
        return;
    }
    
    let status = '';
    let alertClass = '';
    
    if (!isNaN(finalGrade) && !isNaN(absences)) {
        if (finalGrade >= 50 && absences <= 20) {
            status = '<i class="fas fa-check-circle"></i> Aluno será <strong>APROVADO</strong>';
            alertClass = 'alert-success';
        } else {
            const reasons = [];
            if (finalGrade < 50) reasons.push('nota insuficiente');
            if (absences > 20) reasons.push('excesso de faltas');
            status = `<i class="fas fa-times-circle"></i> Aluno será <strong>REPROVADO</strong> (${reasons.join(', ')})`;
            alertClass = 'alert-danger';
        }
    } else if (!isNaN(finalGrade)) {
        if (finalGrade >= 50) {
            status = '<i class="fas fa-question-circle"></i> Aguardando informação de faltas';
            alertClass = 'alert-warning';
        } else {
            status = '<i class="fas fa-times-circle"></i> Aluno será <strong>REPROVADO</strong> (nota insuficiente)';
            alertClass = 'alert-danger';
        }
    } else if (!isNaN(absences)) {
        if (absences <= 20) {
            status = '<i class="fas fa-question-circle"></i> Aguardando nota final';
            alertClass = 'alert-warning';
        } else {
            status = '<i class="fas fa-times-circle"></i> Aluno será <strong>REPROVADO</strong> (excesso de faltas)';
            alertClass = 'alert-danger';
        }
    }
    
    if (status) {
        statusDiv.className = `alert ${alertClass}`;
        statusDiv.innerHTML = status;
        statusDiv.style.display = 'block';
    } else {
        statusDiv.style.display = 'none';
    }
}

/**
 * Setup delete confirmation dialogs
 */
function setupDeleteConfirmations() {
    const deleteButtons = document.querySelectorAll('[onclick*="confirmDelete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // The onclick handler will still execute
        });
    });
}

/**
 * Utility function to format numbers
 */
function formatGrade(grade) {
    return parseFloat(grade).toFixed(1);
}

/**
 * Utility function to show loading state
 */
function showLoading(element, text = 'Carregando...') {
    element.disabled = true;
    element.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span>${text}`;
}

/**
 * Utility function to hide loading state
 */
function hideLoading(element, originalText) {
    element.disabled = false;
    element.innerHTML = originalText;
}

/**
 * Search functionality enhancement
 */
function setupSearch() {
    const searchInputs = document.querySelectorAll('input[name="search"]');
    searchInputs.forEach(input => {
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                // Auto-submit search after 500ms of no typing
                this.form.submit();
            }, 500);
        });
    });
}

/**
 * Table sorting functionality
 */
function setupTableSorting() {
    const tables = document.querySelectorAll('table.sortable');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, this.dataset.sort);
            });
        });
    });
}

/**
 * Sort table by column
 */
function sortTable(table, column) {
    // Implementation would depend on specific requirements
    console.log('Sorting table by', column);
}

/**
 * Export functionality
 */
function exportTable(format = 'csv') {
    const table = document.querySelector('table');
    if (!table) return;
    
    console.log('Exporting table as', format);
    // Implementation for CSV/Excel export would go here
}

// Initialize search and other enhancements
setupSearch();
setupTableSorting();
