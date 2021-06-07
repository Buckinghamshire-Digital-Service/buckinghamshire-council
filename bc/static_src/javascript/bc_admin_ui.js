import BarChart from './bc_admin_ui/bar_chart';
import Chart from './bc_admin_ui/chart';

class ChartInput {
    constructor(options, chartType) {
        this.options = options;
        this.chartType = chartType;
    }

    render(placeholder, name, id, initialState) {
        const container = document.createElement('div');

        const chartOptions = {
            'Pie chart': {
                konstructor: Chart,
                example: `
                    <table style="font-size: 0.85em;">
                        <tr>
                            <td style="padding-right:20px">Apples</td>
                            <td>234</td>
                        </tr>
                        <tr>
                            <td style="padding-right:20px">Pears</td>
                            <td>56</td>
                        </tr>
                        <tr>
                            <td style="padding-right:20px">Bananas</td>
                            <td>109</td>
                        </tr>
                    </table>
                `,
                dataHelpText:
                    'Enter labels in the first column and values in the second column. The values will be automatically converted to percentages.',
                direction: '', // Do not show this fragment
            },
            'Bar chart': {
                konstructor: BarChart,
                example: `
                    <table style="font-size: 0.85em;">
                        <tr>
                            <td style="padding-right:20px">Fruit eaten</td>
                            <td style="padding-right:20px">Orangutan</td>
                            <td style="padding-right:20px">Spider monkey</td>
                        </tr>
                        <tr>
                            <td style="padding-right:20px">Apples</td>
                            <td>2</td>
                            <td>3</td>
                        </tr>
                        <tr>
                            <td style="padding-right:20px">Pears</td>
                            <td>1</td>
                            <td>5</td>
                        </tr>
                        <tr>
                            <td style="padding-right:20px">Bananas</td>
                            <td>10</td>
                            <td>2</td>
                        </tr>
                    </table>
                `,
                dataHelpText:
                    'The first column will be the x axis. The first row will be labels for groups of data in each bar.',
                direction: `
                    <div class="required">
                        <div class="required field typed_choice_field radio_select">
                            <label for="${id}-handsontable-direction">Chart direction</label>
                            <div class="field-content">
                                <div class="input">
                                    <ul>
                                        <li>
                                            <div>
                                                <label for="${id}-handsontable-horizontal">
                                                    <input type="radio" id="${id}-handsontable-horizontal" name="handsontable-direction-${id}" value="horizontal" required />
                                                    <span>Horizontal</span>
                                                </label>
                                            </div>
                                            <div>
                                                <label for="${id}-handsontable-vertical">
                                                    <input type="radio" id="${id}-handsontable-vertical" name="handsontable-direction-${id}" value="vertical" required checked="checked" />
                                                    <span>Vertical</span>
                                                </label>
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                                <p class="help">Choose whether the bars of the chart display horizontally or vertically.</p>
                            </div>
                        </div>
                    </div>
                `,
            },
            'Line graph': {
                konstructor: Chart,
                example: `
                    <table style="font-size: 0.85em;">
                        <tr>
                            <td style="padding-right:20px">Year</td>
                            <td style="padding-right:20px">Waste management</td>
                            <td style="padding-right:20px">Construction</td>
                        </tr>
                        <tr>
                            <td>2010</td>
                            <td>43934</td>
                            <td>24916</td>
                        </tr>
                        <tr>
                            <td>2011</td>
                            <td>52503</td>
                            <td>24064</td>
                        </tr>
                        <tr>
                            <td>2012</td>
                            <td>57177</td>
                            <td>29742</td>
                        </tr>
                    </table>
                `,
                dataHelpText:
                    'The first column will be the x axis. The first row will be labels for each line on the chart.',
                direction: '', // Do not show this fragment
            },
        }[this.chartType];

        container.innerHTML = `
            <div class="field">
                <label for="${id}-handsontable-title">Chart and table title</label>
                <div class="field-content">
                    <div class="input">
                    <input type="text" id="${id}-handsontable-title" name="handsontable-title"/>
                    </div>
                    <p class="help">Use the title to describe what the chart and table show.
                    The title helps users find, navigate and understand charts and tables.
                    If you do not enter a title, it will display "${this.chartType}".</p>
                </div>
            </div>
            <br/>
            <div class="field">
                <label for="${id}-handsontable-caption">Chart and table caption</label>
                <div class="field-content">
                    <div class="input">
                    <input type="text" id="${id}-handsontable-caption" name="handsontable-caption"/>
                    </div>
                    <p class="help">A short description of the data being displayed and its source.</p>
                </div>
            </div>
            <br/>
            <div class="field boolean_field widget-checkbox_input">
                <label for="${id}-handsontable-show-table-first">Show table first</label>
                <div class="field-content">
                    <div class="input">
                        <input
                            type="checkbox"
                            id="${id}-handsontable-show-table-first" name="handsontable-show-table-first"
                            checked="checked"
                        />
                    </div>
                    <p class="help">Select this to display the table, and the chart will be displayed by clicking a link. If you do not select this box, the chart will be displayed first.</p>
                </div>
            </div>
            <br/>

            ${chartOptions.direction}

            <br/>

            <div class="field">
                <label for="${id}-handsontable-container">Data</label>
                <div class="field-content">
                    <p class="help">
                        ${chartOptions.dataHelpText}
                        An example of a chart data set:
                    </p>
                    ${chartOptions.example}
                    <p class="help">Right click anywhere on the table to change the table layout.</p>

                    <div id="${id}-handsontable-container"></div>
                    <input type="hidden" name="${name}" id="${id}" placeholder="Table">
                </div>
            </div>
        `;
        placeholder.replaceWith(container);

        const input = container.querySelector(`input[name="${name}"]`);
        const { options } = this;

        const widget = {
            getValue() {
                return JSON.parse(input.value);
            },
            getState() {
                return JSON.parse(input.value);
            },
            setState(state) {
                input.value = JSON.stringify(state);
                // eslint-disable-next-line no-new, new-cap
                new chartOptions.konstructor(id, options);
            },
            focus() {},
        };
        widget.setState(initialState);
        return widget;
    }
}
window.telepath.register('bc.utils.widgets.ChartInput', ChartInput);
