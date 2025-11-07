<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let invoices = [];
  let students = [];
  let loading = false;
  let showModal = false;
  let newInvoice = { student_id: '', amount: '', due_date: '', description: 'School Fees' };
  
  onMount(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      goto('/login');
      return;
    }
    await loadInvoices();
    await loadStudents();
  });
  
  async function loadInvoices() {
    loading = true;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8001/api/fees/invoices', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) invoices = await response.json();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loading = false;
    }
  }
  
  async function loadStudents() {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8001/api/admin/students', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) students = await response.json();
    } catch (error) {
      console.error('Error:', error);
    }
  }
  
  async function createInvoice() {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8001/api/fees/invoices', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(newInvoice)
      });
      if (response.ok) {
        showModal = false;
        newInvoice = { student_id: '', amount: '', due_date: '', description: 'School Fees' };
        await loadInvoices();
        alert('Invoice created successfully!');
      }
    } catch (error) {
      alert('Failed to create invoice');
    }
  }
  
  function getStatusColor(status) {
    return status === 'paid' ? 'bg-green-100 text-green-800' : 
           status === 'partial' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800';
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800 mb-2">Manage Invoices</h1>
        <p class="text-gray-600">Create and track student fee invoices</p>
      </div>
      <div class="flex gap-4">
        <button on:click={() => showModal = true} class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg">+ New Invoice</button>
        <button on:click={() => goto('/accountant')} class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg">Back</button>
      </div>
    </div>
    
    {#if loading}
      <div class="text-center py-12"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div></div>
    {:else}
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Paid</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Balance</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            {#each invoices as invoice}
              <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 text-sm text-gray-900">#{invoice.id}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{invoice.student_name}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{invoice.total_amount?.toLocaleString() || 0} RWF</td>
                <td class="px-6 py-4 text-sm text-green-600">{invoice.amount_paid?.toLocaleString() || 0} RWF</td>
                <td class="px-6 py-4 text-sm text-red-600">{((invoice.total_amount || 0) - (invoice.amount_paid || 0)).toLocaleString()} RWF</td>
                <td class="px-6 py-4 text-sm text-gray-900">{new Date(invoice.due_date).toLocaleDateString()}</td>
                <td class="px-6 py-4"><span class="px-3 py-1 rounded-full text-xs {getStatusColor(invoice.status)}">{invoice.status}</span></td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>

{#if showModal}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-8 max-w-md w-full">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Create New Invoice</h2>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Student</label>
          <select bind:value={newInvoice.student_id} class="w-full px-4 py-2 border border-gray-300 rounded-lg">
            <option value="">Select student...</option>
            {#each students as student}
              <option value={student.id}>{student.first_name} {student.last_name} - {student.admission_number}</option>
            {/each}
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Amount (RWF)</label>
          <input type="number" bind:value={newInvoice.amount} class="w-full px-4 py-2 border border-gray-300 rounded-lg" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Due Date</label>
          <input type="date" bind:value={newInvoice.due_date} class="w-full px-4 py-2 border border-gray-300 rounded-lg" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
          <input type="text" bind:value={newInvoice.description} class="w-full px-4 py-2 border border-gray-300 rounded-lg" />
        </div>
      </div>
      <div class="flex gap-4 mt-6">
        <button on:click={createInvoice} class="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg">Create</button>
        <button on:click={() => showModal = false} class="flex-1 bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg">Cancel</button>
      </div>
    </div>
  </div>
{/if}
