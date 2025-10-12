import axios from "axios";

const API_BASE = "http://localhost:8000";

export const googleLogin = async (idToken: string): Promise<any> => {
  const res = await axios.post(`${API_BASE}/api/auth/google`, { id_token: idToken });
  return res.data;
};

export const getMe = async (token: string): Promise<any> => {
  const res = await axios.get(`${API_BASE}/api/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};
