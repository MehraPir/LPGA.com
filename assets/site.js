const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.14 });

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("visible"));
}

const cipherTarget = document.querySelector("[data-cipher-demo]");

if (cipherTarget) {
  const phrases = [
    ["DSZFTM NVODI", "CIPHER MUNCH"],
    ["UIF TFDSFU JT", "THE SECRET IS"],
    ["QMBZ BOE MFBSO", "PLAY AND LEARN"]
  ];
  let phraseIndex = 0;
  let step = 0;

  window.setInterval(() => {
    const [encoded, decoded] = phrases[phraseIndex];
    const letters = encoded.split("");
    const solved = decoded.split("");
    const next = letters.map((letter, index) => {
      if (letter === " ") return " ";
      return index < step ? solved[index] : letter;
    }).join("");

    cipherTarget.textContent = next;
    step += 1;

    if (step > encoded.length + 5) {
      step = 0;
      phraseIndex = (phraseIndex + 1) % phrases.length;
    }
  }, 260);
}
