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
        // this.ehccoSchool = this.node.querySelector(
        //     '[data-autocomplete-school]',
        // );
        this.ehccoName = this.node.querySelector('[data-autocomplete-name]');
        this.bindEvents();
    }

    bindEvents() {
        accessibleAutocomplete({
            element: this.searchWrapper,
            id: 'school-search', // To match the existing HTML element
            source: (query, populateResults) => {
                this.fetchMatchingSchools(query)
                    .then((results) => {
                        populateResults(
                            results.map((school) => ({
                                id: school.id,
                                label: school.name,
                            })),
                        );
                    })
                    .catch((error) =>
                        console.error('error getting schools:', error),
                    );
            },
            onConfirm: (selected) => {
                if (selected) {
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
                console.log('getMatchingSchoolsUrl response:', response);
                if (!response.ok) {
                    throw new Error('response not ok');
                }
                return response.json();
            })
            .then((data) => {
                console.log('getMatchingSchoolsUrl data:', data);
                return data;
            });
    }

    fetchSchoolEHCCO(schoolId) {
        fetch(`${this.getCorrespondingEhcCoUrl}?school_id=${schoolId}`)
            .then((response) => {
                console.log('getCorrespondingEhcCoUrl response:', response); // Debugging
                if (!response.ok) {
                    throw new Error('response not ok');
                }
                return response.json();
            })
            .then((data) => {
                console.log('getCorrespondingEhcCoUrl data:', data);
                this.displayEHCCO(data.name);
            })
            .catch((error) => console.error('error getting EHCCO', error));
    }

    displayEHCCO(name) {
        this.ehccoName.textContent = name;
    }
}

export default EHCCOSearch;
