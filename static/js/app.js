/**
 * AI Crime Intelligence System - Dashboard Controller
 * ===================================================
 * Manages states, dynamic API fetching, client-side rendering, search filters,
 * pagination, micro-interactions, modal dialogs, and persistent theme toggles.
 * 
 * Supports fallback demo mode for direct filesystem access (file://).
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Fallback Offline Dataset for direct file viewing (Double Click)
    const fallbackDataset = [
        {"City":"Karachi","Population":1792743,"Murder Rate":13.68,"Assault Rate":110.88,"Theft Rate":265.1,"Crime Score":87.98333333333335,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Lahore","Population":4404572,"Murder Rate":15.74,"Assault Rate":165.94,"Theft Rate":417.06,"Crime Score":132.69333333333336,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Faisalabad","Population":2334489,"Murder Rate":11.36,"Assault Rate":81.24,"Theft Rate":202.86,"Crime Score":66.57000000000001,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Rawalpindi","Population":1670006,"Murder Rate":7.45,"Assault Rate":66.37,"Theft Rate":309.33,"Crime Score":77.40333333333332,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Gujranwala","Population":1236074,"Murder Rate":11.28,"Assault Rate":40.65,"Theft Rate":160.27,"Crime Score":45.901666666666664,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Peshawar","Population":4144887,"Murder Rate":17.21,"Assault Rate":158.8,"Theft Rate":447.16,"Crime Score":136.06500000000003,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Multan","Population":1339911,"Murder Rate":6.67,"Assault Rate":48.13,"Theft Rate":190.73,"Crime Score":51.166666666666664,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Hyderabad","Population":4572471,"Murder Rate":19.8,"Assault Rate":150.28,"Theft Rate":311.19,"Crime Score":111.85833333333335,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Islamabad","Population":2238242,"Murder Rate":7.83,"Assault Rate":76.49,"Theft Rate":230.85,"Crime Score":67.88666666666667,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Quetta","Population":4623669,"Murder Rate":22.43,"Assault Rate":183.49,"Theft Rate":416.34,"Crime Score":141.76833333333332,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Bahawalpur","Population":1866891,"Murder Rate":10.46,"Assault Rate":86.55,"Theft Rate":266.69,"Crime Score":78.52833333333332,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Sargodha","Population":4621373,"Murder Rate":18.4,"Assault Rate":160.16,"Theft Rate":398.62,"Crime Score":129.02333333333334,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Sialkot","Population":3444769,"Murder Rate":19.58,"Assault Rate":140.6,"Theft Rate":317.25,"Crime Score":109.53166666666668,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Sukkur","Population":891743,"Murder Rate":9.97,"Assault Rate":39.14,"Theft Rate":189.23,"Crime Score":49.56999999999999,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Jhang","Population":203355,"Murder Rate":4.26,"Assault Rate":54.84,"Theft Rate":156.66,"Crime Score":46.52,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Larkana","Population":1362752,"Murder Rate":10.0,"Assault Rate":78.71,"Theft Rate":135.9,"Crime Score":53.88666666666666,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Sheikhupura","Population":1496025,"Murder Rate":9.96,"Assault Rate":58.4,"Theft Rate":192.61,"Crime Score":56.54833333333334,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Mirpur Khas","Population":1407371,"Murder Rate":13.65,"Assault Rate":108.02,"Theft Rate":165.87,"Crime Score":70.47666666666667,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Rahim Yar Khan","Population":1017040,"Murder Rate":11.41,"Assault Rate":74.38,"Theft Rate":238.94,"Crime Score":70.32166666666667,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Kohat","Population":2353882,"Murder Rate":14.63,"Assault Rate":113.83,"Theft Rate":258.74,"Crime Score":88.38166666666666,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Gujrat","Population":3630409,"Murder Rate":16.66,"Assault Rate":158.09,"Theft Rate":418.92,"Crime Score":130.84666666666666,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Mardan","Population":4949115,"Murder Rate":21.12,"Assault Rate":172.46,"Theft Rate":394.89,"Crime Score":133.86166666666668,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Kasur","Population":4821339,"Murder Rate":24.14,"Assault Rate":146.32,"Theft Rate":458.58,"Crime Score":137.27333333333334,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Dera Ghazi Khan","Population":4942447,"Murder Rate":21.29,"Assault Rate":135.98,"Theft Rate":462.43,"Crime Score":133.04333333333332,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Sahiwal","Population":1600942,"Murder Rate":8.08,"Assault Rate":78.72,"Theft Rate":161.39,"Crime Score":57.178333333333335,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Nawabshah","Population":4360029,"Murder Rate":16.71,"Assault Rate":129.62,"Theft Rate":379.82,"Crime Score":114.86500000000001,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Mingora","Population":3375709,"Murder Rate":12.52,"Assault Rate":119.38,"Theft Rate":355.47,"Crime Score":105.29833333333333,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Okara","Population":184654,"Murder Rate":1.4,"Assault Rate":73.9,"Theft Rate":200.76,"Crime Score":58.79333333333333,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Mirpur (AJK)","Population":2054354,"Murder Rate":10.79,"Assault Rate":80.57,"Theft Rate":217.09,"Crime Score":68.43333333333334,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Chiniot","Population":2516182,"Murder Rate":11.95,"Assault Rate":77.72,"Theft Rate":225.51,"Crime Score":69.46666666666665,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Kamoke","Population":3574675,"Murder Rate":14.28,"Assault Rate":120.03,"Theft Rate":369.45,"Crime Score":108.72499999999998,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Hafizabad","Population":2752991,"Murder Rate":9.25,"Assault Rate":138.45,"Theft Rate":339.21,"Crime Score":107.30999999999999,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Sadiqabad","Population":2528388,"Murder Rate":10.22,"Assault Rate":88.52,"Theft Rate":248.04,"Crime Score":75.95666666666666,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Turbat","Population":628178,"Murder Rate":9.02,"Assault Rate":68.27,"Theft Rate":96.53,"Crime Score":43.355,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Muzaffargarh","Population":2763046,"Murder Rate":16.26,"Assault Rate":75.25,"Theft Rate":362.06,"Crime Score":93.55666666666667,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Khanewal","Population":2686644,"Murder Rate":14.37,"Assault Rate":98.03,"Theft Rate":265.4,"Crime Score":84.095,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Dera Ismail Khan","Population":2670406,"Murder Rate":17.21,"Assault Rate":94.28,"Theft Rate":284.9,"Crime Score":87.51499999999999,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Gojra","Population":3516664,"Murder Rate":17.32,"Assault Rate":105.2,"Theft Rate":387.65,"Crime Score":108.335,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Mandi Bahauddin","Population":3485659,"Murder Rate":19.6,"Assault Rate":130.3,"Theft Rate":358.33,"Crime Score":112.955,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Abbottabad","Population":3485357,"Murder Rate":19.01,"Assault Rate":126.84,"Theft Rate":368.44,"Crime Score":113.19166666666668,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Hub","Population":2895513,"Murder Rate":13.6,"Assault Rate":126.93,"White Rate":245.29,"Theft Rate":245.29,"Crime Score":89.99166666666667,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Khuzdar","Population":1565689,"Murder Rate":6.35,"Assault Rate":64.75,"Theft Rate":225.8,"Crime Score":62.39166666666667,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Muridke","Population":168148,"Murder Rate":4.55,"Assault Rate":28.76,"Theft Rate":172.18,"Crime Score":40.55833333333334,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Tando Adam","Population":1925665,"Murder Rate":12.61,"Assault Rate":66.49,"Theft Rate":193.18,"Crime Score":60.665,"Risk Level":"Safe ✅","Cluster":2},
        {"City":"Khairpur","Population":2845683,"Murder Rate":15.4,"Assault Rate":92.55,"Theft Rate":236.64,"Crime Score":77.99,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Pakpattan","Population":3497723,"Murder Rate":16.72,"Assault Rate":132.28,"Theft Rate":411.12,"Crime Score":120.97333333333334,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Jhelum","Population":3103758,"Murder Rate":12.67,"Assault Rate":111.83,"Theft Rate":309.47,"Crime Score":95.19000000000001,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Gilgit","Population":4156518,"Murder Rate":18.47,"Assault Rate":113.89,"Theft Rate":326.14,"Crime Score":101.55499999999999,"Risk Level":"High-Risk 🚨","Cluster":1},
        {"City":"Muzaffarabad","Population":2769995,"Murder Rate":12.62,"Assault Rate":93.16,"Theft Rate":371.93,"Crime Score":99.35166666666667,"Risk Level":"Moderate Risk ⚠️","Cluster":0},
        {"City":"Jacobabad","Population":4550812,"Murder Rate":23.37,"Assault Rate":136.28,"Theft Rate":468.45,"Crime Score":135.18666666666667,"Risk Level":"High-Risk 🚨","Cluster":1}
    ];

    // 2. Core State Store
    const state = {
        cities: [],          // Raw city data list
        stats: [],           // Summarized category metrics
        filteredCities: [],   // Search/filter active list
        currentPage: 1,
        pageSize: 10,
        sortBy: 'Crime Score',
        sortOrder: 'desc',   // 'asc' or 'desc'
        theme: localStorage.getItem('theme') || 'light',
        activePlot: 'clustering_results.png',
        isLocalFile: window.location.protocol === 'file:'
    };

    // 3. DOM Elements Cache
    const el = {
        html: document.documentElement,
        themeToggle: document.getElementById('themeToggle'),
        sunIcon: document.querySelector('.sun-icon'),
        moonIcon: document.querySelector('.moon-icon'),
        navbar: document.getElementById('navbar'),
        mobileMenuBtn: document.getElementById('mobileMenuBtn'),
        mobileNav: document.getElementById('mobileNav'),
        
        // Stats Elements
        statTotal: document.getElementById('stat-total-cities'),
        statSafe: document.getElementById('stat-safe-cities'),
        statMod: document.getElementById('stat-mod-cities'),
        statHigh: document.getElementById('stat-high-cities'),
        pctSafe: document.getElementById('pct-safe'),
        pctMod: document.getElementById('pct-mod'),
        pctHigh: document.getElementById('pct-high'),
        
        // Split lists
        safestList: document.getElementById('safest-cities-list'),
        dangerousList: document.getElementById('dangerous-cities-list'),
        
        // Plot Elements
        tabButtons: document.querySelectorAll('.tab-btn'),
        plotImage: document.getElementById('activePlotImage'),
        plotLoader: document.getElementById('plotLoader'),
        downloadPlotLink: document.getElementById('downloadPlot'),
        
        // Table Elements
        tableBody: document.getElementById('tableBody'),
        tableSearch: document.getElementById('tableSearch'),
        tableFilter: document.getElementById('tableFilter'),
        tableHeaders: document.querySelectorAll('.data-table th.sortable'),
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

    // ==========================================================================
    // Theme Management
    // ==========================================================================
    function initTheme() {
        el.html.setAttribute('data-theme', state.theme);
        updateThemeToggleIcons();
    }

    function toggleTheme() {
        state.theme = state.theme === 'dark' ? 'light' : 'dark';
        el.html.setAttribute('data-theme', state.theme);
        localStorage.setItem('theme', state.theme);
        updateThemeToggleIcons();
        showToast(`Switched to ${state.theme === 'dark' ? 'Dark' : 'Light'} Mode`);
    }

    function updateThemeToggleIcons() {
        if (state.theme === 'dark') {
            el.sunIcon.style.display = 'block';
            el.moonIcon.style.display = 'none';
        } else {
            el.sunIcon.style.display = 'none';
            el.moonIcon.style.display = 'block';
        }
    }

    // ==========================================================================
    // Navbar Scroll & Mobile Actions
    // ==========================================================================
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            el.navbar.classList.add('scrolled');
        } else {
            el.navbar.classList.remove('scrolled');
        }
    });

    el.mobileMenuBtn.addEventListener('click', () => {
        el.mobileNav.classList.toggle('active');
    });

    // Close mobile nav on link click
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', () => {
            el.mobileNav.classList.remove('active');
        });
    });

    // ==========================================================================
    // Toast Notification System
    // ==========================================================================
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = 'toast';
        
        const iconSVG = `
            <svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
        `;
        
        toast.innerHTML = `${iconSVG}<span>${message}</span>`;
        el.toastContainer.appendChild(toast);
        
        // Remove toast after animation finishes
        setTimeout(() => {
            toast.style.animation = 'toastIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) reverse forwards';
            toast.addEventListener('animationend', () => {
                toast.remove();
            });
        }, 3000);
    }

    // ==========================================================================
    // API Data Fetching / Offline Fallback Load
    // ==========================================================================
    async function fetchDashboardData() {
        if (state.isLocalFile) {
            // Local file viewing (file://) fallback loader
            console.log("Local browser access detected. Utilizing embedded pipeline dataset.");
            state.cities = fallbackDataset;
            state.filteredCities = [...state.cities];
            
            // Adjust plot source URL to refer to relative parent folder rather than API routes
            el.plotImage.src = "../static/plots/clustering_results.png";
            el.downloadPlotLink.href = "../static/plots/clustering_results.png";

            renderStatsOverview();
            renderSplitRankings();
            applyTableProcessing();
            
            showToast("Offline System: Loaded local fallback datasets.", "info");
            return;
        }

        try {
            const [dataRes, statsRes] = await Promise.all([
                fetch('/api/data'),
                fetch('/api/stats')
            ]);

            if (!dataRes.ok || !statsRes.ok) {
                throw new Error("Failed to load backend API data.");
            }

            state.cities = await dataRes.json();
            state.stats = await statsRes.json();
            state.filteredCities = [...state.cities];

            // Render components
            renderStatsOverview();
            renderSplitRankings();
            applyTableProcessing();
            showToast("Intelligence dashboard populated successfully", "success");
        } catch (err) {
            console.error("API failed. Falling back to embedded dataset.", err);
            // Fallback inside server environments in case of network discrepancies
            state.cities = fallbackDataset;
            state.filteredCities = [...state.cities];
            renderStatsOverview();
            renderSplitRankings();
            applyTableProcessing();
            showToast("System Warning: Server API unreachable. Operating in Offline mode.", "warning");
        }
    }

    // ==========================================================================
    // Metric Overview Rendering (with Counter Animation)
    // ==========================================================================
    function renderStatsOverview() {
        const total = state.cities.length;
        
        // Extract counts by risk labels
        const safeCount = state.cities.filter(c => c['Risk Level'].includes('Safe')).length;
        const modCount = state.cities.filter(c => c['Risk Level'].includes('Moderate')).length;
        const highCount = state.cities.filter(c => c['Risk Level'].includes('High-Risk')).length;

        // Animate counter values
        animateCounter(el.statTotal, total);
        animateCounter(el.statSafe, safeCount);
        animateCounter(el.statMod, modCount);
        animateCounter(el.statHigh, highCount);

        // Update percentages
        el.pctSafe.textContent = `${((safeCount / total) * 100).toFixed(0)}% of total`;
        el.pctMod.textContent = `${((modCount / total) * 100).toFixed(0)}% of total`;
        el.pctHigh.textContent = `${((highCount / total) * 100).toFixed(0)}% of total`;
    }

    function animateCounter(element, targetValue) {
        let start = 0;
        const duration = 1200; // ms
        const stepTime = Math.abs(Math.floor(duration / targetValue)) || 20;
        
        if (targetValue === 0) {
            element.textContent = "0";
            return;
        }

        const timer = setInterval(() => {
            start += 1;
            element.textContent = start;
            if (start >= targetValue) {
                element.textContent = targetValue;
                clearInterval(timer);
            }
        }, stepTime);
    }

    // ==========================================================================
    // Split Lists (Top Safest vs. Top Dangerous)
    // ==========================================================================
    function renderSplitRankings() {
        // Sort ascending for safest
        const sortedSafest = [...state.cities].sort((a, b) => a['Crime Score'] - b['Crime Score']).slice(0, 5);
        // Sort descending for dangerous
        const sortedDangerous = [...state.cities].sort((a, b) => b['Crime Score'] - a['Crime Score']).slice(0, 5);

        // Normalize max crime score for progress bar calculations
        const maxScore = Math.max(...state.cities.map(c => c['Crime Score']), 150);

        // Render Safest List
        el.safestList.innerHTML = sortedSafest.map(c => {
            const pctWidth = (c['Crime Score'] / maxScore) * 100;
            return `
                <div class="split-item" data-city-name="${c['City']}">
                    <div>
                        <div class="split-city-name">${c['City']}</div>
                        <div class="split-city-pop">Pop: ${c['Population'].toLocaleString()}</div>
                    </div>
                    <div class="split-score-wrapper">
                        <span class="split-score-label">Crime Index</span>
                        <span class="split-score-val text-safe">${c['Crime Score'].toFixed(2)}</span>
                        <div class="split-score-bar-bg">
                            <div class="split-score-bar-fill" style="width: ${pctWidth}%;"></div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        // Render Dangerous List
        el.dangerousList.innerHTML = sortedDangerous.map(c => {
            const pctWidth = (c['Crime Score'] / maxScore) * 100;
            return `
                <div class="split-item" data-city-name="${c['City']}">
                    <div>
                        <div class="split-city-name">${c['City']}</div>
                        <div class="split-city-pop">Pop: ${c['Population'].toLocaleString()}</div>
                    </div>
                    <div class="split-score-wrapper">
                        <span class="split-score-label">Crime Index</span>
                        <span class="split-score-val text-high">${c['Crime Score'].toFixed(2)}</span>
                        <div class="split-score-bar-bg">
                            <div class="split-score-bar-fill" style="width: ${pctWidth}%;"></div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        // Bind clicks to items to open detail modal
        document.querySelectorAll('.split-item').forEach(item => {
            item.addEventListener('click', () => {
                const name = item.getAttribute('data-city-name');
                const matched = state.cities.find(c => c['City'] === name);
                if (matched) openCityDetails(matched);
            });
        });
    }

    // ==========================================================================
    // Visualization Tabs & Plot Loader
    // ==========================================================================
    el.tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active states
            el.tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const plotName = btn.getAttribute('data-plot');
            state.activePlot = plotName;

            // Trigger loader animation
            el.plotLoader.classList.add('active');
            el.plotImage.classList.remove('loaded');

            // Set new image source relative to environment
            const path = state.isLocalFile ? `../static/plots/${plotName}` : `/api/plots/${plotName}`;
            el.plotImage.src = path;
            el.downloadPlotLink.href = path;
        });
    });

    el.plotImage.addEventListener('load', () => {
        el.plotLoader.classList.remove('active');
        el.plotImage.classList.add('loaded');
    });

    el.plotImage.addEventListener('error', () => {
        el.plotLoader.classList.remove('active');
        showToast("Error loading high-resolution visualization.", "error");
    });

    // ==========================================================================
    // Table Sorting, Searching, Filtering and Pagination
    // ==========================================================================
    el.tableSearch.addEventListener('input', () => {
        state.currentPage = 1;
        applyTableProcessing();
    });

    el.tableFilter.addEventListener('change', () => {
        state.currentPage = 1;
        applyTableProcessing();
    });

    // Sort Handler click binds
    el.tableHeaders.forEach(th => {
        th.addEventListener('click', () => {
            const field = th.getAttribute('data-sort');
            
            if (state.sortBy === field) {
                // Toggle direction
                state.sortOrder = state.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                state.sortBy = field;
                state.sortOrder = 'desc'; // Default to desc for fresh sorting
            }

            // Remove active classes
            el.tableHeaders.forEach(h => {
                h.classList.remove('active');
                const indicator = h.querySelector('.sort-indicator');
                if (indicator) {
                    indicator.className = 'sort-indicator';
                }
            });

            // Set active class
            th.classList.add('active');
            const ind = th.querySelector('.sort-indicator');
            if (ind) {
                ind.className = `sort-indicator ${state.sortOrder}`;
            }

            applyTableProcessing();
        });
    });

    function applyTableProcessing() {
        const query = el.tableSearch.value.trim().toLowerCase();
        const riskFilter = el.tableFilter.value;

        // 1. Search Query and Dropdown Filter logic
        state.filteredCities = state.cities.filter(c => {
            const matchesSearch = c['City'].toLowerCase().includes(query);
            
            let matchesFilter = true;
            if (riskFilter === 'safe') {
                matchesFilter = c['Risk Level'].includes('Safe');
            } else if (riskFilter === 'moderate') {
                matchesFilter = c['Risk Level'].includes('Moderate');
            } else if (riskFilter === 'high') {
                matchesFilter = c['Risk Level'].includes('High-Risk');
            }

            return matchesSearch && matchesFilter;
        });

        // 2. Sorting logic
        state.filteredCities.sort((a, b) => {
            let valA = a[state.sortBy];
            let valB = b[state.sortBy];

            // String comparison
            if (typeof valA === 'string') {
                return state.sortOrder === 'asc' 
                    ? valA.localeCompare(valB) 
                    : valB.localeCompare(valA);
            }

            // Numerical comparison
            return state.sortOrder === 'asc' ? valA - valB : valB - valA;
        });

        // Render Table Body
        renderTableBody();
    }

    function renderTableBody() {
        const total = state.filteredCities.length;
        const startIndex = (state.currentPage - 1) * state.pageSize;
        const endIndex = Math.min(startIndex + state.pageSize, total);

        const pageItems = state.filteredCities.slice(startIndex, endIndex);

        if (total === 0) {
            el.tableBody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 40px; color: var(--text-secondary);">
                        No cities found matching search filter parameters.
                    </td>
                </tr>
            `;
            updatePagination(0, 0, 0);
            return;
        }

        el.tableBody.innerHTML = pageItems.map(c => {
            // Determine risk class badge
            let badgeClass = 'badge-safe';
            if (c['Risk Level'].includes('Moderate')) badgeClass = 'badge-moderate';
            else if (c['Risk Level'].includes('High-Risk')) badgeClass = 'badge-high';

            return `
                <tr class="city-row" data-city-name="${c['City']}">
                    <td class="td-city-name">${c['City']}</td>
                    <td class="td-value">${c['Population'].toLocaleString()}</td>
                    <td class="td-value">${c['Murder Rate'].toFixed(2)}</td>
                    <td class="td-value">${c['Assault Rate'].toFixed(2)}</td>
                    <td class="td-value">${c['Theft Rate'].toFixed(2)}</td>
                    <td class="td-value text-blue" style="font-weight: 700;">${c['Crime Score'].toFixed(2)}</td>
                    <td>
                        <span class="badge ${badgeClass}">${c['Risk Level']}</span>
                    </td>
                </tr>
            `;
        }).join('');

        // Bind clicks on table rows to open modal details
        document.querySelectorAll('.city-row').forEach(row => {
            row.addEventListener('click', () => {
                const name = row.getAttribute('data-city-name');
                const matched = state.cities.find(c => c['City'] === name);
                if (matched) openCityDetails(matched);
            });
        });

        updatePagination(startIndex + 1, endIndex, total);
    }

    // Pagination controls builder
    function updatePagination(start, end, total) {
        el.paginationInfo.textContent = `Showing ${start} to ${end} of ${total} entries`;

        const totalPages = Math.ceil(total / state.pageSize);
        
        el.prevPageBtn.disabled = state.currentPage === 1;
        el.nextPageBtn.disabled = state.currentPage === totalPages || totalPages === 0;

        // Generate numbered page buttons
        el.pageNumbers.innerHTML = '';
        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.className = `page-btn ${state.currentPage === i ? 'active' : ''}`;
            btn.textContent = i;
            btn.addEventListener('click', () => {
                state.currentPage = i;
                renderTableBody();
            });
            el.pageNumbers.appendChild(btn);
        }
    }

    // Next / Prev button binds
    el.prevPageBtn.addEventListener('click', () => {
        if (state.currentPage > 1) {
            state.currentPage--;
            renderTableBody();
        }
    });

    // Next button click
    el.nextPageBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(state.filteredCities.length / state.pageSize);
        if (state.currentPage < totalPages) {
            state.currentPage++;
            renderTableBody();
        }
    });

    // ==========================================================================
    // Interactive Detail Modal
    // ==========================================================================
    function openCityDetails(city) {
        el.modalCityName.textContent = `${city['City']} Profile`;
        
        let riskColorClass = 'safe';
        if (city['Risk Level'].includes('Moderate')) riskColorClass = 'moderate';
        else if (city['Risk Level'].includes('High-Risk')) riskColorClass = 'high';

        el.modalBody.innerHTML = `
            <div class="modal-score-panel ${riskColorClass}">
                <div>
                    <div style="font-size: 11px; text-transform: uppercase; font-weight: 600; color: var(--text-muted);">Assigned Classification</div>
                    <div style="font-family: var(--font-heading); font-size: 18px; font-weight: 800; color: var(--text-primary); margin-top: 4px;">${city['Risk Level']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 11px; text-transform: uppercase; font-weight: 600; color: var(--text-muted);">Crime Index Score</div>
                    <div style="font-family: var(--font-heading); font-size: 26px; font-weight: 800; color: var(--accent-blue); margin-top: 4px;">${city['Crime Score'].toFixed(2)}</div>
                </div>
            </div>
            
            <div class="modal-stat-group">
                <div class="modal-stat-card">
                    <span class="modal-stat-label">Murder Rate</span>
                    <span class="modal-stat-value">${city['Murder Rate'].toFixed(2)} <span style="font-size: 12px; font-weight:400; color: var(--text-muted);">/ 100k</span></span>
                </div>
                <div class="modal-stat-card">
                    <span class="modal-stat-label">Assault Rate</span>
                    <span class="modal-stat-value">${city['Assault Rate'].toFixed(2)} <span style="font-size: 12px; font-weight:400; color: var(--text-muted);">/ 100k</span></span>
                </div>
                <div class="modal-stat-card">
                    <span class="modal-stat-label">Theft Rate</span>
                    <span class="modal-stat-value">${city['Theft Rate'].toFixed(2)} <span style="font-size: 12px; font-weight:400; color: var(--text-muted);">/ 100k</span></span>
                </div>
                <div class="modal-stat-card">
                    <span class="modal-stat-label">Population</span>
                    <span class="modal-stat-value">${city['Population'].toLocaleString()}</span>
                </div>
            </div>

            <div style="font-size: 13px; color: var(--text-secondary); background-color: var(--bg-secondary); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
                <strong>K-Means Assignment Information:</strong> This city was grouped into Cluster ID <strong>${city['Cluster']}</strong> based on scaling vectors and Euclidean closeness to the cluster's average centroid.
            </div>
        `;

        el.detailsModal.classList.add('active');
        el.detailsModal.setAttribute('aria-hidden', 'false');
    }

    function closeModal() {
        el.detailsModal.classList.remove('active');
        el.detailsModal.setAttribute('aria-hidden', 'true');
    }

    // Modal click bindings
    el.modalCloseBtn.addEventListener('click', closeModal);
    el.modalBackdrop.addEventListener('click', closeModal);
    
    // Close modal on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && el.detailsModal.classList.contains('active')) {
            closeModal();
        }
    });

    // ==========================================================================
    // Event Binds Initialization
    // ==========================================================================
    el.themeToggle.addEventListener('click', toggleTheme);

    // Initializations
    initTheme();
    fetchDashboardData();
});
