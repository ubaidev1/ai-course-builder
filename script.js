// Load quiz data from the Django template
    const quizData = {{ quiz_data|safe }};
    let currentQuestionIndex = 0; // Keeps track of the current question index
    let score = localStorage.getItem('quizScore') ? parseInt(localStorage.getItem('quizScore')) : 0; // Retrieve score from localStorage or initialize to 0
    let answeredIncorrectly = false; // Tracks if the current question was answered incorrectly

    // Function to load a question onto the page
    function loadQuestion() {
        const questionData = quizData.quiz[currentQuestionIndex]; // Get the current question data
        document.getElementById('question').innerText = questionData.question; // Display the question text

        // Clear the previous options and load new ones
        const optionsContainer = document.getElementById('options-container');
        optionsContainer.innerHTML = ''; // Clear previous options
        questionData.options.forEach((option, index) => {
            const button = document.createElement('button'); // Create a button for each option
            button.innerText = option; // Set button text to the option
            button.onclick = () => selectOption(index); // Set the onClick handler to selectOption
            button.dataset.correct = option === questionData.correct_answer; // Mark the correct answer
            optionsContainer.appendChild(button); // Add the button to the options container
        });

        document.getElementById('result').innerText = ''; // Clear previous result messages
        answeredIncorrectly = false; // Reset the incorrect answer flag
        document.getElementById('score').innerText = score; // Display the current score
    }

    // Function to handle option selection
    function selectOption(optionIndex) {
        const questionData = quizData.quiz[currentQuestionIndex]; // Get current question data
        const selectedButton = document.querySelector(`#options-container button:nth-child(${optionIndex + 1})`); // Get the selected button
        const isCorrect = selectedButton.dataset.correct === 'true'; // Check if the selected answer is correct
        selectedButton.disabled = true; // Disable the button after selection

        if (isCorrect) {
            selectedButton.classList.add('correct'); // Add 'correct' class for styling
            if (answeredIncorrectly) {
                score += 5; // Award 5 points if initially answered incorrectly
            } else {
                score += 10; // Award 10 points for a correct answer without mistakes
            }
            document.getElementById('result').innerText = `Correct! Score: ${score}`; // Display correct result and score
            localStorage.setItem('quizScore', score); // Save the updated score to localStorage
            setTimeout(() => {
                currentQuestionIndex++; // Move to the next question
                if (currentQuestionIndex < quizData.quiz.length) {
                    loadQuestion(); // Load the next question
                } else {
                    // If no more questions, end the quiz
                    document.getElementById('question').innerText = 'Quiz finished!';
                    document.getElementById('result').innerText = `Final Score: ${score}`;
                    document.querySelectorAll('#options-container button').forEach(btn => btn.style.display = 'none'); // Hide all option buttons

                    // Set the final score in a hidden form field for submission
                    document.getElementById('final_score').value = score;
                    document.getElementById('submit-button').style.display = 'inline-block'; // Show the submit button
                }
            }, 1000); // Delay before loading the next question
        } else {
            selectedButton.classList.add('incorrect'); // Add 'incorrect' class for styling
            score -= 10; // Deduct 10 points for an incorrect answer
            document.getElementById('result').innerText = `Incorrect! Score: ${score}`; // Display incorrect result and updated score
            answeredIncorrectly = true; // Mark that the question was answered incorrectly
            localStorage.setItem('quizScore', score); // Save the updated score to localStorage
        }
        document.getElementById('score').innerText = score; // Update the score display
    }

    // Set the 'next' button functionality
    document.getElementById('next-button').addEventListener('click', () => {
        document.getElementById('flip-card').classList.add('flipped'); // Flip the card for animation
        loadQuestion(); // Load the next question
    });

    // Load the first question initially
    loadQuestion();