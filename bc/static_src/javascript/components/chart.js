import Highcharts from 'highcharts';

// Global highcharts settings
Highcharts.setOptions({
    colors: ['#2c2d84', '#4a8500', '#fcbc00', '#9fc63b', '#ed7004', '#c72833'],
    lang: {
        thousandsSep: ',',
    },
});

class Chart {
    static selector() {
        return '[data-chart-block]';
    }

    constructor(node) {
        this.node = node;
        this.chartNode = node.querySelector('[data-chart]');
        this.containerId = this.chartNode.getAttribute('id');
        this.scriptId = this.chartNode.getAttribute('data-chart');
        this.chartData = JSON.parse(
            document.getElementById(this.scriptId).textContent,
        );
        this.toggleToTable = node.querySelector('[data-to-table]');
        this.toggleToChart = node.querySelector('[data-to-chart]');
        this.tableWrapper = node.querySelector('[data-table-wrapper]');
        this.chartWrapper = node.querySelector('[data-chart-wrapper]');
        this.hiddenClass = 'chart-block__wrapper--hidden';
        // General text styles for legend, axis labels and axis titles
        this.textStyles = {
            color: '#212121',
            fontFamily: 'Helvetica',
            fontSize: '14px',
            fontWeight: 'normal',
        };
        // Disbled hover options
        this.disbledHover = {
            hover: {
                halo: false,
                enabled: false,
            },
            inactive: {
                opacity: 1,
            },
        };

        // Configure various highcharts options
        if (
            this.chartData.chart.type === 'bar' ||
            this.chartData.chart.type === 'column'
        ) {
            // set up bar and column charts
            this.configureBarChartOptions();
        } else if (this.chartData.chart.type === 'pie') {
            this.configurePieChartOptions();
        } else if (this.chartData.chart.type === 'line') {
            this.configureLineChartOptions();
        }

        this.configureCommonOptions();

        // Initialise chart
        Highcharts.chart(this.containerId, this.chartData);

        this.bindEvents();
    }

    bindEvents() {
        this.toggleToTable.addEventListener('click', () => {
            this.showTable();
        });

        this.toggleToChart.addEventListener('click', () => {
            this.showChart();
        });
    }

    showChart() {
        this.tableWrapper.classList.add(this.hiddenClass);
        this.chartWrapper.classList.remove(this.hiddenClass);
    }

    showTable() {
        this.tableWrapper.classList.remove(this.hiddenClass);
        this.chartWrapper.classList.add(this.hiddenClass);
    }

    configureBarChartOptions() {
        // Don't show the bar chart data the wrong way round
        this.chartData.yAxis.reversedStacks = false;

        this.chartData.plotOptions = {
            series: {
                dataLabels: {
                    enabled: true,
                    crop: false,
                    overflow: 'none',
                    // hide the data label if the value is 0 or if the percentage width is less than 10
                    // conditionally set the colour of the label based on the background colour
                    // disabling warnings because following highcharts recommended syntax
                    // eslint-disable-next-line consistent-return, object-shorthand, func-names
                    formatter: function() {
                        if (this.y && this.percentage > 10) {
                            let labelColour = 'white';
                            if (
                                this.color === '#fcbc00' ||
                                this.color === '#9fc63b'
                            ) {
                                labelColour = '#212121';
                            }
                            // add thousands separator by hand as returning this.y loses the
                            // global option
                            return `<span style="color: ${labelColour}">${this.y.toLocaleString()}</span>`;
                        }
                    },
                    style: {
                        textOutline: false,
                        fontFamily: 'Helvetica',
                        fontSize: '12px',
                        fontWeight: 'normal',
                    },
                },
                groupPadding: 0,
                borderWidth: 0,
                stacking: 'normal',
                // disable hover effects
                states: this.disbledHover,
            },
        };

        // Axis styling
        this.configureAxisStyles();

        // Legend styling
        this.chartData.legend = {
            margin: 20,
            itemStyle: this.textStyles,
        };
    }

    configurePieChartOptions() {
        this.chartData.plotOptions = {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b><br />{point.y} %',
                    style: this.textStyles,
                    connectorColor: '#6c6c6b',
                    alignTo: 'plotEdges',
                    connectorShape: 'crookedLine',
                },
                states: this.disbledHover,
                borderWidth: 0,
            },
        };
    }

    configureLineChartOptions() {
        this.chartData.plotOptions = {
            series: {
                label: {
                    connectorAllowed: false,
                },
                states: this.disbledHover,
                marker: {
                    enabled: false,
                },
            },
        };
        // Axis styling
        this.configureAxisStyles();
    }

    configureCommonOptions() {
        // Hide overall chart title as we add our own above
        this.chartData.title = null;
        this.chartData.chart.backgroundColor = '#eee';
    }

    configureAxisStyles() {
        // Axis styling
        const axisOptions = {
            margin: 20,
            style: this.textStyles,
        };

        this.chartData.xAxis.labels = axisOptions;
        this.chartData.yAxis.labels = axisOptions;
        this.chartData.xAxis.title = {
            ...axisOptions,
            ...this.chartData.xAxis.title,
        };

        this.chartData.yAxis.title = {
            ...axisOptions,
            ...this.chartData.yAxis.title,
        };
    }
}

export default Chart;
