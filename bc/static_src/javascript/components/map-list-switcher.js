class MapListSwitcher {
    static selector() {
        return '[data-map-list-switcher]';
    }

    constructor(node) {
        this.node = node;
        this.map = node.querySelector('[data-map]');
        this.list = node.querySelector('[data-list]');
        this.mapSwitcherControl = node.querySelector(
            '[data-map-list-switcher-control="map"]',
        );
        this.listSwitcherControl = node.querySelector(
            '[data-map-list-switcher-control="list"]',
        );
        this.bindEvents();
    }

    bindEvents() {
        this.mapSwitcherControl.addEventListener('click', (e) => {
            e.preventDefault();
            this.switchToMap();
        });
        this.listSwitcherControl.addEventListener('click', (e) => {
            e.preventDefault();
            this.switchToList();
        });
    }

    switchToList() {
        this.mapSwitcherControl.classList.remove('is-active');
        this.listSwitcherControl.classList.add('is-active');
        this.map.setAttribute('hidden', '');
        this.list.removeAttribute('hidden');
    }

    switchToMap() {
        this.mapSwitcherControl.classList.add('is-active');
        this.listSwitcherControl.classList.remove('is-active');
        this.list.setAttribute('hidden', '');
        this.map.removeAttribute('hidden');
    }
}

export default MapListSwitcher;
