let timeLeft = DURATION;
const timeEl = document.getElementById("time");

function formatTime(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
}

timeEl.innerText = formatTime(timeLeft);

const timer = setInterval(() => {
    timeLeft--;
    timeEl.innerText = formatTime(timeLeft);

    if (timeLeft <= 0) {
        clearInterval(timer);
        alert("⏰ Hết thời gian làm bài!");
        saveAnswers();
    }
}, 1000);