import React, { useState, useEffect, useContext } from 'react';
import { Text, View } from 'react-native';
import {
  faAngleUp,
  faAngleDown,
  faLocationCrosshairs,
} from '@fortawesome/free-solid-svg-icons';
import Toast from 'react-native-simple-toast';
import { useLazyQuery, gql } from '@apollo/client';

import { styles } from './styles';
import { NetworkContext } from './NetworkProvider';
import { MapButton } from './MapButton';
import { buildGeoJson } from '../lib/geoJson';
import { DrawMap } from './DrawMap';
import { trilateration } from './Trilateration';

const findNearestNode = (location, geoJson) => {
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

const findPath = (start, end) => {
  const qPath = gql`
    query get_route($graph: String!, $start: Int!, $end: Int!) {
      find_route(graph: $graph, start_id: $start, end_id: $end) {
        ids
      }
    }
  `;

  const [
    getPath,
    { loading, error, data: { find_route: find_route } = { find_route: {} } },
  ] = useLazyQuery(qPath);

  useEffect(() => {
    getPath({ variables: { graph: 'test_bragg', start: start, end: end } });
  }, [getPath]);

  return { loading, error, find_route };
};

export const LoadFloorplan = () => {
  const qMap = gql`
    query get_map($graph: String!) {
      polygons(graph: $graph) {
        id
        vertices
        level
        tags
      }

      edges(graph: $graph) {
        edge
      }

      pois(graph: $graph) {
        id
        level
        lat
        lon
        tags
      }

      nodes(graph: $graph) {
        id
        level
        lat
        lon
        tags
        polygon {
          id
        }
      }

      walls(graph: $graph) {
        id
        level
        lat
        lon
        tags
      }
    }
  `;

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

  const [geoJson, setGeoJson] = useState(null);
  const [knownNetworks, setKnownNetworks] = useState([]);

  const loadKnownNetworks = geoJson => {
    if (geoJson == null) {
      return [];
    }

    // get the filter from the queries PoI data here
    const nodes = geoJson.features.filter(
      feature => feature.properties.internet === 'yes',
    );
    return nodes.map(({ geometry, properties }) => ({
      coordinates: geometry.coordinates[0],
      name: properties.ssid,
      BSSID: properties.mac_addres, // NB: not a typo, problem with char limits in shapefiles
      level: properties.level,
    }));
  };

  if (geoJson == null && polygons.length > 0) {
    setGeoJson(buildGeoJson(polygons, nodes, walls, pois, edges));
  }

  if (geoJson != null && knownNetworks.length == 0) {
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
    />
  );
};

export const Floorplan = ({ polygons, geoJson, knownNetworks }) => {
  const [floorId, setFloorId] = useState(2);
  const [shownToast, setShownToast] = useState(false);
  let predictedLocation = {};
  let nearestNode = null;
  let path = [];

  const {
    networks: visibleNetworks,
    state: { scanning },
    startScan,
  } = useContext(NetworkContext);

  const floor_set = new Set(polygons.map(f => f.level));
  const floor_list = [...floor_set].filter(f => f.indexOf(';') === -1).sort();

  const find_route = findPath(1800, 2878);
  if (find_route.find_route.ids) {
    path = find_route.find_route.ids;
  }

  const scan = async () => {
    startScan();
  };

  if (visibleNetworks.length > 0 && knownNetworks.length > 0) {
    let data = trilateration(visibleNetworks, knownNetworks, -50, 3);
    predictedLocation = data.predictedLocation;
    nearestNode = findNearestNode(predictedLocation, geoJson);
  }

  const prevFloor = () => {
    setFloorId(floorId - 1 < 0 ? 0 : floorId - 1);
  };

  const nextFloor = () => {
    setFloorId(floorId + 1 < floor_list.length ? floorId + 1 : floorId);
  };

  if (!scanning && visibleNetworks.length > 0 && !shownToast) {
    Toast.show('Network scan successful.', Toast.LONG);
    setShownToast(true);
  }

  if (scanning) {
    Toast.show('Scanning Wifi APs...', Toast.LONG);
  }

  return (
    <>
      <View style={styles.background}>
        <DrawMap
          geoJson={geoJson}
          location={predictedLocation}
          level={parseInt(floor_list[floorId], 10)}
          nearestNode={nearestNode}
          currentPath={path}
        />

        <MapButton
          icon={faAngleUp}
          position={{ position: 'absolute', top: 0, right: 0 }}
          onPress={nextFloor}
        />

        <MapButton
          icon={faAngleDown}
          position={{ position: 'absolute', top: 70, right: 0 }}
          onPress={prevFloor}
        />

        <MapButton
          icon={faLocationCrosshairs}
          position={{ position: 'absolute', bottom: 0, right: 0 }}
          onPress={scan}
        />

        <View style={styles.levelView}>
          <Text style={[styles.big, styles.levelViewText]}>
            Level: {floor_list[floorId]}
          </Text>
        </View>
      </View>
    </>
  );
};
