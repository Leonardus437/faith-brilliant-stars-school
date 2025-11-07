<script>
  import { goto } from '$app/navigation';
  import { t } from '$lib/i18n/index.js';
  import LanguageToggle from '$lib/components/LanguageToggle.svelte';

  let email = '';
  let password = '';
  let error = '';
  let loading = false;

  const roles = [
    { email: 'head@faithschool.rw', name: 'Head Teacher', role: 'Administrator', color: 'from-purple-500 to-purple-600' },
    { email: 'teacher@faithschool.rw', name: 'Teacher', role: 'Educator', color: 'from-blue-500 to-blue-600' },
    { email: 'accounts@faithschool.rw', name: 'Accountant', role: 'Finance Manager', color: 'from-green-500 to-green-600' },
    { email: 'parent@faithschool.rw', name: 'Parent', role: 'Guardian', color: 'from-orange-500 to-orange-600' }
  ];

  async function handleLogin() {
    error = '';
    loading = true;

    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await fetch('http://localhost:8001/api/auth/login', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Login failed');
      }
      
      const data = await response.json();

      // Import authStore dynamically
      const { authStore } = await import('$lib/stores/auth.js');
      authStore.login(data.user, data.access_token);
      
      // Redirect based on role
      const role = data.user.role;
      if (role === 'head_teacher') {
        goto('/head-teacher');
      } else if (role === 'accountant') {
        goto('/accountant');
      } else if (role === 'teacher') {
        goto('/attendance');
      } else if (role === 'parent') {
        goto('/parent');
      } else {
        goto('/dashboard');
      }
    } catch (err) {
      error = err.message || 'Login failed. Please check your credentials.';
    } finally {
      loading = false;
    }
  }

  function quickLogin(roleEmail) {
    email = roleEmail;
    password = roleEmail.includes('head') ? 'Head2024' : 
               roleEmail.includes('teacher') ? 'Teacher2024' :
               roleEmail.includes('accounts') ? 'Accounts2024' : 'Parent2024';
  }
</script>

<svelte:head>
  <title>Login - Faith Brilliant Stars School</title>
</svelte:head>

<div class="min-h-screen relative overflow-hidden">
  <!-- Background Image -->
  <div class="absolute inset-0 bg-cover bg-center bg-no-repeat" style="background-image: url('/1.jpg');"></div>
  <div class="absolute inset-0 bg-black/40"></div>
  
  <!-- Content -->
  <div class="relative z-10 min-h-screen flex items-center justify-center p-6">
    <div class="w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="flex justify-center items-center mb-6 space-x-4">
          <div class="w-16 h-16 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl flex items-center justify-center text-white font-bold text-2xl shadow-2xl">
            FBS
          </div>
          <LanguageToggle />
        </div>
        <h1 class="text-3xl font-bold text-white mb-2 drop-shadow-lg">{$t('welcomeBack')}</h1>
        <p class="text-white/90 text-lg drop-shadow">{$t('signIn')} {$t('schoolName')}</p>
      </div>

      <!-- Login Form -->
      <div class="bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/30 p-8">
        <div class="mb-6">
          <h2 class="text-xl font-bold text-gray-900 mb-1">{$t('signInToAccount')}</h2>
          <p class="text-gray-600 text-sm">{$t('enterCredentials')}</p>
        </div>
        
        {#if error}
          <div class="bg-red-50 border-l-4 border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
            <div class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
              {error}
            </div>
          </div>
        {/if}

        <form on:submit|preventDefault={handleLogin} class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/>
                </svg>
              </div>
              <input 
                type="email" 
                bind:value={email}
                placeholder="your.email@faithschool.rw"
                required
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white/90 backdrop-blur-sm transition-all duration-200 text-gray-900 placeholder-gray-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
              </div>
              <input 
                type="password" 
                bind:value={password}
                placeholder="Enter your password"
                required
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white/90 backdrop-blur-sm transition-all duration-200 text-gray-900 placeholder-gray-500"
              />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white py-3 rounded-lg font-semibold shadow-xl transform hover:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {#if loading}
              <div class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                </svg>
                Signing in...
              </div>
            {:else}
              Sign In
            {/if}
          </button>
        </form>

        <div class="mt-6 pt-4 border-t border-gray-200">
          <div class="text-center">
            <a href="/" class="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium transition-colors text-sm">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
              </svg>
              Back to Home
            </a>
          </div>
        </div>
      </div>

      <!-- Quick Access Panel -->
      <div class="mt-6">
        <div class="bg-white/90 backdrop-blur-xl rounded-xl p-4 border border-white/30">
          <h3 class="text-lg font-bold text-gray-900 mb-2">Quick Access</h3>
          <p class="text-gray-600 text-xs mb-4">Demo credentials</p>
          
          <div class="grid grid-cols-2 gap-2">
            {#each roles as role}
              <button 
                on:click={() => quickLogin(role.email)}
                class="bg-white/80 hover:bg-white hover:shadow-md rounded-lg p-3 text-left transform hover:scale-[1.02] transition-all duration-200 border border-gray-100"
              >
                <div class="flex items-center space-x-2">
                  <div class="w-8 h-8 bg-gradient-to-br {role.color} rounded-md flex items-center justify-center">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      {#if role.name === 'Head Teacher'}
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                      {:else if role.name === 'Teacher'}
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                      {:else if role.name === 'Accountant'}
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      {:else}
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                      {/if}
                    </svg>
                  </div>
                  <div>
                    <h4 class="font-medium text-gray-900 text-xs">{role.name}</h4>
                    <p class="text-xs text-gray-500">{role.role}</p>
                  </div>
                </div>
              </button>
            {/each}
          </div>
        </div>
      </div>
    </div>
  </div>
</div>