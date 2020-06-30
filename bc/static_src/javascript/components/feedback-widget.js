class FeedbackWidget {
    static selector() {
        return '[data-feedback-widget]';
    }

    constructor(node) {
        this.widget = node;
        this.feedbackHeading = this.widget.querySelector(
            '[data-feedback-heading]',
        );
        this.feedbackButtons = this.widget.querySelectorAll(
            '[data-feedback-button]',
        );
        this.bindEvents();
    }

    bindEvents() {
        this.feedbackButtons.forEach((feedbackButton) => {
            feedbackButton.addEventListener('click', () => {
                this.widget.classList.remove('active');
                this.feedbackHeading.innerText = 'Thank you for your feedback!';
            });
        });
    }
}

export default FeedbackWidget;
