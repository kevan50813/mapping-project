import React, { useState } from 'react';
import { Text, View, Button } from 'react-native';
import { useLazyQuery } from '@apollo/client';
import { SearchBar } from 'react-native-elements';
import { qPolygons } from '../queries/qPolygons';
import { styles } from './styles';
import { server } from './App';

const RoomList = ({ loading, error, polygons = [] }) => {
  if (error) {
    console.error(error);
  }
  return (
    <>
      {loading ? (
        <Text style={styles.info}>Loading from {server}...</Text>
      ) : null}

      {error ? <Text style={styles.error}>{error.message}</Text> : null}
      <Text style={styles.info}>Results: {polygons.length}</Text>

      {polygons.map(p => (
        <View key={p.id} style={styles.box}>
          <Text style={styles.small}>
            {p.tags['room-no']} - {p.tags['room-name']}
          </Text>
        </View>
      ))}
    </>
  );
};

export const SearchModal = ({ setDestination, setModalVisible }) => {
  const [search, setSearch] = useState('');

  const [
    getPolygons,
    {
      polyLoading,
      polyError,
      polyData: { search_polygons: polygons } = { search_polygons: [] },
    },
  ] = useLazyQuery(qPolygons);

  const updateSearch = newSearch => {
    setSearch(newSearch);
    getPolygons({ variables: { search, graph: 'test_bragg' } });
  };

  return (
    <View>
      <Button
        style={styles.button}
        title="MODAL"
        onPress={() => setModalVisible(false)}
      />
      <SearchBar
        value={search}
        style={styles.input}
        placeholder="Enter destination here..."
        onChangeText={updateSearch}
      />
      <RoomList loading={polyLoading} error={polyError} polygons={polygons} />
    </View>
  );
};
