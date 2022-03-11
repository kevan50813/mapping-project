import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import {
  faMagnifyingGlassLocation,
  faXmark,
} from '@fortawesome/free-solid-svg-icons';
import { Text, View, Button, ScrollView, TouchableOpacity } from 'react-native';
import { useLazyQuery } from '@apollo/client';
import { SearchBar } from 'react-native-elements';
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

      <Text style={styles.info}>Results: {polygons.length}</Text>

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

export const SearchModal = ({ setDestination, setModalVisible }) => {
  const [search, setSearch] = useState('');
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

  const updateSearch = newSearch => {
    setSearch(newSearch);
    getNodes({ variables: { search, graph: 'test_bragg' } });
  };

  return (
    <View>
      <Button
        style={styles.button}
        title={'MODAL'}
        onPress={() => setModalVisible(false)}
      />
      <SearchBar
        value={search}
        style={styles.search}
        placeholder="Enter destination here..."
        onChangeText={updateSearch}
        lightTheme={true}
        searchIcon={<FontAwesomeIcon icon={faMagnifyingGlassLocation} />}
        clearIcon={<FontAwesomeIcon icon={faXmark} />}
      />

      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <RoomList
          loading={loading}
          error={error}
          polygons={search_polygons}
          setDestination={setDestination}
          setModalVisible={setModalVisible}
        />
      </ScrollView>
    </View>
  );
};
