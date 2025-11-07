<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let payments = [];
  let invoices = [];
  let loading = false;
  let showModal = false;
  let newPayment = { invoice_id: '', amount: '', payment_method: 'cash', transaction_ref: '' };
  
  onMount(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      goto('/login');
      return;
    }
    await loadPayments();
    await loadInvoices();
  });
  
  async function loadPayments() {
    loading = true;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8001/api/fees/payments', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) payments = await response.json();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loading = false;
    }
  }
  
  async function loadInvoices() {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8001/api/fees/invoices', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) invoices = await response.json();
    } catch (error) {
      console.error('Error:', error);
    }
  }
  
  async function recordPayment() {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8001/api/fees/payments', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(newPayment)
      });
      if (response.ok) {
        showModal = false;
        newPayment = { invoice_id: '', amount: '', payment_method: 'cash', transaction_ref: '' };
        await loadPayments();
        await loadInvoices();
        alert('Payment recorded successfully!');
      }
    } catch (error) {
      alert('Failed to record payment');
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800 mb-2">Record Payments</h1>
        <p class="text-gray-600">Process and track student fee payments</p>
      </div>
      <div class="flex gap-4">
        <button on:click={() => showModal = true} class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg">+ Record Payment</button>
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
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Receipt #</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Method</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ref</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            {#each payments as payment}
              <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 text-sm font-medium text-gray-900">#{payment.id}</td>
                <td class="px-6 py-4 text-sm text-gray-900">#{payment.invoice_id}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{payment.student_name}</td>
                <td class="px-6 py-4 text-sm text-green-600 font-semibold">{payment.amount?.toLocaleString() || 0} RWF</td>
                <td class="px-6 py-4 text-sm text-gray-900">{payment.payment_method}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{new Date(payment.payment_date).toLocaleDateString()}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{payment.transaction_reference || '-'}</td>
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
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Record Payment</h2>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Invoice</label>
          <select bind:value={newPayment.invoice_id} class="w-full px-4 py-2 border border-gray-300 rounded-lg">
            <option value="">Select invoice...</option>
            {#each invoices.filter(i => i.status !== 'paid') as invoice}
              <option value={invoice.id}>#{invoice.id} - {invoice.student_name} - {((invoice.total_amount || 0) - (invoice.amount_paid || 0)).toLocaleString()} RWF due</option>
            {/each}
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Amount (RWF)</label>
          <input type="number" bind:value={newPayment.amount} class="w-full px-4 py-2 border border-gray-300 rounded-lg" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Payment Method</label>
          <select bind:value={newPayment.payment_method} class="w-full px-4 py-2 border border-gray-300 rounded-lg">
            <option value="cash">Cash</option>
            <option value="bank_transfer">Bank Transfer</option>
            <option value="mobile_money">Mobile Money</option>
            <option value="cheque">Cheque</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Transaction Reference</label>
          <input type="text" bind:value={newPayment.transaction_ref} placeholder="Optional" class="w-full px-4 py-2 border border-gray-300 rounded-lg" />
        </div>
      </div>
      <div class="flex gap-4 mt-6">
        <button on:click={recordPayment} class="flex-1 bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg">Record</button>
        <button on:click={() => showModal = false} class="flex-1 bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg">Cancel</button>
      </div>
    </div>
  </div>
{/if}
