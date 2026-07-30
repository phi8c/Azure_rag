import { Button, Card, Typography } from "antd";

import AuthService from "../services/authService";

const { Title, Paragraph } = Typography;

export default function LoginPage() {
    const handleLogin = async () => {
        const response = await AuthService.microsoftLogin();

        window.location.href = response.login_url;
    };

    return (
        <div
            style={{
                height: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <Card
                style={{
                    width: 420,
                }}
            >
                <Title level={3}>
                    Planner Dashboard
                </Title>

                <Paragraph>
                    Sign in with your Microsoft account.
                </Paragraph>

                <Button
                    type="primary"
                    block
                    size="large"
                    onClick={handleLogin}
                >
                    Sign in with Microsoft
                </Button>
            </Card>
        </div>
    );
}