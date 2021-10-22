import Accordion from './accordion';

class Steps {
    static selector() {
        return '[data-steps-container]';
    }

    constructor(stepsContainer) {
        this.stepsContainer = stepsContainer;
        this.steps = [];

        stepsContainer
            .querySelectorAll('[data-step-accordion]')
            .forEach((accordion) => {
                this.steps.push(new Accordion(accordion));
            });

        this.toggleSteps = stepsContainer.querySelector('[data-steps-toggle]');

        this.state = {
            open: false,
        };

        this.bindEvents();
    }

    bindEvents() {
        this.toggleSteps.addEventListener('click', (e) => {
            e.preventDefault();
            if (this.state.open) {
                this.steps.forEach((accordion) => accordion.close());
                this.state.open = false;
            } else {
                this.steps.forEach((accordion) => accordion.open());
                this.state.open = true;
            }
            this.toggleSteps.classList.toggle('is-open');
        });
    }
}

export default Steps;
