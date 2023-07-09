// Создаем функцию для создания WMS слоя
function createWMSLayer(layerName) {
    return new ol.layer.Tile({
        source: new ol.source.TileWMS({
            url: 'http://localhost:8080/geoserver/layers/wms?',
            params: {
                'LAYERS': "layers:" + layerName,
            },
            serverType: 'geoserver',
            title: layerName,
            zIndex: 99
        }),
    });
}

// Создаем функцию для добавления WMS слоя в группу слоев
function addWMSLayerToGroup(group, layer) {
  group.getLayers().push(layer);
}

function setVisability(layer){
    layer.setVisable(true)
}

function setUnVisability(layer){
    layer.setVisable(false)
}

const view = new ol.View({
    center: ol.proj.fromLonLat([26, 53.8]),
    zoom: 7
});

const osmlayer = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible: true,
    zIndex: 0,
    title: "osmlayer"
});

const googleImages = new ol.layer.Tile({
    source: new ol.source.XYZ({
        url: "https://mt{0-3}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        ratio: 1,
        crossOrigin: "anonymous"
    }),
    visible: false,
    zIndex: 0,
    title: "googleImages"
});

var map = new ol.Map({
    layers: [

    ],
    target: 'map',
    view: view,
});

const projectlayergroup = new ol.layer.Group({
    layers: [],
    visible: false,
    zIndex:99
});
map.addLayer(projectlayergroup)

const baselayergroup = new ol.layer.Group({
    layers: [osmlayer, googleImages],
    zIndex: 0
});
map.addLayer(baselayergroup);


//change base layer
const baseLayerSelector = document.getElementById('baselayers').querySelectorAll(".dropdown-menu > button[type=button]")
for (let baseLayer of baseLayerSelector) {
    baseLayer.addEventListener('click', function () {
        let baseLayerValue = this.value;
        baselayergroup.getLayers().forEach(function (element, index, array) {
            console.log(element);
            let baseLayerTitle = element.get('title');
            element.setVisible(baseLayerTitle === baseLayerValue);
        })
    })
}


const projectValueElements = document.getElementById('proj-work').querySelectorAll("input[type=checkbox]")

for (var i = 0; i < projectValueElements.length; i++) {
    console.log(projectValueElements[i].value);
    window[projectValueElements[i].value] = createWMSLayer(projectValueElements[i].value)
    // eval('var s_' + projectValueElements[i].value + ' = ' + createWMSLayer(projectValueElements[i].value));
    console.log (window[projectValueElements[i].value]);
    projectValueElements[i].addEventListener('change', function () {
        if (this.checked) {
            map.addLayer(window[this.value]);
        } else {
            map.removeLayer(window[this.value]);
        }
    })
}


//get coords on click
map.on('singleclick', function (evt) {
    console.log(ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326'))
});
