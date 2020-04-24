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
        this.allConditionalSubFields = this.conditional.querySelectorAll(
            '[data-conditional-subfields]',
        );

        this.bindEvents();
    }

    handleInput(item) {
        const parentField = item.closest('[data-conditional-field]');

        // remove active class from all fields
        this.allConditionalFields.forEach(field => {
            field.classList.remove('is-checked');
            field.setAttribute('aria-expanded', 'false');
            field.setAttribute('aria-hidden', 'true');
        });

        if (item.checked) {
            parentField.classList.add('is-checked');
            parentField.setAttribute('aria-expanded', 'true');
            parentField.setAttribute('aria-hidden', 'false');
        }
    }

    bindEvents() {
        this.allConditionalInputs.forEach(item => {
            item.addEventListener('click', () => {
                this.handleInput(item);
            });
        });

        this.conditional.addEventListener('focus', () => {
            this.conditional.setAttribute('aria-selected', 'true');
        });

        this.conditional.addEventListener('blur', () => {
            this.conditional.setAttribute('aria-selected', 'false');
        });
    }
}

export default ConditionalField;
