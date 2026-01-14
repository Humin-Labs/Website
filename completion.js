document.addEventListener("DOMContentLoaded", () => {
  const lessons = document.querySelectorAll("[data-lesson-id]");
  lessons.forEach(el => {
    const id = el.dataset.lessonId;
    const key = `/mobile_labs/circuits/forces-linkages/${id}.html_complete`;
    if (localStorage.getItem(key) === "true") {
      el.classList.add("completed");
      const mark = document.createElement("span");
      mark.textContent = " ✅";
      mark.style.color = "green";
      mark.style.fontWeight = "700";
      el.appendChild(mark);
    }
  });
});
