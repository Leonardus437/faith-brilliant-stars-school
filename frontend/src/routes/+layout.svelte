<script>
  import '../app.css';
  import { onMount } from 'svelte';
  import { themeStore } from '$lib/stores/theme.js';
  import { languageStore } from '$lib/stores/language.js';

  // Accept SvelteKit props to suppress warnings
  export let data = undefined;
  export let form = undefined;

  onMount(() => {
    try {
      themeStore.init();
      languageStore.init();
    } catch (error) {
      console.warn('Theme/Language initialization failed:', error);
    }
  });
</script>

<slot />