import { api }
from "@/shared/api/axios";

export interface MicrosoftLoginResponse {
    login_url: string;
}

class AuthService {
    async microsoftLogin(): Promise<MicrosoftLoginResponse> {
        const { data } = await api.get<MicrosoftLoginResponse>(
            "/auth/microsoft/login",
        );

        return data;
    }
}

export default new AuthService();