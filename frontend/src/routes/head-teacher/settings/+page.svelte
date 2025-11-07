<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let settings = { 
    school_name: 'Faith Brilliant Stars School', 
    address: 'Kigali, Rwanda', 
    phone: '+250788000000', 
    email: 'info@faithschool.rw', 
    academic_year: '2024-2025',
    principal_name: 'Dr. Sarah Mugisha',
    motto: 'Excellence in Education',
    website: 'www.faithschool.rw'
  };
  let loading = false;
  let showSuccess = false;
  
  onMount(async () => {
    await loadSettings();
  });
  
  async function loadSettings() {
    const token = localStorage.getItem('token');
    try {
      const res = await fetch('http://localhost:8001/api/head-teacher/settings', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        if (data.school_name) settings = data;
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  }
  
  async function saveSettings() {
    loading = true;
    const token = localStorage.getItem('token');
    try {
      const res = await fetch('http://localhost:8001/api/head-teacher/settings', {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      });
      if (res.ok) {
        showSuccess = true;
        setTimeout(() => showSuccess = false, 3000);
      }
    } catch (error) {
      alert('Error saving settings');
    } finally {
      loading = false;
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 p-6">
  <div class="max-w-4xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800">School Settings</h1>
        <p class="text-gray-600">Configure school information and policies</p>
      </div>
      <button on:click={() => goto('/head-teacher')} class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg">
        Back to Dashboard
      </button>
    </div>
    
    <div class="bg-white rounded-xl shadow-lg p-8">
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">School Name</label>
          <input bind:value={settings.school_name} class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Principal Name</label>
          <input bind:value={settings.principal_name} class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">School Motto</label>
          <input bind:value={settings.motto} class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Address</label>
          <textarea bind:value={settings.address} rows="2" class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500"></textarea>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Phone</label>
            <input bind:value={settings.phone} class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input bind:value={settings.email} type="email" class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Academic Year</label>
            <input bind:value={settings.academic_year} class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Website</label>
            <input bind:value={settings.website} class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>
        </div>
        
        <button on:click={saveSettings} disabled={loading} 
                class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white py-3 rounded-lg font-semibold text-lg">
          {loading ? 'Saving...' : 'Save Settings'}
        </button>
      </div>
    </div>
  </div>
</div>

{#if showSuccess}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-8 max-w-md w-full text-center">
      <div class="text-6xl mb-4">✅</div>
      <h2 class="text-2xl font-bold text-gray-800 mb-2">Settings Saved!</h2>
      <p class="text-gray-600">School settings have been updated successfully.</p>
    </div>
  </div>
{/if}
