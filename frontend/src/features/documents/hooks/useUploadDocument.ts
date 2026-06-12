import {
  useMutation
}
from "@tanstack/react-query";

import {
  uploadDocument
}
from "../api/document.api";

export function useUploadDocument() {

  return useMutation({

    mutationFn:
    uploadDocument

  });

}