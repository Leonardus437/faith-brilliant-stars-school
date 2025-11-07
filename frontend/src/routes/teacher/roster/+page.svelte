<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let classes = [];
  let selectedClass = null;
  let roster = null;
  let loadingClasses = true;
  let loadingRoster = false;
  
  onMount(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      goto('/login');
      return;
    }
    await loadClasses();
  });
  
  async function loadClasses() {
    loadingClasses = true;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8001/api/attendance/classes', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) classes = await response.json();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loadingClasses = false;
    }
  }
  
  async function selectClass(classId) {
    if (!classId) return;
    selectedClass = parseInt(classId);
    loadingRoster = true;
    roster = null;
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8001/api/teacher/classes/${selectedClass}/roster`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) roster = await response.json();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loadingRoster = false;
    }
  }
  
  function getStatusBadge(status) {
    const badges = {
      present: '✓',
      absent: '✗',
      late: '⏰',
      sick: '🏥'
    };
    return badges[status] || '?';
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800 mb-2">Class Roster</h1>
        <p class="text-gray-600">View all students in your classes</p>
      </div>
      <button on:click={() => goto('/teacher')} class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg">Back to Dashboard</button>
    </div>
    
    <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Select Class</label>
      {#if loadingClasses}
        <div class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500">Loading classes...</div>
      {:else if classes.length === 0}
        <div class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-yellow-50 text-yellow-700">No classes assigned</div>
      {:else}
        <select on:change={(e) => selectClass(e.target.value)} class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
          <option value="">Choose a class...</option>
          {#each classes as class_}
            <option value={class_.id}>{class_.name} ({class_.student_count} students)</option>
          {/each}
        </select>
      {/if}
    </div>
    
    {#if loadingRoster}
      <div class="text-center py-12"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div></div>
    {:else if roster}
      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">{roster.class_name} - Grade {roster.grade}</h2>
        <p class="text-gray-600">Total Students: {roster.total_students}</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each roster.students as student}
          <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
            <div class="flex items-start gap-4">
              <div class="w-16 h-16 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                {student.name.split(' ').map(n => n[0]).join('')}
              </div>
              <div class="flex-1">
                <h3 class="font-bold text-gray-800 text-lg">{student.name}</h3>
                <p class="text-sm text-gray-600">#{student.admission_number}</p>
                <p class="text-sm text-gray-600">{student.gender}</p>
                
                <div class="mt-3">
                  <p class="text-xs text-gray-500 mb-1">Recent Attendance:</p>
                  <div class="flex gap-1">
                    {#each student.recent_attendance as status}
                      <span class="text-lg" title={status}>{getStatusBadge(status)}</span>
                    {/each}
                  </div>
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>
