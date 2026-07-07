/**
 * 3C Intelligence — Dashboard Controller (Redesign Build)
 * ========================================================
 * Manages theme, API fetching, counter animations, visualization tabs,
 * split rankings, sortable/filterable table, pagination, city detail modal,
 * mobile nav, scroll-fade-in animations, and toast notifications.
 *
 * Supports fallback offline mode when accessed via file:// protocol.
 */

document.addEventListener('DOMContentLoaded', () => {

    // ─── 1. OFFLINE FALLBACK DATASET ─────────────────────────────────────────
    const fallbackDataset = [
        {"City":"Karachi","Population":1792743,"Murder Rate":13.68,"Assault Rate":110.88,"Theft Rate":265.1,"Crime Score":87.98,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Lahore","Population":4404572,"Murder Rate":15.74,"Assault Rate":165.94,"Theft Rate":417.06,"Crime Score":132.69,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Faisalabad","Population":2334489,"Murder Rate":11.36,"Assault Rate":81.24,"Theft Rate":202.86,"Crime Score":66.57,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Rawalpindi","Population":1670006,"Murder Rate":7.45,"Assault Rate":66.37,"Theft Rate":309.33,"Crime Score":77.40,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Gujranwala","Population":1236074,"Murder Rate":11.28,"Assault Rate":40.65,"Theft Rate":160.27,"Crime Score":45.90,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Peshawar","Population":4144887,"Murder Rate":17.21,"Assault Rate":158.8,"Theft Rate":447.16,"Crime Score":136.07,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Multan","Population":1339911,"Murder Rate":6.67,"Assault Rate":48.13,"Theft Rate":190.73,"Crime Score":51.17,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Hyderabad","Population":4572471,"Murder Rate":19.8,"Assault Rate":150.28,"Theft Rate":311.19,"Crime Score":111.86,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Islamabad","Population":2238242,"Murder Rate":7.83,"Assault Rate":76.49,"Theft Rate":230.85,"Crime Score":67.89,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Quetta","Population":4623669,"Murder Rate":22.43,"Assault Rate":183.49,"Theft Rate":416.34,"Crime Score":141.77,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Bahawalpur","Population":1866891,"Murder Rate":10.46,"Assault Rate":86.55,"Theft Rate":266.69,"Crime Score":78.53,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Sargodha","Population":4621373,"Murder Rate":18.4,"Assault Rate":160.16,"Theft Rate":398.62,"Crime Score":129.02,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Sialkot","Population":3444769,"Murder Rate":19.58,"Assault Rate":140.6,"Theft Rate":317.25,"Crime Score":109.53,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Sukkur","Population":891743,"Murder Rate":9.97,"Assault Rate":39.14,"Theft Rate":189.23,"Crime Score":49.57,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Jhang","Population":203355,"Murder Rate":4.26,"Assault Rate":54.84,"Theft Rate":156.66,"Crime Score":46.52,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Larkana","Population":1362752,"Murder Rate":10.0,"Assault Rate":78.71,"Theft Rate":135.9,"Crime Score":53.89,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Sheikhupura","Population":1496025,"Murder Rate":9.96,"Assault Rate":58.4,"Theft Rate":192.61,"Crime Score":56.55,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Mirpur Khas","Population":1407371,"Murder Rate":13.65,"Assault Rate":108.02,"Theft Rate":165.87,"Crime Score":70.48,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Rahim Yar Khan","Population":1017040,"Murder Rate":11.41,"Assault Rate":74.38,"Theft Rate":238.94,"Crime Score":70.32,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Kohat","Population":2353882,"Murder Rate":14.63,"Assault Rate":113.83,"Theft Rate":258.74,"Crime Score":88.38,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Gujrat","Population":3630409,"Murder Rate":16.66,"Assault Rate":158.09,"Theft Rate":418.92,"Crime Score":130.85,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Mardan","Population":4949115,"Murder Rate":21.12,"Assault Rate":172.46,"Theft Rate":394.89,"Crime Score":133.86,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Kasur","Population":4821339,"Murder Rate":24.14,"Assault Rate":146.32,"Theft Rate":458.58,"Crime Score":137.27,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Dera Ghazi Khan","Population":4942447,"Murder Rate":21.29,"Assault Rate":135.98,"Theft Rate":462.43,"Crime Score":133.04,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Sahiwal","Population":1600942,"Murder Rate":8.08,"Assault Rate":78.72,"Theft Rate":161.39,"Crime Score":57.18,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Nawabshah","Population":4360029,"Murder Rate":16.71,"Assault Rate":129.62,"Theft Rate":379.82,"Crime Score":114.87,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Mingora","Population":3375709,"Murder Rate":12.52,"Assault Rate":119.38,"Theft Rate":355.47,"Crime Score":105.30,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Okara","Population":184654,"Murder Rate":1.4,"Assault Rate":73.9,"Theft Rate":200.76,"Crime Score":58.79,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Mirpur (AJK)","Population":2054354,"Murder Rate":10.79,"Assault Rate":80.57,"Theft Rate":217.09,"Crime Score":68.43,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Chiniot","Population":2516182,"Murder Rate":11.95,"Assault Rate":77.72,"Theft Rate":225.51,"Crime Score":69.47,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Kamoke","Population":3574675,"Murder Rate":14.28,"Assault Rate":120.03,"Theft Rate":369.45,"Crime Score":108.72,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Hafizabad","Population":2752991,"Murder Rate":9.25,"Assault Rate":138.45,"Theft Rate":339.21,"Crime Score":107.31,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Sadiqabad","Population":2528388,"Murder Rate":10.22,"Assault Rate":88.52,"Theft Rate":248.04,"Crime Score":75.96,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Turbat","Population":628178,"Murder Rate":9.02,"Assault Rate":68.27,"Theft Rate":96.53,"Crime Score":43.36,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Muzaffargarh","Population":2763046,"Murder Rate":16.26,"Assault Rate":75.25,"Theft Rate":362.06,"Crime Score":93.56,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Khanewal","Population":2686644,"Murder Rate":14.37,"Assault Rate":98.03,"Theft Rate":265.4,"Crime Score":84.10,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Dera Ismail Khan","Population":2670406,"Murder Rate":17.21,"Assault Rate":94.28,"Theft Rate":284.9,"Crime Score":87.51,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Gojra","Population":3516664,"Murder Rate":17.32,"Assault Rate":105.2,"Theft Rate":387.65,"Crime Score":108.34,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Mandi Bahauddin","Population":3485659,"Murder Rate":19.6,"Assault Rate":130.3,"Theft Rate":358.33,"Crime Score":112.96,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Abbottabad","Population":3485357,"Murder Rate":19.01,"Assault Rate":126.84,"Theft Rate":368.44,"Crime Score":113.19,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Hub","Population":2895513,"Murder Rate":13.6,"Assault Rate":126.93,"Theft Rate":245.29,"Crime Score":90.0,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Khuzdar","Population":1565689,"Murder Rate":6.35,"Assault Rate":64.75,"Theft Rate":225.8,"Crime Score":62.39,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Muridke","Population":168148,"Murder Rate":4.55,"Assault Rate":28.76,"Theft Rate":172.18,"Crime Score":40.56,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Tando Adam","Population":1925665,"Murder Rate":12.61,"Assault Rate":66.49,"Theft Rate":193.18,"Crime Score":60.67,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Khairpur","Population":2845683,"Murder Rate":15.4,"Assault Rate":92.55,"Theft Rate":236.64,"Crime Score":78.0,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Pakpattan","Population":3497723,"Murder Rate":16.72,"Assault Rate":132.28,"Theft Rate":411.12,"Crime Score":120.97,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Jhelum","Population":3103758,"Murder Rate":12.67,"Assault Rate":111.83,"Theft Rate":309.47,"Crime Score":95.19,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Gilgit","Population":4156518,"Murder Rate":18.47,"Assault Rate":113.89,"Theft Rate":326.14,"Crime Score":101.55,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Muzaffarabad","Population":2769995,"Murder Rate":12.62,"Assault Rate":93.16,"Theft Rate":371.93,"Crime Score":99.35,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Jacobabad","Population":4550812,"Murder Rate":23.37,"Assault Rate":136.28,"Theft Rate":468.45,"Crime Score":135.19,"Risk Level":"High-Risk 🚨","Cluster":1}
    ];

    // ─── 2. STATE STORE ───────────────────────────────────────────────────────
    const state = {
        cities: [],
        filteredCities: [],
        currentPage: 1,
        pageSize: 10,
        sortBy: 'Crime Score',
        sortOrder: 'desc',
        theme: localStorage.getItem('3c-theme') || 'dark',
        activePlot: 'clustering_results.png',
        isLocalFile: window.location.protocol === 'file:'
    };

    // ─── 3. DOM CACHE ─────────────────────────────────────────────────────────
    const el = {
        html: document.documentElement,
        themeToggle: document.getElementById('themeToggle'),
        mobileMenuBtn: document.getElementById('mobileMenuBtn'),
        mobileNav: document.getElementById('mobileNav'),

        // Stats
        statTotal: document.getElementById('stat-total-cities'),
        statSafe: document.getElementById('stat-safe-cities'),
        statMod: document.getElementById('stat-mod-cities'),
        statHigh: document.getElementById('stat-high-cities'),
        pctSafe: document.getElementById('pct-safe'),
        pctMod: document.getElementById('pct-mod'),
        pctHigh: document.getElementById('pct-high'),

        // Split ranking lists
        safestList: document.getElementById('safest-cities-list'),
        dangerousList: document.getElementById('dangerous-cities-list'),

        // Plot
        tabButtons: document.querySelectorAll('.plot-tab'),
        plotImage: document.getElementById('activePlotImage'),
        plotLoader: document.getElementById('plotLoader'),
        downloadPlot: document.getElementById('downloadPlot'),

        // Table
        tableBody: document.getElementById('tableBody'),
        tableSearch: document.getElementById('tableSearch'),
        tableFilter: document.getElementById('tableFilter'),
        tableHeaders: document.querySelectorAll('.data-table th.col-sortable'),
        paginationInfo: document.getElementById('paginationInfo'),
        prevPageBtn: document.getElementById('prevPageBtn'),
        nextPageBtn: document.getElementById('nextPageBtn'),
        pageNumbers: document.getElementById('pageNumbers'),

        // Modal
        detailsModal: document.getElementById('detailsModal'),
        modalCloseBtn: document.getElementById('modalCloseBtn'),
        modalBackdrop: document.getElementById('modalBackdrop'),
        modalCityName: document.getElementById('modalCityName'),
        modalBody: document.getElementById('modalBody'),

        // Toast
        toastContainer: document.getElementById('toastContainer')
    };

    // ─── 4. THEME MANAGEMENT ─────────────────────────────────────────────────
    function initTheme() {
        el.html.setAttribute('data-theme', state.theme);
    }

    function toggleTheme() {
        state.theme = state.theme === 'dark' ? 'light' : 'dark';
        el.html.setAttribute('data-theme', state.theme);
        localStorage.setItem('3c-theme', state.theme);
        showToast(`Switched to ${state.theme === 'dark' ? 'Dark' : 'Light'} mode`);
    }

    el.themeToggle.addEventListener('click', toggleTheme);

    // ─── 5. MOBILE NAV ───────────────────────────────────────────────────────
    el.mobileMenuBtn.addEventListener('click', () => {
        const isOpen = el.mobileNav.classList.toggle('open');
        el.mobileNav.setAttribute('aria-hidden', String(!isOpen));
    });

    document.querySelectorAll('.mobile-nav-item').forEach(link => {
        link.addEventListener('click', () => {
            el.mobileNav.classList.remove('open');
            el.mobileNav.setAttribute('aria-hidden', 'true');
        });
    });

    // ─── 6. SCROLL FADE-IN ───────────────────────────────────────────────────
    function initScrollAnimations() {
        const targets = document.querySelectorAll(
            '.bento-cell, .split-panel, .method-card, .plot-card, .table-panel, .hero-copy, .hero-viz'
        );
        targets.forEach(el => el.classList.add('fade-in-up'));

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, i * 60);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.08 });

        targets.forEach(t => observer.observe(t));
    }

    // ─── 7. TOAST NOTIFICATION ───────────────────────────────────────────────
    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        el.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(20px)';
            toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            setTimeout(() => toast.remove(), 350);
        }, 3000);
    }

    // ─── 8. DATA FETCHING ────────────────────────────────────────────────────
    async function fetchDashboardData() {
        if (state.isLocalFile) {
            console.log('Local file access: using embedded dataset.');
            state.cities = fallbackDataset;
            state.filteredCities = [...state.cities];
            el.plotImage.src = '../static/plots/clustering_results.png';
            el.downloadPlot.href = '../static/plots/clustering_results.png';
            renderStatsOverview();
            renderSplitRankings();
            applyTableProcessing();
            showToast('Offline mode: embedded dataset loaded');
            return;
        }

        try {
            const [dataRes, statsRes] = await Promise.all([
                fetch('/api/data'),
                fetch('/api/stats')
            ]);
            if (!dataRes.ok || !statsRes.ok) throw new Error('API error');
            state.cities = await dataRes.json();
            state.filteredCities = [...state.cities];
            renderStatsOverview();
            renderSplitRankings();
            applyTableProcessing();
            showToast('Dashboard data loaded');
        } catch (err) {
            console.warn('API unreachable, using fallback dataset.', err);
            state.cities = fallbackDataset;
            state.filteredCities = [...state.cities];
            renderStatsOverview();
            renderSplitRankings();
            applyTableProcessing();
            showToast('Offline mode: embedded dataset loaded');
        }
    }

    // ─── 9. ANIMATED COUNTER ─────────────────────────────────────────────────
    function animateCounter(element, targetValue) {
        if (!element) return;
        if (targetValue === 0) { element.textContent = '0'; return; }
        const duration = 1100;
        const steps = Math.min(targetValue, 60);
        const stepTime = duration / steps;
        let current = 0;
        const increment = targetValue / steps;

        const timer = setInterval(() => {
            current = Math.min(current + increment, targetValue);
            element.textContent = Math.round(current);
            if (current >= targetValue) {
                element.textContent = targetValue;
                clearInterval(timer);
            }
        }, stepTime);
    }

    // ─── 10. STATS OVERVIEW ──────────────────────────────────────────────────
    function renderStatsOverview() {
        const total = state.cities.length;
        const safeCount = state.cities.filter(c => c['Risk Level'].includes('Safe')).length;
        const modCount  = state.cities.filter(c => c['Risk Level'].includes('Moderate')).length;
        const highCount = state.cities.filter(c => c['Risk Level'].includes('High-Risk')).length;

        animateCounter(el.statTotal, total);
        animateCounter(el.statSafe, safeCount);
        animateCounter(el.statMod,  modCount);
        animateCounter(el.statHigh, highCount);

        if (el.pctSafe) el.pctSafe.textContent = `${Math.round((safeCount / total) * 100)}% of jurisdictions`;
        if (el.pctMod)  el.pctMod.textContent  = `${Math.round((modCount  / total) * 100)}% of jurisdictions`;
        if (el.pctHigh) el.pctHigh.textContent = `${Math.round((highCount / total) * 100)}% of jurisdictions`;
    }

    // ─── 11. SPLIT RANKINGS ──────────────────────────────────────────────────
    function renderSplitRankings() {
        const maxScore = Math.max(...state.cities.map(c => c['Crime Score']), 150);
        const sortedSafe = [...state.cities].sort((a, b) => a['Crime Score'] - b['Crime Score']).slice(0, 5);
        const sortedHigh = [...state.cities].sort((a, b) => b['Crime Score'] - a['Crime Score']).slice(0, 5);

        const buildRow = (c, maxS) => {
            const pct = Math.round((c['Crime Score'] / maxS) * 100);
            return `
                <div class="city-row" data-city-name="${c['City']}" style="cursor:pointer;">
                    <div class="city-row-left">
                        <span class="city-row-name">${c['City']}</span>
                        <span class="city-row-pop">Pop. ${c['Population'].toLocaleString()}</span>
                    </div>
                    <div class="city-row-right">
                        <span class="city-row-score">${c['Crime Score'].toFixed(2)}</span>
                        <div class="city-score-bar">
                            <div class="city-score-fill" style="width: ${pct}%;"></div>
                        </div>
                    </div>
                </div>
            `;
        };

        if (el.safestList) {
            el.safestList.innerHTML = sortedSafe.map(c => buildRow(c, maxScore)).join('');
        }
        if (el.dangerousList) {
            el.dangerousList.innerHTML = sortedHigh.map(c => buildRow(c, maxScore)).join('');
        }

        // Bind city-row click to modal
        document.querySelectorAll('#safest-cities-list .city-row, #dangerous-cities-list .city-row').forEach(row => {
            row.addEventListener('click', () => {
                const name = row.getAttribute('data-city-name');
                const match = state.cities.find(c => c['City'] === name);
                if (match) openCityModal(match);
            });
        });
    }

    // ─── 12. VISUALIZATION TABS ──────────────────────────────────────────────
    el.tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            el.tabButtons.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected', 'false'); });
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');

            const plotName = btn.getAttribute('data-plot');
            state.activePlot = plotName;

            el.plotLoader.classList.add('active');
            el.plotImage.classList.remove('loaded');

            const basePath = state.isLocalFile ? '../static/plots/' : '/api/plots/';
            const src = basePath + plotName;
            el.plotImage.src = src;
            el.downloadPlot.href = src;
        });
    });

    if (el.plotImage) {
        el.plotImage.addEventListener('load', () => {
            el.plotLoader.classList.remove('active');
            el.plotImage.classList.add('loaded');
        });
        el.plotImage.addEventListener('error', () => {
            el.plotLoader.classList.remove('active');
            showToast('Visualization could not be loaded');
        });
    }

    // ─── 13. TABLE: SEARCH, FILTER, SORT ─────────────────────────────────────
    if (el.tableSearch) {
        el.tableSearch.addEventListener('input', () => {
            state.currentPage = 1;
            applyTableProcessing();
        });
    }

    if (el.tableFilter) {
        el.tableFilter.addEventListener('change', () => {
            state.currentPage = 1;
            applyTableProcessing();
        });
    }

    el.tableHeaders.forEach(th => {
        th.addEventListener('click', () => {
            const field = th.getAttribute('data-sort');
            if (state.sortBy === field) {
                state.sortOrder = state.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                state.sortBy = field;
                state.sortOrder = 'desc';
            }

            el.tableHeaders.forEach(h => {
                h.classList.remove('active', 'asc', 'desc');
                const ind = h.querySelector('.sort-ind');
                if (ind) ind.className = 'sort-ind';
            });

            th.classList.add('active');
            const ind = th.querySelector('.sort-ind');
            if (ind) ind.className = `sort-ind ${state.sortOrder}`;

            applyTableProcessing();
        });
    });

    function applyTableProcessing() {
        const query = el.tableSearch ? el.tableSearch.value.trim().toLowerCase() : '';
        const riskFilter = el.tableFilter ? el.tableFilter.value : 'all';

        state.filteredCities = state.cities.filter(c => {
            const matchSearch = c['City'].toLowerCase().includes(query);
            let matchFilter = true;
            if (riskFilter === 'safe') matchFilter = c['Risk Level'].includes('Safe') && !c['Risk Level'].includes('Moderate') && !c['Risk Level'].includes('High');
            else if (riskFilter === 'moderate') matchFilter = c['Risk Level'].includes('Moderate');
            else if (riskFilter === 'high') matchFilter = c['Risk Level'].includes('High-Risk');
            return matchSearch && matchFilter;
        });

        state.filteredCities.sort((a, b) => {
            const valA = a[state.sortBy];
            const valB = b[state.sortBy];
            if (typeof valA === 'string') {
                return state.sortOrder === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return state.sortOrder === 'asc' ? valA - valB : valB - valA;
        });

        renderTableBody();
    }

    // ─── 14. TABLE BODY RENDER ───────────────────────────────────────────────
    function getRiskBadge(riskLevel) {
        let cls = 'rb-safe', label = 'Safe';
        if (riskLevel.includes('Moderate')) { cls = 'rb-moderate'; label = 'Moderate Risk'; }
        else if (riskLevel.includes('High-Risk')) { cls = 'rb-high'; label = 'High-Risk'; }
        return `<span class="risk-badge ${cls}">${label}</span>`;
    }

    function renderTableBody() {
        const total = state.filteredCities.length;
        const start = (state.currentPage - 1) * state.pageSize;
        const end   = Math.min(start + state.pageSize, total);
        const items = state.filteredCities.slice(start, end);

        if (total === 0) {
            el.tableBody.innerHTML = `
                <tr><td colspan="7" style="text-align:center; padding:48px; color:var(--c-text-3); font-family:var(--ff-head);">
                    No jurisdictions match the current filters.
                </td></tr>
            `;
            updatePagination(0, 0, 0);
            return;
        }

        el.tableBody.innerHTML = items.map(c => `
            <tr class="table-city-row" data-city-name="${c['City']}">
                <td class="td-city">${c['City']}</td>
                <td class="td-num">${c['Population'].toLocaleString()}</td>
                <td class="td-num">${c['Murder Rate'].toFixed(2)}</td>
                <td class="td-num">${c['Assault Rate'].toFixed(2)}</td>
                <td class="td-num">${c['Theft Rate'].toFixed(2)}</td>
                <td class="td-num" style="font-family:var(--ff-head); font-weight:700; color:var(--c-indigo-light);">${c['Crime Score'].toFixed(2)}</td>
                <td>${getRiskBadge(c['Risk Level'])}</td>
            </tr>
        `).join('');

        document.querySelectorAll('.table-city-row').forEach(row => {
            row.addEventListener('click', () => {
                const name = row.getAttribute('data-city-name');
                const match = state.cities.find(c => c['City'] === name);
                if (match) openCityModal(match);
            });
        });

        updatePagination(start + 1, end, total);
    }

    // ─── 15. PAGINATION ──────────────────────────────────────────────────────
    function updatePagination(start, end, total) {
        if (el.paginationInfo) {
            el.paginationInfo.textContent = total === 0
                ? 'No entries found'
                : `Showing ${start}–${end} of ${total} jurisdictions`;
        }

        const totalPages = Math.ceil(total / state.pageSize);

        if (el.prevPageBtn) el.prevPageBtn.disabled = state.currentPage <= 1;
        if (el.nextPageBtn) el.nextPageBtn.disabled = state.currentPage >= totalPages || totalPages === 0;

        if (el.pageNumbers) {
            el.pageNumbers.innerHTML = '';
            for (let i = 1; i <= totalPages; i++) {
                const btn = document.createElement('button');
                btn.className = `page-num-btn ${state.currentPage === i ? 'active' : ''}`;
                btn.textContent = i;
                btn.setAttribute('aria-label', `Go to page ${i}`);
                btn.addEventListener('click', () => {
                    state.currentPage = i;
                    renderTableBody();
                });
                el.pageNumbers.appendChild(btn);
            }
        }
    }

    if (el.prevPageBtn) {
        el.prevPageBtn.addEventListener('click', () => {
            if (state.currentPage > 1) { state.currentPage--; renderTableBody(); }
        });
    }

    if (el.nextPageBtn) {
        el.nextPageBtn.addEventListener('click', () => {
            const totalPages = Math.ceil(state.filteredCities.length / state.pageSize);
            if (state.currentPage < totalPages) { state.currentPage++; renderTableBody(); }
        });
    }

    // ─── 16. CITY DETAIL MODAL ───────────────────────────────────────────────
    function getRiskColor(riskLevel) {
        if (riskLevel.includes('Moderate')) return 'var(--c-amber)';
        if (riskLevel.includes('High-Risk')) return 'var(--c-crimson)';
        return 'var(--c-emerald)';
    }

    function getRiskLabel(riskLevel) {
        if (riskLevel.includes('Moderate')) return 'Moderate Risk';
        if (riskLevel.includes('High-Risk')) return 'High-Risk';
        return 'Safe';
    }

    function openCityModal(city) {
        if (!el.modalCityName || !el.modalBody || !el.detailsModal) return;

        const color = getRiskColor(city['Risk Level']);
        const label = getRiskLabel(city['Risk Level']);

        el.modalCityName.textContent = city['City'];
        el.modalBody.innerHTML = `
            <div style="display:flex; align-items:center; justify-content:space-between; padding:16px 20px; background:var(--c-bg-2); border-radius:var(--r-md); margin-bottom:20px; border:1px solid var(--c-border);">
                <div>
                    <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.06em; color:var(--c-text-3); font-family:var(--ff-head); font-weight:600; margin-bottom:4px;">Classification</div>
                    <div style="font-family:var(--ff-head); font-size:16px; font-weight:700; color:${color};">${label}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.06em; color:var(--c-text-3); font-family:var(--ff-head); font-weight:600; margin-bottom:4px;">Crime Index</div>
                    <div style="font-family:var(--ff-head); font-size:26px; font-weight:700; color:var(--c-indigo-light); line-height:1; padding-bottom:0.05em;">${city['Crime Score'].toFixed(2)}</div>
                </div>
            </div>

            <div class="modal-metric-row">
                <span class="modal-metric-label">Population</span>
                <span class="modal-metric-value">${city['Population'].toLocaleString()}</span>
            </div>
            <div class="modal-metric-row">
                <span class="modal-metric-label">Murder Rate (per 100k)</span>
                <span class="modal-metric-value" style="color:var(--c-crimson);">${city['Murder Rate'].toFixed(2)}</span>
            </div>
            <div class="modal-metric-row">
                <span class="modal-metric-label">Assault Rate (per 100k)</span>
                <span class="modal-metric-value" style="color:var(--c-amber);">${city['Assault Rate'].toFixed(2)}</span>
            </div>
            <div class="modal-metric-row">
                <span class="modal-metric-label">Theft Rate (per 100k)</span>
                <span class="modal-metric-value">${city['Theft Rate'].toFixed(2)}</span>
            </div>
            <div class="modal-metric-row" style="border-bottom:none;">
                <span class="modal-metric-label">K-Means Cluster ID</span>
                <span class="modal-metric-value">Cluster ${city['Cluster']}</span>
            </div>

            <div style="margin-top:16px; padding:14px 16px; background:var(--c-indigo-dim); border:1px solid rgba(var(--c-indigo-rgb),0.15); border-radius:var(--r-md); font-size:13px; color:var(--c-text-2); line-height:1.6;">
                Grouped into Cluster&nbsp;<strong style="color:var(--c-indigo-light);">${city['Cluster']}</strong> by K-Means minimizing Euclidean distance to the nearest centroid across all StandardScaler-normalized features.
            </div>
        `;

        el.detailsModal.classList.add('open');
        el.detailsModal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        if (!el.detailsModal) return;
        el.detailsModal.classList.remove('open');
        el.detailsModal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    if (el.modalCloseBtn) el.modalCloseBtn.addEventListener('click', closeModal);
    if (el.modalBackdrop) el.modalBackdrop.addEventListener('click', closeModal);

    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && el.detailsModal && el.detailsModal.classList.contains('open')) {
            closeModal();
        }
    });

    // ─── 17. ACTIVE NAV HIGHLIGHT (scroll-based) ─────────────────────────────
    function initNavHighlight() {
        const sections = ['overview', 'visualization', 'rankings', 'insights'];
        const navItems = {
            overview:      document.getElementById('nav-dashboard'),
            visualization: document.getElementById('nav-analytics'),
            rankings:      document.getElementById('nav-rankings'),
            insights:      document.getElementById('nav-methodology')
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.id;
                    Object.values(navItems).forEach(n => n && n.classList.remove('active'));
                    if (navItems[id]) navItems[id].classList.add('active');
                }
            });
        }, { rootMargin: '-40% 0px -50% 0px' });

        sections.forEach(id => {
            const el = document.getElementById(id);
            if (el) observer.observe(el);
        });
    }

    // ─── 18. INITIALIZE ──────────────────────────────────────────────────────
    initTheme();
    initScrollAnimations();
    initNavHighlight();
    fetchDashboardData();
});
