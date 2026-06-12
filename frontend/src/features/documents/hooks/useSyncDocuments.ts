import {
  useMutation
} from "@tanstack/react-query";

import {
  syncDocuments
} from "../api/document.api";

export function useSyncDocuments() {

  return useMutation({

    mutationFn:
    syncDocuments

  });

}