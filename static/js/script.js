// Blue Enigma - Vietnam Travel Assistant JavaScript
class VietnamTravelApp {
    constructor() {
        this.API_BASE = '/api';
        this.initializeElements();
        this.bindEvents();
        this.loadStats();
    }

    initializeElements() {
        this.searchInput = document.getElementById('searchInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.resultsTitle = document.getElementById('resultsTitle');
        this.resultsStats = document.getElementById('resultsStats');
        this.resultsGrid = document.getElementById('resultsGrid');
        this.connectionsSection = document.getElementById('connectionsSection');
        this.connectionsGrid = document.getElementById('connectionsGrid');
        this.errorModal = document.getElementById('errorModal');
        this.errorMessage = document.getElementById('errorMessage');
        this.closeModal = document.getElementById('closeModal');
    }

    bindEvents() {
        // Search events
        this.searchBtn.addEventListener('click', () => this.performSearch());
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.performSearch();
        });

        // Suggestion clicks
        document.querySelectorAll('.suggestion').forEach(suggestion => {
            suggestion.addEventListener('click', () => {
                const query = suggestion.getAttribute('data-query');
                this.searchInput.value = query;
                this.performSearch();
            });
        });

        // Modal events
        this.closeModal.addEventListener('click', () => this.hideModal());
        window.addEventListener('click', (e) => {
            if (e.target === this.errorModal) this.hideModal();
        });

        // Input focus effect
        this.searchInput.addEventListener('focus', () => {
            this.searchInput.parentElement.style.transform = 'scale(1.02)';
        });

        this.searchInput.addEventListener('blur', () => {
            this.searchInput.parentElement.style.transform = 'scale(1)';
        });
    }

    async loadStats() {
        try {
            const response = await fetch(`${this.API_BASE}/stats`);
            const data = await response.json();
            
            if (data.success) {
                // You could display stats somewhere if needed
                console.log('App stats:', data.stats);
            }
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }

    async performSearch() {
        const query = this.searchInput.value.trim();
        
        if (!query) {
            this.showError('Please enter a search query');
            return;
        }

        this.showLoading();
        
        try {
            const response = await fetch(`${this.API_BASE}/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query })
            });

            const data = await response.json();

            if (data.success) {
                this.displayResults(data);
            } else {
                this.showError(data.error || 'Search failed');
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
            console.error('Search error:', error);
        }
    }

    showLoading() {
        this.loadingSection.style.display = 'block';
        this.resultsSection.style.display = 'none';
        this.searchBtn.disabled = true;
        this.searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }

    displayResults(data) {
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'block';
        this.searchBtn.disabled = false;
        this.searchBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';

        // Update results header
        this.resultsTitle.textContent = `Results for "${data.query}"`;
        this.resultsStats.textContent = `${data.total_found} places found`;

        // Clear previous results
        this.resultsGrid.innerHTML = '';
        this.connectionsGrid.innerHTML = '';

        // Display places
        data.results.forEach((place, index) => {
            const card = this.createPlaceCard(place, index);
            this.resultsGrid.appendChild(card);
        });

        // Display connections
        if (data.connections && data.connections.length > 0) {
            this.connectionsSection.style.display = 'block';
            data.connections.forEach(connection => {
                const connectionCard = this.createConnectionCard(connection);
                this.connectionsGrid.appendChild(connectionCard);
            });
        } else {
            this.connectionsSection.style.display = 'none';
        }

        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    createPlaceCard(place, index) {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.style.animationDelay = `${index * 0.1}s`;

        const typeColors = {
            'City': '#10b981',
            'Attraction': '#f59e0b',
            'Restaurant': '#ef4444',
            'Hotel': '#8b5cf6',
            'Beach': '#06b6d4',
            'Temple': '#f97316'
        };

        const typeColor = typeColors[place.type] || '#6b7280';
        const scorePercentage = Math.round(place.score * 100);

        card.innerHTML = `
            <div class="result-header">
                <div>
                    <div class="result-title">${this.escapeHtml(place.name)}</div>
                    <div class="result-location">
                        <i class="fas fa-map-marker-alt"></i>
                        ${this.escapeHtml(place.location)}
                    </div>
                </div>
                <div class="result-type" style="background-color: ${typeColor}">
                    ${this.escapeHtml(place.type)}
                </div>
            </div>
            
            <div class="result-score">
                <span>Relevance:</span>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${scorePercentage}%"></div>
                </div>
                <span>${place.score.toFixed(3)}</span>
            </div>
            
            ${place.tags && place.tags.length > 0 ? `
                <div class="result-tags">
                    ${place.tags.map(tag => `<span class="tag">${this.escapeHtml(tag)}</span>`).join('')}
                </div>
            ` : ''}
        `;

        return card;
    }

    createConnectionCard(connection) {
        const card = document.createElement('div');
        card.className = 'connection-card';

        const relationshipColors = {
            'Connected_To': '#10b981',
            'Located_In': '#3b82f6',
            'Near': '#f59e0b',
            'Similar_To': '#8b5cf6'
        };

        const relationshipColor = relationshipColors[connection.relationship] || '#6b7280';

        card.innerHTML = `
            <div class="connection-text">
                <strong>${this.escapeHtml(connection.to)}</strong>
                <span class="connection-type" style="background-color: ${relationshipColor}; color: white;">
                    ${this.escapeHtml(connection.type)}
                </span>
                <br>
                <small style="color: #6b7280;">
                    ${this.escapeHtml(connection.relationship.replace('_', ' '))}
                </small>
            </div>
        `;

        return card;
    }

    showError(message) {
        this.loadingSection.style.display = 'none';
        this.searchBtn.disabled = false;
        this.searchBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
        
        this.errorMessage.textContent = message;
        this.errorModal.style.display = 'flex';
    }

    hideModal() {
        this.errorModal.style.display = 'none';
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, (m) => map[m]);
    }
}

// Add some nice scroll animations
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideUp 0.6s ease-out forwards';
            }
        });
    }, observerOptions);

    // Observe result cards
    document.addEventListener('DOMNodeInserted', (e) => {
        if (e.target.classList && e.target.classList.contains('result-card')) {
            observer.observe(e.target);
        }
    });
}

// Add typing effect for search placeholder
function addTypingEffect() {
    const searchInput = document.getElementById('searchInput');
    const placeholders = [
        "Ask me about Vietnam travel...",
        "Best beaches in Vietnam?",
        "Where to eat in Hanoi?",
        "Cultural sites in Ho Chi Minh City?",
        "Adventure activities in Sapa?"
    ];
    
    let currentIndex = 0;
    let currentText = '';
    let isDeleting = false;
    
    function typeEffect() {
        const currentPlaceholder = placeholders[currentIndex];
        
        if (!isDeleting) {
            currentText = currentPlaceholder.substring(0, currentText.length + 1);
        } else {
            currentText = currentPlaceholder.substring(0, currentText.length - 1);
        }
        
        searchInput.placeholder = currentText;
        
        let typeSpeed = isDeleting ? 50 : 100;
        
        if (!isDeleting && currentText === currentPlaceholder) {
            typeSpeed = 2000; // Pause at end
            isDeleting = true;
        } else if (isDeleting && currentText === '') {
            isDeleting = false;
            currentIndex = (currentIndex + 1) % placeholders.length;
            typeSpeed = 500; // Pause before next word
        }
        
        setTimeout(typeEffect, typeSpeed);
    }
    
    // Only start typing effect if search input is not focused
    if (document.activeElement !== searchInput) {
        setTimeout(typeEffect, 1000);
    }
    
    // Stop typing effect when input is focused
    searchInput.addEventListener('focus', () => {
        searchInput.placeholder = "Ask me about Vietnam travel...";
    });
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VietnamTravelApp();
    addScrollAnimations();
    addTypingEffect();
    
    // Add some sparkle effects
    createSparkles();
});

// Create sparkle effects for the header
function createSparkles() {
    const header = document.querySelector('.header');
    
    for (let i = 0; i < 20; i++) {
        setTimeout(() => {
            const sparkle = document.createElement('div');
            sparkle.innerHTML = '✨';
            sparkle.style.position = 'absolute';
            sparkle.style.left = Math.random() * 100 + '%';
            sparkle.style.top = Math.random() * 100 + '%';
            sparkle.style.fontSize = '10px';
            sparkle.style.opacity = '0.7';
            sparkle.style.animation = `sparkle 3s ease-in-out infinite`;
            sparkle.style.animationDelay = Math.random() * 3 + 's';
            sparkle.style.pointerEvents = 'none';
            
            header.appendChild(sparkle);
            
            setTimeout(() => sparkle.remove(), 3000);
        }, i * 200);
    }
}

// Add sparkle keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
        50% { opacity: 1; transform: scale(1) rotate(180deg); }
    }
`;
document.head.appendChild(style);