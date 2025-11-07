<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let announcements = [];
  let showModal = false;
  let newAnnouncement = { 
    title: '', 
    content: '', 
    priority: 'normal',
    target_roles: []
  };
  let loading = true;
  
  function openModal() {
    console.log('Button clicked!');
    showModal = true;
    console.log('Modal should be:', showModal);
  }
  
  const roles = [
    { value: 'all', label: 'All Users' },
    { value: 'teacher', label: 'Teachers' },
    { value: 'accountant', label: 'Accountants' },
    { value: 'parent', label: 'Parents' }
  ];
  
  onMount(async () => {
    await loadAnnouncements();
  });
  
  async function loadAnnouncements() {
    const token = localStorage.getItem('token');
    try {
      const res = await fetch('http://localhost:8001/api/announcements', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        announcements = Array.isArray(data) ? data : [];
      } else {
        announcements = [];
      }
    } catch (error) {
      console.error('Error:', error);
      announcements = [];
    }
    loading = false;
  }
  
  function toggleRole(role) {
    if (role === 'all') {
      newAnnouncement.target_roles = ['all'];
    } else {
      newAnnouncement.target_roles = newAnnouncement.target_roles.filter(r => r !== 'all');
      if (newAnnouncement.target_roles.includes(role)) {
        newAnnouncement.target_roles = newAnnouncement.target_roles.filter(r => r !== role);
      } else {
        newAnnouncement.target_roles = [...newAnnouncement.target_roles, role];
      }
    }
  }
  
  async function sendAnnouncement() {
    if (!newAnnouncement.title || !newAnnouncement.content) {
      alert('Please fill in all fields');
      return;
    }
    
    if (newAnnouncement.target_roles.length === 0) {
      alert('Please select at least one recipient group');
      return;
    }
    
    const token = localStorage.getItem('token');
    try {
      const res = await fetch('http://localhost:8001/api/announcements', {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newAnnouncement)
      });
      
      if (res.ok) {
        showModal = false;
        newAnnouncement = { title: '', content: '', priority: 'normal', target_roles: [] };
        await loadAnnouncements();
      }
    } catch (error) {
      alert('Error sending announcement');
    }
  }
  
  async function deleteAnnouncement(id) {
    if (!confirm('Delete this announcement?')) return;
    
    const token = localStorage.getItem('token');
    await fetch(`http://localhost:8001/api/announcements/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    await loadAnnouncements();
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 p-6">
  <div class="max-w-5xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800">Announcements</h1>
        <p class="text-gray-600">Send messages to teachers, accountants, parents, or all users</p>
      </div>
      <div class="flex gap-3">
        <button on:click={openModal} type="button"
                class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-semibold cursor-pointer">
          + New Announcement
        </button>
        <button on:click={() => goto('/head-teacher')} class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg">
          Back
        </button>
      </div>
    </div>
    
    {#if loading}
      <div class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      </div>
    {:else}
      {#if announcements.length === 0}
        <div class="bg-white rounded-xl shadow-lg p-12 text-center">
          <div class="text-6xl mb-4">📢</div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">No Announcements Yet</h3>
          <p class="text-gray-600">Click "+ New Announcement" to send your first message</p>
        </div>
      {:else}
        <div class="space-y-4">
          {#each announcements as announcement}
          <div class="bg-white rounded-xl shadow-lg p-6">
            <div class="flex justify-between items-start mb-4">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <h3 class="text-xl font-bold text-gray-800">{announcement.title}</h3>
                  <span class="px-3 py-1 rounded text-xs font-semibold {announcement.priority === 'high' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'}">
                    {announcement.priority}
                  </span>
                </div>
                <p class="text-gray-600 mb-3">{announcement.content}</p>
                <div class="flex items-center gap-4 text-sm text-gray-500">
                  <span>📅 {new Date(announcement.created_at).toLocaleDateString()}</span>
                  {#if announcement.target_roles}
                    <span>👥 To: {announcement.target_roles.join(', ')}</span>
                  {/if}
                </div>
              </div>
              <button on:click={() => deleteAnnouncement(announcement.id)} 
                      class="text-red-600 hover:text-red-800 ml-4">
                Delete
              </button>
            </div>
          </div>
          {/each}
        </div>
      {/if}
    {/if}
  </div>
</div>

{#if showModal}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" on:click|self={() => showModal = false}>
    <div class="bg-white rounded-xl p-8 max-w-2xl w-full max-h-screen overflow-y-auto shadow-2xl">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Send New Announcement</h2>
        <button on:click={() => showModal = false} class="text-gray-400 hover:text-gray-600 text-3xl">&times;</button>
      </div>
      
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Title</label>
          <input bind:value={newAnnouncement.title} placeholder="Announcement title" 
                 class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Message</label>
          <textarea bind:value={newAnnouncement.content} placeholder="Announcement content" rows="4" 
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"></textarea>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Priority</label>
          <select bind:value={newAnnouncement.priority} class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
            <option value="normal">Normal</option>
            <option value="high">High Priority</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-3">Send To:</label>
          <div class="space-y-2">
            {#each roles as role}
              <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input type="checkbox" 
                       checked={newAnnouncement.target_roles.includes(role.value)}
                       on:change={() => toggleRole(role.value)}
                       class="w-5 h-5 text-blue-600 rounded" />
                <span class="ml-3 font-medium text-gray-700">{role.label}</span>
              </label>
            {/each}
          </div>
          {#if newAnnouncement.target_roles.length > 0}
            <p class="mt-2 text-sm text-gray-600">
              Selected: {newAnnouncement.target_roles.join(', ')}
            </p>
          {/if}
        </div>
        
        <div class="flex space-x-3 pt-4">
          <button on:click={sendAnnouncement} 
                  class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold">
            Send Announcement
          </button>
          <button on:click={() => { showModal = false; newAnnouncement = { title: '', content: '', priority: 'normal', target_roles: [] }; }} 
                  class="flex-1 bg-gray-300 hover:bg-gray-400 py-3 rounded-lg font-semibold">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}
