class HeightEqualizer {
    static selector() {
        return '[data-height-equalizer]';
    }

    constructor(node) {
        this.parent = node;
        this.children = node.querySelectorAll('[data-height-equalizer-child]');

        this.updateHeight = (children) => {
            // Get biggest height
            let biggestHeight = 0;
            for (let i = 0; i < children.length; i += 1) {
                const currentHeight = children[i].offsetHeight;
                if (biggestHeight < currentHeight) {
                    biggestHeight = currentHeight;
                }
            }

            // Update to biggest height
            for (let i = 0; i < children.length; i += 1) {
                children[i].style.height = `${biggestHeight}px`;
            }
        };

        this.bindEvents();
    }

    bindEvents() {
        const { children } = this;
        if (
            document.readyState === 'complete' ||
            document.readyState === 'interactive'
        ) {
            this.updateHeight(children);
        } else {
            document.addEventListener('DOMContentLoaded', () => {
                this.updateHeight(children);
            });
        }
    }
}

export default HeightEqualizer;
