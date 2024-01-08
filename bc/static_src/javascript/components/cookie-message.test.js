import Cookies from 'js-cookie';
import CookieWarning from './cookie-message';

describe('CookieWarning', () => {
    /* eslint-disable no-new */

    beforeEach(() => {
        document.body.innerHTML =
            '<div class="cookie" data-cookie-message><button data-cookie-accept>Accept</button><button data-cookie-decline>Decline</button></div>';
        Cookies.remove('client-cookie');
    });

    it('gracefully fails to render for missing element', () => {
        expect(() => {
            document.body.innerHTML = '';
            new CookieWarning(document.querySelector('[data-missing]'));
        }).not.toThrowError();
    });

    it('becomes active on init', () => {
        new CookieWarning(document.querySelector(CookieWarning.selector()));
        expect(document.querySelector('[data-cookie-message]').className).toBe(
            'cookie active',
        );
    });

    it('does not activate if cookie is set', () => {
        Cookies.set('client-cookie', 'agree to cookies');

        new CookieWarning(document.querySelector(CookieWarning.selector()));
        expect(document.querySelector('[data-cookie-message]').className).toBe(
            'cookie',
        );
    });

    it('can be accepted', () => {
        new CookieWarning(document.querySelector(CookieWarning.selector()));
        expect(document.querySelector('[data-cookie-message]').className).toBe(
            'cookie active',
        );

        const accept = document.querySelector('[data-cookie-accept]');

        accept.dispatchEvent(new Event('click'));

        expect(document.querySelector('[data-cookie-message]').className).toBe(
            'cookie inactive',
        );
        expect(Cookies.get('client-cookie')).toBe('agree to cookies');
    });

    it('can be declined', () => {
        new CookieWarning(document.querySelector(CookieWarning.selector()));
        expect(document.querySelector('[data-cookie-message]').className).toBe(
            'cookie active',
        );

        const decline = document.querySelector('[data-cookie-decline]');

        decline.dispatchEvent(new Event('click'));

        expect(document.querySelector('[data-cookie-message]').className).toBe(
            'cookie inactive',
        );
        expect(Cookies.get('client-cookie')).toBe('decline cookies');
    });

    it('does not activate if cookie is rejected', () => {
        Cookies.set('client-cookie', 'decline cookies');

        new CookieWarning(document.querySelector(CookieWarning.selector()));
        expect(document.querySelector('[data-cookie-message]').className).toBe(
            'cookie inactive',
        );
    });
});
