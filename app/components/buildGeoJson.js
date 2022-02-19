export function polyFeatures(polygons) {
  var features = [];

  for (var i = 0; i < polygons.length; i++) {
    var feature = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'Polygon',
        coordinates: [],
      },
    };

    const vertices = polygons[i].vertices.map(v => [v[1], v[0]]);
    feature.geometry.coordinates = [vertices];
    feature.properties = {
      ...polygons[i].tags,
      ...{ level: polygons[i].level },
    };
    features.push(feature);
  }

  return features;
}

export function nodeFeatures(nodes) {
  var features = [];
  for (var i = 0; i < nodes.length; i++) {
    const feature = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'Point',
        coordinates: [],
      },
    };
    const vertices = [nodes[i].lon, nodes[i].lat];
    feature.geometry.coordinates = [vertices];
    feature.properties = { ...nodes[i].tags, ...{ level: nodes[i].level } };
    features.push(feature);
  }

  return features;
}

export function buildGeoJson(polygons, nodes, walls, edges) {
  // Create a GeoJson object
  var geoJson = {
    type: 'FeatureCollection',
    name: 'Map',
    crs: {
      type: 'name',
      properties: { name: 'urn:ogc:def:crs:OGC:1.3:CRS84' },
    },
    features: [],
  };

  // would be nice if there was a way of doing this in place
  geoJson.features = geoJson.features.concat(polyFeatures(polygons));
  geoJson.features = geoJson.features.concat(nodeFeatures(nodes));
  geoJson.features = geoJson.features.concat(nodeFeatures(walls));

  return geoJson;
}
