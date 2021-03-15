/* global $ Handsontable */
class Chart {
    constructor(id, tableOptions) {
        this.id = id;
        const containerId = `${id}-handsontable-container`;

        this.resizeTargets = [
            '.input > .handsontable',
            '.wtHider',
            '.wtHolder',
        ];
        this.isInitialized = false;

        this.getFields();

        // Load previously saved data into the fields
        this.readData();
        this.loadFieldData();

        this.bindEvents(tableOptions);
        this.initHandsonTable(containerId, tableOptions);

        // Apply resize after document is finished loading (parent .sequence-member-inner width is set)
        if ('resize' in $(window)) {
            this.resizeHeight.bind(this)(this.getHeight());
            $(window).on('load', () => {
                $(window).trigger('resize');
            });
        }
    }

    _bindEvents(tableOptions) {
        if (tableOptions && (tableOptions.width || tableOptions.height)) {
            // Size to parent .sequence-member-inner width if width is not given in tableOptions
            // eslint-disable-next-line func-names
            const resizeAction = function() {
                this.hot.updateSettings({
                    width: this.getWidth(),
                    height: this.getHeight(),
                });
                this.resizeWidth('100%');
            };
            $(window).on('resize', resizeAction.bind(this));
        }

        const boundPersist = this.persist.bind(this);

        this.chartCaption.on('change', () => {
            boundPersist();
        });

        this.tableFirst.on('change', () => {
            boundPersist();
        });

        this.tableTitle.on('change', () => {
            boundPersist();
        });
    }

    bindEvents(tableOptions) {
        // eslint-disable-next-line no-underscore-dangle
        this._bindEvents(tableOptions);
    }

    getCellsClassnames() {
        const meta = this.hot.getCellsMeta();
        const cellsClassnames = [];
        for (let i = 0; i < meta.length; i += 1) {
            const currentMeta = meta[i];
            if (currentMeta && currentMeta.className) {
                cellsClassnames.push({
                    row: meta[i].row,
                    col: meta[i].col,
                    className: meta[i].className,
                });
            }
        }
        return cellsClassnames;
    }

    getDefaultOptions() {
        const boundPersist = this.persist.bind(this);

        const cellEvent = (change, source) => {
            if (source === 'loadData') {
                return; // don't save this change
            }

            boundPersist();
        };

        /* eslint-disable no-unused-vars */
        const metaEvent = (row, column, key, value) => {
            if (this.isInitialized && key === 'className') {
                boundPersist();
            }
        };
        /* eslint-enable no-unused-vars */

        const initEvent = () => {
            this.isInitialized = true;
        };

        /* eslint-disable no-unused-vars */
        const structureEvent = (index, amount) => {
            this.resizeHeight(this.getHeight());
            boundPersist();
        };
        const boundStructureEvent = structureEvent.bind(this);
        /* eslint-enable no-unused-vars */

        return {
            afterChange: cellEvent.bind(this),
            afterCreateCol: boundStructureEvent,
            afterCreateRow: boundStructureEvent,
            afterRemoveCol: boundStructureEvent,
            afterRemoveRow: boundStructureEvent,
            afterSetCellMeta: metaEvent.bind(this),
            afterInit: initEvent.bind(this),
            // contextMenu set via init, from server defaults
        };
    }

    _getFields() {
        const chartCaptionId = `${this.id}-handsontable-caption`;
        const tableFirstId = `${this.id}-handsontable-show-table-first`;
        const tableTitleId = `${this.id}-handsontable-title`;

        this.hiddenStreamInput = $(`#${this.id}`);
        this.chartCaption = $(`#${chartCaptionId}`);
        this.tableFirst = $(`#${tableFirstId}`);
        this.tableTitle = $(`#${tableTitleId}`);
    }

    getFields() {
        // eslint-disable-next-line no-underscore-dangle
        this._getFields();
    }

    getHeight() {
        const tableParent = $(`#${this.id}`).parent();
        return (
            tableParent.find('.htCore').height() +
            tableParent.find('.input').height() * 2
        );
    }

    /* eslint-disable class-methods-use-this */
    getWidth() {
        return $('.widget-table_input')
            .closest('.sequence-member-inner')
            .width();
    }
    /* eslint-enable class-methods-use-this */

    initHandsonTable(containerId, tableOptions) {
        const defaultOptions = this.getDefaultOptions();

        if (this.dataForForm !== null) {
            // Overrides default value from tableOptions (if given) with value from database
            if (this.dataForForm.data) {
                defaultOptions.data = this.dataForForm.data;
            }

            if (this.dataForForm.data.cell) {
                defaultOptions.cell = this.dataForForm.cell;
            }
        }

        const finalOptions = {};
        Object.keys(defaultOptions).forEach((key) => {
            finalOptions[key] = defaultOptions[key];
        });
        Object.keys(tableOptions).forEach((key) => {
            finalOptions[key] = tableOptions[key];
        });

        this.hot = new Handsontable(
            document.getElementById(containerId),
            finalOptions,
        );
        this.hot.render(); // Call to render removes 'null' literals from empty cells
    }

    // To Implement: Override with specific chart fields
    _loadFieldData() {
        if (this.dataForForm !== null) {
            if (this.dataForForm.chart_caption) {
                this.chartCaption.prop('value', this.dataForForm.chart_caption);
            }
            if (this.dataForForm.table_first) {
                this.tableFirst.attr('checked', this.dataForForm.table_first);
            }
            if (this.dataForForm.table_title) {
                this.tableTitle.prop('value', this.dataForForm.table_title);
            }
        }
    }

    loadFieldData() {
        // eslint-disable-next-line no-underscore-dangle
        this._loadFieldData();
    }

    _persistChartData() {
        return {
            id: this.id,
            data: this.hot.getData(),
            cell: this.getCellsClassnames(),
            chart_caption: this.chartCaption.val(),
            table_first: this.tableFirst.is(':checked'),
            table_title: this.tableTitle.val(),
        };
    }

    _persistData() {
        // eslint-disable-next-line no-underscore-dangle
        return this.__persistChartData();
    }

    persist() {
        // eslint-disable-next-line no-underscore-dangle
        this.hiddenStreamInput.val(JSON.stringify(this._persistData()));
    }

    readData() {
        try {
            this.dataForForm = JSON.parse(this.hiddenStreamInput.val());
        } catch (e) {
            // do nothing
        }
    }

    resizeHeight(height) {
        const currTable = $(`#${this.id}`);
        $.each(this.resizeTargets, () => {
            currTable
                .closest('.field-content')
                .find(this)
                .height(height);
        });
    }

    resizeWidth(width) {
        $.each(this.resizeTargets, () => {
            $(this).width(width);
        });
        const parentDiv = $('.widget-table_input').parent();
        parentDiv.find('.field-content').width(width);
        parentDiv
            .find('.fieldname-table .field-content .field-content')
            .width('80%');
    }
}

// To implement:
// initChart will be called in the HTML so that the id can be provided
// window.initChart = (id, tableOptions) => {
//     new Chart(id, tableOptions);
// }
/* eslint-enable no-undef */

export default Chart;
