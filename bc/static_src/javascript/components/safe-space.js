const hostWidgetInContainer = (result, targetEl) => {
    const iframe = document.createElement('iframe');
    iframe.setAttribute('id', 'safe-space-iframe');
    targetEl.appendChild(iframe);
    targetEl.style.overflow = 'hidden';
    iframe.setAttribute(
        'style',
        'height:100%;width:100%;position:fixed;top:0;bottom:0;background-color:rgba(0,0,0,0.26);z-index:2000',
    );
    iframe.contentDocument.open();
    iframe.contentDocument.write(result);
    iframe.contentDocument.close();
    iframe.focus();
};

const launchSafeSpace = () => {
    fetch('https://apps.parcelforce.com/sso/')
        .then((resp) => resp.text())
        .then((resp) => hostWidgetInContainer(resp, document.body))
        .catch((err) => {
            console.log(err); // eslint-disable-line no-console
        });
};

const isSafeSpaceAvailable = () => {
    fetch('https://apps.parcelforce.com/sso/Home/IsAlive')
        .then((resp) => resp.json())
        .then((_) => launchSafeSpace()) // eslint-disable-line no-unused-vars
        .catch((err) => {
            console.log(err); // eslint-disable-line no-console
        });
};

class SafeSpace {
    static selector() {
        return '[data-launch-safespace]';
    }

    constructor(node) {
        this.node = node;
        this.bindEvents();
        this.widgetComponentId = 'safeSpaceWidget-Component';
    }

    bindEvents() {
        this.node.addEventListener('click', (e) => this.onSafeSpaceClick(e));
    }

    onSafeSpaceClick(e) {
        e.stopPropagation();
        isSafeSpaceAvailable();
        document.body.addEventListener('keyup', (e1) => {
            e1.stopPropagation();
            if (e1.key === 'Escape') {
                this.destroySafeSpaceWidget();
            }
        });
    }

    destroySafeSpaceWidget() {
        const widgetContainer = document.getElementById(this.widgetComponentId);
        if (widgetContainer) {
            widgetContainer.parentNode.style.overflow = '';
            widgetContainer.parentNode.removeChild(widgetContainer);
        }
    }
}

export default SafeSpace;
