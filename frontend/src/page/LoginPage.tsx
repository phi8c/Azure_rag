import { useMsal } from "@azure/msal-react";
import { loginRequest } from "@/shared/auth/authConfig";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {

  const navigate = useNavigate();

  const { instance } = useMsal();

  const login = async () => {

  try {

    const result =
      await instance.loginPopup(
        loginRequest
      );

    instance.setActiveAccount(
      result.account
    );

    navigate("/");

  } catch (error) {

    console.error(error);

  }

};
  return (

    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        background:
          "linear-gradient(135deg,#f8fafc 0%,#eef2ff 100%)",
      }}
    >

      <div
        style={{
          flex: 1,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: "48px",
        }}
      >

        <div
          style={{
            width: "100%",
            maxWidth: "480px",
            background: "#ffffff",
            borderRadius: "24px",
            padding: "48px",
            boxShadow:
              "0 20px 60px rgba(15,23,42,0.08)",
            border:
              "1px solid rgba(226,232,240,0.8)",
          }}
        >

          <div
            style={{
              marginBottom: "40px",
            }}
          >

            <div
              style={{
                width: "56px",
                height: "56px",
                borderRadius: "16px",
                background: "#2563eb",
                color: "#fff",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "24px",
                fontWeight: 700,
                marginBottom: "24px",
              }}
            >
              R
            </div>

            <h1
              style={{
                margin: 0,
                fontSize: "32px",
                fontWeight: 700,
                color: "#0f172a",
              }}
            >
              Enterprise RAG
            </h1>

            <p
              style={{
                marginTop: "12px",
                color: "#64748b",
                lineHeight: 1.7,
                fontSize: "15px",
              }}
            >
              Secure access to internal knowledge,
              company policies and enterprise
              documents through Microsoft Entra ID.
            </p>

          </div>

          <button
            onClick={login}
            style={{
              width: "100%",
              height: "56px",
              border: "none",
              borderRadius: "14px",
              background: "#2563eb",
              color: "#ffffff",
              fontSize: "16px",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            Sign in with Microsoft
          </button>

          <div
            style={{
              marginTop: "24px",
              textAlign: "center",
              fontSize: "13px",
              color: "#94a3b8",
            }}
          >
            Powered by Microsoft Entra ID
          </div>

        </div>

      </div>

      <div
        style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "64px",
        }}
      >

        <div
          style={{
            maxWidth: "520px",
          }}
        >

          <div
            style={{
              fontSize: "14px",
              fontWeight: 600,
              color: "#2563eb",
              marginBottom: "16px",
            }}
          >
            ENTERPRISE AI PLATFORM
          </div>

          <h2
            style={{
              margin: 0,
              fontSize: "48px",
              lineHeight: 1.2,
              color: "#0f172a",
            }}
          >
            Chat with your company's knowledge.
          </h2>

          <p
            style={{
              marginTop: "24px",
              fontSize: "18px",
              lineHeight: 1.8,
              color: "#64748b",
            }}
          >
            Access policies, procedures,
            documentation and internal
            information securely with
            role-based permissions.
          </p>

        </div>

      </div>

    </div>

  );

}