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

  // Verifica rolagem
  window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > lastScroll && !mouseNearTop) {
      // Rolar para baixo → esconder
      navbar.style.transform = "translateY(-100%)";
    } else {
      // Rolar para cima → mostrar
      navbar.style.transform = "translateY(0)";
    }

    lastScroll = currentScroll;
  });

  // Verifica posição do mouse
  document.addEventListener("mousemove", (e) => {
    if (e.clientY < 80) {
      // Mouse perto do topo → mostrar
      navbar.style.transform = "translateY(0)";
      mouseNearTop = true;
    } else {
      mouseNearTop = false;
    }
  });

  // Transição suave
  navbar.style.transition = "transform 0.3s ease-in-out";
