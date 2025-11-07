import { goto } from '$app/navigation';
import { browser } from '$app/environment';

export function checkAuth() {
  if (!browser) return false;
  
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  
  if (!token || !role) {
    goto('/login');
    return false;
  }
  
  return true;
}

export function logout() {
  if (browser) {
    localStorage.clear();
    goto('/login');
  }
}

export function getRole() {
  if (!browser) return null;
  return localStorage.getItem('role');
}

export function getToken() {
  if (!browser) return null;
  return localStorage.getItem('token');
}
