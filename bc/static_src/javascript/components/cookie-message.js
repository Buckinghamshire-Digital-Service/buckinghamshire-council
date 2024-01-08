import Cookies from 'js-cookie';

class CookieWarning {
    static selector() {
        return '[data-cookie-message]';
    }

    constructor(node) {
        if (!node) {
            return;
        }
        this.rcConsentRequired = node.hasAttribute('data-rc-consent-required');
        this.acceptButton = document.querySelector('[data-cookie-accept]');
        this.declineButton = document.querySelector('[data-cookie-decline]');
        this.messageContainer = node;
        this.cookieDomain = window.COOKIE_DOMAIN;
        this.cookieName = 'client-cookie';
        this.acceptValue = 'agree to cookies, agree to rc';
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

        // If cookie has been declined, do not show the cookie message
        if (Cookies.get(this.cookieName) === this.declineValue) {
            this.messageContainer.classList.add(this.inactiveClass);
        }
        // If consent is required and not given, show the cookie message
        else if (!this.hasConsent()) {
            this.messageContainer.classList.add(this.activeClass);
        }
    }

    hasConsent() {
        const cookieValue = Cookies.get(this.cookieName) || '';
        const hasGeneralCookieConsent = cookieValue.includes(
            'agree to cookies',
        );
        const hasRCCookieConsent = this.rcConsentRequired
            ? cookieValue.includes('agree to rc')
            : true;

        if (hasGeneralCookieConsent && hasRCCookieConsent) {
            return true;
        }
        return false;
    }

    applyCookie(event) {
        // prevent default link action
        event.preventDefault();
        // Add classes
        this.messageContainer.classList.remove(this.activeClass);
        this.messageContainer.classList.add(this.inactiveClass);
        // Set cookie
        Cookies.set(
            this.cookieName,
            this.rcConsentRequired ? this.acceptValue : 'agree to cookies',
            {
                domain: this.cookieDomain,
                expires: this.cookieDuration,
            },
        );
        if (this.rcConsentRequired) {
            window.location.reload();
        }
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
        if (this.acceptButton) {
            this.acceptButton.addEventListener('click', (event) =>
                this.applyCookie(event),
            );
        }

        if (this.declineButton) {
            this.declineButton.addEventListener('click', (event) => {
                this.declineCookie(event);
            });
        }
    }
}

export default CookieWarning;
