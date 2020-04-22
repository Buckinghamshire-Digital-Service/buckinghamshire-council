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
            const submitButton = this.querySelector('[type="submit"]');
            const submittedClass = 'js-submitted';
            // if form contains submitted class, disallow further submissions & add disabled attribute to submit button
            if (this.classList.contains(submittedClass)) {
                e.preventDefault();
                submitButton.disabled = true;
                // if form does not contain submitted class (first submission), add it
            } else {
                this.classList.add(submittedClass);
            }
        });
    }
}

export default FormSubmit;
