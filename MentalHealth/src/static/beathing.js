// static/breathing.js

const circle = document.querySelector(".circle");
const text = document.getElementById("breathing-text");
const audio = document.getElementById("breathing-audio");

let isBreathing = false;

function startBreathing() {
  if (isBreathing) return;

  isBreathing = true;
  audio.play();

  const totalTime = 19000; // 4s inhale, 7s hold, 8s exhale

  animateBreathing(); // start immediately
  setInterval(animateBreathing, totalTime);
}

function animateBreathing() {
  text.innerText = "Breathe In";
  circle.style.transform = "scale(1.3)";
  setTimeout(() => {
    text.innerText = "Hold";
  }, 4000);
  setTimeout(() => {
    text.innerText = "Breathe Out";
    circle.style.transform = "scale(1)";
  }, 11000);
}
