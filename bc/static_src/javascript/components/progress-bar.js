import Utilities from '../utilities';

class ProgressBar {
    static selector() {
        return '[data-progress-bar]';
    }

    constructor(node) {
        this.node = node;
        this.progressBar();
    }

    progressBar() {
        const getMax = () => {
            return document.documentElement.scrollHeight - window.innerHeight;
        };

        const getValue = () => {
            return window.pageYOffset;
        };

        const scrollListener = () => {
            // On scroll only the value attr needs to be calculated
            this.node.setAttribute('value', getValue());
        };

        const windowListener = () => {
            // On resize, both max/value attr needs to be calculated
            this.node.setAttribute('max', getMax());
            this.node.setAttribute('value', getValue());
        };

        // Check browser supports progress element
        if ('max' in document.createElement('progress')) {
            // Set the max attr for the first time
            this.node.setAttribute('max', getMax());

            document.addEventListener(
                'scroll',
                Utilities.throttle(scrollListener, 100),
            );

            window.addEventListener(
                'resize',
                Utilities.throttle(windowListener, 100),
            );
        }
    }
}

export default ProgressBar;
