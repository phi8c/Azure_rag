import { LogLevel } from "@azure/msal-browser";

export const msalConfig = {
  auth: {
    clientId: "0179a856-6a0e-450f-8a06-1afddd5727ee",
    authority:
      "https://login.microsoftonline.com/858bad56-b0d7-4d5e-94d7-aa0d82eedbe2",
    redirectUri: window.location.origin,
  },

  cache: {
    cacheLocation: "localStorage",
    storeAuthStateInCookie: false,
  },

  system: {
    loggerOptions: {
      loggerCallback: () => {},
      piiLoggingEnabled: false,
      logLevel: LogLevel.Info,
    },
  },
};

export const loginRequest = {
  scopes: ["User.Read",  "GroupMember.Read.All"],
};