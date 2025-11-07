import { writable } from 'svelte/store';

function createAuthStore() {
  const { subscribe, set, update } = writable({
    user: null,
    token: null,
    isAuthenticated: false
  });

  return {
    subscribe,
    init: () => {
      if (typeof window !== 'undefined') {
        const storedUser = localStorage.getItem('user');
        const storedToken = localStorage.getItem('token');
        
        if (storedUser && storedToken) {
          set({
            user: JSON.parse(storedUser),
            token: storedToken,
            isAuthenticated: true
          });
        }
      }
    },
    login: (user, token) => {
      set({ user, token, isAuthenticated: true });
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('token', token);
      }
    },
    logout: () => {
      set({ user: null, token: null, isAuthenticated: false });
      if (typeof window !== 'undefined') {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
  };
}

export const authStore = createAuthStore();
export const user = writable(null);
export const token = writable(null);
