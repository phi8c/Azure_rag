import { api }
from "@/shared/api/axios";

type UploadRequest = {

  file: File;

  email: string;

  role: string;

  securityLevel: string;

  documentType: string;

};

export async function uploadDocument(

  body: UploadRequest

) {

  const formData =
  new FormData();

  formData.append(
    "file",
    body.file
  );

  formData.append(
    "email",
    body.email
  );

  formData.append(
    "role",
    body.role
  );
  formData.append(
  "security_level",
  body.securityLevel
);

formData.append(
  "document_type",
  body.documentType
);

  const res =
  await api.post(

    "/documents/upload",

    formData,

    {

      headers: {

        "Content-Type":
        "multipart/form-data"

      }

    }

  );

  return res.data;

}

export async function syncDocuments() {

  const res =
  await api.post(
    "/documents/sync"
  );

  return res.data;

}
export async function  getMyDepartment() {

}

export async function getSyncStatus() {

  const res = await api.get(
    "/documents/sync-status"
  );

  return res.data;
}