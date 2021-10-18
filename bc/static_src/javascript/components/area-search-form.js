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
        this.postcodeErrorWrapper = this.form.querySelector(
            '[data-postcode-error-wrapper]',
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
        this.postcodeErrorWrapper.innerHTML = '';
        this.postcodeWrapper.classList.remove('form-item--errors');
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

    redirectToLocalAreaLink(area) {
        window.location.href = this.areaLinkUrls[area];
    }

    updateResponseBorderOverlap(html) {
        this.hideForm();
        this.appendResponseHTML(html);
    }

    updateAddresses(addresses) {
        const addressSelectDiv = document.createElement('div');
        const addressSelectElement = document.createElement('select');
        const errorDiv = document.createElement('div');
        errorDiv.classList.add('form-item__errors');

        addressSelectElement.addEventListener('change', (e) => {
            // stop propagration to prevent firing the form's onchange method
            e.stopPropagation();
        });

        let numAddresses = 0;
        Object.values(addresses).forEach((addressArray) => {
            numAddresses += addressArray.length;
        });

        const numAddressesOption = document.createElement('option');
        numAddressesOption.textContent = `${numAddresses} addresses found`;
        addressSelectElement.appendChild(numAddressesOption);

        Object.keys(addresses).forEach((district) => {
            const addressArray = addresses[district];
            addressArray.forEach((address) => {
                const option = document.createElement('option');
                option.setAttribute('value', district);
                option.textContent = address;
                addressSelectElement.appendChild(option);
            });
        });

        const furtherInfoButton = document.createElement('button');
        furtherInfoButton.textContent = 'Find further information';
        furtherInfoButton.classList.add(
            'button',
            'button--basic',
            'button--area-search',
        );

        furtherInfoButton.addEventListener('click', (e) => {
            e.preventDefault();
            if (addressSelectElement.value in this.areaLinkUrls) {
                this.redirectToLocalAreaLink(addressSelectElement.value);
            } else {
                // if option 'x addresses found' is selected
                errorDiv.innerText = 'Select a valid address';
            }
        });

        addressSelectDiv.appendChild(addressSelectElement);
        addressSelectDiv.appendChild(furtherInfoButton);
        addressSelectDiv.appendChild(errorDiv);

        this.responseText.appendChild(addressSelectDiv);
    }

    updateResponseMessage(message) {
        this.hideForm();
        this.appendResponseText(message);
    }

    updateResponseError(message) {
        this.responseClear();

        const errorListElement = document.createElement('ul');
        errorListElement.classList.add('errorlist');
        const errorMessageElement = document.createElement('li');
        errorMessageElement.innerText = message;
        errorListElement.appendChild(errorMessageElement);
        this.postcodeErrorWrapper.replaceChildren(errorListElement);
        this.postcodeWrapper.classList.add('form-item--errors');
    }

    submitForm() {
        const url = this.form.getAttribute('url');
        const postcodeValue = this.postcodeInput.value;

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
                    this.redirectToLocalAreaLink(response.area);
                } else if (response.border_overlap_html) {
                    this.updateResponseBorderOverlap(
                        response.border_overlap_html,
                    );
                    this.updateAddresses(response.addresses);
                    this.appendResponseHTML(response.contact_us_html);
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

export default AreaSearchForm;
