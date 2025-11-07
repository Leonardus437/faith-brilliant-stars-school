<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let classes = [];
  let selectedClass = null;
  let selectedMonth = new Date().toISOString().slice(0, 7);
  let report = null;
  let loadingClasses = true;
  let loadingReport = false;
  
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
  
  async function loadReport() {
    if (!selectedClass) return;
    loadingReport = true;
    report = null;
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8001/api/teacher/reports/attendance-summary?class_id=${selectedClass}&month=${selectedMonth}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) report = await response.json();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loadingReport = false;
    }
  }
  
  function exportToCSV() {
    if (!report) return;
    const csv = [
      ['Student Name', 'Total Days', 'Present', 'Absent', 'Late', 'Attendance Rate'],
      ...report.summary.map(s => [s.name, s.total, s.present, s.absent, s.late, `${s.rate}%`])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `attendance-report-${selectedMonth}.csv`;
    a.click();
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800 mb-2">Attendance Reports</h1>
        <p class="text-gray-600">Monthly attendance summaries and analytics</p>
      </div>
      <button on:click={() => goto('/teacher')} class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg">Back to Dashboard</button>
    </div>
    
    <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Select Class</label>
          {#if loadingClasses}
            <div class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500">Loading classes...</div>
          {:else if classes.length === 0}
            <div class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-yellow-50 text-yellow-700">No classes assigned</div>
          {:else}
            <select bind:value={selectedClass} on:change={loadReport} class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="">Choose a class...</option>
              {#each classes as class_}
                <option value={class_.id}>{class_.name}</option>
              {/each}
            </select>
          {/if}
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Select Month</label>
          <input type="month" bind:value={selectedMonth} on:change={loadReport} class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
        </div>
        <div class="flex items-end">
          <button on:click={exportToCSV} disabled={!report} class="w-full bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg disabled:opacity-50">📥 Export CSV</button>
        </div>
      </div>
    </div>
    
    {#if loadingReport}
      <div class="text-center py-12"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div></div>
    {:else if report}
      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Report for {report.month}</h2>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-blue-50 rounded-lg p-4">
            <p class="text-sm text-gray-600">Total Students</p>
            <p class="text-3xl font-bold text-blue-600">{report.summary.length}</p>
          </div>
          <div class="bg-green-50 rounded-lg p-4">
            <p class="text-sm text-gray-600">Avg Attendance</p>
            <p class="text-3xl font-bold text-green-600">{Math.round(report.summary.reduce((sum, s) => sum + s.rate, 0) / report.summary.length)}%</p>
          </div>
          <div class="bg-yellow-50 rounded-lg p-4">
            <p class="text-sm text-gray-600">Below 75%</p>
            <p class="text-3xl font-bold text-yellow-600">{report.summary.filter(s => s.rate < 75).length}</p>
          </div>
          <div class="bg-red-50 rounded-lg p-4">
            <p class="text-sm text-gray-600">Below 50%</p>
            <p class="text-3xl font-bold text-red-600">{report.summary.filter(s => s.rate < 50).length}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student Name</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Total Days</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Present</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Absent</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Late</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Rate</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            {#each report.summary as student}
              <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 text-sm font-medium text-gray-900">{student.name}</td>
                <td class="px-6 py-4 text-sm text-center text-gray-900">{student.total}</td>
                <td class="px-6 py-4 text-sm text-center text-green-600">{student.present}</td>
                <td class="px-6 py-4 text-sm text-center text-red-600">{student.absent}</td>
                <td class="px-6 py-4 text-sm text-center text-yellow-600">{student.late}</td>
                <td class="px-6 py-4 text-sm text-center">
                  <span class="px-3 py-1 rounded-full text-white {student.rate >= 90 ? 'bg-green-500' : student.rate >= 75 ? 'bg-yellow-500' : 'bg-red-500'}">
                    {student.rate}%
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
