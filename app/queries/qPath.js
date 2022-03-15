import { gql } from '@apollo/client';

export const qPath = gql`
  query get_route($graph: String!, $start: Int!, $end: Int!) {
    find_route(graph: $graph, start_id: $start, end_id: $end) {
      ids
    }
  }
`;
