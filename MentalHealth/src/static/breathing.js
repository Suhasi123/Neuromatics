document.addEventListener("DOMContentLoaded", () => {
  console.log("JS Loaded");

  const circle = document.querySelector(".circle");
  const text = document.getElementById("breathing-text");
  const audio = document.getElementById("breathing-audio");
  const startBtn = document.getElementById("startBtn");
  const stopBtn = document.getElementById("stopBtn");

  if (!circle || !text || !audio || !startBtn || !stopBtn) {
    console.error("Some DOM elements not found!");
    return;
  }

  let isBreathing = false;
  let intervalId = null;

  startBtn.addEventListener("click", () => {
    if (isBreathing) return;
    isBreathing = true;
    audio.play();

    const totalTime = 19000;

    function animateBreathing() {
      text.innerText = "Breathe In";
      circle.style.transform = "scale(1.4)";

      setTimeout(() => {
        text.innerText = "Hold";
      }, 4000);

      setTimeout(() => {
        text.innerText = "Breathe Out";
        circle.style.transform = "scale(1)";
      }, 11000);
    }

    animateBreathing();
    intervalId = setInterval(animateBreathing, totalTime);
  });

  stopBtn.addEventListener("click", () => {
    clearInterval(intervalId);
    isBreathing = false;
    audio.pause();
    audio.currentTime = 0;
    text.innerText = "Breathe In";
    circle.style.transform = "scale(1)";
  });
});
