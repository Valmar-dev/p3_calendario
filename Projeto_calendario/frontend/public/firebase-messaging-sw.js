importScripts("https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/9.6.1/firebase-messaging-compat.js");

// Configuração do Firebase
firebase.initializeApp({
    apiKey: "AIzaSyDDFv3SIghsqBTZ9x1wbYI0hU4-sHjFHSE",
    authDomain: "callendario-51b66.firebaseapp.com",
    projectId: "callendario-51b66",
    storageBucket: "callendario-51b66.firebasestorage.app",
    messagingSenderId: "137161499282",
    appId: "1:137161499282:web:51469bfc22dc7f06e4fc4b",
    measurementId: "G-YEP2CRGFVN"
});

const messaging = firebase.messaging();

// Evento para exibir notificações em segundo plano
messaging.onBackgroundMessage((payload) => {
  console.log("Notificação recebida em segundo plano:", payload);
  self.registration.showNotification(payload.notification.title, {
    body: payload.notification.body,
  });
});
