<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  onMount(() => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    
    if (!token || !role) {
      goto('/login');
      return;
    }
    
    // Redirect to role-specific dashboard
    switch(role) {
      case 'head_teacher':
        goto('/head-teacher');
        break;
      case 'teacher':
        goto('/teacher');
        break;
      case 'accountant':
        goto('/accountant');
        break;
      case 'parent':
        goto('/parent');
        break;
      default:
        goto('/login');
    }
  });
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center">
  <div class="text-center">
    <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
    <p class="text-gray-600">Redirecting to your dashboard...</p>
  </div>
</div>
