class FeedbackWidget {
    static selector() {
        return '[data-feedback-widget]';
    }

    constructor(node) {
        this.widget = node;
        this.feedbackHeading = this.widget.querySelector(
            '[data-feedback-heading]',
        );
        this.yesForm = this.widget.querySelector('[data-yes-form]');
        this.yesFormAction = this.yesForm.getAttribute('action');
        this.noForm = this.widget.querySelector('[data-no-form]');
        this.noFormAction = this.yesForm.getAttribute('action');
        this.extraFeedbackBlock = this.widget.querySelector(
            '[data-extra-feedback-block]',
        );
        this.extraFeedbackForm = this.widget.querySelector(
            '[data-extra-feedback-form]',
        );
        this.extraFeedbackFormAction = this.extraFeedbackForm.getAttribute(
            'action',
        );
        this.closeButton = this.widget.querySelector('[data-close-form]');
        this.bindEvents();
    }

    sendFormData(url, data, form) {
        const XHR = new XMLHttpRequest();
        XHR.addEventListener('error', () => {
            this.setResponseClasses();
            this.feedbackHeading.innerText =
                'Something went wrong submitting your feedback. Please refresh the page and try again.';
        });

        XHR.addEventListener('load', () => {
            if (form === 'yes') {
                this.setResponseClasses();
                this.feedbackHeading.innerText = 'Thank you for your feedback!';
            } else if (form === 'no') {
                this.feedbackHeading.innerText = '';
                this.showFeedbackForm();
            } else {
                // feedback form
                this.hideFeedbackForm();
                this.feedbackHeading.innerText = 'Thank you for your feedback!';
            }
        });

        XHR.open('POST', url);
        XHR.send(data);
    }

    setResponseClasses() {
        this.widget.classList.remove('show-yes-no', 'show-feedback-form');
    }

    setFeedbackFormClasses() {
        this.widget.classList.remove('show-yes-no');
        this.widget.classList.add('show-feedback-form');
    }

    showFeedbackForm() {
        this.setFeedbackFormClasses();
        this.extraFeedbackBlock.setAttribute('aria-hidden', false);
    }

    hideFeedbackForm() {
        this.setResponseClasses();
        this.extraFeedbackBlock.setAttribute('aria-hidden', true);
        this.feedbackHeading.innerText = 'Thank you for your feedback!';
    }

    bindEvents() {
        this.yesForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(this.yesForm);
            this.sendFormData(this.yesFormAction, formData, 'yes');
        });

        this.noForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(this.noForm);
            this.sendFormData(this.noFormAction, formData, 'no');
        });
        this.extraFeedbackForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(this.extraFeedbackForm);
            this.sendFormData(
                this.extraFeedbackFormAction,
                formData,
                'feedback',
            );
        });
        this.closeButton.addEventListener('click', () => {
            this.hideFeedbackForm();
        });
    }
}

export default FeedbackWidget;
