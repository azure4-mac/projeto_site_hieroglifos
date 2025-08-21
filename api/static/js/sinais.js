document.addEventListener("DOMContentLoaded", function() {
    
    const grid = document.getElementById("signalGrid");
    const searchInput = document.getElementById("searchInput");
    const loadingIndicator = document.getElementById("loading");

    let allHieroglyphs = [];
    let filteredHieroglyphs = []; 
    let currentPage = 1;
    const batchSize = 50;
    let isLoading = false;

    function renderBatch(page, sourceData) {
        isLoading = true;
        loadingIndicator.style.display = 'block';
        
        const start = (page - 1) * batchSize;
        const end = start + batchSize;
        const batch = sourceData.slice(start, end);

        if (batch.length === 0) {
            loadingIndicator.style.display = 'none';
            isLoading = false;
            return;
        }

        const batchHTML = batch.map(hieroglyph => `
            <div class="col mb-4 signal-card" data-gardiner="${hieroglyph.gardiner}" data-description="${hieroglyph.description.toLowerCase()}">
                <div class="card h-100 shadow-sm border-0">
                    <div class="card-body text-center d-flex flex-column justify-content-center">
                        <div class="fs-1 mb-2">${hieroglyph.symbol}</div>
                        <div class="fw-bold">${hieroglyph.gardiner}</div>
                        <small class="text-muted">${hieroglyph.description}</small>
                    </div>
                </div>
            </div>
        `).join('');

        grid.insertAdjacentHTML('beforeend', batchHTML);
        
        isLoading = false;
        loadingIndicator.style.display = 'none';
    }

    async function initialLoad() {
        try {
            const response = await fetch('/api/hieroglyphs');
            allHieroglyphs = await response.json();
            filteredHieroglyphs = [...allHieroglyphs]; 
            
            grid.innerHTML = '';
            currentPage = 1;
            renderBatch(currentPage, filteredHieroglyphs);
        } catch (error) {
            console.error("Erro ao carregar hieróglifos:", error);
            grid.innerHTML = '<p class="text-center text-danger">Falha ao carregar os sinais. Tente novamente mais tarde.</p>';
        }
    }

    window.addEventListener('scroll', () => {
        if (searchInput.value.trim() !== '' || isLoading) {
            return;
        }

        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200) {
            currentPage++;
            renderBatch(currentPage, filteredHieroglyphs);
        }
    });

    searchInput.addEventListener("input", function() {
        const searchTerm = this.value.toLowerCase().trim();
        
        if (searchTerm === '') {
            filteredHieroglyphs = [...allHieroglyphs];
            grid.innerHTML = '';
            currentPage = 1;
            renderBatch(currentPage, filteredHieroglyphs);
            return;
        }

        filteredHieroglyphs = allHieroglyphs.filter(h => 
            h.gardiner.toLowerCase().includes(searchTerm) || 
            h.description.toLowerCase().includes(searchTerm)
        );
        
        grid.innerHTML = '';
        const resultsHTML = filteredHieroglyphs.map(hieroglyph => `
            <div class="col mb-4 signal-card">
                 <div class="card h-100 shadow-sm border-0">
                    <div class="card-body text-center d-flex flex-column justify-content-center">
                        <div class="fs-1 mb-2">${hieroglyph.symbol}</div>
                        <div class="fw-bold">${hieroglyph.gardiner}</div>
                        <small class="text-muted">${hieroglyph.description}</small>
                    </div>
                </div>
            </div>
        `).join('');
        
        grid.innerHTML = resultsHTML;

        if(filteredHieroglyphs.length === 0) {
            grid.innerHTML = '<p class="text-center">Nenhum sinal encontrado.</p>';
        }
    });

    initialLoad();
});