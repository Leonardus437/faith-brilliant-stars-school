<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let classes = [];
  let teachers = [];
  let loading = true;
  let showAddModal = false;
  let showEditModal = false;
  let editingClass = null;
  
  let newClass = {
    name: '',
    grade_level: 'P1',
    academic_year: '2024',
    class_teacher_id: null,
    capacity: 40,
    room_number: ''
  };
  
  onMount(async () => {
    await loadData();
  });
  
  async function loadData() {
    const token = localStorage.getItem('token');
    if (!token) {
      goto('/login');
      return;
    }
    
    try {
      const [classesRes, teachersRes] = await Promise.all([
        fetch('http://localhost:8001/api/classes/', { headers: { 'Authorization': `Bearer ${token}` }}),
        fetch('http://localhost:8001/api/head-teacher/teachers', { headers: { 'Authorization': `Bearer ${token}` }})
      ]);
      
      if (classesRes.ok) classes = await classesRes.json();
      if (teachersRes.ok) teachers = await teachersRes.json();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loading = false;
    }
  }
  
  async function addClass() {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch('http://localhost:8001/api/head-teacher/classes', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newClass)
      });
      
      if (response.ok) {
        showAddModal = false;
        await loadData();
        resetForm();
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  
  function resetForm() {
    newClass = {
      name: '',
      grade_level: 'P1',
      academic_year: '2024',
      class_teacher_id: null,
      capacity: 40,
      room_number: ''
    };
  }
  
  function editClass(class_) {
    editingClass = { ...class_ };
    showEditModal = true;
  }
  
  async function updateClass() {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`http://localhost:8001/api/classes/${editingClass.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editingClass)
      });
      
      if (response.ok) {
        showEditModal = false;
        await loadData();
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
</script>

<div class="min-h-screen bg-gray-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-3xl font-bold text-gray-800">Class Management</h1>
        <p class="text-gray-600">Manage all classes in the school</p>
      </div>
      <div class="flex gap-3">
        <button on:click={() => goto('/head-teacher')} class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg">
          Back to Dashboard
        </button>
        <button on:click={() => showAddModal = true} class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg">
          + Add Class
        </button>
      </div>
    </div>
    
    {#if loading}
      <div class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      </div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        {#each classes as class_}
          <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="text-2xl font-bold text-gray-800">{class_.name}</h3>
                <p class="text-gray-600">{class_.grade_level} • {class_.academic_year}</p>
              </div>
              <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                Room {class_.room_number || 'N/A'}
              </span>
            </div>
            
            <div class="space-y-2 mb-4">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Capacity:</span>
                <span class="font-semibold">{class_.capacity} students</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Class Teacher:</span>
                <span class="font-semibold">{class_.teacher_name || 'Not assigned'}</span>
              </div>
            </div>
            
            <div class="flex gap-2">
              <button on:click={() => goto(`/classes/${class_.id}/students`)} 
                      class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm">
                View Students
              </button>
              <button on:click={() => editClass(class_)} 
                      class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 py-2 rounded-lg text-sm">
                Edit
              </button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

{#if showEditModal && editingClass}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-xl p-6 max-w-lg w-full">
      <h2 class="text-2xl font-bold mb-4">Edit Class</h2>
      <form on:submit|preventDefault={updateClass} class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Class Name</label>
          <input type="text" bind:value={editingClass.name} required 
                 class="w-full px-3 py-2 border border-gray-300 rounded-lg" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Capacity</label>
            <input type="number" bind:value={editingClass.capacity} required 
                   class="w-full px-3 py-2 border border-gray-300 rounded-lg" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Room Number</label>
            <input type="text" bind:value={editingClass.room_number} 
                   class="w-full px-3 py-2 border border-gray-300 rounded-lg" />
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" on:click={() => showEditModal = false} 
                  class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</button>
          <button type="submit" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">Update</button>
        </div>
      </form>
    </div>
  </div>
{/if}

{#if showAddModal}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-xl p-6 max-w-lg w-full">
      <h2 class="text-2xl font-bold mb-4">Add New Class</h2>
      
      <form on:submit|preventDefault={addClass} class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Class Name</label>
          <input type="text" bind:value={newClass.name} required placeholder="e.g., P1 A"
                 class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Grade Level</label>
            <select bind:value={newClass.grade_level} required 
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="P1">Primary 1</option>
              <option value="P2">Primary 2</option>
              <option value="P3">Primary 3</option>
              <option value="P4">Primary 4</option>
              <option value="P5">Primary 5</option>
              <option value="P6">Primary 6</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Academic Year</label>
            <input type="text" bind:value={newClass.academic_year} required 
                   class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Capacity</label>
            <input type="number" bind:value={newClass.capacity} required 
                   class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Room Number</label>
            <input type="text" bind:value={newClass.room_number} 
                   class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Class Teacher (Optional)</label>
          <select bind:value={newClass.class_teacher_id} 
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
            <option value={null}>No teacher assigned</option>
            {#each teachers as teacher}
              <option value={teacher.id}>{teacher.name}</option>
            {/each}
          </select>
        </div>
        
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" on:click={() => { showAddModal = false; resetForm(); }} 
                  class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancel
          </button>
          <button type="submit" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">
            Add Class
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
