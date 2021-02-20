let score = 0;
let timer = 60;
let myTimer = null;
let words = new Set();

$(function () {
  updateScore();
  updateTimer();
});

$(function () {
  myTimer = setInterval(timerFunction, 1000);
});

function timerFunction() {
  if (timer > 0) {
    timer -= 1;
    updateTimer();
  } else {
    $("#time_remaining").html("Time's Up!");
    $(".guess_form")
      .off("submit")
      .submit(function (evt) {
        evt.preventDefault();
      });
    //prettier-ignore
    $("#time_remaining").append('<form action="/boggle"></form>')
    $("#time_remaining form").html(
      '<button id="play_again">Play Again?</button>'
    );
    scoreGame();

    clearInterval(myTimer);
  }
}

function updateScore() {
  $("#score_board").html(`Score Board: ${score}
  `);
}

function updateTimer() {
  $("#time_remaining").html(`Time Remaining: ${timer}s`);
}

async function checkGuess(evt) {
  evt.preventDefault();
  const $guess = $("#input_guess");
  let word = $guess.val();
  if (!$guess) return;

  if (words.has(word)) {
    $(".messages").html(`You have already found ${word}`);
    return;
  }

  const response = await axios.get("/guess", { params: { word: word } });
  if (response.data.result === "not-word") {
    $(".messages").html(`${word} is not a valid word`);
  } else if (response.data.result === "not-on-board") {
    $(".messages").html(`${word} is not on this board`);
  } else {
    $(".messages").html(`${word} is OK`);
    $(".words").append(`<li>${word}</li>`);
    score += 1;
    updateScore();
    words.add(word);
  }
}

async function scoreGame() {
  const resp = await axios.post("/post-score", { score: score });
  if (resp.data.brokeRecord) {
    $(".messages").html(`New record: ${score}`);
  } else {
    $(".messages").html(`Final score: ${score}`);
  }
}

$(".guess_form").on("submit", checkGuess.bind(this));
