<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let user = null;

  onMount(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      user = JSON.parse(userData);
    }
  });

  function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    goto('/login');
  }

  function canAccess(roles) {
    return user && roles.includes(user.role);
  }
</script>

<nav class="bg-blue-600 text-white shadow-lg">
  <div class="container mx-auto px-4">
    <div class="flex items-center justify-between h-16">
      <div class="flex items-center space-x-8">
        <a href="/dashboard" class="text-xl font-bold">
          ⭐ Faith Brilliant Stars School
        </a>
        
        {#if user}
          <div class="hidden md:flex space-x-4">
            <a href="/dashboard" class="hover:bg-blue-700 px-3 py-2 rounded">
              🏠 Dashboard
            </a>
            
            {#if canAccess(['admin', 'head_teacher'])}
              <a href="/students" class="hover:bg-blue-700 px-3 py-2 rounded">
                👨🎓 Students
              </a>
              <a href="/classes" class="hover:bg-blue-700 px-3 py-2 rounded">
                🏫 Classes
              </a>
            {/if}
            
            {#if canAccess(['teacher', 'admin', 'head_teacher'])}
              <a href="/attendance" class="hover:bg-blue-700 px-3 py-2 rounded">
                ✅ Attendance
              </a>
            {/if}
            
            {#if canAccess(['accountant', 'admin'])}
              <a href="/fees" class="hover:bg-blue-700 px-3 py-2 rounded">
                💳 Fees
              </a>
            {/if}
          </div>
        {/if}
      </div>
      
      {#if user}
        <div class="flex items-center space-x-4">
          <div class="text-sm">
            <div class="font-medium">{user.full_name}</div>
            <div class="text-blue-200 text-xs">{user.role.replace('_', ' ').toUpperCase()}</div>
          </div>
          <button on:click={logout} class="bg-red-500 hover:bg-red-600 px-4 py-2 rounded">
            Logout
          </button>
        </div>
      {/if}
    </div>
  </div>
</nav>
