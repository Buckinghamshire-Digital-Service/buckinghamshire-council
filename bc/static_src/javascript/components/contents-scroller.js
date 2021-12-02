class ContentsScroller {
    static selector() {
        return '[data-contents-list]';
    }

    static scrollSelector() {
        return '[data-contents-scroller]';
    }

    constructor(node) {
        this.topThreshold = node.offsetTop + node.scrollHeight;
        const footer = document.querySelector('footer');
        this.bottomThreshold = footer.offsetTop;
        this.scroller = document.querySelector(
            ContentsScroller.scrollSelector(),
        );
        this.bindEvents();
    }

    bindEvents() {
        window.addEventListener('scroll', () => this.toggleScroller());
    }

    toggleScroller() {
        const { scrollY } = window;
        const winHeight = window.innerHeight;
        if (
            scrollY > this.topThreshold &&
            scrollY + winHeight < this.bottomThreshold
        ) {
            this.scroller.style.display = 'block';
        } else {
            this.scroller.style.display = 'none';
        }
    }
}

export default ContentsScroller;
