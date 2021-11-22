/* global google */

const getLatLng = (location) => ({
    lat: parseFloat(location.lat),
    lng: parseFloat(location.lng),
});

class GoogleMap {
    static selector() {
        return '.js-map';
    }

    constructor(node) {
        this.node = node;
        this.locations = JSON.parse(
            document.getElementById('markers').textContent,
        );

        // if there's only 1 location, convert it to array for further processing
        if (!Array.isArray(this.locations)) {
            this.locations = [this.locations];
        }
        this.zoom = parseInt(this.node.dataset.zoomLevel, 10);
        this.markerImageURL = this.node.dataset.markerImageUrl;

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
            center: getLatLng(this.locations[0]),
        });
        this.markers = this.locations.map((location) => {
            const marker = new google.maps.Marker({
                position: getLatLng(location),
                map: this.googleMap,
                icon: this.markerImageURL,
            });
            const infowindow = new google.maps.InfoWindow({
                content: location.map_info_text,
            });
            marker.addListener('click', () => {
                infowindow.open({
                    anchor: marker,
                    map: this.googleMap,
                    shouldFocus: false,
                });
            });
            return marker;
        });
    }
}

export default GoogleMap;
