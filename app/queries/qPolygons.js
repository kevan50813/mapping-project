import { gql } from '@apollo/client';

export const qPolygons = gql`
  query polygons($graph: String!, $search: String!) {
    search_polygons(graph: $graph, search: $search) {
      id
      tags
    }
  }
`;
