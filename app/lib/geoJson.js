const levelToArray = level => {
  const parts = level.split(';').map(n => parseInt(n, 10));
  let levels = parts;

  // Convert to array of intermediate levels, e.g. 1,4 -> [1,2,3,4]
  if (parts.length === 2) {
    let [start, end] = parts;
    levels = [];

    for (let i = start; i <= end; i++) {
      levels.push(i);
    }
  }

  return levels;
};

const polyFeatures = polygons =>
  polygons.map(polygon => ({
    type: 'Feature',
    geometry: {
      type: 'Polygon',
      coordinates: [polygon.vertices.map(([lat, lon]) => [lon, lat])],
    },
    properties: {
      ...polygon.tags,
      queryObject: polygon,
      level: levelToArray(polygon.level),
    },
  }));

const nodeFeatures = nodes =>
  nodes.map(node => ({
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: [[node.lon, node.lat]],
    },
    properties: {
      ...node.tags,
      queryObject: node,
      level: levelToArray(node.level),
    },
  }));

const buildLineString = (nodes, edges) => {
  // create a lookup table of nodes
  // id should be unique here so it's really a 'hash map'
  var nodeLookup = {};
  nodes.map(n => (nodeLookup[n.id] = n));

  // then use edges to find all links between them
  // for now these are just pairs
  return edges
    .filter(edge => nodeLookup[edge.edge[0]] && nodeLookup[edge.edge[1]])
    .map(edge => {
      const node1 = nodeLookup[edge.edge[0].toString()];
      const node2 = nodeLookup[edge.edge[1].toString()];

      return {
        type: 'Feature',
        geometry: {
          type: 'LineString',
          coordinates: [
            [node1.lon, node1.lat],
            [node2.lon, node2.lat],
          ],
        },
        properties: {
          ...node1.tags,
          edge: edge.edge,
          level: levelToArray(node1.level),
        },
      };
    });
};

export const onLevel = level => feature =>
  feature.properties.level.includes(level);

export const buildGeoJson = (polygons, nodes, walls, pois, edges) => ({
  type: 'FeatureCollection',
  name: 'Map',
  crs: {
    type: 'name',
    properties: { name: 'urn:ogc:def:crs:OGC:1.3:CRS84' },
  },
  features: [
    ...polyFeatures(polygons),
    ...buildLineString(walls, edges),
    ...buildLineString(nodes, edges),
    ...nodeFeatures(nodes),
    ...nodeFeatures(pois),
  ],
});
