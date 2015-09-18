
// http://dev.openlayers.org/examples/draw-feature.html

// http://dev.openlayers.org/examples/

/* sample data type from telegraph.py to mit.edu from cape cod, ma

[{'sdev': 1.8647199999999997, 'min': 7.463, 'importance': '', 'ip': '96.120.65.101', 'address': 'United States of America', 'times': [7.463, 7.817, 7.777, 11.392, 11.749], 'host': '96.120.65.101', 'max': 11.749, 'lat': '', 'lng': '', 'avg': 9.2396}, {'sdev': 0.4149599999999996, 'min': 11.468, 'importance': 0.3, 'ip': '68.87.154.73', 'address': 'Stafford, Virginia, United States of America', 'times': [11.531, 11.468, 12.41, 12.364, 12.318], 'host': 'te-5-5-ur01.mashpee.ma.boston.comcast.net', 'max': 12.41, 'lat': 38.4221, 'lng': -77.4083, 'avg': 12.018200000000002}, {'sdev': 1.4957499999999992, 'min': 16.837, 'importance': '', 'ip': '68.85.37.93', 'address': 'United States of America', 'times': [16.837, 17.188, 17.603, 21.198], 'host': 'be-113-ar01.needham.ma.boston.comcast.net', 'max': 21.198, 'lat': '', 'lng': '', 'avg': 18.2065}, {'sdev': 1.9473599999999998, 'min': 22.468, 'importance': '', 'ip': '68.86.90.217', 'address': 'United States of America', 'times': [27.095, 22.468, 22.778, 26.485, 26.46], 'host': 'be-7015-cr01.newyork.ny.ibone.comcast.net', 'max': 27.095, 'lat': '', 'lng': '', 'avg': 25.0572}, {'sdev': 0.21296000000000034, 'min': 24.82, 'importance': '', 'ip': '68.86.85.54', 'address': 'United States of America', 'times': [25.587, 24.82, 25.492, 25.451, 25.412], 'host': 'be-10203-cr02.newyork.ny.ibone.comcast.net', 'max': 25.587, 'lat': '', 'lng': '', 'avg': 25.3524}, {'sdev': 2.06672, 'min': 19.995, 'importance': '', 'ip': '68.86.84.238', 'address': 'United States of America', 'times': [24.527, 24.086, 20.433, 19.995, 24.946], 'host': 'he-0-13-0-0-pe02.111eighthave.ny.ibone.comcast.net', 'max': 24.946, 'lat': '', 'lng': '', 'avg': 22.7974}, {'sdev': 1.3667199999999995, 'min': 25.755, 'importance': '', 'ip': '50.242.151.70', 'address': 'United States of America', 'times': [25.8, 25.755, 27.191, 28.987, 29.205], 'host': '50.242.151.70', 'max': 29.205, 'lat': '', 'lng': '', 'avg': 27.3876}, {'sdev': 0.11711999999999989, 'min': 27.605, 'importance': 0.1, 'ip': '129.250.4.205', 'address': 'East Belleview Avenue, Greenwood Village, Arapahoe County, Colorado, 80111:80121, United States of America', 'times': [28.047, 27.605, 27.987, 27.946, 27.904], 'host': 'ae-3.r06.nycmny01.us.bb.gin.ntt.net', 'max': 28.047, 'lat': 39.6237, 'lng': -104.8738, 'avg': 27.8978}, {'sdev': 2.2448799999999998, 'min': 26.508, 'importance': 0.1, 'ip': '157.238.64.114', 'address': 'East Belleview Avenue, Greenwood Village, Arapahoe County, Colorado, 80111:80121, United States of America', 'times': [31.127, 31.489, 31.456, 26.508, 26.853], 'host': 'ae-2.akamai.nycmny01.us.bb.gin.ntt.net', 'max': 31.489, 'lat': 39.6237, 'lng': -104.8738, 'avg': 29.4866}, {'sdev': 4.2660800000000005, 'min': 21.766, 'importance': 0.2, 'ip': '23.208.94.93', 'address': 'Broadway, East Cambridge, Cambridge, Middlesex County, Massachusetts, 02142, United States of America', 'times': [30.569, 30.965, 30.91, 21.766, 22.088], 'host': 'a23-208-94-93.deploy.static.akamaitechnologies.com', 'max': 30.965, 'lat': 42.3626, 'lng': -71.0843, 'avg': 27.2596}]

*/

var lat = -70.485361;
var lng = 41.618116;

// Ubuntu UK

var locations = [{'sdev': 1.8647199999999997, 'min': 7.463, 'importance': '', 'ip': '96.120.65.101', 'address': 'United States of America', 'times': [7.463, 7.817, 7.777, 11.392, 11.749], 'host': '96.120.65.101', 'max': 11.749, 'lat': '', 'lng': '', 'avg': 9.2396}, {'sdev': 0.4149599999999996, 'min': 11.468, 'importance': 0.3, 'ip': '68.87.154.73', 'address': 'Stafford, Virginia, United States of America', 'times': [11.531, 11.468, 12.41, 12.364, 12.318], 'host': 'te-5-5-ur01.mashpee.ma.boston.comcast.net', 'max': 12.41, 'lat': 38.4221, 'lng': -77.4083, 'avg': 12.018200000000002}, {'sdev': 1.4957499999999992, 'min': 16.837, 'importance': '', 'ip': '68.85.37.93', 'address': 'United States of America', 'times': [16.837, 17.188, 17.603, 21.198], 'host': 'be-113-ar01.needham.ma.boston.comcast.net', 'max': 21.198, 'lat': '', 'lng': '', 'avg': 18.2065}, {'sdev': 1.9473599999999998, 'min': 22.468, 'importance': '', 'ip': '68.86.90.217', 'address': 'United States of America', 'times': [27.095, 22.468, 22.778, 26.485, 26.46], 'host': 'be-7015-cr01.newyork.ny.ibone.comcast.net', 'max': 27.095, 'lat': '', 'lng': '', 'avg': 25.0572}, {'sdev': 0.21296000000000034, 'min': 24.82, 'importance': '', 'ip': '68.86.85.54', 'address': 'United States of America', 'times': [25.587, 24.82, 25.492, 25.451, 25.412], 'host': 'be-10203-cr02.newyork.ny.ibone.comcast.net', 'max': 25.587, 'lat': '', 'lng': '', 'avg': 25.3524}, {'sdev': 2.06672, 'min': 19.995, 'importance': '', 'ip': '68.86.84.238', 'address': 'United States of America', 'times': [24.527, 24.086, 20.433, 19.995, 24.946], 'host': 'he-0-13-0-0-pe02.111eighthave.ny.ibone.comcast.net', 'max': 24.946, 'lat': '', 'lng': '', 'avg': 22.7974}, {'sdev': 1.3667199999999995, 'min': 25.755, 'importance': '', 'ip': '50.242.151.70', 'address': 'United States of America', 'times': [25.8, 25.755, 27.191, 28.987, 29.205], 'host': '50.242.151.70', 'max': 29.205, 'lat': '', 'lng': '', 'avg': 27.3876}, {'sdev': 0.11711999999999989, 'min': 27.605, 'importance': 0.1, 'ip': '129.250.4.205', 'address': 'East Belleview Avenue, Greenwood Village, Arapahoe County, Colorado, 80111:80121, United States of America', 'times': [28.047, 27.605, 27.987, 27.946, 27.904], 'host': 'ae-3.r06.nycmny01.us.bb.gin.ntt.net', 'max': 28.047, 'lat': 39.6237, 'lng': -104.8738, 'avg': 27.8978}, {'sdev': 2.2448799999999998, 'min': 26.508, 'importance': 0.1, 'ip': '157.238.64.114', 'address': 'East Belleview Avenue, Greenwood Village, Arapahoe County, Colorado, 80111:80121, United States of America', 'times': [31.127, 31.489, 31.456, 26.508, 26.853], 'host': 'ae-2.akamai.nycmny01.us.bb.gin.ntt.net', 'max': 31.489, 'lat': 39.6237, 'lng': -104.8738, 'avg': 29.4866}, {'sdev': 4.2660800000000005, 'min': 21.766, 'importance': 0.2, 'ip': '23.208.94.93', 'address': 'Broadway, East Cambridge, Cambridge, Middlesex County, Massachusetts, 02142, United States of America', 'times': [30.569, 30.965, 30.91, 21.766, 22.088], 'host': 'a23-208-94-93.deploy.static.akamaitechnologies.com', 'max': 30.965, 'lat': 42.3626, 'lng': -71.0843, 'avg': 27.2596}];

window.addEventListener('load', function() {openmap();}, false);

function openmap() {

  map = new OpenLayers.Map("mapdiv");
  map.addLayer(new OpenLayers.Layer.OSM());

  var fromProjection = new OpenLayers.Projection("EPSG:4326");   // Transform from WGS 1984
  var toProjection   = new OpenLayers.Projection("EPSG:900913"); // to Spherical Mercator Projection
  var center         = new OpenLayers.LonLat(lng, lat).transform(fromProjection, toProjection);

  // http://wiki.openstreetmap.org/wiki/Zoom_levels
  var zoom=1;
  map.setCenter (center, zoom);

  // Add the Markers Layer
  var markers = new OpenLayers.Layer.Vector("Markers Overlay");
  for (var l = 0; l < locations.length; l++){
    var feature = new OpenLayers.Feature.Vector(
      new OpenLayers.Geometry.Point( locations[l].lng, locations[l].lat ).transform(fromProjection, toProjection),
      {description:"Longitude: " + locations[l].lng + " Latitude: " + locations[l].lat} ,
      {externalGraphic: 'marker.png', graphicHeight: 25, graphicWidth: 21, graphicXOffset:-12, graphicYOffset:-25  }
    );
    markers.addFeatures(feature);
  }
  map.addLayer(markers);

  //http://dev.openlayers.org/docs/files/OpenLayers/Geometry/LineString-js.html#OpenLayers.Geometry.LineString
  // All lines to the Map
  var lines = new OpenLayers.Layer.Vector("Lines Overlay");
  var coordinates = [];
  for (var i = 0; i < locations.length; i++) {
    coordinates.push(new OpenLayers.Geometry.Point(locations[i].lat, locations[i].lng).transform(fromProjection, toProjection));
  }
  var feature = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.LineString(coordinates));
  lines.addFeatures(feature);
  map.addLayer(lines);

  //Add a selector control to the vectorLayer with popup functions
  var controls = {
    selector: new OpenLayers.Control.SelectFeature(markers, { onSelect: createPopup, onUnselect: destroyPopup })
  };

  function createPopup(feature) {
    feature.popup = new OpenLayers.Popup.FramedCloud("pop",
    feature.geometry.getBounds().getCenterLonLat(),
    null,
    '<div class="markerContent">'+feature.attributes.description+'</div>',
    null,
    true,
    function() { controls['selector'].unselectAll(); }
  );
  //feature.popup.closeOnMove = true;
  map.addPopup(feature.popup);
}

function destroyPopup(feature) {
  feature.popup.destroy();
  feature.popup = null;
}

map.addControl(controls['selector']);
//map.addControl(new OpenLayers.Control.MousePosition());
controls['selector'].activate();

}
