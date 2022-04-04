import { gql } from '@apollo/client';

// TODO change this to search_nodes with polygon part
export const qPolygons = gql`
  query nodes($graph: String!, $search: String!) {
    search_nodes(graph: $graph, search: $search) {
      id
      tags
      polygon {
        id
        tags
      }
    }
  }
`;
