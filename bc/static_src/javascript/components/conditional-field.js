class ConditionalField {
    static selector() {
        return '[data-conditional]';
    }

    constructor(node) {
        this.conditional = node;
        this.allConditionalFields = this.conditional.querySelectorAll(
            '[data-conditional-field]',
        );
        this.allConditionalInputs = this.conditional.querySelectorAll(
            '[data-conditional-input]',
        );

        this.bindEvents();

        // run once on page load
        this.conditional
            .querySelectorAll('[data-conditional-input]:checked')
            .forEach((item) => {
                this.handleInput(item);
            });
    }

    handleInput(item) {
        const parentField = item.closest('[data-conditional-field]');

        // remove active class from all conditional fields
        this.allConditionalFields.forEach((field) => {
            field.classList.remove('is-checked');
            field.setAttribute('aria-expanded', 'false');
            field.setAttribute('aria-hidden', 'true');
        });

        // if radio is checked, add is-checked class & aria-attributes to parent
        if (item.checked) {
            parentField.classList.add('is-checked');
            this.setAttribute('aria-selected', 'true');
            parentField.setAttribute('aria-expanded', 'true');
            parentField.setAttribute('aria-hidden', 'false');
        }
    }

    bindEvents() {
        this.allConditionalInputs.forEach((item) => {
            item.addEventListener('click', () => {
                this.handleInput(item);
            });
        });
    }
}

export default ConditionalField;
