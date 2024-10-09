class PromoMobileMenu {
    static selector() {
        return '[data-mobile-menu-toggle]';
    }

    constructor(node) {
        this.node = node;
        this.body = document.querySelector('body');
        this.mobileMenu = document.querySelector('[data-mobile-menu]');
        this.lastMenuItem = document.querySelector(
            '[data-last-menu-item-mobile]',
        );

        this.state = {
            open: false,
        };

        this.bindEventListeners();
    }

    bindEventListeners() {
        this.node.addEventListener('click', () => {
            this.toggle();
        });

        // Close mobile dropdown with escape key for improved accessibility
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                if (this.state.open) {
                    this.close();
                    this.state.open = false;
                }
            }
        });

        // Close the mobile menu when the focus moves away from the last item in the top level
        if (this.lastMenuItem === null) {
            return;
        }

        this.lastMenuItem.addEventListener('focusout', () => {
            if (this.state.open) {
                this.close();
                this.state.open = false;
            }
        });
    }

    toggle() {
        if (this.state.open) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        const menuOpenEvent = new Event('onMenuOpen');
        document.dispatchEvent(menuOpenEvent);
        this.node.classList.add('is-open');
        this.node.setAttribute('aria-expanded', 'true');
        this.body.classList.add('no-scroll');
        this.mobileMenu.classList.add('is-visible');

        this.state.open = true;
    }

    close() {
        this.node.classList.remove('is-open');
        this.node.setAttribute('aria-expanded', 'false');
        this.body.classList.remove('no-scroll');
        this.mobileMenu.classList.remove('is-visible');

        this.state.open = false;
    }
}

export default PromoMobileMenu;
