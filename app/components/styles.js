import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  background: {
    backgroundColor: '#f8f8f8',
    flex: 1,
  },
  inputRow: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
  },
  label: {
    color: 'black',
    fontSize: 18,
    marginRight: 8,
  },
  input: {
    minWidth: 180,
    borderBottomWidth: 2,
    borderColor: 'black',
    backgroundColor: '#e8e8e8',
    color: 'black',
    padding: 4,
    fontSize: 18,
  },
  button: {
    padding: 12,
    backgroundColor: '#4c94eb',
    margin: 10,
  },
  buttonText: {
    fontSize: 18,
    color: '#eee',
    fontWeight: '700',
    textTransform: 'uppercase',
    textAlign: 'center',
  },
  box: {
    padding: 8,
    borderBottomWidth: 1,
    borderColor: '#ccc',
    backgroundColor: '#eee',
  },
  spacedBox: {
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  big: {
    fontSize: 18,
    fontWeight: '600',
    color: 'black',
  },
  small: {
    marginTop: 8,
    fontSize: 18,
    fontWeight: '400',
    color: '#222',
  },
  error: {
    backgroundColor: '#fdd',
    color: '#f22',
    fontSize: 18,
    padding: 8,
    borderRadius: 4,
  },
  info: {
    backgroundColor: '#def',
    color: '#048',
    fontSize: 18,
    padding: 8,
    borderRadius: 4,
  },
  highlight: {
    fontWeight: '700',
  },
  plotly: {
    height: '70%',
  },
  poi: {
    fill: '#CA8702',
    stroke: '#201600',
  },
  hallway: {
    fill: '#BFBEC5',
    stroke: '#18171A',
  },
  walls: {
    stroke: '#777',
  },
  location: {
    fill: '#92D5E6',
    stroke: '#31bede',
    innerStroke: '#70CADF',
  },
  locationOld: {
    fill: '#334950',
    stroke: '#000000',
    innerStroke: '#234149',
  },
  ap: {
    fill: '#068b00',
    stroke: '#201600',
  },
  room: {
    fill: '#C4F6B7',
    stroke: '#113507',
  },
  currentRoom: {
    fill: '#5acff2',
  },
  mapButton: {
    backgroundColor: '#4c94eb',
    borderRadius: 15,
    height: 60,
    width: 60,
    margin: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  mapButtonIcon: {
    color: '#eee',
    fontSize: 30,
  },
  mapButtonIconSvg: {
    size: 30,
  },
  levelView: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    left: 0,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
  },
  levelViewText: {
    backgroundColor: '#4c94eb',
    color: '#eee',
    borderRadius: 15,
    padding: 10,
  },
  centerAbsolute: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  indicatorText: {
    color: 'grey',
    fontSize: 12,
  },
  search: {
    color: 'black',
  },
  searchBar: {
    position: 'absolute',
    top: 0,
    width: '100%',
  },
  modalHeight: {
    height: 700,
  },
  // input: {
  //   height: 40,
  //   margin: 12,
  //   borderWidth: 1,
  //   padding: 10,
  // },
});
