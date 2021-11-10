/* global google */

const strip = (str) => {
    let strippedStr = str;
    if (strippedStr.startsWith('[')) {
        strippedStr = strippedStr.substr(1);
    }

    if (strippedStr.endsWith(']')) {
        strippedStr = strippedStr.slice(0, -1);
    }

    return strippedStr;
};

class GoogleMap {
    static selector() {
        return '.js-map';
    }

    constructor(node) {
        this.node = node;

        // remove the [ and ] characters from the strings
        this.latitudes = strip(this.node.dataset.latitudes).split(',');
        this.longitudes = strip(this.node.dataset.longitudes).split(',');

        this.locations = [];
        this.latitudes.forEach((latitude, ind) => {
            const longitude = this.longitudes[ind];
            if (latitude.length === 0 || longitude.length === 0) return;
            this.locations.push({
                lat: parseFloat(latitude),
                lng: parseFloat(longitude),
            });
        });
        this.zoom = parseInt(this.node.dataset.zoomLevel, 10);

        // populated in mapLoad();
        this.googleMap = null;
        this.markers = null;

        this.mapLoad();
    }

    mapLoad() {
        if (this.locations.length === 0) return;
        this.googleMap = new google.maps.Map(this.node, {
            zoom: this.zoom,
            scrollwheel: false,
            streetViewControl: false,
            mapTypeControl: false,
            fullscreenControl: true,
            center: this.locations[0],
        });
        this.markers = this.locations.map(
            (location) =>
                new google.maps.Marker({
                    position: location,
                    map: this.googleMap,
                }),
        );
    }
}

export default GoogleMap;
