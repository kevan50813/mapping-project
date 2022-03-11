import React, { useState, useEffect, useContext } from 'react';
import { Text } from 'react-native';
import { styles } from './styles';
import { useLazyQuery } from '@apollo/client';
import { NetworkContext } from './NetworkProvider';
import { buildGeoJson } from '../lib/geoJson';
import { findNearestNode } from '../lib/findNearestNode';
import { qMap } from '../queries/qMap';
import { qPath } from '../queries/qPath';
import { trilateration } from './Trilateration';
import { Floorplan } from './Floorplan';

export const LoadFloorplan = () => {
  const [destination, setDestination] = useState(-1);
  const [geoJson, setGeoJson] = useState(null);
  const [knownNetworks, setKnownNetworks] = useState([]);
  const [path, setPath] = useState([]);
  const { networks: visibleNetworks, startScan } = useContext(NetworkContext);
  let predictedLocation = null;
  let nearestNode = null;
  let nearestId = -1;

  const scan = async () => {
    startScan();
  };

  if (visibleNetworks.length > 0 && knownNetworks.length > 0) {
    let data = trilateration(visibleNetworks, knownNetworks, -50, 3);
    predictedLocation = data.predictedLocation;
    nearestNode = findNearestNode(predictedLocation, geoJson);
    nearestId = nearestNode.properties.queryObject.id;
  }

  const [
    getMap,
    {
      loading,
      error,
      data: {
        polygons: polygons,
        edges: edges,
        nodes: nodes,
        walls: walls,
        pois: pois,
      } = {
        polygons: [],
        edges: [],
        nodes: [],
        walls: [],
        pois: [],
      },
    },
  ] = useLazyQuery(qMap);

  useEffect(() => {
    getMap({ variables: { graph: 'test_bragg' } });
  }, [getMap]);

  const loadKnownNetworks = geo => {
    if (geo == null) {
      return [];
    }

    // get the filter from the queries PoI data here
    const knownWifi = geo.features.filter(
      feature => feature.properties.internet === 'yes',
    );
    return knownWifi.map(({ geometry, properties }) => ({
      coordinates: geometry.coordinates[0],
      name: properties.ssid,
      BSSID: properties.mac_addres, // NB: not a typo, problem with char limits in shapefiles
      level: properties.level,
    }));
  };

  const [
    getPath,
    {
      loading: pathLoading,
      error: pathError,
      data: { find_route: find_route } = { find_route: {} },
    },
  ] = useLazyQuery(qPath);

  useEffect(() => {
    if (nearestId === -1 || destination === -1) {
      return;
    }

    getPath({
      variables: { graph: 'test_bragg', start: nearestId, end: destination },
    });
  }, [getPath, nearestId, destination]);

  useEffect(() => {
    if (pathError) {
      console.error('Pathfinding error');
    }

    if (!pathLoading && find_route.ids) {
      setPath(find_route.ids);
    }
  }, [find_route, pathError, pathLoading]);

  if (geoJson == null && polygons.length > 0) {
    setGeoJson(buildGeoJson(polygons, nodes, walls, pois, edges));
  }

  if (geoJson != null && knownNetworks.length === 0) {
    const networks = loadKnownNetworks(geoJson);
    setKnownNetworks(networks);
  }

  return loading ? (
    <Text style={styles.info}>Loading Floorplan...</Text>
  ) : (
    <Floorplan
      polygons={polygons}
      loading={loading}
      error={error}
      geoJson={geoJson}
      knownNetworks={knownNetworks}
      setDestination={setDestination}
      path={path}
      scan={scan}
      nearestId={nearestId}
      predictedLocation={predictedLocation}
      nearestNode={nearestNode}
    />
  );
};
