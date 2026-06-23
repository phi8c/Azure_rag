import { useQuery } from
"@tanstack/react-query";

import { getGraph } from
"../api/graph.api";

export function useGraph() {

  return useQuery({

    queryKey: [
      "graph"
    ],

    queryFn:
      getGraph
  });
}