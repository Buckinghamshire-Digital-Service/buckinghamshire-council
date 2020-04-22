class FormSubmit {
    static selector() {
        return '[data-form]';
    }

    constructor(node) {
        this.form = node;
        this.bindEvents();
    }

    bindEvents() {
        this.form.addEventListener('submit', (e) => {
            const submittedClass = 'js-submitted';
            if (this.classList.contains(submittedClass)) {
                e.preventDefault();
            } else {
                this.classList.add(submittedClass);
            }
        });
    }
}

export default FormSubmit;
