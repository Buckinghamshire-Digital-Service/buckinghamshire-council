/* global google */

import accessibleAutocomplete from 'accessible-autocomplete';

class LocationAutocomplete {
    static selector() {
        return '[data-autocomplete-container]';
    }

    constructor(node) {
        this.container = node;
        this.form = node.closest('form');
        this.labelId = node.dataset.labelId;

        this.latInput = this.form.querySelector('input[name="lat"]');
        this.lngInput = this.form.querySelector('input[name="lng"]');
        this.locationInput = this.form.querySelector('input[name="location"]');

        this.sessionToken = LocationAutocomplete.getSessionToken();

        this.autocompleteService = new google.maps.places.AutocompleteService();
        this.geocoder = new google.maps.Geocoder();

        this.focusOnLocation = false;
        this.locationSelected = false;

        this.bindEvents();

        this.predictions = [];
    }

    static getSessionToken() {
        return new google.maps.places.AutocompleteSessionToken();
    }

    deduceOption(autocompleteInput) {
        let item;
        if (autocompleteInput.value.trim() === '') {
            item = '';
        } else if (this.predictions.length === 0) {
            autocompleteInput.value = '';
            item = '';
        } else if (this.locationSelected) {
            const description = this.locationInput.value;
            item = this.predictions.find((p) => p.description === description);
            if (!item) {
                [item] = this.predictions;
            }
        } else {
            [item] = this.predictions;
        }
        this.selectElement(item);
    }

    bindEvents() {
        const self = this;
        accessibleAutocomplete({
            element: this.container,
            id: this.labelId,
            source: (query, populateResults) => {
                self.getLocations(query, populateResults);
            },
            displayMenu: 'overlay', // displays menu as an absolute positioned div
            autoSelect: true,
            minLength: 3, // minimum number of characters required to trigger autocomplete
            showNoOptionsFound: true, // displays a "no options found" message if no options are found
            templates: {
                suggestion: (item) =>
                    `<div class="autocomplete-suggestion">${item.description ||
                        item}</div>`,
                noResults: () =>
                    `<div class="autocomplete-no-results">No results found</div>`,
                inputValue: (item) => {
                    if (item) {
                        const placeId = item.place_id;
                        if (!placeId) {
                            return item;
                        }
                        return item.description;
                    }
                    return item;
                },
            },
            onConfirm: (item) => {
                if (item) {
                    this.selectElement(item, () => {
                        this.focusOnLocation = false;
                    });
                }
            },
        });
        this.autocompleteInput = this.container.querySelector('input');
        this.autocompleteInput.setAttribute(
            'placeholder',
            this.form
                .querySelector(`#${this.labelId}`)
                .getAttribute('placeholder'),
        );
        this.autocompleteInput.addEventListener('blur', (e) => {
            this.deduceOption(e.target);
        });
        this.autocompleteInput.addEventListener('focus', () => {
            this.focusOnLocation = true;
        });
        this.autocompleteInput.addEventListener('keydown', (e) => {
            if (e.keyCode === 13) {
                // enter key
                e.preventDefault();
                if (this.locationSelected) {
                    this.form.submit();
                    return;
                }
                this.deduceOption(e.target);
            }
        });

        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitForm();
        });
    }

    submitForm() {
        const waitForFocusChange = () =>
            new Promise((resolve) => {
                const interval = setInterval(() => {
                    if (!this.focusOnLocation) {
                        clearInterval(interval);
                        resolve();
                    }
                }, 10); // Check every 100 milliseconds
            });

        if (this.autocompleteInput.value.length < 3) {
            this.locationInput.value = '';
            this.latInput.value = '';
            this.lngInput.value = '';
            this.form.submit();
        } else {
            waitForFocusChange().then(() => {
                this.form.submit();
            });
        }
    }

    selectElement(item, cb) {
        if (item) {
            const placeId = item.place_id;
            this.geocoder.geocode({ placeId }, (results, status) => {
                if (status === 'OK') {
                    const { lat, lng } = results[0].geometry.location;
                    this.latInput.value = lat();
                    this.lngInput.value = lng();
                    this.locationInput.value = item.description;
                    this.autocompleteInput.value = item.description;
                } else {
                    // eslint-disable-next-line no-console
                    console.log(
                        `Geocoder failed due to: ${status}`,
                        results,
                        placeId,
                    );
                }
                if (cb) cb();
            });
        } else {
            this.locationInput.value = '';
            this.latInput.value = '';
            this.lngInput.value = '';
        }
        // regenerate a new session token after each selection
        // as per https://developers.google.com/maps/documentation/javascript/place-autocomplete#session_tokens
        this.sessionToken = LocationAutocomplete.getSessionToken();
        this.focusOnLocation = false;
        this.locationSelected = true;
    }

    getLocations(query, populateResults) {
        if (!this.focusOnLocation) return;
        this.locationSelected = false;

        this.autocompleteService.getPlacePredictions(
            {
                input: query,
                sessionToken: this.sessionToken,
                componentRestrictions: {
                    country: 'gb',
                },
                types: ['geocode'],
            },
            (predictions, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    this.predictions = predictions;
                } else {
                    // eslint-disable-next-line no-console
                    console.log(
                        'Autocomplete service failed: ',
                        status,
                        predictions,
                    );
                    this.predictions = [];
                }
                populateResults(this.predictions);
            },
        );
    }
}

export default LocationAutocomplete;
