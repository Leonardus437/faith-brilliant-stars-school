<script>
  import { onMount } from 'svelte';
  import { languageStore } from '$lib/stores/language.js';
  
  let currentLang = 'en';
  
  onMount(() => {
    languageStore.init();
  });
  
  languageStore.subscribe(value => {
    currentLang = value;
  });
  
  function setLanguage(lang) {
    languageStore.setLanguage(lang);
  }
</script>

<div class="flex items-center space-x-1 bg-white border-2 border-gray-300 rounded-lg p-1">
  <button
    on:click={() => setLanguage('en')}
    class="px-3 py-1.5 rounded-md text-sm font-semibold transition-all {currentLang === 'en' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}"
  >
    English
  </button>
  <button
    on:click={() => setLanguage('rw')}
    class="px-3 py-1.5 rounded-md text-sm font-semibold transition-all {currentLang === 'rw' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}"
  >
    Kinyarwanda
  </button>
</div>
