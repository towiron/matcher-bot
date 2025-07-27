class ProfileForm {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 16;
        this.formData = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateProgress();
        this.updateNavigation();
    }

    bindEvents() {
        // Navigation buttons
        document.getElementById('prevBtn').addEventListener('click', () => this.previousStep());
        document.getElementById('nextBtn').addEventListener('click', () => this.nextStep());

        // Input fields
        document.getElementById('name').addEventListener('input', (e) => this.validateName(e.target.value));
        document.getElementById('surname').addEventListener('input', (e) => this.validateSurname(e.target.value));
        document.getElementById('age').addEventListener('input', (e) => this.validateAge(e.target.value));
        document.getElementById('city').addEventListener('input', (e) => this.validateCity(e.target.value));
        document.getElementById('job').addEventListener('input', (e) => this.validateJob(e.target.value));
        document.getElementById('height').addEventListener('input', (e) => this.validateHeight(e.target.value));
        document.getElementById('weight').addEventListener('input', (e) => this.validateWeight(e.target.value));

        // Location button
        document.getElementById('locationBtn').addEventListener('click', () => this.getLocation());

        // Option buttons
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.selectOption(e.target.closest('.option-btn')));
        });

        // Success buttons
        document.getElementById('viewProfileBtn').addEventListener('click', () => this.viewProfile());
        document.getElementById('startSearchBtn').addEventListener('click', () => this.startSearch());

        // Enter key support
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.nextStep();
            }
        });
    }

    // Navigation methods
    nextStep() {
        if (this.validateCurrentStep()) {
            if (this.currentStep === this.totalSteps) {
                this.submitForm();
            } else {
                this.currentStep++;
                this.showStep(this.currentStep);
                this.updateProgress();
                this.updateNavigation();
            }
        }
    }

    previousStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.showStep(this.currentStep);
            this.updateProgress();
            this.updateNavigation();
        }
    }

    showStep(stepNumber) {
        // Hide all steps
        document.querySelectorAll('.step').forEach(step => {
            step.style.display = 'none';
        });

        // Show current step
        const currentStepElement = document.getElementById(`step${stepNumber}`);
        if (currentStepElement) {
            currentStepElement.style.display = 'block';
        }

        // Load saved data for current step
        this.loadStepData(stepNumber);
    }

    updateProgress() {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const percentage = (this.currentStep / this.totalSteps) * 100;
        
        progressFill.style.width = `${percentage}%`;
        progressText.textContent = `${this.currentStep} из ${this.totalSteps}`;
    }

    updateNavigation() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');

        // Show/hide previous button
        prevBtn.style.display = this.currentStep > 1 ? 'flex' : 'none';

        // Update next button text
        if (this.currentStep === this.totalSteps) {
            nextBtn.innerHTML = 'Создать профиль <i class="fas fa-check"></i>';
        } else {
            nextBtn.innerHTML = 'Далее <i class="fas fa-arrow-right"></i>';
        }
    }

    // Validation methods
    validateCurrentStep() {
        switch (this.currentStep) {
            case 1: return this.validateName(this.formData.name || '');
            case 2: return this.validateSurname(this.formData.surname || '');
            case 3: return this.validateGender();
            case 4: return this.validateAge(this.formData.age || '');
            case 5: return this.validateCity(this.formData.city || '');
            case 6: return this.validateEthnicity();
            case 7: return this.validateReligion();
            case 8: return this.validateReligiousLevel();
            case 9: return this.validateEducation();
            case 10: return true; // Job is optional
            case 11: return this.validateHeight(this.formData.height || '');
            case 12: return this.validateWeight(this.formData.weight || '');
            case 13: return this.validateMaritalStatus();
            case 14: return this.validateHasChildren();
            case 15: return this.validatePolygamy();
            case 16: return this.validateGoal();
            default: return true;
        }
    }

    validateName(value) {
        const validation = document.getElementById('nameValidation');
        if (!value || value.trim().length < 2) {
            validation.textContent = 'Имя должно содержать минимум 2 символа';
            validation.className = 'input-validation error';
            return false;
        }
        if (value.trim().length > 200) {
            validation.textContent = 'Имя не должно превышать 200 символов';
            validation.className = 'input-validation error';
            return false;
        }
        validation.textContent = '✓';
        validation.className = 'input-validation success';
        this.formData.name = value.trim();
        return true;
    }

    validateSurname(value) {
        const validation = document.getElementById('surnameValidation');
        if (!value || value.trim().length < 2) {
            validation.textContent = 'Фамилия должна содержать минимум 2 символа';
            validation.className = 'input-validation error';
            return false;
        }
        if (value.trim().length > 200) {
            validation.textContent = 'Фамилия не должна превышать 200 символов';
            validation.className = 'input-validation error';
            return false;
        }
        validation.textContent = '✓';
        validation.className = 'input-validation success';
        this.formData.surname = value.trim();
        return true;
    }

    validateGender() {
        if (!this.formData.gender) {
            this.showError('Пожалуйста, выберите ваш пол');
            return false;
        }
        return true;
    }

    validateAge(value) {
        const validation = document.getElementById('ageValidation');
        const age = parseInt(value);
        if (!value || isNaN(age) || age < 18 || age > 100) {
            validation.textContent = 'Возраст должен быть от 18 до 100 лет';
            validation.className = 'input-validation error';
            return false;
        }
        validation.textContent = '✓';
        validation.className = 'input-validation success';
        this.formData.age = age;
        return true;
    }

    validateCity(value) {
        const validation = document.getElementById('cityValidation');
        if (!value || value.trim().length < 2) {
            validation.textContent = 'Укажите название города';
            validation.className = 'input-validation error';
            return false;
        }
        validation.textContent = '✓';
        validation.className = 'input-validation success';
        this.formData.city = value.trim();
        return true;
    }

    validateJob(value) {
        const validation = document.getElementById('jobValidation');
        if (value && value.trim().length > 100) {
            validation.textContent = 'Профессия не должна превышать 100 символов';
            validation.className = 'input-validation error';
            return false;
        }
        validation.textContent = value ? '✓' : '';
        validation.className = value ? 'input-validation success' : 'input-validation';
        this.formData.job = value ? value.trim() : null;
        return true;
    }

    validateHeight(value) {
        const validation = document.getElementById('heightValidation');
        const height = parseInt(value);
        if (!value || isNaN(height) || height < 100 || height > 250) {
            validation.textContent = 'Рост должен быть от 100 до 250 см';
            validation.className = 'input-validation error';
            return false;
        }
        validation.textContent = '✓';
        validation.className = 'input-validation success';
        this.formData.height = height;
        return true;
    }

    validateWeight(value) {
        const validation = document.getElementById('weightValidation');
        const weight = parseInt(value);
        if (!value || isNaN(weight) || weight < 30 || weight > 200) {
            validation.textContent = 'Вес должен быть от 30 до 200 кг';
            validation.className = 'input-validation error';
            return false;
        }
        validation.textContent = '✓';
        validation.className = 'input-validation success';
        this.formData.weight = weight;
        return true;
    }

    validateEthnicity() {
        if (!this.formData.ethnicity) {
            this.showError('Пожалуйста, выберите вашу национальность');
            return false;
        }
        return true;
    }

    validateReligion() {
        if (!this.formData.religion) {
            this.showError('Пожалуйста, выберите вашу религию');
            return false;
        }
        return true;
    }

    validateReligiousLevel() {
        if (!this.formData.religious_level) {
            this.showError('Пожалуйста, выберите уровень религиозности');
            return false;
        }
        return true;
    }

    validateEducation() {
        if (!this.formData.education) {
            this.showError('Пожалуйста, выберите уровень образования');
            return false;
        }
        return true;
    }

    validateMaritalStatus() {
        if (!this.formData.marital_status) {
            this.showError('Пожалуйста, выберите семейное положение');
            return false;
        }
        return true;
    }

    validateHasChildren() {
        if (this.formData.has_children === undefined) {
            this.showError('Пожалуйста, укажите, есть ли у вас дети');
            return false;
        }
        return true;
    }

    validatePolygamy() {
        if (this.formData.polygamy === undefined) {
            this.showError('Пожалуйста, укажите ваше отношение к многожёнству');
            return false;
        }
        return true;
    }

    validateGoal() {
        if (!this.formData.goal) {
            this.showError('Пожалуйста, выберите цель знакомства');
            return false;
        }
        return true;
    }

    // Option selection
    selectOption(button) {
        const step = button.closest('.step');
        const options = step.querySelectorAll('.option-btn');
        
        // Remove selection from all options in this step
        options.forEach(opt => opt.classList.remove('selected'));
        
        // Select clicked option
        button.classList.add('selected');
        
        // Save the value
        const value = button.dataset.value;
        const stepNumber = parseInt(step.dataset.step);
        
        switch (stepNumber) {
            case 3: this.formData.gender = value; break;
            case 6: this.formData.ethnicity = value; break;
            case 7: this.formData.religion = value; break;
            case 8: this.formData.religious_level = value; break;
            case 9: this.formData.education = value; break;
            case 13: this.formData.marital_status = value; break;
            case 14: this.formData.has_children = value === 'true'; break;
            case 15: this.formData.polygamy = value === 'null' ? null : value === 'true'; break;
            case 16: this.formData.goal = value; break;
        }
    }

    // Location services
    getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    this.reverseGeocode(latitude, longitude);
                },
                (error) => {
                    console.error('Error getting location:', error);
                    this.showError('Не удалось определить местоположение. Пожалуйста, введите город вручную.');
                }
            );
        } else {
            this.showError('Геолокация не поддерживается в вашем браузере.');
        }
    }

    async reverseGeocode(latitude, longitude) {
        try {
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=10`);
            const data = await response.json();
            
            if (data.address && data.address.city) {
                const cityInput = document.getElementById('city');
                cityInput.value = data.address.city;
                this.formData.city = data.address.city;
                this.formData.latitude = latitude;
                this.formData.longitude = longitude;
                this.validateCity(data.address.city);
            }
        } catch (error) {
            console.error('Error reverse geocoding:', error);
            this.showError('Не удалось определить город. Пожалуйста, введите вручную.');
        }
    }

    // Data management
    loadStepData(stepNumber) {
        switch (stepNumber) {
            case 1:
                if (this.formData.name) {
                    document.getElementById('name').value = this.formData.name;
                }
                break;
            case 2:
                if (this.formData.surname) {
                    document.getElementById('surname').value = this.formData.surname;
                }
                break;
            case 3:
                if (this.formData.gender) {
                    const btn = document.querySelector(`[data-value="${this.formData.gender}"]`);
                    if (btn) btn.classList.add('selected');
                }
                break;
            case 4:
                if (this.formData.age) {
                    document.getElementById('age').value = this.formData.age;
                }
                break;
            case 5:
                if (this.formData.city) {
                    document.getElementById('city').value = this.formData.city;
                }
                break;
            case 6:
                if (this.formData.ethnicity) {
                    const btn = document.querySelector(`[data-value="${this.formData.ethnicity}"]`);
                    if (btn) btn.classList.add('selected');
                }
                break;
            case 7:
                if (this.formData.religion) {
                    const btn = document.querySelector(`[data-value="${this.formData.religion}"]`);
                    if (btn) btn.classList.add('selected');
                }
                break;
            case 8:
                if (this.formData.religious_level) {
                    const btn = document.querySelector(`[data-value="${this.formData.religious_level}"]`);
                    if (btn) btn.classList.add('selected');
                }
                break;
            case 9:
                if (this.formData.education) {
                    const btn = document.querySelector(`[data-value="${this.formData.education}"]`);
                    if (btn) btn.classList.add('selected');
                }
                break;
            case 10:
                if (this.formData.job) {
                    document.getElementById('job').value = this.formData.job;
                }
                break;
            case 11:
                if (this.formData.height) {
                    document.getElementById('height').value = this.formData.height;
                }
                break;
            case 12:
                if (this.formData.weight) {
                    document.getElementById('weight').value = this.formData.weight;
                }
                break;
            case 13:
                if (this.formData.marital_status) {
                    const btn = document.querySelector(`[data-value="${this.formData.marital_status}"]`);
                    if (btn) btn.classList.add('selected');
                }
                break;
            case 14:
                if (this.formData.has_children !== undefined) {
                    const btn = document.querySelector(`[data-value="${this.formData.has_children}"]`);
                    if (btn) btn.classList.add('selected');
                }
                break;
            case 15:
                if (this.formData.polygamy !== undefined) {
                    const value = this.formData.polygamy === null ? 'null' : this.formData.polygamy.toString();
                    const btn = document.querySelector(`[data-value="${value}"]`);
                    if (btn) btn.classList.add('selected');
                }
                break;
            case 16:
                if (this.formData.goal) {
                    const btn = document.querySelector(`[data-value="${this.formData.goal}"]`);
                    if (btn) btn.classList.add('selected');
                }
                break;
        }
    }

    // Form submission
    async submitForm() {
        this.showLoading(true);
        
        try {
            // Prepare data for API
            const submitData = {
                ...this.formData,
                // Convert boolean values to proper format
                has_children: Boolean(this.formData.has_children),
                polygamy: this.formData.polygamy === null ? null : Boolean(this.formData.polygamy),
                // Ensure numeric values
                age: parseInt(this.formData.age),
                height: parseInt(this.formData.height),
                weight: parseInt(this.formData.weight),
                // Add coordinates if available
                latitude: this.formData.latitude || 0,
                longitude: this.formData.longitude || 0
            };

            // Simulate API call (replace with actual endpoint)
            const response = await this.sendToAPI(submitData);
            
            if (response.success) {
                this.showSuccess();
            } else {
                throw new Error(response.message || 'Ошибка при создании профиля');
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            this.showError('Произошла ошибка при создании профиля. Пожалуйста, попробуйте еще раз.');
        } finally {
            this.showLoading(false);
        }
    }

    async sendToAPI(data) {
        // Replace this with your actual API endpoint
        const response = await fetch('/api/profile/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    // UI helpers
    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        overlay.style.display = show ? 'flex' : 'none';
    }

    showSuccess() {
        document.querySelectorAll('.step').forEach(step => {
            step.style.display = 'none';
        });
        document.getElementById('successStep').style.display = 'block';
        
        // Hide navigation
        document.querySelector('.navigation').style.display = 'none';
    }

    showError(message) {
        // Create a temporary error notification
        const notification = document.createElement('div');
        notification.className = 'error-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #e74c3c;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1001;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    viewProfile() {
        // Navigate to profile view
        window.location.href = '/profile';
    }

    startSearch() {
        // Navigate to search page
        window.location.href = '/search';
    }
}

// Initialize the form when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ProfileForm();
});

// Add CSS for error notification animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style); 