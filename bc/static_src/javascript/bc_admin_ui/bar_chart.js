import Chart from './chart'

class BarChart extends Chart {
    bindEvents(tableOptions) {
        // eslint-disable-next-line no-underscore-dangle, no-undef
        this._bindEvents(tableOptions);

        const boundPersist = this.persist.bind(this);

        this.direction.on('change', () => {
            boundPersist();
        });
    }

    getFields() {
        // eslint-disable-next-line no-underscore-dangle
        this._getFields();

        const directionId = `${this.id}-handsontable-direction`;
        // eslint-disable-next-line no-undef
        this.direction = $(`#${directionId}`);
    }

    loadFieldData() {
        // eslint-disable-next-line no-underscore-dangle
        this._loadFieldData();

        if (this.dataForForm !== null) {
            if (Object.prototype.hasOwnProperty.call('dataForForm', 'direction')) {
                this.direction.prop('value', this.dataForForm.direction);
            }
        }
    }

    _persistData() {
        // eslint-disable-next-line no-underscore-dangle
        const data = this._persistChartData();
        data.direction = this.direction.val();
        return data;
    }
}

export default BarChart;
