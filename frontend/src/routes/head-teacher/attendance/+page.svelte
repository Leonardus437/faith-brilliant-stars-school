<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let attendanceData = [];
  let students = [];
  let classes = [];
  let selectedClass = 'all';
  let selectedDate = new Date().toISOString().split('T')[0];
  let stats = { total: 0, present: 0, absent: 0, late: 0, rate: 0 };
  let loading = true;
  
  onMount(async () => {
    await loadData();
  });
  
  async function loadData() {
    const token = localStorage.getItem('token');
    
    const [attendanceRes, studentsRes, classesRes] = await Promise.all([
      fetch('http://localhost:8001/api/attendance', { headers: { 'Authorization': `Bearer ${token}` }}),
      fetch('http://localhost:8001/api/students', { headers: { 'Authorization': `Bearer ${token}` }}),
      fetch('http://localhost:8001/api/classes', { headers: { 'Authorization': `Bearer ${token}` }})
    ]);
    
    if (attendanceRes.ok) attendanceData = await attendanceRes.json();
    if (studentsRes.ok) students = await studentsRes.json();
    if (classesRes.ok) classes = await classesRes.json();
    
    calculateStats();
    loading = false;
  }
  
  function calculateStats() {
    let filtered = attendanceData;
    
    if (selectedClass !== 'all') {
      filtered = filtered.filter(a => a.class_id == selectedClass);
    }
    
    if (selectedDate) {
      filtered = filtered.filter(a => a.date.startsWith(selectedDate));
    }
    
    stats.total = filtered.length;
    stats.present = filtered.filter(a => a.status === 'present').length;
    stats.absent = filtered.filter(a => a.status === 'absent').length;
    stats.late = filtered.filter(a => a.status === 'late').length;
    stats.rate = stats.total ? ((stats.present / stats.total) * 100).toFixed(1) : 0;
  }
  
  function getStudentName(studentId) {
    const student = students.find(s => s.id === studentId);
    return student ? `${student.first_name} ${student.last_name}` : `Student #${studentId}`;
  }
  
  function getClassName(classId) {
    const cls = classes.find(c => c.id === classId);
    return cls ? cls.name : `Class #${classId}`;
  }
  
  $: {
    selectedClass;
    selectedDate;
    calculateStats();
  }
  
  $: filteredAttendance = attendanceData.filter(a => {
    let match = true;
    if (selectedClass !== 'all') match = match && a.class_id == selectedClass;
    if (selectedDate) match = match && a.date.startsWith(selectedDate);
    return match;
  });
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800">Attendance Reports</h1>
        <p class="text-gray-600">Track student attendance across all classes</p>
      </div>
      <button on:click={() => goto('/head-teacher')} class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg">
        Back to Dashboard
      </button>
    </div>
    
    {#if loading}
      <div class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      </div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
          <p class="text-gray-500 text-sm">Total Records</p>
          <p class="text-3xl font-bold text-gray-800">{stats.total}</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
          <p class="text-gray-500 text-sm">Present</p>
          <p class="text-3xl font-bold text-green-600">{stats.present}</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-red-500">
          <p class="text-gray-500 text-sm">Absent</p>
          <p class="text-3xl font-bold text-red-600">{stats.absent}</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-yellow-500">
          <p class="text-gray-500 text-sm">Attendance Rate</p>
          <p class="text-3xl font-bold text-blue-600">{stats.rate}%</p>
          <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
            <div class="bg-blue-600 h-2 rounded-full" style="width: {stats.rate}%"></div>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Filters</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Select Class</label>
            <select bind:value={selectedClass} class="w-full px-4 py-2 border rounded-lg">
              <option value="all">All Classes</option>
              {#each classes as cls}
                <option value={cls.id}>{cls.name}</option>
              {/each}
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Select Date</label>
            <input type="date" bind:value={selectedDate} class="w-full px-4 py-2 border rounded-lg" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <div class="px-6 py-4 bg-gray-50 border-b">
          <h2 class="text-xl font-bold text-gray-800">Attendance Records ({filteredAttendance.length})</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Class</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Recorded At</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              {#each filteredAttendance.slice(0, 100) as record}
                <tr class="hover:bg-gray-50">
                  <td class="px-6 py-4">{new Date(record.date).toLocaleDateString()}</td>
                  <td class="px-6 py-4">{getStudentName(record.student_id)}</td>
                  <td class="px-6 py-4">{getClassName(record.class_id)}</td>
                  <td class="px-6 py-4">
                    <span class="px-3 py-1 rounded-full text-xs font-semibold {
                      record.status === 'present' ? 'bg-green-100 text-green-800' :
                      record.status === 'absent' ? 'bg-red-100 text-red-800' :
                      record.status === 'late' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }">
                      {record.status}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-600">{new Date(record.recorded_at).toLocaleString()}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    {/if}
  </div>
</div>
