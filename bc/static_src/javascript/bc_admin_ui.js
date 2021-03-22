import BarChart from './bc_admin_ui/bar_chart';
import Chart from './bc_admin_ui/chart';

document.addEventListener('DOMContentLoaded', () => {
    // initBarChart will be called in the HTML so that the id can be provided
    window.initBarChart = (id, tableOptions) => {
        // eslint-disable-next-line no-new
        new BarChart(id, tableOptions);
    };
    window.initPieChart = (id, tableOptions) => {
        // eslint-disable-next-line no-new
        new Chart(id, tableOptions);
    };
    window.initLineChart = (id, tableOptions) => {
        // eslint-disable-next-line no-new
        new Chart(id, tableOptions);
    };
});
