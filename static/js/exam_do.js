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

const examId = "{{ exam.id }}";
const storageKey = "exam_" + examId;

// Lưu khi chọn đáp án
document.querySelectorAll("input[type=radio]").forEach(input => {
    input.addEventListener("change", saveAnswers);
});

function saveAnswers() {
    const answers = {};
    document.querySelectorAll("input[type=radio]:checked").forEach(input => {
        answers[input.name] = input.value;
    });
    localStorage.setItem(storageKey, JSON.stringify(answers));
}

// Load lại bài làm
function loadAnswers() {
    const saved = localStorage.getItem(storageKey);
    if (!saved) return;

    const answers = JSON.parse(saved);
    for (let name in answers) {
        const input = document.querySelector(
            `input[name="${name}"][value="${answers[name]}"]`
        );
        if (input) input.checked = true;
    }
}

loadAnswers();