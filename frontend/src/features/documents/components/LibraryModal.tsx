import { useState, useEffect } from "react";
import {
  X,
  Upload,
  RefreshCw,
  FileText,
  User,
  Briefcase,
  Shield,
  Tag,
  CloudUpload,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";
// import { useMyDepartment } from "../hooks/useMyDepartment";
import { useUploadDocument } from "../hooks/useUploadDocument";
import { useSyncDocuments } from "../hooks/useSyncDocuments";
import { getSyncStatus } from "../api/document.api";
import { useMsal } from "@azure/msal-react";

type Props = {
  onClose: () => void;
};

export default function LibraryModal({ onClose }: Props) {
  // ==========================================
  // LOGIC ĐƯỢC GIỮ NGUYÊN TUYỆT ĐỐI
  // ==========================================
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const uploadMutation = useUploadDocument();
  const syncMutation = useSyncDocuments();

  const [securityLevel, setSecurityLevel] = useState("");
  const [documentType, setDocumentType] = useState("");

  const { instance } = useMsal();
  const account = instance.getActiveAccount();
  const email = account?.username ?? "";

  const isProcessing = uploadMutation.isPending || syncMutation.isPending;
  const [role, setRole] = useState("");

  useEffect(() => {
    const run = async () => {
      const account = instance.getActiveAccount();
      if (!account) return;

      const token = await instance.acquireTokenSilent({
        account,
        scopes: ["User.Read", "GroupMember.Read.All"],
      });

      const response = await fetch(
        "https://graph.microsoft.com/v1.0/me/memberOf?$select=id,displayName",
        {
          headers: {
            Authorization: `Bearer ${token.accessToken}`,
          },
        },
      );

      const data = await response.json();

      const validRoles = [
        "CEO",
        "HR_MANAGER",
        "HR_STAFF",
        "IT_MANAGER",
        "IT_STAFF",
        "SALE_MANAGER",
        "SALE_STAFF",
      ];

      const matchedRole = data.value
        ?.map((group: any) => group.displayName)
        .find((name: string) => validRoles.includes(name));

      setRole(matchedRole ?? "");

      console.log("groups =", data.value);
    };

    run();
  }, []);

  async function handleUpload() {
    if (!file) {
      setError("Vui lòng chọn file");
      return;
    }

    try {
      setError("");
      setMessage("");

      await uploadMutation.mutateAsync({
        file,
        email,
        role,
        securityLevel,
        documentType,
      });
      setUploadSuccess(true);

      setMessage("Upload tài liệu thành công");
      setTimeout(() => {
        setMessage("");
      }, 10000);

      setFile(null);
    } catch (err) {
      console.error(err);
      setError("Upload thất bại");
    }
  }

  async function handleSync() {
    try {
      setError("");
      setMessage("");

      await syncMutation.mutateAsync();
      //setUploadSuccess(false);

      setMessage("Đang đồng bộ dữ liệu...");

      const timer = setInterval(async () => {
        const result = await getSyncStatus();
        if (result.status === "COMPLETED") {
          clearInterval(timer);
          setUploadSuccess(false);

          setMessage("✅ Đồng bộ hoàn tất");
          setTimeout(() => {
            setMessage("");
          }, 10000);
        }
      }, 3000);
    } catch (err) {
      console.error(err);
      setError("Đồng bộ thất bại");
    }
  }

  // ==========================================
  // GIAO DIỆN MỚI DÀN NGANG - STEP BY STEP
  // ==========================================
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0, 0, 0, 0.4)",
        backdropFilter: "blur(8px)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 9999,
        padding: "20px",
        fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "900px",
          maxHeight: "95vh",
          backgroundColor: "#ffffff",
          borderRadius: "24px",
          boxShadow: "0 24px 48px rgba(0, 0, 0, 0.12)",
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: "20px 28px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            borderBottom: "1px solid #f1f3f4",
            backgroundColor: "#ffffff",
          }}
        >
          <h2
            style={{
              margin: 0,
              fontSize: "22px",
              color: "#202124",
              fontWeight: 500,
              display: "flex",
              alignItems: "center",
              gap: "10px",
            }}
          >
            <FileText size={24} color="#1a73e8" />
            Quản lý tài liệu
          </h2>
          <button
            onClick={onClose}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: "40px",
              height: "40px",
              border: "none",
              borderRadius: "50%",
              backgroundColor: "transparent",
              color: "#5f6368",
              cursor: "pointer",
              transition: "background-color 0.2s",
            }}
            onMouseOver={(e) =>
              (e.currentTarget.style.backgroundColor = "#f1f3f4")
            }
            onMouseOut={(e) =>
              (e.currentTarget.style.backgroundColor = "transparent")
            }
            title="Đóng"
          >
            <X size={22} />
          </button>
        </div>

        {/* Scrollable Body */}
        <div
          style={{
            padding: "28px",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "24px",
          }}
        >
          {/* STEPPER (Thanh tiến trình) */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingBottom: "10px",
            }}
          >
            {/* Step 1 */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                color: !uploadSuccess ? "#1a73e8" : "#10b981",
                transition: "all 0.3s ease",
              }}
            >
              <div
                style={{
                  width: "32px",
                  height: "32px",
                  borderRadius: "50%",
                  backgroundColor: !uploadSuccess ? "#e8f0fe" : "#d1fae5",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "14px",
                  fontWeight: "bold",
                }}
              >
                {uploadSuccess ? <CheckCircle2 size={18} /> : "1"}
              </div>
              <span style={{ fontWeight: 600, fontSize: "15px" }}>
                Tải lên tài liệu
              </span>
            </div>

            {/* Divider */}
            <div
              style={{
                width: "80px",
                height: "2px",
                backgroundColor: uploadSuccess ? "#10b981" : "#dadce0",
                margin: "0 16px",
                transition: "all 0.3s ease",
              }}
            />

            {/* Step 2 */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                color: uploadSuccess ? "#1a73e8" : "#9aa0a6",
                transition: "all 0.3s ease",
              }}
            >
              <div
                style={{
                  width: "32px",
                  height: "32px",
                  borderRadius: "50%",
                  backgroundColor: uploadSuccess ? "#e8f0fe" : "#f1f3f4",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "14px",
                  fontWeight: "bold",
                }}
              >
                2
              </div>
              <span style={{ fontWeight: 600, fontSize: "15px" }}>
                Đồng bộ hệ thống
              </span>
            </div>
          </div>

          {/* Status Messages */}
          {(message || error) && (
            <div
              style={{
                padding: "16px 20px",
                borderRadius: "12px",
                fontSize: "14px",
                fontWeight: 500,
                display: "flex",
                alignItems: "center",
                gap: "10px",
                backgroundColor: message ? "#e6f4ea" : "#fce8e6",
                color: message ? "#137333" : "#c5221f",
                border: `1px solid ${message ? "#ceead6" : "#fad2cf"}`,
              }}
            >
              {message ? <CheckCircle2 size={20} /> : <AlertCircle size={20} />}
              {message || error}
            </div>
          )}

          {/* Render theo từng bước */}
          {!uploadSuccess ? (
            /* ==================================================== */
            /* BƯỚC 1: HIỂN THỊ FORM UPLOAD VÀ THÔNG TIN NGƯỜI DÙNG */
            /* ==================================================== */
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1.2fr",
                gap: "28px",
              }}
            >
              {/* CỘT TRÁI: Thông tin User */}
              <div style={{ display: "flex", flexDirection: "column" }}>
                <div
                  style={{
                    backgroundColor: "#f8f9fa",
                    borderRadius: "16px",
                    padding: "24px",
                    display: "flex",
                    flexDirection: "column",
                    gap: "20px",
                    height: "100%",
                  }}
                >
                  <h3
                    style={{
                      margin: 0,
                      fontSize: "16px",
                      color: "#202124",
                      fontWeight: 600,
                    }}
                  >
                    Thông tin người dùng
                  </h3>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "14px",
                      color: "#3c4043",
                    }}
                  >
                    <div
                      style={{
                        padding: "10px",
                        backgroundColor: "#e8f0fe",
                        borderRadius: "10px",
                        color: "#1a73e8",
                      }}
                    >
                      <User size={20} />
                    </div>
                    <div style={{ display: "flex", flexDirection: "column" }}>
                      <span
                        style={{
                          fontSize: "13px",
                          color: "#5f6368",
                          fontWeight: 500,
                        }}
                      >
                        Vai trò
                      </span>
                      <span style={{ fontWeight: 500, fontSize: "15px" }}>
                        {role ?? "Đang tải..."}
                      </span>
                    </div>
                  </div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "14px",
                      color: "#3c4043",
                    }}
                  >
                    <div
                      style={{
                        padding: "10px",
                        backgroundColor: "#e8f0fe",
                        borderRadius: "10px",
                        color: "#1a73e8",
                      }}
                    >
                      <Briefcase size={20} />
                    </div>
                    <div style={{ display: "flex", flexDirection: "column" }}>
                      <span
                        style={{
                          fontSize: "13px",
                          color: "#5f6368",
                          fontWeight: 500,
                        }}
                      >
                        Phòng ban
                      </span>
                      <span style={{ fontWeight: 500, fontSize: "15px" }}>
                        {role ? role.split("_")[0] : "Đang tải..."}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* CỘT PHẢI: Upload Section */}
              <div
                style={{
                  backgroundColor: "#f8f9fa",
                  borderRadius: "16px",
                  padding: "24px",
                  display: "flex",
                  flexDirection: "column",
                  gap: "20px",
                }}
              >
                <h3
                  style={{
                    margin: 0,
                    fontSize: "16px",
                    color: "#202124",
                    fontWeight: 600,
                  }}
                >
                  Tải lên tài liệu mới
                </h3>

                {/* Dropdowns */}
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "16px",
                  }}
                >
                  <div style={{ position: "relative" }}>
                    <div
                      style={{
                        position: "absolute",
                        left: "14px",
                        top: "50%",
                        transform: "translateY(-50%)",
                        color: "#5f6368",
                        pointerEvents: "none",
                      }}
                    >
                      <Tag size={18} />
                    </div>
                    <select
                      value={documentType}
                      onChange={(e) => setDocumentType(e.target.value)}
                      style={{
                        width: "100%",
                        height: "48px",
                        borderRadius: "12px",
                        border: "1px solid #dadce0",
                        padding: "0 16px 0 44px",
                        fontSize: "14px",
                        color: "#202124",
                        backgroundColor: "#ffffff",
                        outline: "none",
                        appearance: "none",
                        cursor: "pointer",
                        boxSizing: "border-box",
                      }}
                    >
                      <option value="">Chọn loại tài liệu</option>
                      <option value="Chính sách">Chính sách</option>
                      <option value="Kế hoạch">Kế hoạch</option>
                      <option value="Báo cáo">Báo cáo</option>
                    </select>
                  </div>

                  <div style={{ position: "relative" }}>
                    <div
                      style={{
                        position: "absolute",
                        left: "14px",
                        top: "50%",
                        transform: "translateY(-50%)",
                        color: "#5f6368",
                        pointerEvents: "none",
                      }}
                    >
                      <Shield size={18} />
                    </div>
                    <select
                      value={securityLevel}
                      onChange={(e) => setSecurityLevel(e.target.value)}
                      style={{
                        width: "100%",
                        height: "48px",
                        borderRadius: "12px",
                        border: "1px solid #dadce0",
                        padding: "0 16px 0 44px",
                        fontSize: "14px",
                        color: "#202124",
                        backgroundColor: "#ffffff",
                        outline: "none",
                        appearance: "none",
                        cursor: "pointer",
                        boxSizing: "border-box",
                      }}
                    >
                      <option value="">Chọn lớp bảo mật</option>
                      <option value="Công khai">Công khai</option>
                      <option value="Lựa chọn 2">Lựa chọn 2</option>
                      <option value="Lựa chọn 3">Lựa chọn 3</option>
                    </select>
                  </div>
                </div>

                {/* File Input */}
                <div
                  style={{
                    position: "relative",
                    width: "100%",
                    padding: "32px 24px",
                    border: `2px dashed ${file ? "#1a73e8" : "#dadce0"}`,
                    borderRadius: "12px",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "12px",
                    backgroundColor: file ? "#e8f0fe" : "#ffffff",
                    transition: "all 0.2s ease",
                    boxSizing: "border-box",
                    textAlign: "center",
                  }}
                >
                  <input
                    type="file"
                    onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                    style={{
                      position: "absolute",
                      inset: 0,
                      width: "100%",
                      height: "100%",
                      opacity: 0,
                      cursor: "pointer",
                    }}
                  />
                  <CloudUpload
                    color={file ? "#1a73e8" : "#5f6368"}
                    size={36}
                  />
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "4px",
                    }}
                  >
                    <span
                      style={{
                        color: file ? "#1a73e8" : "#202124",
                        fontSize: "14px",
                        fontWeight: 500,
                      }}
                    >
                      {file ? file.name : "Nhấp hoặc kéo thả file vào đây"}
                    </span>
                    {!file && (
                      <span style={{ color: "#5f6368", fontSize: "12px" }}>
                        Hỗ trợ PDF, DOCX, XLSX...
                      </span>
                    )}
                  </div>
                </div>

                <button
                  onClick={handleUpload}
                  disabled={isProcessing}
                  style={{
                    marginTop: "auto",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "8px",
                    padding: "14px 24px",
                    border: "none",
                    borderRadius: "12px",
                    backgroundColor: "#1a73e8",
                    color: "white",
                    fontWeight: 500,
                    fontSize: "15px",
                    cursor: !file || isProcessing ? "not-allowed" : "pointer",
                    opacity: !file || isProcessing ? 0.6 : 1,
                    transition: "opacity 0.2s",
                    width: "100%",
                  }}
                >
                  <Upload size={18} />
                  {uploadMutation.isPending
                    ? "Đang tải lên..."
                    : "Tải lên tài liệu"}
                </button>
              </div>
            </div>
          ) : (
            /* ==================================================== */
            /* BƯỚC 2: HIỂN THỊ PHẦN ĐỒNG BỘ NẾU UPLOAD THÀNH CÔNG  */
            /* ==================================================== */
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                padding: "20px 0 40px 0",
                animation: "fadeIn 0.4s ease-out",
              }}
            >
              <div
                style={{
                  backgroundColor: "#f8f9fa",
                  borderRadius: "20px",
                  padding: "40px 32px",
                  width: "100%",
                  maxWidth: "500px",
                  display: "flex",
                  flexDirection: "column",
                  gap: "24px",
                  textAlign: "center",
                  border: "1px solid #e8eaed",
                }}
              >
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div
                    style={{
                      padding: "20px",
                      backgroundColor: "#e6f4ea",
                      borderRadius: "50%",
                    }}
                  >
                    <RefreshCw size={48} color="#137333" />
                  </div>
                </div>
                <div>
                  <h3
                    style={{
                      margin: "0 0 12px 0",
                      fontSize: "20px",
                      color: "#202124",
                      fontWeight: 600,
                    }}
                  >
                    Tài liệu đã sẵn sàng
                  </h3>
                  <p
                    style={{
                      margin: 0,
                      color: "#5f6368",
                      fontSize: "15px",
                      lineHeight: "1.6",
                    }}
                  >
                    Tài liệu của bạn đã được lưu trữ an toàn. Vui lòng chạy
                    Logic App để ingest tài liệu từ SharePoint vào hệ thống
                    Azure AI Search.
                  </p>
                </div>

                <button
                  onClick={handleSync}
                  disabled={isProcessing}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "10px",
                    padding: "16px 24px",
                    border: "none",
                    borderRadius: "12px",
                    backgroundColor: "#188038", // Màu xanh lá mạnh mẽ cho Sync
                    color: "white",
                    fontWeight: 600,
                    fontSize: "16px",
                    cursor: isProcessing ? "not-allowed" : "pointer",
                    opacity: isProcessing ? 0.7 : 1,
                    transition: "all 0.2s",
                    width: "100%",
                    marginTop: "8px",
                  }}
                >
                  <RefreshCw
                    size={20}
                    style={{
                      animation: syncMutation.isPending
                        ? "spin 1s linear infinite"
                        : "none",
                    }}
                  />
                  {syncMutation.isPending ? "Đang đồng bộ..." : "Đồng bộ ngay"}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      <style>
        {`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
          }
        `}
      </style>
    </div>
  );
}