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

            // if form contains submitted class, don't allow further submissions
            if (this.form.classList.contains(submittedClass)) {
                e.preventDefault();
                // if form does not contain submitted class (first submission), add it and disable submit button
            } else {
                submitButton.disabled = true;
                this.form.classList.add(submittedClass);
            }
        });
    }
}

export default FormSubmit;
