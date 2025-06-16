document.addEventListener('DOMContentLoaded', function () {
    const donationForm = document.getElementById('donationForm');
    if (donationForm) {
        donationForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const requiredFields = ['quantity', 'foodType', 'description', 'pickupDate'];
            for (let id of requiredFields) {
                if (!document.getElementById(id).value) {
                    alert('Please fill in all required fields');
                    return;
                }
            }
            alert('Donation submitted successfully!');
            donationForm.reset();
        });
    }

    const sidebar = document.querySelector('.sidebar');
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => sidebar.classList.toggle('active'));
    }

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.sidebar') && !e.target.closest('.mobile-menu-button')) {
            sidebar?.classList.remove('active');
        }
        if (!e.target.closest('#dateRangeFilter') && !e.target.closest('#dateDropdown')) {
            dateDropdown?.classList.remove('active');
        }
        if (!e.target.closest('#locationFilter') && !e.target.closest('#locationDropdown')) {
            locationDropdown?.classList.remove('active');
        }
    });

    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function () {
            document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            if (window.innerWidth <= 768) sidebar?.classList.remove('active');
        });
    });

    document.querySelector('.search-box button')?.addEventListener('click', () => {
        const val = document.querySelector('.search-box input').value;
        alert('Searching for: ' + val);
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) sidebar?.classList.remove('active');
    });

    const dateFilter = document.getElementById('dateRangeFilter');
    const locationFilter = document.getElementById('locationFilter');
    const dateDropdown = document.getElementById('dateDropdown');
    const locationDropdown = document.getElementById('locationDropdown');

    dateFilter?.addEventListener('click', (e) => {
        e.stopPropagation();
        dateDropdown.classList.toggle('active');
        locationDropdown?.classList.remove('active');
        if (dateDropdown.classList.contains('active')) generateCalendar();
    });

    locationFilter?.addEventListener('click', (e) => {
        e.stopPropagation();
        locationDropdown.classList.toggle('active');
        dateDropdown?.classList.remove('active');
    });

    let currentDate = new Date(), currentMonth = currentDate.getMonth(), currentYear = currentDate.getFullYear();

    document.getElementById('prevMonth')?.addEventListener('click', () => {
        if (--currentMonth < 0) { currentMonth = 11; currentYear--; }
        generateCalendar();
    });

    document.getElementById('nextMonth')?.addEventListener('click', () => {
        if (++currentMonth > 11) { currentMonth = 0; currentYear++; }
        generateCalendar();
    });

    function generateCalendar() {
        const monthNames = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"];
        const calendarGrid = document.getElementById('calendarGrid');
        const today = new Date();
        document.querySelector('.calendar-title').textContent = `${monthNames[currentMonth]} ${currentYear}`;
        const firstDay = new Date(currentYear, currentMonth, 1).getDay();
        const lastDate = new Date(currentYear, currentMonth + 1, 0).getDate();
        calendarGrid.innerHTML = '<div class="calendar-day header">Sun</div><div class="calendar-day header">Mon</div><div class="calendar-day header">Tue</div><div class="calendar-day header">Wed</div><div class="calendar-day header">Thu</div><div class="calendar-day header">Fri</div><div class="calendar-day header">Sat</div>';
        for (let i = 0; i < firstDay; i++) calendarGrid.appendChild(document.createElement('div')).className = 'calendar-day inactive';
        for (let i = 1; i <= lastDate; i++) {
            const day = document.createElement('div');
            day.className = 'calendar-day';
            day.textContent = i;
            if (i === today.getDate() && currentMonth === today.getMonth() && currentYear === today.getFullYear()) {
                day.classList.add('today');
            }
            day.addEventListener('click', function () {
                document.querySelectorAll('.calendar-day').forEach(d => d.classList.remove('selected'));
                this.classList.add('selected');
                dateFilter.firstChild.textContent = `${monthNames[currentMonth].substring(0, 3)} ${i}, ${currentYear} `;
                document.querySelectorAll('.preset-date').forEach(p => p.classList.remove('selected'));
                dateDropdown.classList.remove('active');
            });
            calendarGrid.appendChild(day);
        }
    }

    document.querySelectorAll('.preset-date').forEach(preset => {
        preset.addEventListener('click', function () {
            document.querySelectorAll('.preset-date').forEach(p => p.classList.remove('selected'));
            this.classList.add('selected');
            const map = {
                today: 'Today', yesterday: 'Yesterday',
                'this-month': 'This Month', 'last-month': 'Last Month', 'this-year': 'This Year'
            };
            dateFilter.firstChild.textContent = (map[this.dataset.value] || 'Custom Range') + ' ';
            dateDropdown?.classList.remove('active');
        });
    });

    document.querySelectorAll('.location-option').forEach(opt => {
        opt.addEventListener('click', function () {
            document.querySelectorAll('.location-option').forEach(o => o.classList.remove('selected'));
            this.classList.add('selected');
            locationFilter.firstChild.textContent = this.textContent + ' ';
            locationDropdown?.classList.remove('active');
        });
    });
});
