/* // Importando os módulos do Firebase
import { initializeApp } from 'firebase/app';
import axios from 'axios';
import { getMessaging, getToken, onMessage } from 'firebase/messaging';

// Sua configuração do Firebase
const firebaseConfig = {
  apiKey: "AIzaSyDDFv3SIghsqBTZ9x1wbYI0hU4-sHjFHSE",
  authDomain: "callendario-51b66.firebaseapp.com",
  projectId: "callendario-51b66",
  storageBucket: "callendario-51b66.firebasestorage.app",
  messagingSenderId: "137161499282",
  appId: "1:137161499282:web:51469bfc22dc7f06e4fc4b",
  measurementId: "G-YEP2CRGFVN"
};

// Inicializando o Firebase
const app = initializeApp(firebaseConfig);

// Inicializando o Firebase Messaging
const messaging = getMessaging(app);

// Função para obter o token do Firebase Cloud Messaging
export function solicitarPermissao() {
  Notification.requestPermission().then(permission => {
    if (permission === "granted") {
      console.log("Permissão concedida");
      const messaging = getMessaging();
      getToken(messaging, {
        vapidKey: "BKEm2-jnvje44g8ubK9AQX4HmbTxzogRbcj_Gr0q9pgJqQZTHTt4LLAbY5E5yg_cBn_bL9AazkrKjwWwRzohh6s" // Substitua pela sua chave VAPID
      }).then((currentToken) => {
        if (currentToken) {
          console.log("Token do dispositivo: ", currentToken);

          // Enviar o token para o backend via POST
          axios.post('http://localhost:8000/api/registrar_token/', { token: currentToken })
            .then(response => {
              console.log('Token enviado com sucesso:', response);
            })
            .catch(error => {
              console.error('Erro ao enviar o token:', error);
            });
        } else {
          console.log("Não foi possível obter o token");
        }
      }).catch((err) => {
        console.log("Erro ao obter o token", err);
      });
    } else {
      console.log("Permissão negada");
    }
  });
}

// Definir como reagir a mensagens recebidas no primeiro plano
onMessage(messaging, (payload) => {
  console.log("Mensagem recebida em primeiro plano: ", payload);
  const notificationTitle = "Nova Notificação";
  const notificationOptions = {
    body: payload.notification.body,
    icon: payload.notification.icon
  };

  if (Notification.permission === "granted") {
    new Notification(notificationTitle, notificationOptions);
  }
});
 */