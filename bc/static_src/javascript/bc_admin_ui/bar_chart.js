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

        const verticalId = `${this.id}-handsontable-vertical`;
        const horizontalId = `${this.id}-handsontable-horizontal`;
        this.direction = $(`[name=handsontable-direction-${this.id}]`);
        this.vertical = $(`#${verticalId}`);
        this.horizontal = $(`#${horizontalId}`);
    }

    loadFieldData() {
        // eslint-disable-next-line no-underscore-dangle
        this._loadFieldData();

        if (this.dataForForm && this.dataForForm.direction) {
            // eslint-disable-next-line func-names
            this.direction.each(function() {
                $(this).removeAttr('checked');
            });
            this.direction
                .filter(`[value="${this.dataForForm.direction}"]`)
                .attr('checked', 'checked');
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
