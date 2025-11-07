<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let classes = [];
  let selectedClass = null;
  let students = [];
  let attendanceDate = new Date().toISOString().split('T')[0];
  let attendanceRecords = {};
  let loadingClasses = true;
  let loadingStudents = false;
  let saving = false;
  
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
      if (response.ok) {
        classes = await response.json();
        console.log('Classes loaded:', classes);
      } else {
        console.error('Failed to load classes:', response.status);
      }
    } catch (error) {
      console.error('Error loading classes:', error);
    } finally {
      loadingClasses = false;
    }
  }
  
  async function selectClass(classId) {
    if (!classId) return;
    selectedClass = parseInt(classId);
    loadingStudents = true;
    students = [];
    attendanceRecords = {};
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8001/api/attendance/students/${selectedClass}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        students = await response.json();
        console.log('Students loaded:', students.length);
        students.forEach(s => attendanceRecords[s.id] = 'present');
        await loadExistingAttendance();
      } else {
        console.error('Failed to load students:', response.status);
      }
    } catch (error) {
      console.error('Error loading students:', error);
    } finally {
      loadingStudents = false;
    }
  }
  
  async function loadExistingAttendance() {
    if (!selectedClass) return;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8001/api/attendance/view/${selectedClass}/${attendanceDate}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const existing = await response.json();
        console.log('Existing attendance loaded:', existing.length);
        existing.forEach(record => attendanceRecords[record.student_id] = record.status);
        attendanceRecords = {...attendanceRecords};
      }
    } catch (error) {
      console.error('Error loading existing attendance:', error);
    }
  }
  
  function markAllPresent() {
    students.forEach(s => attendanceRecords[s.id] = 'present');
    attendanceRecords = {...attendanceRecords};
  }
  
  async function submitAttendance() {
    saving = true;
    try {
      const token = localStorage.getItem('token');
      const records = students.map(s => ({ student_id: s.id, status: attendanceRecords[s.id] }));
      const response = await fetch('http://localhost:8001/api/attendance/submit', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ class_id: selectedClass, date: attendanceDate, records })
      });
      if (response.ok) {
        alert('Attendance saved successfully!');
      } else {
        const error = await response.json();
        alert('Failed to save: ' + (error.detail || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error saving attendance:', error);
      alert('Failed to save attendance');
    } finally {
      saving = false;
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800 mb-2">Mark Attendance</h1>
        <p class="text-gray-600">Daily roll call for your classes</p>
      </div>
      <button on:click={() => goto('/teacher')} class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg">Back to Dashboard</button>
    </div>
    
    <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
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
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Date</label>
          <input type="date" bind:value={attendanceDate} on:change={loadExistingAttendance} class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
        </div>
      </div>
      {#if selectedClass}
        <div class="flex gap-4">
          <button on:click={markAllPresent} class="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg">✓ Mark All Present</button>
          <button on:click={submitAttendance} disabled={saving} class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg disabled:opacity-50">{saving ? 'Saving...' : '💾 Save Attendance'}</button>
        </div>
      {/if}
    </div>
    
    {#if loadingStudents}
      <div class="text-center py-12"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div></div>
    {:else if selectedClass && students.length > 0}
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Admission #</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student Name</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Present</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Absent</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Late</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Sick</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            {#each students as student}
              <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 text-sm text-gray-900">{student.admission_number}</td>
                <td class="px-6 py-4 text-sm font-medium text-gray-900">{student.full_name}</td>
                <td class="px-6 py-4 text-center"><input type="radio" name="attendance-{student.id}" value="present" bind:group={attendanceRecords[student.id]} class="w-5 h-5 text-green-600" /></td>
                <td class="px-6 py-4 text-center"><input type="radio" name="attendance-{student.id}" value="absent" bind:group={attendanceRecords[student.id]} class="w-5 h-5 text-red-600" /></td>
                <td class="px-6 py-4 text-center"><input type="radio" name="attendance-{student.id}" value="late" bind:group={attendanceRecords[student.id]} class="w-5 h-5 text-yellow-600" /></td>
                <td class="px-6 py-4 text-center"><input type="radio" name="attendance-{student.id}" value="sick" bind:group={attendanceRecords[student.id]} class="w-5 h-5 text-blue-600" /></td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>
