import React, { useState } from 'react';
import { ScrollView, Text, View, TextInput } from 'react-native';
import { useLazyQuery, gql } from '@apollo/client';
import { styles } from './styles';
import { Button } from './Button';
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

export const RoomSearch = ({ navigation }) => {
  const [search, setSearch] = useState('');

  const qPolygons = gql`
    query polygons($search: String!) {
      search_polygons(graph: "test_bragg", search: $search) {
        id
        tags
      }
    }
  `;

  const [
    getPolygons,
    {
      loading,
      error,
      data: { search_polygons: polygons } = { search_polygons: [] },
    },
  ] = useLazyQuery(qPolygons);

  const doSearch = () => getPolygons({ variables: { search } });

  return (
    <View style={styles.background}>
      <View style={styles.inputRow}>
        <Text style={styles.label}>Search:</Text>
        <TextInput
          style={styles.input}
          value={search}
          onChangeText={setSearch}
        />
      </View>
      <Button style={styles.button} title="Search" onPress={doSearch} />
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <RoomList loading={loading} error={error} polygons={polygons} />
      </ScrollView>
    </View>
  );
};
