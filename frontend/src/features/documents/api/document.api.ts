import { api }
from "@/shared/api/axios";

type UploadRequest = {

  file: File;

  email: string;

  role: string;

  securityLevel: string;

  documentType: string;
  siteId: string;
  driveId: string;
  folderId?: string;

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

formData.append(
  "site_id",
  body.siteId
);

formData.append(
  "drive_id",
  body.driveId
);

if (body.folderId) {
    formData.append("folder_id", body.folderId);
}
  for (const [key, value] of formData.entries()) {
    console.log(key, value);
}
  const res =
  await api.post(

    "/documents/upload-sharepoint",

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
export async function getUploadOptions() {
  const response = await api.get("/documents/upload-options");

  return response.data;
}