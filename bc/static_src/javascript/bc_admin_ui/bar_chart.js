/* global $ */
import Chart from './chart';

class BarChart extends Chart {
    bindEvents(tableOptions) {
        // eslint-disable-next-line no-underscore-dangle
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
        const verticalId = `${this.id}-handsontable-vertical`;
        const horizontalId = `${this.id}-handsontable-horizontal`;
        this.direction = $(`#${directionId} [name=handsontable-direction]`);
        this.vertical = $(`#${verticalId}`);
        this.horizontal = $(`#${horizontalId}`);
    }

    loadFieldData() {
        // eslint-disable-next-line no-underscore-dangle
        this._loadFieldData();

        if (this.dataForForm && this.dataForForm.direction) {
            this.direction
                .filter(`[value="${this.dataForForm.direction}"]`)
                .attr('checked', true);
        }
    }

    _persistData() {
        // eslint-disable-next-line no-underscore-dangle
        const data = this._persistChartData();
        data.direction = this.horizontal.is(':checked')
            ? 'horizontal'
            : 'vertical';
        return data;
    }
}

export default BarChart;
