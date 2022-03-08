import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  background: {
    // backgroundColor: '#f8f8f8',
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
    backgroundColor: 'black',
  },
  buttonText: {
    fontSize: 18,
    color: 'white',
    fontWeight: '700',
    textTransform: 'uppercase',
    textAlign: 'center',
  },
  box: {
    padding: 8,
    borderBottomWidth: 1,
    borderColor: '#ccc',
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
    stroke: '#0F1108',
  },
  location: {
    fill: '#92D5E6',
    stroke: '#0B2A31',
    innerStroke: '#70CADF',
  },
  room: {
    fill: '#C4F6B7',
    stroke: '#113507',
  },
  currentRoom: {
    fill: '#E05263',
  },
  mapButton: {
    backgroundColor: '#0F3843',
    borderRadius: 15,
    height: 60,
    width: 60,
    margin: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  mapButtonIcon: {
    size: 50,
    color: '#ddd',
    // padding: 10,
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
    backgroundColor: '#0F3843',
    color: '#ddd',
    borderRadius: 15,
    padding: 10,
  },
  // input: {
  //   height: 40,
  //   margin: 12,
  //   borderWidth: 1,
  //   padding: 10,
  // },
});
