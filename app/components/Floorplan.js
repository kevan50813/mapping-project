import React from 'react';
import * as d3 from 'd3';
import polygons from './Polygons.json'; // assert { type: 'json' }
import { Svg, G, Path } from 'react-native-svg';

const features = polygons.features;
const rooms = features.map(f => f.geometry.coordinates[0]);

const minX = rooms.reduce(
  (m, room) => Math.min(m, ...room.map(r => r[0])),
  Infinity,
);
const maxX = rooms.reduce(
  (m, room) => Math.max(m, ...room.map(r => r[0])),
  -Infinity,
);
const minY = rooms.reduce(
  (m, room) => Math.min(m, ...room.map(r => r[1])),
  Infinity,
);
const maxY = rooms.reduce(
  (m, room) => Math.max(m, ...room.map(r => r[1])),
  -Infinity,
);

const W = 640;
const H = 480;

//const map = d3.select('#d3').append('svg').attr('width', W).attr('height', H)

const scaleX = d3.scaleLinear([minX, maxX], [20, 620]);
const scaleY = d3.scaleLinear([minY, maxY], [460, 20]);
const projection = d3.geoEquirectangular().fitSize([W, H], polygons);
const path = d3.geoPath().projection(projection);

/*
map
  .selectAll('path')
  .data(features)
  .enter()
  .append('path')
  .attr('d', path)
  .attr('opacity', '0.5')
  .attr('fill', (room) =>
    room.properties.type === 'Room' ? 'lightblue' : 'none'
  )
  .attr('stroke', (room) =>
    room.properties.type === 'Room' ? 'blue' : 'black'
  )
*/

// Needs a floor filter
var floor = 2.0;

export const Floorplan = () => {
  return (
    <Svg width="100%" height="100%">
      <G>
        {features.map((feature, index) => {
          //if (feature.properties.level === floor) {
            return (
              <Path
                d={path(feature)}
                key={index}
                opacity={0.5}
                fill={feature.properties.type === 'Room' ? 'lightblue' : 'none'}
                stroke={feature.properties.type === 'Room' ? 'blue' : 'black'}
              />
            );
          //}
        })}
      </G>
    </Svg>
  );
}