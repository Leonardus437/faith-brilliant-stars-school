import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function createLanguageStore() {
  const { subscribe, set } = writable('en');

  return {
    subscribe,
    setLanguage: (lang) => {
      if (browser) {
        localStorage.setItem('language', lang);
      }
      set(lang);
    },
    init: () => {
      if (browser) {
        const stored = localStorage.getItem('language');
        const lang = stored || 'en';
        set(lang);
      }
    }
  };
}

export const languageStore = createLanguageStore();