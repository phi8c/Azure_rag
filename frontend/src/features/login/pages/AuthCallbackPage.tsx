import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function AuthCallbackPage() {
    const navigate = useNavigate();

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);

        const token = params.get("token");

        if (!token) {
            navigate("/login");
            return;
        }

        localStorage.setItem(
            "access_token",
            token,
        );

        navigate("/");
    }, [navigate]);

    return <div>Signing in...</div>;
}