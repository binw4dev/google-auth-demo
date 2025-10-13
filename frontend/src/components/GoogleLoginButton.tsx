import { useEffect } from "react";

declare global {
  interface Window {
    google: any;
  }
}
const google = window.google;
import { googleLogin } from "../api";

interface GoogleLoginButtonProps {
  onLogin: (data: any) => void;
}

export default function GoogleLoginButton({ onLogin }: GoogleLoginButtonProps) {
  useEffect(() => {
    google.accounts.id.initialize({
      client_id: "1051103924645-mmlfpc1ara82g8da5lhcmsf35slrrcju.apps.googleusercontent.com",
      callback: handleCredentialResponse,
    });
    google.accounts.id.renderButton(
      document.getElementById("googleSignInDiv"),
      { theme: "outline", size: "large" }
    );
  }, []);

  const handleCredentialResponse = async (response: { credential: string }) => {
    const data = await googleLogin(response.credential);
    onLogin(data);
  };

  return <div id="googleSignInDiv"></div>;
}
