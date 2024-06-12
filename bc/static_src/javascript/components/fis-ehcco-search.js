import accessibleAutocomplete from 'accessible-autocomplete';

class EHCCOSearch {
    static selector() {
        return '[data-ehcco-search]';
    }

    constructor(node) {
        this.node = node;
        this.searchWrapper = this.node.querySelector(
            '[data-autocomplete-wrapper]',
        );
        this.getMatchingSchoolsUrl = this.node.getAttribute(
            'data-matching-schools-url',
        );
        this.getCorrespondingEhcCoUrl = this.node.getAttribute(
            'data-ehc-co-url',
        );
        this.ehccoSchool = this.node.querySelector(
            '[data-autocomplete-school]',
        );
        this.ehccoName = this.node.querySelector('[data-autocomplete-name]');

        this.state = {
            school: null,
            name: null,
        };

        this.bindEvents();
    }

    bindEvents() {
        accessibleAutocomplete({
            element: this.searchWrapper,
            id: 'school-search', // To match the existing HTML element
            inputClasses: 'ehcco-search__input',
            menuClasses: 'ehcco-search__options',
            showNoOptionsFound: false,
            source: (query, populateResults) => {
                this.fetchMatchingSchools(query)
                    .then((results) => {
                        populateResults(
                            results.map((school) => ({
                                id: school.id,
                                label: school.text,
                            })),
                        );
                    })

                    .catch((error) =>
                        console.error('error getting schools:', error),
                    );
            },
            onConfirm: (selected) => {
                if (selected) {
                    this.state.school = selected.label;
                    this.fetchSchoolEHCCO(selected.id);
                }
            },
            templates: {
                inputValue: (result) => result && result.label,
                suggestion: (result) => result && result.label,
            },
        });
    }

    fetchMatchingSchools(query) {
        return fetch(`${this.getMatchingSchoolsUrl}?q=${query}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('response not ok');
                }
                return response.json();
            })
            .then((data) => {
                return data;
            });
    }

    fetchSchoolEHCCO(schoolId) {
        fetch(`${this.getCorrespondingEhcCoUrl}?school_id=${schoolId}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('response not ok');
                }
                return response.json();
            })
            .then((data) => {
                this.state.name = data.name;
                this.displayResult();
            })
            .catch((error) => console.error('error getting EHCCO', error));
    }

    displayResult() {
        if (this.state.school && this.state.name) {
            this.ehccoSchool.textContent = this.state.school;
            this.ehccoName.textContent = this.state.name;
        }
    }
}

export default EHCCOSearch;
