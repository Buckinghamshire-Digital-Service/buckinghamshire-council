class DesktopSubMenu {
    static selector() {
        return '[data-desktop-menu] [data-open-promo-subnav]';
    }

    static parentSelector() {
        return this.node.closest('[data-has-subnav]');
    }

    constructor(node) {
        this.node = node;
        this.body = document.querySelector('body');
        this.toggleNode = this.node.closest('[data-has-subnav]');
        this.allToggleNodes = document.querySelectorAll(
            '[data-desktop-menu] [data-has-subnav]',
        );
        this.activeClass = 'active';
        this.lastMenuItems = document.querySelectorAll(
            '[data-last-menu-item-desktop]',
        );
        this.bindEventListeners();
    }

    close() {
        this.toggleNode.classList.remove('active');
        this.node.setAttribute('aria-expanded', 'false');
        this.body.classList.remove('no-scroll');
    }

    open() {
        const menuOpenEvent = new Event('onMenuOpen');
        document.dispatchEvent(menuOpenEvent);
        this.toggleNode.classList.add('active');
        this.node.setAttribute('aria-expanded', 'true');
        this.body.classList.add('no-scroll');
    }

    bindEventListeners() {
        this.node.addEventListener('click', (e) => {
            e.preventDefault();

            // Close other menu items that may be open
            this.allToggleNodes.forEach((item) => {
                if (item !== this.toggleNode) {
                    item.classList.remove(this.activeClass);
                    item.querySelector('[data-open-promo-subnav]').setAttribute(
                        'aria-expanded',
                        'false',
                    );
                }
            });

            if (this.toggleNode.classList.contains('active')) {
                this.close();
            } else {
                this.open();
            }
        });

        // Close the desktop menu when the focus moves away from the last item
        this.lastMenuItems.forEach((item) => {
            item.addEventListener('focusout', () => {
                this.close();
            });
        });
    }
}

export default DesktopSubMenu;
