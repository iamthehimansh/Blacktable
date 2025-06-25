// Utility function to show response
function showResponse(elementId, data, isError = false) {
    const element = document.getElementById(elementId);
    element.style.display = 'block';
    element.className = `response ${isError ? 'error' : 'success'}`;
    element.textContent = JSON.stringify(data, null, 2);
}

// Utility function to set loading state
function setLoadingState(buttonId, isLoading) {
    const button = document.getElementById(buttonId);
    if (isLoading) {
        button.disabled = true;
        const originalText = button.textContent;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = '<span class="loading"></span>Processing...';
    } else {
        button.disabled = false;
        const originalText = button.getAttribute('data-original-text');
        button.textContent = originalText;
    }
}

// Utility function to create FormData from form and file
function createFormDataWithFile(formData, fileInputId) {
    const fileInput = document.getElementById(fileInputId);
    if (fileInput.files.length === 0) {
        throw new Error('Please select a file');
    }
    formData.append('file', fileInput.files[0]);
    return formData;
}

// Resume Parser
document.getElementById('resumeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        setLoadingState('resumeBtn', true);
        
        const formData = new FormData();
        const fileInput = document.getElementById('resumeFile');
        
        if (fileInput.files.length === 0) {
            throw new Error('Please select a resume file');
        }
        
        formData.append('file', fileInput.files[0]);
        
        const response = await fetch('/api/parse-resume', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('resumeResponse', result);
        } else {
            showResponse('resumeResponse', result, true);
        }
    } catch (error) {
        showResponse('resumeResponse', { error: error.message }, true);
    } finally {
        setLoadingState('resumeBtn', false);
    }
});

// Question Generation
document.getElementById('questionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        setLoadingState('questionBtn', true);
        
        const requestData = {
            job_description: document.getElementById('jobDescription').value,
            interview_round: document.getElementById('interviewRound').value,
            focus_area: document.getElementById('focusArea').value,
            question_count: parseInt(document.getElementById('questionCount').value),
            difficulty_levels: ['medium'] // Default for now
        };
        
        const response = await fetch('/api/generate-questions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('questionResponse', result);
        } else {
            showResponse('questionResponse', result, true);
        }
    } catch (error) {
        showResponse('questionResponse', { error: error.message }, true);
    } finally {
        setLoadingState('questionBtn', false);
    }
});

// Personalized Question Generation
document.getElementById('personalizedQuestionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        setLoadingState('personalizedQuestionBtn', true);
        
        const formData = new FormData();
        formData.append('job_description', document.getElementById('personalizedJobDescription').value);
        formData.append('interview_round', document.getElementById('personalizedInterviewRound').value);
        formData.append('question_count', document.getElementById('personalizedQuestionCount').value);
        
        const fileInput = document.getElementById('personalizedResumeFile');
        if (fileInput.files.length === 0) {
            throw new Error('Please select a resume file');
        }
        formData.append('file', fileInput.files[0]);
        
        const response = await fetch('/api/generate-personalized-questions', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('personalizedQuestionResponse', result);
        } else {
            showResponse('personalizedQuestionResponse', result, true);
        }
    } catch (error) {
        showResponse('personalizedQuestionResponse', { error: error.message }, true);
    } finally {
        setLoadingState('personalizedQuestionBtn', false);
    }
});

// FIT Score
document.getElementById('fitScoreForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        setLoadingState('fitScoreBtn', true);
        
        const formData = new FormData();
        formData.append('job_description', document.getElementById('fitJobDescription').value);
        
        const fileInput = document.getElementById('fitResumeFile');
        if (fileInput.files.length === 0) {
            throw new Error('Please select a resume file');
        }
        formData.append('file', fileInput.files[0]);
        
        const response = await fetch('/api/calculate-fit-score', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('fitScoreResponse', result);
        } else {
            showResponse('fitScoreResponse', result, true);
        }
    } catch (error) {
        showResponse('fitScoreResponse', { error: error.message }, true);
    } finally {
        setLoadingState('fitScoreBtn', false);
    }
});

// Pre-screening Questions Management
let questionCount = 0;

function updateQuestionCounter() {
    const counter = document.getElementById('questionCounter');
    const noQuestionsMsg = document.getElementById('noQuestionsMsg');
    
    counter.textContent = `${questionCount} Question${questionCount !== 1 ? 's' : ''}`;
    
    if (questionCount === 0) {
        noQuestionsMsg.style.display = 'block';
    } else {
        noQuestionsMsg.style.display = 'none';
    }
}

function addPrescreeningQuestion() {
    questionCount++;
    const questionsContainer = document.getElementById('prescreeningQuestions');
    
    const questionItem = document.createElement('div');
    questionItem.className = 'prescreening-item';
    questionItem.setAttribute('data-question-id', questionCount);
    
    questionItem.innerHTML = `
        <div class="question-field">
            <label>Question ${questionCount}:</label>
            <input type="text" 
                   placeholder="Enter your pre-screening question..." 
                   data-question-input="${questionCount}"
                   required>
        </div>
        <div class="answer-field">
            <label>Expected Answer:</label>
            <textarea placeholder="Enter the candidate's expected answer..." 
                      data-answer-input="${questionCount}"
                      style="height: 80px;"
                      required></textarea>
        </div>
        <div class="remove-btn-container">
            <button type="button" class="remove-question" onclick="removePrescreeningQuestion(${questionCount})">
                🗑️ Remove
            </button>
        </div>
    `;
    
    questionsContainer.appendChild(questionItem);
    updateQuestionCounter();
    
    // Add animation
    questionItem.style.opacity = '0';
    questionItem.style.transform = 'translateY(-20px)';
    setTimeout(() => {
        questionItem.style.transition = 'all 0.3s ease';
        questionItem.style.opacity = '1';
        questionItem.style.transform = 'translateY(0)';
    }, 10);
}

function removePrescreeningQuestion(questionId) {
    const questionItem = document.querySelector(`[data-question-id="${questionId}"]`);
    if (questionItem) {
        // Add exit animation
        questionItem.style.transition = 'all 0.3s ease';
        questionItem.style.opacity = '0';
        questionItem.style.transform = 'translateX(-100%)';
        
        setTimeout(() => {
            questionItem.remove();
            questionCount--;
            updateQuestionCounter();
            renumberQuestions();
        }, 300);
    }
}

function renumberQuestions() {
    const questionItems = document.querySelectorAll('.prescreening-item');
    questionItems.forEach((item, index) => {
        const newNumber = index + 1;
        item.setAttribute('data-question-id', newNumber);
        
        const label = item.querySelector('.question-field label');
        label.textContent = `Question ${newNumber}:`;
        
        const questionInput = item.querySelector('[data-question-input]');
        questionInput.setAttribute('data-question-input', newNumber);
        
        const answerInput = item.querySelector('[data-answer-input]');
        answerInput.setAttribute('data-answer-input', newNumber);
        
        const removeBtn = item.querySelector('.remove-question');
        removeBtn.setAttribute('onclick', `removePrescreeningQuestion(${newNumber})`);
    });
    
    questionCount = questionItems.length;
    updateQuestionCounter();
}

// Add event listener for adding questions
document.getElementById('addPrescreeningBtn').addEventListener('click', addPrescreeningQuestion);

// Initialize counter
updateQuestionCounter();

// Application Analyzer
document.getElementById('applicationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        setLoadingState('applicationBtn', true);
        
        const formData = new FormData();
        formData.append('job_title', document.getElementById('jobTitle').value);
        formData.append('job_description', document.getElementById('appJobDescription').value);
        formData.append('salary_range', document.getElementById('salaryRange').value);
        formData.append('current_ctc', document.getElementById('currentCtc').value);
        formData.append('expected_ctc', document.getElementById('expectedCtc').value);
        formData.append('notice_period', document.getElementById('noticePeriod').value);
        
        // Handle pre-screening questions
        const questionInputs = document.querySelectorAll('[data-question-input]');
        const answerInputs = document.querySelectorAll('[data-answer-input]');
        
        if (questionInputs.length > 0) {
            const questions = [];
            const responses = {};
            
            questionInputs.forEach((questionInput, index) => {
                const question = questionInput.value.trim();
                const answerInput = answerInputs[index];
                const answer = answerInput ? answerInput.value.trim() : '';
                
                if (question) {
                    questions.push(question);
                    if (answer) {
                        responses[question] = answer;
                    }
                }
            });
            
            if (questions.length > 0) {
                formData.append('prescreening_questions', JSON.stringify(questions));
            }
            
            if (Object.keys(responses).length > 0) {
                formData.append('prescreening_responses', JSON.stringify(responses));
            }
        }
        
        const fileInput = document.getElementById('appResumeFile');
        if (fileInput.files.length === 0) {
            throw new Error('Please select a resume file');
        }
        formData.append('file', fileInput.files[0]);
        
        const response = await fetch('/api/analyze-application', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('applicationResponse', result);
        } else {
            showResponse('applicationResponse', result, true);
        }
    } catch (error) {
        showResponse('applicationResponse', { error: error.message }, true);
    } finally {
        setLoadingState('applicationBtn', false);
    }
});
