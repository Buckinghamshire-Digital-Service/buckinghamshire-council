import Cookies from 'js-cookie';

class CookieWarning {
    static selector() {
        return '[data-cookie-message]';
    }

    constructor(node) {
        this.acceptButton = document.querySelector('[data-cookie-accept]');
        this.declineButton = document.querySelector('[data-cookie-decline]');
        this.messageContainer = node;
        this.cookieDomain = window.COOKIE_DOMAIN;
        this.cookieName = 'client-cookie';
        this.acceptValue = 'agree to cookies';
        this.declineValue = 'decline cookies';
        this.cookieDuration = 365;
        this.activeClass = 'active';
        this.inactiveClass = 'inactive';

        this.checkCookie();
        this.bindEvents();
    }

    checkCookie() {
        if (!this.messageContainer) {
            return;
        }

        // If cookie doesn't exists
        if (!Cookies.get(this.cookieName)) {
            this.messageContainer.classList.add(this.activeClass);
        }
    }

    applyCookie(event) {
        // prevent default link action
        event.preventDefault();
        // Add classes
        this.messageContainer.classList.remove(this.activeClass);
        this.messageContainer.classList.add(this.inactiveClass);
        // Set cookie
        Cookies.set(this.cookieName, this.acceptValue, {
            domain: this.cookieDomain,
            expires: this.cookieDuration,
        });
    }

    declineCookie(event) {
        // prevent default link action
        event.preventDefault();
        // Add classes
        this.messageContainer.classList.remove(this.activeClass);
        this.messageContainer.classList.add(this.inactiveClass);
        // Set cookie
        Cookies.set(this.cookieName, this.declineValue, {
            domain: this.cookieDomain,
            expires: this.cookieDuration,
        });
    }

    bindEvents() {
        if (!this.acceptButton) {
            return;
        }

        this.acceptButton.addEventListener('click', (event) =>
            this.applyCookie(event),
        );

        if (!this.declineButton) {
            return;
        }

        this.declineButton.addEventListener('click', (event) => {
            this.declineCookie(event);
        });
    }
}

export default CookieWarning;
