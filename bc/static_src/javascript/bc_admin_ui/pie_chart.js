import Chart from './chart';

class PieChart extends Chart {
    initHandsonTable(containerId, tableOptions) {
        // Only show 2 columns, and don't allow columns to be added or removed
        tableOptions.startCols = 2;
        tableOptions.maxCols = 2;
        tableOptions.allowInsertColumn = false;
        tableOptions.allowRemoveColumn = false;
        // eslint-disable-next-line no-underscore-dangle
        this._initHandsonTable(containerId, tableOptions);
    }
}

export default PieChart;
