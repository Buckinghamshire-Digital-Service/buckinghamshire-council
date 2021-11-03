class Accordion {
    static selector() {
        return '[data-accordion]';
    }

    constructor(node) {
        this.accordion = node;
        this.question = this.accordion.querySelector(
            '[data-accordion-question]',
        );
        this.answer = this.accordion.querySelector('[data-accordion-answer]');
        this.state = {
            open: false,
        };
        this.bindEvents();
    }

    bindEvents() {
        this.question.addEventListener('click', (e) => {
            e.preventDefault();
            if (this.state.open) {
                this.close();
            } else {
                this.open();
            }
        });
    }

    open() {
        if (this.state.open) {
            return;
        }
        this.accordion.classList.toggle('is-open');
        this.question.setAttribute('aria-expanded', 'true');
        this.answer.setAttribute('aria-hidden', 'false');
        this.state.open = true;
    }

    close() {
        if (!this.state.open) {
            return;
        }
        this.accordion.classList.toggle('is-open');
        this.question.setAttribute('aria-expanded', 'false');
        this.answer.setAttribute('aria-hidden', 'true');
        this.state.open = false;
    }
}

export default Accordion;
