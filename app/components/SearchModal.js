import React, { useState } from 'react';
import { useEffect } from 'react';
import { Text, ScrollView, TouchableOpacity } from 'react-native';
import { useLazyQuery } from '@apollo/client';
import { CenteredActivityIndicator } from './CenteredActivityIndicator';
import { qPolygons } from '../queries/qPolygons';
import { styles } from './styles';

const RoomList = ({
  loading,
  error,
  polygons = [],
  setDestination,
  setModalVisible,
}) => {
  if (error) {
    console.error(error);
  }

  return (
    <>
      {loading ? (
        <CenteredActivityIndicator text="Loading search results" />
      ) : null}
      {error ? <Text style={styles.error}>{error.message}</Text> : null}

      {/* <Text style={styles.info}>Results: {polygons.length}</Text> */}

      {polygons.map(p => {
        return (
          <TouchableOpacity
            key={p.polygon.id}
            style={styles.box}
            onPress={() => {
              setDestination(p.node.id);
              setModalVisible(false);
            }}>
            <Text style={styles.small}>
              {p.polygon.tags['room-no']} - {p.polygon.tags['room-name']}
            </Text>
          </TouchableOpacity>
        );
      })}
    </>
  );
};

export const SearchModal = ({ setDestination, setModalVisible, search }) => {
  const [startingPoint, setStartingPoint] = useState(false);
  let search_polygons = [];

  const [
    getNodes,
    {
      loading,
      error,
      data: { search_nodes: search_nodes } = { search_nodes: [] },
    },
  ] = useLazyQuery(qPolygons);

  if (search_nodes) {
    search_polygons = [
      ...new Set(
        search_nodes.map(node => {
          return { polygon: node.polygon, node: node };
        }),
      ),
    ];
  }

  useEffect(() => {
    const escaped = search.replace('.', '.\\');
    getNodes({ variables: { search: escaped, graph: 'test_bragg' } });
  }, [getNodes, search]);

  return (
    <ScrollView
      style={styles.background}
      contentInsetAdjustmentBehavior="automatic">
      <RoomList
        loading={loading}
        error={error}
        polygons={search_polygons}
        setDestination={setDestination}
        setModalVisible={setModalVisible}
        setStartingPoint={setStartingPoint}
        startingPoint={startingPoint}
      />
    </ScrollView>
  );
};
