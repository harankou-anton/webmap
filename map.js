const wmsSource = new ol.source.TileWMS({
  url: 'http://localhost:8080/geoserver/cite/wms',
  params: {'LAYERS': 'cite:map_worldborder', 'TILED': true},
  serverType: 'geoserver',
  crossOrigin: 'anonymous',
});

const view = new ol.View({
        center: ol.proj.fromLonLat([28, 53.8]),
        zoom: 7
    });

var map = new ol.Map({
    layers: [
        new ol.layer.Tile({
           source: new ol.source.TileWMS({
               attributions: '@geoserver',
               url: 'http://localhost:8080/geoserver/cite/wms?',
               params:{
                   'LAYERS': 'cite:map_worldborder'
               }
           })
       })
    ],
    target: 'map',
    view: view,
});

//get coords on click
map.on('singleclick', function (evt) {
    console.log(ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326'));
    console.log(wmsSource);
  document.getElementById('info').innerHTML = '';
  const viewResolution = /** @type {number} */ (view.getResolution());
  const url = wmsSource.getFeatureInfoUrl(
    evt.coordinate,
    viewResolution,
    'EPSG:3857',
    {'INFO_FORMAT': 'text/html'}
  );
  if (url) {
    fetch(url)
      .then((response) => response.text())
      .then((html) => {
        document.getElementById('info').innerHTML = html;
      });
  }
});