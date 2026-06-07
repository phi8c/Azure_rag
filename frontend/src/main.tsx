import ReactDOM from "react-dom/client";
import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";

import App from "./App";
import { msalConfig } from "./shared/auth/authConfig";

import "./app/style/global.css";

const msalInstance = new PublicClientApplication(
  msalConfig
);

async function bootstrap() {
  await msalInstance.initialize();

  ReactDOM.createRoot(
    document.getElementById("root")!
  ).render(
    <MsalProvider
      instance={msalInstance}
    >
      <App />
    </MsalProvider>
  );
}

bootstrap();