/* global $ */
import Chart from './chart';

class PieChart extends Chart {
    initHandsonTable(containerId, tableOptions) {
        tableOptions.startCols = 2;
        tableOptions.maxCols = 2;
        tableOptions.allowInsertColumn = false;
        tableOptions.allowRemoveColumn = false;
        this._initHandsonTable(containerId, tableOptions);
    }
}

export default PieChart;
