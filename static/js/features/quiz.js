// Quiz Feature
class Quiz {
    constructor(quizId) {
        this.quizId = quizId;
        this.currentQuestion = 0;
        this.score = 0;
        this.questions = [];
    }
    
    init() {
        const quizEl = document.getElementById(this.quizId);
        if (!quizEl) return;
        
        console.log('Quiz initialized');
    }
    
    nextQuestion() {
        this.currentQuestion++;
        this.updateDisplay();
    }
    
    updateDisplay() {
        // Update quiz display
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const quizzes = document.querySelectorAll('[data-quiz]');
    quizzes.forEach(el => {
        const quiz = new Quiz(el.id);
        quiz.init();
    });
});
