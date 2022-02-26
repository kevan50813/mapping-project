function polyFeatures(polygons) {
  var features = [];

  polygons.forEach(polygon => {
    var feature = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'Polygon',
        coordinates: [],
      },
    };

    const vertices = polygon.vertices.map(v => [v[1], v[0]]);
    feature.geometry.coordinates = [vertices];
    feature.properties = {
      ...polygon.tags,
      ...{ level: polygon.level },
    };
    features.push(feature);
  })

  return features;
}

function nodeFeatures(nodes) {
  var features = [];
  nodes.forEach(node => {
    const feature = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'Point',
        coordinates: [],
      },
    };

    const vertices = [node.lon, node.lat];
    feature.geometry.coordinates = [vertices];
    feature.properties = { ...node.tags, ...{ level: node.level } };
    features.push(feature);
  })

  return features;
}

function buildLineString(nodes, edges) {
  var features = [];

  // create a lookup table of nodes
  // id should be unique here so it's really a 'hash map'
  var nodeLookup = {};
  nodes.map(n => (nodeLookup[n.id] = n));

  // then use edges to find all links between them
  // for now these are just pairs
  edges.forEach(edge => {
    const feature = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'LineString',
        coordinates: [],
      },
    };

    const node1 = nodeLookup[edge.edge[0].toString()];
    const node2 = nodeLookup[edge.edge[1].toString()];
    
    if (node1 !== undefined && node2 !== undefined) {
      feature.properties = {...node1.tags, 
                            ...{level: node1.level}};
      feature.geometry.coordinates = [
        [node1.lon, node1.lat],
        [node2.lon, node2.lat],
      ];
      features.push(feature);
    }

  });

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
  geoJson.features = geoJson.features.concat(buildLineString(nodes, edges));
  geoJson.features = geoJson.features.concat(buildLineString(walls, edges));

  return geoJson;
}
