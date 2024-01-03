function showOptions() {
    // Trigger the click event on the select element
    document.getElementById("fruits").click();
  }

  document.addEventListener("DOMContentLoaded", function () {
    const numberOfDots = 80;
    const dots = [];
    const container = document.querySelector(".container");
    const oneLiner = document.getElementById("one-liner");
    const textContent =
      "Explore various algorithms for efficient data imputation. Compare and analyze different methods to enhance data quality and analysis.";

    for (let i = 0; i < numberOfDots; i++) {
      createDot();
    }

    function createDot() {
      const dot = document.createElement("div");
      dot.className = "dot";
      dot.style.left = Math.random() * window.innerWidth + "px";
      dot.style.top = Math.random() * window.innerHeight + "px";
      container.appendChild(dot);
      dots.push({
        element: dot,
        xSpeed: Math.random() * 4 - 2,
        ySpeed: Math.random() * 4 - 2,
      });
    }

    function updateDots() {
      for (const dot of dots) {
        dot.element.style.left =
          parseFloat(dot.element.style.left) + dot.xSpeed + "px";
        dot.element.style.top =
          parseFloat(dot.element.style.top) + dot.ySpeed + "px";

        if (
          parseFloat(dot.element.style.left) < 0 ||
          parseFloat(dot.element.style.left) > window.innerWidth - 10
        ) {
          dot.xSpeed *= -2;
        }

        if (
          parseFloat(dot.element.style.top) < 0 ||
          parseFloat(dot.element.style.top) > window.innerHeight - 10
        ) {
          dot.ySpeed *= -2;
        }
      }

      requestAnimationFrame(updateDots);
    }

    updateDots();

    // Function to type text with specified number of characters at each step
    function typeText(step) {
      const currentText = textContent.substring(0, step);
      oneLiner.innerHTML = `<span>${currentText}</span>`;
    }

    // Delay before starting typing animation
    setTimeout(function () {
      let step = 0;
      const typingInterval = setInterval(function () {
        typeText(step);
        step++;

        if (step > textContent.length) {
          clearInterval(typingInterval);
        }
      }, 50); // Adjust the interval for typing speed
    }, 1000); // Delay before starting typing animation
  });


  

  
  function scrollToDiv() {
    // Get the target div
    var targetDiv = document.getElementById('targetDiv');

    // Scroll to the target div
    targetDiv.scrollIntoView({ behavior: 'smooth' })};




    document.addEventListener('DOMContentLoaded', function() {
      // Get the target element by its id
      var targetElement = document.getElementById("targetDiv");

      // Use smooth scrolling behavior
      targetElement.scrollIntoView({ behavior: "smooth" });
  });