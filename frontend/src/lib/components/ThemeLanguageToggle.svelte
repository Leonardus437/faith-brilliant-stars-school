<script>
  import { themeStore } from '../stores/theme.js';
  import { languageStore } from '../stores/language.js';
  import { t } from '../i18n/index.js';
  import { onMount } from 'svelte';

  let currentTheme = 'light';
  let currentLanguage = 'en';
  let showDropdown = false;

  $: currentTheme = $themeStore;
  $: currentLanguage = $languageStore;

  onMount(() => {
    themeStore.init();
    languageStore.init();
  });

  function handleThemeToggle() {
    themeStore.toggle();
  }

  function setLanguage(lang) {
    languageStore.setLanguage(lang);
    showDropdown = false;
  }
</script>

<div class="flex items-center space-x-3">
  <!-- Theme Toggle Button -->
  <button
    on:click={handleThemeToggle}
    class="p-2.5 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 transition-all duration-200 border border-gray-200 dark:border-gray-600"
    title={currentTheme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
  >
    {#if currentTheme === 'light'}
      <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
      </svg>
    {:else}
      <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
      </svg>
    {/if}
  </button>

  <!-- Language Dropdown -->
  <div class="relative">
    <button
      on:click={() => showDropdown = !showDropdown}
      class="flex items-center space-x-2 p-2.5 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 transition-all duration-200 border border-gray-200 dark:border-gray-600"
    >
      <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
      </svg>
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
        {currentLanguage === 'en' ? 'EN' : 'RW'}
      </span>
      <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
      </svg>
    </button>

    {#if showDropdown}
      <div class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50">
        <div class="py-1">
          <button
            on:click={() => setLanguage('en')}
            class="w-full text-left px-4 py-3 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center space-x-3 transition-colors {currentLanguage === 'en' ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' : ''}"
          >
            <span class="text-lg">🇬🇧</span>
            <span>English</span>
            {#if currentLanguage === 'en'}
              <svg class="w-4 h-4 ml-auto" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            {/if}
          </button>
          <button
            on:click={() => setLanguage('rw')}
            class="w-full text-left px-4 py-3 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center space-x-3 transition-colors {currentLanguage === 'rw' ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' : ''}"
          >
            <span class="text-lg">🇷🇼</span>
            <span>Kinyarwanda</span>
            {#if currentLanguage === 'rw'}
              <svg class="w-4 h-4 ml-auto" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            {/if}
          </button>
        </div>
      </div>
    {/if}
  </div>
</div>

<!-- Click outside to close dropdown -->
{#if showDropdown}
  <div class="fixed inset-0 z-40" on:click={() => showDropdown = false}></div>
{/if}