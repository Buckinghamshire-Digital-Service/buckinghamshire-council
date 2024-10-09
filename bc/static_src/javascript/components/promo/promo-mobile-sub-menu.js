class PromoMobileSubMenu {
    static selector() {
        return '[data-mobile-menu] [data-open-subnav]';
    }

    constructor(node) {
        this.node = node;
        this.subnav = this.node.nextElementSibling;
        this.bindEventListeners();
    }

    bindEventListeners() {
        // Open submenu
        this.node.addEventListener('click', (e) => {
            e.preventDefault();
            this.open();
        });

        if (this.subnav) {
            const backLink = this.subnav.querySelector('[data-subnav-back]');

            // Click back button to close it
            backLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.close();
            });
        }

        // After the end of the sub-nav, the focus moves back to the parent,
        // So close the current sub-navigation
        document.addEventListener('focusin', (e) => {
            const inSubMenu = !!e.target.closest('[data-subnav]');
            const inSubChildMenu = !!e.target.closest('[data-subnav-child]');

            if (this.subnav) {
                // leaving subnav for primary nav
                if (!inSubMenu) {
                    this.subnav.classList.remove('is-visible');
                    this.node.setAttribute('aria-expanded', 'false');
                }

                // leaving child subnav for parent subnav
                const isSubnavChild = this.subnav.hasAttribute(
                    'data-subnav-child',
                );
                if (isSubnavChild && !inSubChildMenu) {
                    this.close();
                }
            }
        });
    }

    open() {
        this.subnav.classList.add('is-visible');
        this.node.setAttribute('aria-expanded', 'true');
    }

    close() {
        this.subnav.classList.remove('is-visible');
        this.node.setAttribute('aria-expanded', 'false');
    }
}

export default PromoMobileSubMenu;
