/* global $, Handsontable */

function stringify(value) {
    let result;

    switch (typeof value) {
        case 'string':
        case 'number':
            result = `${value}`;
            break;

        case 'object':
            result = value === null ? '' : value.toString();
            break;
        case 'undefined':
            result = '';
            break;
        default:
            result = value.toString();
            break;
    }

    return result;
}

function addAnchorTagsInMarkdown(value) {
    // this function is used to identify links in the text and replace them with anchor tags
    let result = value;
    // urlRegex matches cases like [link](http://www.example.com) or simply http://www.example.com
    const urlRegex = /(\[([^\]]+)\]\()?(https?:\/\/|www\.)[^\s]+(\))?/g;
    const matches = value.match(urlRegex);
    if (matches) {
        matches.forEach((match) => {
            // if the match is of the form [link](http://www.example.com)
            if (match.startsWith('[')) {
                const linkText = match.split(']')[0].slice(1);
                const linkUrl = match.split(']')[1].slice(1, -1);
                result = result.replace(
                    match,
                    `<a href="${linkUrl}">${linkText}</a>`,
                );
            } else {
                result = result.replace(
                    match,
                    `<a href="${match}">${match}</a>`,
                );
            }
        });
    }
    return result;
}

function TextRendered(instance, TD, row, col, prop, value, cellProperties) {
    // eslint-disable-next-line prefer-rest-params
    Handsontable.renderers.BaseRenderer.apply(this, arguments);

    let escaped = value;

    if (!escaped && cellProperties.placeholder) {
        escaped = cellProperties.placeholder;
    }

    escaped = stringify(escaped);

    if (cellProperties.trimWhitespace) {
        escaped = escaped.trim();
    }

    escaped = addAnchorTagsInMarkdown(escaped);

    TD.innerHTML = escaped;
}

$(document).ready(() => {
    Handsontable.renderers.registerRenderer('html', TextRendered);
});
