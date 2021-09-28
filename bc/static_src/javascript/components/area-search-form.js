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
        this.input = this.form.querySelector('[data-input-value]');
        this.formInfo = this.form.querySelector('[data-form-info]');
        this.responseText = this.form.querySelector('[data-response-text]');
        this.formInputWrapper = this.form.querySelector(
            '[data-form-input-wrapper]',
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
            this.toggleForm();
        });
    }

    responseClear() {
        this.responseText.innerHTML = '';
        this.form.classList.remove('form--area-search-error');
        this.responseText.classList.remove('area-search__response-text--error');
    }

    toggleForm() {
        this.responseClear();

        if (this.formInputWrapper.classList.contains('hide')) {
            this.formInputWrapper.classList.remove('hide');
            this.formInfo.classList.remove('hide');
            this.findAnotherButton.classList.add('hide');
        } else {
            this.formInputWrapper.classList.add('hide');
            this.formInfo.classList.add('hide');
            this.findAnotherButton.classList.remove('hide');
        }
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

    updateResponseArea(html, name) {
        this.toggleForm();
        this.appendResponseHTML(html);

        const block = this.form.closest('[data-area-links]');
        const bucksAreas = {
            'Aylesbury Vale': {
                link:
                    block.querySelector('[data-area-link="aylesbury-vale-url"]')
                        .href || 'https://www.aylesburyvaledc.gov.uk/',
                shortname: 'Aylesbury Vale',
            },
            'Wycombe': {
                link:
                    block.querySelector('[data-area-link="wycombe-url"]')
                        .href || 'https://www.wycombe.gov.uk/',
                shortname: 'Wycombe',
            },
            'Chiltern': {
                link:
                    block.querySelector('[data-area-link="chiltern-url"]')
                        .href || 'https://www.chiltern.gov.uk/',
                shortname: 'Chiltern',
            },
            'South Bucks': {
                link:
                    block.querySelector('[data-area-link="south-bucks-url"]')
                        .href || 'https://www.southbucks.gov.uk/',
                shortname: 'South Bucks',
            },
        };
        const areaName = name;

        if (areaName in bucksAreas === true) {
            const buttonElement = document.createElement('button');
            buttonElement.innerText = `Go to ${bucksAreas[name].shortname}`;
            buttonElement.classList.add('button');
            buttonElement.classList.add('button--basic');
            buttonElement.classList.add('button--area-search');
            buttonElement.type = 'button';
            buttonElement.onclick = () => {
                location.href = `${bucksAreas[name].link}`; // eslint-disable-line
            };
            this.responseText.appendChild(buttonElement);
        }
    }

    updateResponseBorderOverlap(html) {
        this.toggleForm();
        this.appendResponseHTML(html);
    }

    updateResponseMessage(message) {
        this.toggleForm();
        this.appendResponseText(message);
    }

    updateResponseError(message) {
        this.responseClear();
        this.responseError();
        this.appendResponseText(message);
    }

    submitForm() {
        const url = this.form.getAttribute('url');
        const postcodeValue = this.input.value;

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
                        this.updateResponseArea(response.html, response.area);
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
