export const findNearestNode = (location, geoJson) => {
  const nodes = geoJson.features.filter(
    feature =>
      feature.properties.indoor === 'way' &&
      feature.properties.level[0] === location.level,
  );
  var minDistance = Number.MAX_SAFE_INTEGER;
  var closestNode = null;

  for (let i = 0; i < nodes.length; i++) {
    const nodeLocation = nodes[i].geometry.coordinates[0];
    const distanceTo = Math.hypot(
      location.point[0] - nodeLocation[0],
      location.point[1] - nodeLocation[1],
    );

    if (distanceTo < minDistance) {
      closestNode = nodes[i];
      minDistance = distanceTo;
    }
  }

  return closestNode;
};
