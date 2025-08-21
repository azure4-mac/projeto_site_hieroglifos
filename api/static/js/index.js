// Scroll reveal
ScrollReveal().reveal('.reveal', {
  distance: '45px',
  duration: 800,
  easing: 'ease-in-out',
  origin: 'bottom',
  interval: 200,
  reset: true
});

const navbar = document.getElementById("navbarTopo");
  let lastScroll = 0;
  let mouseNearTop = false;

  window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > lastScroll && !mouseNearTop) {
      navbar.style.transform = "translateY(-100%)";
    } else {
      navbar.style.transform = "translateY(0)";
    }

    lastScroll = currentScroll;
  });

  document.addEventListener("mousemove", (e) => {
    if (e.clientY < 80) {
      navbar.style.transform = "translateY(0)";
      mouseNearTop = true;
    } else {
      mouseNearTop = false;
    }
  });

  navbar.style.transition = "transform 0.3s ease-in-out";