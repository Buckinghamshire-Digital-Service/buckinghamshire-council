import Highcharts from 'highcharts';

class Chart {
    static selector() {
        return '[data-chart]';
    }

    constructor(node) {
        this.node = node;
        this.containerId = node.getAttribute('id');
        this.scriptId = this.node.getAttribute('data-chart');
        this.chartData = JSON.parse(
            document.getElementById(this.scriptId).textContent,
        );

        const updatedSeries = this.convertDataToNumbers();
        this.chartData.series = updatedSeries;

        Highcharts.chart(this.containerId, this.chartData);
    }

    // chart data arrives as an array of numbers and we need it as integers for high charts
    convertDataToNumbers() {
        const updatedSeries = this.chartData.series.map((seriesItem) => {
            const updatedData = seriesItem.data.map((dataItem) =>
                parseInt(dataItem, 10),
            );
            seriesItem.data = updatedData;
            return seriesItem;
        });
        return updatedSeries;
    }
}

export default Chart;
