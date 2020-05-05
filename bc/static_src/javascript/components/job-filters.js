class Filters {
    static selector() {
        return '[data-filters]';
    }

    constructor(node) {
        this.filters = node;
        this.filter = this.filters.querySelectorAll('[data-filter]');
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

        // update active filter counter if present
        if (filtersActiveCounter) {
            filtersActiveCounter.innerHTML = this.checkboxCount();

            if (checkboxCount > 0) {
                // show active filter container when at least 1 filter (checkbox) is active (checked)
                filtersActive.classList.add('active');
            } else {
                // hide active filter container when no filters (checkboxes) are active (checked)
                filtersActive.classList.remove('active');
            }
        }
    }

    resetAllFilters() {
        this.filter.forEach((filter) => {
            // remove each checked filter
            filter.checked = false;

            // if text input (postcode search) is not blank, reset it
            if (filter.value !== '') {
                filter.value = '';
            }

            this.showChecked();
        });
    }

    bindEvents() {
        this.submitFilters = document.querySelector('[data-filters-submit]');
        this.resetFilters = document.querySelector('[data-filters-reset]');

        this.filter.forEach((filter) => {
            filter.addEventListener('click', () => {
                this.showChecked();
            });
        });

        this.resetFilters.addEventListener('click', () => {
            this.resetAllFilters();
            this.submitFilters.click();
        });
    }
}

export default Filters;
