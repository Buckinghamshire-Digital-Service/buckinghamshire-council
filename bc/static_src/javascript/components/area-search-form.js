class AreaSearchForm {
    static selector() {
        return '[data-area-search]';
    }

    constructor(node) {
        this.form = node;
        this.submitButton = this.form.querySelector('[data-submit-button]');
        this.findAnotherButton = this.form.querySelector(
            '[data-find-another-button]',
        );

        this.postcodeInput = this.form.querySelector('[data-postcode-input]');
        this.postcodeWrapper = this.form.querySelector(
            '[data-postcode-wrapper]',
        );

        this.responseText = this.form.querySelector('[data-response-text]');
        this.areaLinkUrls = JSON.parse(
            document.getElementById('area-link-urls').textContent,
        );
        this.bindEvents();
    }

    bindEvents() {
        this.form.onchange = () => {
            this.responseClear();
        };

        this.submitButton.addEventListener('click', (e) => {
            this.responseClear();
            e.preventDefault();
            this.submitForm();
        });

        this.findAnotherButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.showForm();
        });
    }

    responseClear() {
        this.responseText.innerHTML = '';
        this.form.classList.remove('form--area-search-error');
        this.responseText.classList.remove('area-search__response-text--error');
    }

    hideForm() {
        this.responseClear();
        this.postcodeWrapper.classList.add('hide');
        this.submitButton.classList.add('hide');
        this.findAnotherButton.classList.remove('hide');
    }

    showForm() {
        this.responseClear();
        this.postcodeWrapper.classList.remove('hide');
        this.submitButton.classList.remove('hide');
        this.findAnotherButton.classList.add('hide');
    }

    responseError() {
        this.form.classList.add('form--area-search');
        this.form.classList.add('form--area-search-error');
        this.responseText.classList.add('area-search__response-text');
        this.responseText.classList.add('area-search__response-text--error');
    }

    appendResponseText(text) {
        this.responseText.textContent = text;
    }

    appendResponseHTML(html) {
        const e = document.createElement('div');
        e.innerHTML = html;

        while (e.firstChild) {
            this.responseText.appendChild(e.firstChild);
        }
    }

    updateResponseArea(name) {
        this.hideForm();

        const areaName = name;

        if (areaName in this.areaLinkUrls === true) {
            const targetUrl = this.areaLinkUrls[areaName];
            // window.location.href = targetUrl;

            // this.responseText.appendChild(buttonElement);
            const buttonElement = document.createElement('button');
            buttonElement.innerText = 'Go to information';
            buttonElement.classList.add('button');
            buttonElement.classList.add('button--basic');
            buttonElement.classList.add('button--area-search');
            buttonElement.type = 'button';
            buttonElement.onclick = () => {
                window.location.href = targetUrl;
            };
            this.responseText.appendChild(buttonElement);
        }
    }

    updateResponseBorderOverlap(html) {
        this.hideForm();
        this.appendResponseHTML(html);
    }

    updateResponseMessage(message) {
        this.hideForm();
        this.appendResponseText(message);
    }

    updateResponseError(message) {
        this.responseClear();
        this.responseError();
        this.appendResponseText(message);
    }

    submitForm() {
        const url = this.form.getAttribute('url');
        const postcodeValue = this.postcodeInput.value;

        // Regex for UK postcodes https://stackoverflow.com/a/164994
        const UKPostCodePattern = /^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})/;
        const isUKPostCodeValid = UKPostCodePattern.test(postcodeValue);

        if (!isUKPostCodeValid) {
            this.updateResponseError('Invalid postcode');
        } else {
            fetch(`${url}?postcode=${postcodeValue}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json; charset=utf-8',
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then((response) => response.json())
                .then((response) => {
                    if (response.area) {
                        this.updateResponseArea(response.area);
                    } else if (response.border_overlap) {
                        this.updateResponseBorderOverlap(
                            response.border_overlap,
                        );
                    } else if (response.message) {
                        this.updateResponseMessage(response.message);
                    } else if (response.error) {
                        this.updateResponseError(response.error);
                    }
                })
                .catch((error) => {
                    const parsedError = JSON.parse(error.responseText);
                    this.updateResponseError(parsedError.message || error);
                });
        }
    }
}

export default AreaSearchForm;
