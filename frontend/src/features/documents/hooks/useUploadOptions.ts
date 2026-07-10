import { useQuery } from "@tanstack/react-query";
import { getUploadOptions } from "../api/document.api";

export function useUploadOptions() {
  return useQuery({
    queryKey: ["upload-options"],
    queryFn: getUploadOptions,
  });
}