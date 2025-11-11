/**
 * Timeline Ruler Widget
 * Pulls data from calendar and vault APIs to display events on a horizontal ruler
 */

class TimelineWidget {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.events = [];
        this.currentZoom = 1;
        this.PIXELS_PER_DAY = 60;
        
        this.init();
    }
    
    async init() {
        // Fetch data from calendar and vault
        await this.loadData();
        
        // Render the timeline
        this.render();
        
        // Setup controls
        this.setupControls();
    }
    
    async loadData() {
        try {
            // Fetch calendar events
            const calendarRes = await fetch('/api/calendar/events');
            const calendarData = await calendarRes.json();
            
            // Fetch vault documents
            const vaultRes = await fetch('/api/vault/documents');
            const vaultData = await vaultRes.json();
            
            // Combine and format events
            this.events = this.formatEvents(calendarData, vaultData);
            this.events.sort((a, b) => new Date(a.date) - new Date(b.date));
            
        } catch (error) {
            console.error('Failed to load timeline data:', error);
            // Use fallback sample data if APIs fail
            this.loadFallbackData();
        }
    }
    
    formatEvents(calendarData, vaultData) {
        const events = [];
        
        // Format calendar events
        if (calendarData && calendarData.events) {
            calendarData.events.forEach(event => {
                events.push({
                    date: event.date,
                    type: event.type || 'deadline',
                    title: event.title,
                    amount: event.amount,
                    icon: this.getIcon(event.type),
                    source: 'calendar'
                });
            });
        }
        
        // Format vault documents
        if (vaultData && vaultData.documents) {
            vaultData.documents.forEach(doc => {
                events.push({
                    date: doc.uploaded_at || doc.created_at,
                    type: 'document',
                    title: doc.filename || doc.title,
                    icon: '📄',
                    source: 'vault'
                });
            });
        }
        
        return events;
    }
    
    getIcon(type) {
        const icons = {
            'rent': '💵',
            'document': '📄',
            'call': '📞',
            'notice': '✉️',
            'deadline': '⏰',
            'court': '⚖️'
        };
        return icons[type] || '📌';
    }
    
    loadFallbackData() {
        // Sample data for development/fallback
        this.events = [
            { date: '2025-11-01', type: 'rent', title: 'November Rent', amount: '$1,200', icon: '💵' },
            { date: '2025-10-15', type: 'document', title: 'Lease Signed', icon: '📄' },
            { date: '2025-11-05', type: 'call', title: 'Landlord Call', icon: '📞' },
            { date: '2025-10-20', type: 'notice', title: '30-Day Notice', icon: '✉️' },
            { date: '2025-11-12', type: 'deadline', title: 'Response Due', icon: '⏰' },
            { date: '2025-11-15', type: 'court', title: 'Court Hearing', icon: '⚖️' }
        ];
    }
    
    render() {
        if (!this.container) return;
        
        this.container.innerHTML = `
            <div class="timeline-ruler-container">
                <div class="ruler-track" id="rulerTrack">
                    <div class="center-indicator"></div>
                    <div class="ruler-content" id="rulerContent">
                        <div class="ruler-line"></div>
                        <div class="ruler-marks" id="rulerMarks"></div>
                        <div class="event-items" id="eventItems"></div>
                    </div>
                </div>
            </div>
        `;
        
        this.renderRuler();
    }
    
    renderRuler() {
        const marksContainer = document.querySelector('#rulerMarks');
        const itemsContainer = document.querySelector('#eventItems');
        
        if (!marksContainer || !itemsContainer) return;
        
        marksContainer.innerHTML = '';
        itemsContainer.innerHTML = '';
        
        if (this.events.length === 0) return;
        
        // Calculate date range
        const startDate = new Date(this.events[0].date);
        startDate.setDate(startDate.getDate() - 7);
        const endDate = new Date(this.events[this.events.length - 1].date);
        endDate.setDate(endDate.getDate() + 7);
        
        // Generate ruler marks
        const pixelsPerDay = this.PIXELS_PER_DAY * this.currentZoom;
        let currentDate = new Date(startDate);
        let position = 0;
        
        while (currentDate <= endDate) {
            const isMonthStart = currentDate.getDate() === 1;
            const isWeekStart = currentDate.getDay() === 0;
            
            let markType = 'day';
            if (isMonthStart) markType = 'month';
            else if (isWeekStart) markType = 'week';
            
            const mark = document.createElement('div');
            mark.className = `ruler-mark ${markType}`;
            mark.style.left = `${position}px`;
            
            let labelText = '';
            if (markType === 'month') {
                labelText = currentDate.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
            } else if (markType === 'week') {
                labelText = currentDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            } else if (this.currentZoom > 1.5) {
                labelText = currentDate.getDate();
            }
            
            mark.innerHTML = `
                <div class="tick"></div>
                ${labelText ? `<div class="label">${labelText}</div>` : ''}
            `;
            
            marksContainer.appendChild(mark);
            
            currentDate.setDate(currentDate.getDate() + 1);
            position += pixelsPerDay;
        }
        
        // Render events
        this.events.forEach((event, index) => {
            const eventDate = new Date(event.date);
            const daysSinceStart = Math.floor((eventDate - startDate) / (1000 * 60 * 60 * 24));
            const eventPosition = daysSinceStart * pixelsPerDay;
            
            const item = document.createElement('div');
            item.className = `event-item event-${event.type}`;
            item.style.left = `${eventPosition}px`;
            item.dataset.position = eventPosition;
            item.dataset.index = index;
            
            // Alternate above/below
            if (index % 2 === 0) {
                item.classList.add('above');
            } else {
                item.classList.add('below');
            }
            
            item.innerHTML = `
                <div class="event-card">
                    <h4>${event.icon} ${event.title}</h4>
                    <div class="event-date">${new Date(event.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</div>
                    ${event.amount ? `<div class="event-amount">${event.amount}</div>` : ''}
                </div>
                <div class="event-dot"></div>
            `;
            
            item.addEventListener('click', () => this.focusEvent(item));
            itemsContainer.appendChild(item);
        });
        
        this.updateFocusedItem();
    }
    
    updateFocusedItem() {
        const track = document.querySelector('#rulerTrack');
        if (!track) return;
        
        const centerPosition = track.scrollLeft + (track.clientWidth / 2);
        const items = document.querySelectorAll('.event-item');
        let closestItem = null;
        let closestDistance = Infinity;
        
        items.forEach(item => {
            const itemPosition = parseFloat(item.dataset.position);
            const distance = Math.abs(centerPosition - itemPosition);
            
            item.classList.remove('focused');
            
            if (distance < closestDistance) {
                closestDistance = distance;
                closestItem = item;
            }
        });
        
        if (closestItem) {
            closestItem.classList.add('focused');
            closestItem.classList.remove('above', 'below');
        }
    }
    
    focusEvent(item) {
        const track = document.querySelector('#rulerTrack');
        if (!track) return;
        
        const itemPosition = parseFloat(item.dataset.position);
        const scrollTo = itemPosition - (track.clientWidth / 2);
        
        track.scrollTo({
            left: scrollTo,
            behavior: 'smooth'
        });
    }
    
    setupControls() {
        const track = document.querySelector('#rulerTrack');
        if (!track) return;
        
        let isDown = false;
        let startX;
        let scrollLeft;
        let lastDistance = 0;
        
        // Mouse drag
        track.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - track.offsetLeft;
            scrollLeft = track.scrollLeft;
        });
        
        track.addEventListener('mouseleave', () => { isDown = false; });
        track.addEventListener('mouseup', () => { isDown = false; });
        
        track.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - track.offsetLeft;
            const walk = (x - startX) * 2;
            track.scrollLeft = scrollLeft - walk;
        });
        
        // Touch controls
        track.addEventListener('touchstart', (e) => {
            startX = e.touches[0].pageX;
            scrollLeft = track.scrollLeft;
            lastDistance = 0;
        });
        
        track.addEventListener('touchmove', (e) => {
            // Pinch to zoom
            if (e.touches.length === 2) {
                const distance = Math.hypot(
                    e.touches[0].pageX - e.touches[1].pageX,
                    e.touches[0].pageY - e.touches[1].pageY
                );
                
                if (lastDistance > 0) {
                    if (distance > lastDistance && this.currentZoom < 3) {
                        this.currentZoom += 0.1;
                        this.renderRuler();
                    } else if (distance < lastDistance && this.currentZoom > 0.5) {
                        this.currentZoom -= 0.1;
                        this.renderRuler();
                    }
                }
                lastDistance = distance;
            } else {
                // Single finger swipe
                const x = e.touches[0].pageX;
                const walk = (startX - x) * 1.5;
                track.scrollLeft = scrollLeft + walk;
            }
        });
        
        track.addEventListener('touchend', () => {
            lastDistance = 0;
        });
        
        // Update focused item on scroll
        track.addEventListener('scroll', () => this.updateFocusedItem());
    }
    
    // Public method to refresh data
    async refresh() {
        await this.loadData();
        this.renderRuler();
    }
}

// Auto-initialize if timeline container exists
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('timelineWidget');
    if (container) {
        window.timelineWidget = new TimelineWidget('timelineWidget');
    }
});
