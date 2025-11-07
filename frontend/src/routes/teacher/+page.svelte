<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let dashboard = {
    assigned_classes: [],
    total_students: 0,
    today_attendance_rate: 0,
    this_week_attendance_rate: 0,
    students_with_low_attendance: [],
    quick_stats: {}
  };
  
  let loading = true;
  
  onMount(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      goto('/login');
      return;
    }
    
    try {
      const response = await fetch('http://localhost:8001/api/teacher/dashboard', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        dashboard = await response.json();
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loading = false;
    }
  });
  
  function logout() {
    localStorage.clear();
    goto('/login');
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800 mb-2">Teacher Dashboard</h1>
        <p class="text-gray-600">Attendance Management & Class Overview</p>
      </div>
      <button on:click={logout} class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg">
        Logout
      </button>
    </div>
    
    {#if loading}
      <div class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      </div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
          <p class="text-gray-500 text-sm">My Classes</p>
          <p class="text-3xl font-bold text-gray-800">{dashboard.quick_stats.classes || 0}</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
          <p class="text-gray-500 text-sm">Total Students</p>
          <p class="text-3xl font-bold text-gray-800">{dashboard.total_students}</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-yellow-500">
          <p class="text-gray-500 text-sm">Today's Attendance</p>
          <p class="text-3xl font-bold text-gray-800">{dashboard.today_attendance_rate}%</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-red-500">
          <p class="text-gray-500 text-sm">Low Attendance Alerts</p>
          <p class="text-3xl font-bold text-gray-800">{dashboard.quick_stats.alerts || 0}</p>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">My Classes</h2>
          <div class="space-y-3">
            {#each dashboard.assigned_classes as class_}
              <div class="p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition cursor-pointer">
                <div class="flex justify-between items-center">
                  <div>
                    <h3 class="font-bold text-gray-800">{class_.name}</h3>
                    <p class="text-sm text-gray-600">{class_.student_count} students • Room {class_.room}</p>
                  </div>
                  <button on:click={() => goto('/teacher/attendance')} class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm">
                    Mark Attendance
                  </button>
                </div>
              </div>
            {/each}
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Low Attendance Alerts</h2>
          <div class="space-y-3">
            {#each dashboard.students_with_low_attendance as student}
              <div class="p-3 bg-red-50 rounded-lg">
                <p class="font-semibold text-gray-800">{student.name}</p>
                <p class="text-sm text-gray-600">{student.class} • {student.rate}% attendance</p>
              </div>
            {/each}
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <button on:click={() => goto('/teacher/attendance')} 
                class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all hover:scale-105">
          <div class="text-4xl mb-3">✅</div>
          <h3 class="font-bold text-gray-800 text-lg mb-2">Mark Attendance</h3>
          <p class="text-sm text-gray-600">Daily roll call for your classes</p>
        </button>
        
        <button on:click={() => goto('/teacher/reports')} 
                class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all hover:scale-105">
          <div class="text-4xl mb-3">📊</div>
          <h3 class="font-bold text-gray-800 text-lg mb-2">View Reports</h3>
          <p class="text-sm text-gray-600">Attendance summaries and analytics</p>
        </button>
        
        <button on:click={() => goto('/teacher/roster')} 
                class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all hover:scale-105">
          <div class="text-4xl mb-3">👥</div>
          <h3 class="font-bold text-gray-800 text-lg mb-2">Student Roster</h3>
          <p class="text-sm text-gray-600">View all students in your classes</p>
        </button>
      </div>
    {/if}
  </div>
</div>
