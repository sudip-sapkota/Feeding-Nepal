 // Dropdown functionality
 document.addEventListener('DOMContentLoaded', function() {
    // Date dropdown
    const dateDropdown = document.getElementById('dateDropdown');
    const dateButton = dateDropdown.querySelector('.dropdown-button');
    const dateMenu = document.getElementById('dateMenu');
    const dateValue = document.getElementById('dateValue');
    const dateItems = dateMenu.querySelectorAll('.dropdown-item');

    // Location dropdown
    const locationDropdown = document.getElementById('locationDropdown');
    const locationButton = locationDropdown.querySelector('.dropdown-button');
    const locationMenu = document.getElementById('locationMenu');
    const locationValue = document.getElementById('locationValue');
    const locationItems = locationMenu.querySelectorAll('.dropdown-item');

    // Toggle date dropdown
    dateButton.addEventListener('click', function() {
        dateMenu.classList.toggle('show');
        locationMenu.classList.remove('show'); // Close other dropdown
    });

    // Toggle location dropdown
    locationButton.addEventListener('click', function() {
        locationMenu.classList.toggle('show');
        dateMenu.classList.remove('show'); // Close other dropdown
    });

    // Date dropdown item selection
    dateItems.forEach(item => {
        item.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            dateValue.textContent = value;
            dateMenu.classList.remove('show');
        });
    });

    // Location dropdown item selection
    locationItems.forEach(item => {
        item.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            locationValue.textContent = value;
            locationMenu.classList.remove('show');
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(event) {
        if (!dateDropdown.contains(event.target)) {
            dateMenu.classList.remove('show');
        }
        if (!locationDropdown.contains(event.target)) {
            locationMenu.classList.remove('show');
        }
    });
});