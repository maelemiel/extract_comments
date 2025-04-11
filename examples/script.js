/**
 * Script d'exemple pour démontrer les annotations de commentaires
 */

// TODO: Convertir ce script en TypeScript @pierre P2 DUE:2023-11-30
const API_URL = 'https://api.example.com';

/**
 * Récupère les données utilisateur
 */
async function fetchUserData(userId) {
  try {
    // FIXME: Gérer les erreurs de réseau correctement @alice P1 #12 DUE:2023-10-30
    const response = await fetch(`${API_URL}/users/${userId}`);
    return await response.json();
  } catch (error) {
    // BUG: L'erreur n'est pas correctement transmise à l'interface P1
    console.error('Erreur lors de la récupération des données:', error);
    return null;
  }
}

/**
 * Initialise l'application
 */
function initApp() {
  // OPTIMIZE: Réduire le nombre d'appels DOM @bob P3
  const loginButton = document.getElementById('login-button');
  const signupButton = document.getElementById('signup-button');
  
  // HACK: Contourne le problème de rendu sur Safari @pierre
  setTimeout(() => {
    document.body.classList.add('loaded');
  }, 100);
  
  // NOTE: Les gestionnaires d'événements devraient être déplacés dans un module séparé
  loginButton?.addEventListener('click', handleLogin);
  signupButton?.addEventListener('click', handleSignup);
}

// QUESTION: Devrions-nous utiliser une bibliothèque de validation? @alice
function validateForm(formData) {
  // REVIEW: Cette logique de validation pourrait être simplifiée @bob P2 DUE:2023-12-05
  return Object.values(formData).every(value => value !== '');
}

// IDEA: Implémenter un système de thèmes pour l'interface @pierre P3 CREATED:2023-09-15
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
}

// IN PROGRESS: Refactorisation du système d'authentification @alice P2 DUE:2023-11-15
function handleLogin() {
  console.log('Login functionality coming soon...');
}

function handleSignup() {
  // TEMP: À remplacer par l'intégration avec le système d'authentification
  alert('Inscription temporairement désactivée');
}

// Initialisation
document.addEventListener('DOMContentLoaded', initApp);
