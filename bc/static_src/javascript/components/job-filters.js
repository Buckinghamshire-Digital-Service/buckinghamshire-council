class Filters {
    static selector() {
        return '[data-filters]';
    }

    constructor(node) {
        this.filters = node;
        this.filter = this.filters.querySelectorAll(
            '[data-filter]',
        );
        this.showChecked();
        this.bindEvents();
    }

    getCheckboxCount() {
        // add data attr
        return this.querySelectorAll('input:checked').length;
    }

    showChecked() {
        this.getElementById('selected').innerHTML = getCheckBoxCount();
    }

    bindEvents() {
        this.filter.addEventListener('click', (e) => {
            e.preventDefault();
            let checked = this.filter.checked === true;
            this.filter.classList.toggle('checked');
            // add data attr
            return this.querySelectorAll('input:checked').length;

            if (checked) {
                checked = false;
            } else {
                checked = true;
            }
        });
    }
}

export default Filters;
