import BarChart from './bc_admin_ui/bar_chart';

document.addEventListener('DOMContentLoaded', () => {
    // initBarChart will be called in the HTML so that the id can be provided
    window.initBarChart = (id, tableOptions) => {
        // eslint-disable-next-line no-new
        new BarChart(id, tableOptions);
    }
});
