var map = new ol.Map({
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        }),
    ],
    target: 'map',
    view: new ol.View({
        center: ol.proj.fromLonLat([28, 53.8]),
        zoom: 7
    })
});