<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  onMount(() => {
    goto('/admin/students');
  });
</script>

<div class="min-h-screen flex items-center justify-center">
  <p>Redirecting...</p>
</div>
