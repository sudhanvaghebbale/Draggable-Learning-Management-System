/**
 * @author Sayali Tanawade <ssuryaka@asu.edu>
 */

(function() {
  const urlParams = new URLSearchParams(window.location.search);
  const myParam = urlParams.get('quizName');
  let score = 0;
  console.log(myParam)
  const myQuestions = []
  var quizContainer = document.getElementById("quiz");
  var resultsContainer = document.getElementById("results");
  var submitButton = document.getElementById("submit");
  var previousButton = document.getElementById("previous");
  var nextButton = document.getElementById("next");
  var slides = document.querySelectorAll(".slide");
  var currentSlide = 0;

  $.ajax({
        url: `/getQuestions?quizname=${myParam}`,
        type: 'GET',
        success: function(res) {
            console.log(res);
            //alert(res);
            res = JSON.parse(res)
            res.forEach(e => myQuestions.push({question: e.question, id: e.id}));


  // display quiz right away
  buildQuiz();
  slides = document.querySelectorAll(".slide");



  showSlide(0);

  // on submit, show results
  submitButton.addEventListener("click", showResults);
  previousButton.addEventListener("click", showPreviousSlide);
  nextButton.addEventListener("click", showNextSlide);
        }
    });

  function buildQuiz() {
    // we'll need a place to store the HTML output
    const output = [];
    console.log(myQuestions)
    // for each question...
    myQuestions.forEach((currentQuestion, questionNumber) => {
      // we'll want to store the list of answer choices
      const answers = [];

      // and for each available answer...
      for (letter in currentQuestion.answers) {
        // ...add an HTML radio button
        answers.push(
          `<label>
             <input type="radio" name="question${questionNumber}" value="${letter}">
              ${letter} :
              ${currentQuestion.answers[letter]}
           </label>`
        );
      }

      // add this question and its answers to the output
      output.push(
        `<div class="slide">
           <div class="question"> ${currentQuestion.question} </div>
           <div class="answers"> <input type="text" id="answer_${questionNumber}" class="form-control" /></div>
         </div>`
      );
    });

    // finally combine our output list into one string of HTML and put it on the page
    quizContainer.innerHTML = output.join("");
  }

function showResults() {
    const answerContainers = quizContainer.querySelectorAll(".answers");

    // keep track of user's answers
    let numCorrect = 0;

    // for each question...
    myQuestions.forEach((currentQuestion, questionNumber) => {
      // find selected answer
      const answerContainer = answerContainers[questionNumber];
      const selector = `input[name=question${questionNumber}]:checked`;
      const userAnswer = (answerContainer.querySelector(selector) || {}).value;

      // if answer is correct
      if (userAnswer === currentQuestion.correctAnswer) {
        // add to the number of correct answers
        numCorrect++;

        // color the answers green
        answerContainers[questionNumber].style.color = "lightgreen";
      } else {
        // if answer is wrong or blank
        // color the answers red
        answerContainers[questionNumber].style.color = "red";
      }
    });
    const ans = document.getElementById('answer_'+currentSlide).value.trim()
    const qDetails = myQuestions[currentSlide];
    console.log(ans, qDetails)
    $.ajax({
        url: `/checkAnswers?questionName=${qDetails.id}&quizName=${myParam}&ans=${ans}`,
        type: 'GET',
        success: function(res) {
           score = score + 1;
      resultsContainer.innerHTML = `${score} out of ${myQuestions.length}`;
      previousButton.style.display = "none";
      submitButton.style.display = "none";
      $.ajax({
        url: `/postResult?marks=${score}`,
        type: 'POST',
        success: function(res) {
        console.log("inside ajax");
        }
    });
        },
        error: function(res) {
        resultsContainer.innerHTML = `${score} out of ${myQuestions.length}`;
      previousButton.style.display = "none";
      submitButton.style.display = "none";
      $.ajax({
        url: `/postResult?marks=${score}`,
        type: 'POST',
        success: function(res) {
        console.log("inside ajax");
        }
    });
        }
    });

}

  function showSlide(n) {
    slides[currentSlide].classList.remove("active-slide");
    slides[n].classList.add("active-slide");
    currentSlide = n;

    if (currentSlide === 0) {
      previousButton.style.display = "none";
    } else {
      previousButton.style.display = "inline-block";
    }

    if (currentSlide === slides.length - 1) {
      nextButton.style.display = "none";
      submitButton.style.display = "inline-block";
    } else {
      nextButton.style.display = "inline-block";
      submitButton.style.display = "none";
    }
  }

  function showNextSlide() {
    console.log(document.getElementById('answer_'+currentSlide).value)
    const ans = document.getElementById('answer_'+currentSlide).value.trim()
    const qDetails = myQuestions[currentSlide];
    $.ajax({
        url: `/checkAnswers?questionName=${qDetails.id}&quizName=${myParam}&ans=${ans}`,
        type: 'GET',
        success: function(res) {
           showSlide(currentSlide + 1);
           score = score + 1;
        },
        error: function(res) {
           showSlide(currentSlide + 1);
        }
    });
  }

  function showPreviousSlide() {
    showSlide(currentSlide - 1);
  }


})();