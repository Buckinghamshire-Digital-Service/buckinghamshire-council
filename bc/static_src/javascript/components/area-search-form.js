class AreaSearchForm {
    static selector() {
        return '[data-area-search]';
    }

    constructor(node) {
        this.form = node;
        this.submitButton = this.form.querySelector('[data-submit-button]');

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
        this.moreInfoButtons = this.form.querySelectorAll(
            '[data-more-info-button]',
        );
        this.postcodeLookupTexts = this.form.querySelectorAll(
            '[data-postcode-lookup-text]',
        );
        this.addressLookupTexts = this.form.querySelectorAll(
            '[data-address-lookup-text]',
        );
        this.areaLookupTexts = this.form.querySelectorAll(
            '[data-area-lookup-text]',
        );
        this.changePostcodeButton = this.form.querySelector(
            '[data-change-postcode]',
        );
        this.areaLinksDiv = this.form.querySelector('[data-local-links]');
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

        this.moreInfoButtons.forEach((button) => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.hideForm();
                this.showAreaLinks();
                this.postcodeLookupTexts.forEach((el) =>
                    el.setAttribute('hidden', ''),
                );
                this.addressLookupTexts.forEach((el) =>
                    el.setAttribute('hidden', ''),
                );
                this.areaLookupTexts.forEach((el) =>
                    el.removeAttribute('hidden'),
                );
            });
        });

        this.changePostcodeButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.revertFormState();
        });
    }

    showAreaLinks() {
        this.areaLinksDiv.removeAttribute('hidden');
    }

    hideAreaLinks() {
        this.areaLinksDiv.setAttribute('hidden', '');
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
    }

    showForm() {
        this.responseClear();
        this.postcodeWrapper.classList.remove('hide');
        this.submitButton.classList.remove('hide');
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

    revertFormState() {
        this.showForm();
        this.hideAreaLinks();
        this.addressLookupTexts.forEach((el) => el.setAttribute('hidden', ''));
        this.postcodeLookupTexts.forEach((el) => el.removeAttribute('hidden'));
        this.areaLookupTexts.forEach((el) => el.setAttribute('hidden', ''));
    }

    updateResponsePostcode(postcode) {
        const div = document.createElement('div');
        div.innerHTML = `<strong>${postcode}</strong>`;
        const changePostcodeButton = document.createElement('a');
        changePostcodeButton.classList.add(
            'area-search__button--change-postcode',
        );
        changePostcodeButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.revertFormState();
        });
        changePostcodeButton.innerText = 'Change';
        div.appendChild(changePostcodeButton);
        this.responseText.appendChild(div);
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

        const numAddressesOption = document.createElement('option');
        numAddressesOption.textContent = `${addresses.length} addresses found`;
        numAddressesOption.setAttribute('hidden', '');
        addressSelectElement.appendChild(numAddressesOption);

        addresses.forEach(([district, address]) => {
            const option = document.createElement('option');
            option.setAttribute('value', district);
            option.textContent = address;
            addressSelectElement.appendChild(option);
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

        const addressSelectWrapper = document.createElement('div');
        addressSelectWrapper.classList.add(
            'area-search__response-select-wrapper',
        );
        addressSelectWrapper.appendChild(addressSelectElement);

        addressSelectDiv.appendChild(addressSelectWrapper);
        addressSelectDiv.appendChild(furtherInfoButton);
        addressSelectDiv.appendChild(errorDiv);

        this.responseText.appendChild(addressSelectDiv);

        this.postcodeLookupTexts.forEach((el) => el.setAttribute('hidden', ''));
        this.addressLookupTexts.forEach((el) => el.removeAttribute('hidden'));
        this.areaLookupTexts.forEach((el) => el.setAttribute('hidden', ''));
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
                    this.hideForm();
                    this.updateResponsePostcode(postcodeValue);
                    this.appendResponseHTML(response.border_overlap_html);
                    this.updateAddresses(response.addresses);
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
