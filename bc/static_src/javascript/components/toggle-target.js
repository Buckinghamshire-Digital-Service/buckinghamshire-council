class ToggleTarget {
    static selector() {
        return '[data-toggle-target]';
    }

    constructor(node) {
        this.node = node;
        this.targetNode = document.querySelector(node.dataset.toggleTarget);

        this.bindEvents();
    }

    bindEvents() {
        const { node, targetNode } = this;
        this.node.addEventListener('click', () => {
            if (targetNode.dataset.active === 'true') {
                node.dataset.active = 'false';
                targetNode.dataset.active = 'false';
            } else {
                node.dataset.active = 'true';
                targetNode.dataset.active = 'true';
            }
        });
    }
}

export default ToggleTarget;
