class Filters {
    static selector() {
        return '[data-filters]';
    }

    constructor(node) {
        this.filters = node;
        this.filter = this.filters.querySelectorAll('[data-filter]');
        this.resetFilters = document.querySelector('[data-filters-reset]');
        this.showChecked();
        this.bindEvents();
    }

    checkboxCount() {
        // find number of active filters (i.e. checked checkboxes)
        const activeFilters = this.filters.querySelectorAll(
            '[data-filter]:checked',
        ).length;
        // return that number
        return activeFilters;
    }

    showChecked() {
        // number of checkboxes checked
        const checkboxCount = this.checkboxCount();
        // parent container of the active filter counter (display:none by default)
        const filtersActive = this.filters.querySelector(
            '[data-filters-active]',
        );
        // counter displaying the number of active filters
        const filtersActiveCounter = this.filters.querySelector(
            '[data-filters-counter]',
        );

        // update active filter counter
        filtersActiveCounter.innerHTML = this.checkboxCount();

        if (checkboxCount > 0) {
            // show active filter container when at least 1 filter (checkbox) is active (checked)
            filtersActive.classList.add('active');
        } else {
            // hide active filter container when no filters (checkboxes) are active (checked)
            filtersActive.classList.remove('active');
        }
    }

    resetAllFilters() {
        this.filter.forEach((filter) => {
            filter.checked = false;
            this.showChecked();
        });
    }

    bindEvents() {
        this.filter.forEach((filter) => {
            filter.addEventListener('click', () => {
                this.showChecked();
            });
        });

        this.resetFilters.addEventListener('click', (e) => {
            e.preventDefault();
            this.resetAllFilters();
        });
    }
}

export default Filters;
