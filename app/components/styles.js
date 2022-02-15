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
  // input: {
  //   height: 40,
  //   margin: 12,
  //   borderWidth: 1,
  //   padding: 10,
  // },
});
