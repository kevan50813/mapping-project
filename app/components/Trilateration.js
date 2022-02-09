import React from 'react';
import { ScrollView, View } from 'react-native';
import { styles } from './styles';
import Plotly from 'react-native-plotly';


export const Trilateration = () => {
    const data = {
      x: [1, 2, 3, 4, 5],
      y: [1, 2, 3, 4, 8],
      type: 'scatter',
    };
    const layout = { title: 'Trilateration Scatterplot' };

    return (
      <Plotly
        data={data}
        layout={layout}
      />
    )

};
