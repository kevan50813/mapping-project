import * as d3 from 'https://cdn.skypack.dev/d3'
import polygons from './Polygons.json' assert { type: 'json' }

const features = polygons.features
console.log(JSON.stringify(features));
console.log(features);
const rooms = features.map((f) => f.geometry.coordinates[0])

const minX = rooms.reduce(
  (m, room) => Math.min(m, ...room.map((r) => r[0])),
  Infinity
)
const maxX = rooms.reduce(
  (m, room) => Math.max(m, ...room.map((r) => r[0])),
  -Infinity
)
const minY = rooms.reduce(
  (m, room) => Math.min(m, ...room.map((r) => r[1])),
  Infinity
)
const maxY = rooms.reduce(
  (m, room) => Math.max(m, ...room.map((r) => r[1])),
  -Infinity
)

const W = 640
const H = 480

const map = d3.select('#d3').append('svg').attr('width', W).attr('height', H)

const scaleX = d3.scaleLinear([minX, maxX], [20, 620])
const scaleY = d3.scaleLinear([minY, maxY], [460, 20])
const projection = d3.geoEquirectangular().fitSize([W, H], polygons)
const path = d3.geoPath().projection(projection)

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
