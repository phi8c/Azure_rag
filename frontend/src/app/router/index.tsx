import {
    createBrowserRouter,
} from "react-router-dom";

import ChatPage from "@/features/chat/pages/ChatPage";
import LoginPage from "@/features/login/pages/LoginPage";
import AuthCallbackPage from "@/features/login/pages/AuthCallbackPage";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <ChatPage />,
    },
    {
        path: "/login",
        element: <LoginPage />,
    },
    {
        path: "/auth/callback",
        element: <AuthCallbackPage />,
    },
]);