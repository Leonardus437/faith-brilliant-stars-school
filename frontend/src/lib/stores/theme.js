import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const defaultTheme = 'light';

function createThemeStore() {
  const { subscribe, set } = writable(defaultTheme);

  return {
    subscribe,
    toggle: () => {
      if (!browser) return;
      
      const currentTheme = localStorage.getItem('theme') || defaultTheme;
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      
      localStorage.setItem('theme', newTheme);
      
      if (newTheme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      
      set(newTheme);
    },
    init: () => {
      if (!browser) return;
      
      const savedTheme = localStorage.getItem('theme') || defaultTheme;
      
      if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      
      set(savedTheme);
    }
  };
}

export const themeStore = createThemeStore();