<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  
  let students = [];
  let className = '';
  let loading = true;
  
  onMount(async () => {
    const classId = $page.params.id;
    const token = localStorage.getItem('token');
    
    try {
      const [studentsRes, classRes] = await Promise.all([
        fetch(`http://localhost:8001/api/students/?class_id=${classId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`http://localhost:8001/api/classes/${classId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);
      
      if (studentsRes.ok) {
        const data = await studentsRes.json();
        students = data.filter(s => s.class_id == classId);
      }
      if (classRes.ok) {
        const classData = await classRes.json();
        className = classData.name;
      }
    } catch (error) {
      console.error('Error loading data:', error);
    }
    loading = false;
  });
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800">Students in {className}</h1>
        <p class="text-gray-600">View all students enrolled in this class</p>
      </div>
      <button on:click={() => goto('/classes')} class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg">
        Back to Classes
      </button>
    </div>
    
    {#if loading}
      <div class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      </div>
    {:else}
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Admission #</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gender</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date of Birth</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            {#each students as student}
              <tr class="hover:bg-gray-50">
                <td class="px-6 py-4">{student.admission_number}</td>
                <td class="px-6 py-4">{student.first_name} {student.last_name}</td>
                <td class="px-6 py-4">{student.gender}</td>
                <td class="px-6 py-4">{new Date(student.date_of_birth).toLocaleDateString()}</td>
                <td class="px-6 py-4">
                  <span class="px-2 py-1 rounded text-xs bg-green-100 text-green-800">
                    {student.enrollment_status}
                  </span>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>
