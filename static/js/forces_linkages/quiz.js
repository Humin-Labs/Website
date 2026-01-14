document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".quizform").forEach(form => {
    const answers = JSON.parse(form.dataset.answers || "{}");
    const resultEl = form.querySelector(".result");
    const nextLink = document.querySelector(".nav-links a[href*='lesson']");
    const key = window.location.pathname + "_complete";

    // Disable Next Lesson by default
    if (nextLink) {
      nextLink.classList.add("disabled");
      nextLink.style.pointerEvents = "none";
      nextLink.style.opacity = "0.4";
      nextLink.style.cursor = "not-allowed";
      nextLink.title = "Complete the quiz to continue";
    }

    // If already completed, re-enable immediately
    if (localStorage.getItem(key) === "true") {
      unlockNextLesson(nextLink);
    }

    form.addEventListener("submit", e => {
      e.preventDefault();
      let correct = 0;
      const total = Object.keys(answers).length;

      form.querySelectorAll(".q").forEach(qDiv => {
        const qid = qDiv.dataset.qid;
        const picked = form.querySelector(`input[name='${qid}']:checked`);
        const feedback = qDiv.querySelector(".feedback");

        if (!picked) {
          feedback.textContent = "Select an answer.";
          feedback.style.color = "#555";
          return;
        }

        if (picked.value === answers[qid]) {
          feedback.textContent = "✓ Correct!";
          feedback.style.color = "green";
          correct++;
        } else {
          feedback.textContent = "✗ Try again.";
          feedback.style.color = "red";
        }
      });

      // Result summary
      if (resultEl) {
        if (correct === total) {
          resultEl.textContent = "All answers correct! You may proceed to the next lesson.";
          resultEl.style.color = "green";
          localStorage.setItem(key, "true");
          unlockNextLesson(nextLink);
        } else {
          resultEl.textContent = `${correct} of ${total} correct. Try again before continuing.`;
          resultEl.style.color = "#e21c21";
        }
      }
    });
  });

  function unlockNextLesson(link) {
    if (!link) return;
    link.classList.remove("disabled");
    link.style.pointerEvents = "auto";
    link.style.opacity = "1";
    link.style.cursor = "pointer";
    link.title = "";
  }
});
