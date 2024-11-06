//import axios from "axios";

//const API_URL = "https://api.seudominio.com/api";

//export const login = async (username, password) => {
//  const response = await axios.post(`${API_URL}/login`, { username, password });
// return response.data;
//};

//src / api / auth.js;

const testUser = {
  username: "usuario_teste",
  password: "senha123",
  name: "Usuário Teste",
  email: "teste@exemplo.com",
};

export const login = async (username, password) => {
  // Simula uma chamada de API
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (username === testUser.username && password === testUser.password) {
        resolve({
          token: "fake-jwt-token",
          user: {
            name: testUser.name,
            email: testUser.email,
          },
        });
      } else {
        reject(new Error("Credenciais inválidas"));
      }
    }, 300); // Simula um delay de rede
  });
};
