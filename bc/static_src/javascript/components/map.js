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

    openInfoWindow(marker) {
        if (marker.isOpen) return;
        marker.isOpen = true;
        marker.infowindow.open({
            anchor: marker.marker,
            map: this.googleMap,
            shouldFocus: false,
        });
    }

    static closeInfoWindow(marker) {
        if (!marker.isOpen) return;
        marker.isOpen = false;
        marker.infowindow.close();
    }

    toggleInfoWindow(marker) {
        if (marker.isOpen) {
            GoogleMap.closeInfoWindow(marker);
        } else {
            this.openInfoWindow(marker);
        }
    }

    mapLoad() {
        if (this.locations.length === 0) return;
        this.googleMap = new google.maps.Map(this.node, {
            scrollwheel: true,
            streetViewControl: false,
            mapTypeControl: false,
            fullscreenControl: true,
        });
        const bounds = new google.maps.LatLngBounds();
        this.markers = this.locations.map((location, index) => {
            const marker = new google.maps.Marker({
                position: getLatLng(location),
                map: this.googleMap,
                icon: this.markerImageURL,
            });
            const infowindow = new google.maps.InfoWindow({
                content: `
                <section>
                    <h2><a href="${location.url}">${location.title}</a></h2>
                    <div>${location.map_info_text}</div>
                </section
                `,
            });
            bounds.extend(marker.position);
            return {
                marker,
                infowindow,
                index,
                isOpen: false,
            };
        });

        this.googleMap.fitBounds(bounds);

        const listener = google.maps.event.addListener(
            this.googleMap,
            'idle',
            () => {
                this.googleMap.setZoom(this.zoom);
                google.maps.event.removeListener(listener);
            },
        );

        this.markers.forEach((marker) => {
            marker.marker.addListener('click', () =>
                this.toggleInfoWindow(marker),
            );
        });

        google.maps.event.addListener(this.googleMap, 'click', () => {
            this.markers.forEach((marker) => {
                marker.marker.addListener('click', () =>
                    GoogleMap.closeInfoWindow(marker),
                );
            });
        });

        this.markers.forEach((marker) => {
            marker.marker.addListener('click', () => {
                this.markers.forEach((_marker) => {
                    if (_marker.index !== marker.index) {
                        GoogleMap.closeInfoWindow(_marker);
                    }
                });
            });
        });
    }
}

export default GoogleMap;
