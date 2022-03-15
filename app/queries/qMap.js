import { gql } from '@apollo/client';

export const qMap = gql`
  query get_map($graph: String!) {
    polygons(graph: $graph) {
      id
      vertices
      level
      tags
    }

    edges(graph: $graph) {
      edge
    }

    pois(graph: $graph) {
      id
      level
      lat
      lon
      tags
    }

    nodes(graph: $graph) {
      id
      level
      lat
      lon
      tags
      polygon {
        id
      }
    }

    walls(graph: $graph) {
      id
      level
      lat
      lon
      tags
    }
  }
`;
