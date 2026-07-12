/* Cipher Munch site — decode headline + scroll reveals */
(function () {
  "use strict";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Decode animation: element starts with its REAL text in the DOM (SEO/no-JS
  // safe); we scramble visually and resolve letter by letter, left to right.
  function decode(el) {
    var target = el.textContent;
    var glyphs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var frame = 0;
    var solvedPerFrame = target.length / 52; // ~solve over 52 frames
    function tick() {
      var solved = Math.floor(frame * solvedPerFrame);
      var out = "";
      for (var i = 0; i < target.length; i++) {
        var ch = target[i];
        if (!/[a-zA-Z]/.test(ch) || i < solved) {
          out += ch;
        } else {
          out += glyphs[Math.floor(Math.random() * 26)];
        }
      }
      el.textContent = out;
      frame++;
      if (solved < target.length) {
        requestAnimationFrame(tick);
      } else {
        el.textContent = target;
        el.classList.add("decoded");
      }
    }
    tick();
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!reduced) {
      var els = document.querySelectorAll(".decode");
      for (var i = 0; i < els.length; i++) decode(els[i]);
    }

    // Scroll reveal
    var revealed = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && !reduced) {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) {
              e.target.classList.add("in");
              io.unobserve(e.target);
            }
          });
        },
        { rootMargin: "0px 0px -8% 0px" }
      );
      revealed.forEach(function (el) { io.observe(el); });
    } else {
      revealed.forEach(function (el) { el.classList.add("in"); });
    }
  });
})();
