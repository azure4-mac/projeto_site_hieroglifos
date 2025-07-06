    // Função para carregar os hieróglifos via API
    async function loadHieroglyphs() {
      const response = await fetch('/api/hieroglyphs');
      const hieroglyphs = await response.json();

      const grid = document.getElementById("signalGrid");
      grid.innerHTML = '';

      hieroglyphs.forEach(hieroglyph => {
        const card = `
          <div class="col mb-4 signal-card" data-name="${hieroglyph.gardiner}">
            <div class="card shadow-sm border-0">
              <div class="card-body text-center">
                <div class="fs-1 mb-2">${hieroglyph.symbol}</div>
                <div class="fw-bold">${hieroglyph.gardiner}</div>
                <small class="text-muted">${hieroglyph.description}</small>
              </div>
            </div>
          </div>
        `;
        grid.innerHTML += card;
      });
    }

    // Filtro simples
    document.getElementById("searchInput").addEventListener("keyup", function() {
      const searchTerm = this.value.toLowerCase();
      const cards = document.querySelectorAll('.signal-card');
      cards.forEach(card => {
        const name = card.getAttribute("data-name").toLowerCase();
        card.style.display = name.includes(searchTerm) ? 'block' : 'none';
      });
    });

    // Carregar hieróglifos ao iniciar
    loadHieroglyphs();