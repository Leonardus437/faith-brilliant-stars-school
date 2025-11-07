import { derived } from 'svelte/store';
import { languageStore } from '../stores/language.js';
import { translations } from './translations.js';

export const t = derived(languageStore, ($lang) => {
  return (key) => {
    const keys = key.split('.');
    let value = translations[$lang];
    
    for (const k of keys) {
      if (value && typeof value === 'object') {
        value = value[k];
      } else {
        return key; // Return key if translation not found
      }
    }
    
    return value || key;
  };
});