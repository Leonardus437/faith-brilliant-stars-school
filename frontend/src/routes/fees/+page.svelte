<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  
  let invoices = [];
  let students = [];
  let loading = true;
  let showInvoiceModal = false;
  let showPaymentModal = false;
  let currentInvoice = {
    student_id: '',
    category: 'tuition',
    amount: '',
    term: 'term_1',
    due_date: ''
  };
  let currentPayment = {
    invoice_id: '',
    amount: '',
    method: 'cash',
    reference: ''
  };
  
  onMount(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }
    
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    await loadData();
  });
  
  async function loadData() {
    try {
      const [invoicesRes, studentsRes] = await Promise.all([
        axios.get('/api/fees/invoices'),
        axios.get('/api/students/')
      ]);
      invoices = invoicesRes.data;
      students = studentsRes.data;
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      loading = false;
    }
  }
  
  function openInvoiceModal() {
    currentInvoice = {
      student_id: students[0]?.id || '',
      category: 'tuition',
      amount: '',
      term: 'term_1',
      due_date: new Date().toISOString().split('T')[0]
    };
    showInvoiceModal = true;
  }
  
  function openPaymentModal(invoice) {
    currentPayment = {
      invoice_id: invoice.id,
      amount: invoice.amount - invoice.amount_paid,
      method: 'cash',
      reference: ''
    };
    showPaymentModal = true;
  }
  
  async function createInvoice() {
    try {
      await axios.post('/api/fees/invoices', currentInvoice);
      showInvoiceModal = false;
      await loadData();
    } catch (error) {
      alert('Error creating invoice: ' + (error.response?.data?.detail || error.message));
    }
  }
  
  async function recordPayment() {
    try {
      await axios.post('/api/fees/payments', currentPayment);
      showPaymentModal = false;
      await loadData();
    } catch (error) {
      alert('Error recording payment: ' + (error.response?.data?.detail || error.message));
    }
  }
  
  async function deleteInvoice(id) {
    if (!confirm('Are you sure you want to delete this invoice?')) return;
    
    try {
      await axios.delete(`/api/fees/invoices/${id}`);
      await loadData();
    } catch (error) {
      alert('Error deleting invoice: ' + (error.response?.data?.detail || error.message));
    }
  }
  
  function formatCurrency(amount) {
    return new Intl.NumberFormat('en-RW', {
      style: 'currency',
      currency: 'RWF',
      minimumFractionDigits: 0
    }).format(amount);
  }
  
  function getStatusColor(status) {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      partial: 'bg-blue-100 text-blue-800',
      paid: 'bg-green-100 text-green-800',
      overdue: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  }
  
  $: totalInvoiced = invoices.reduce((sum, inv) => sum + inv.amount, 0);
  $: totalCollected = invoices.reduce((sum, inv) => sum + inv.amount_paid, 0);
  $: totalPending = totalInvoiced - totalCollected;
  $: collectionRate = totalInvoiced > 0 ? (totalCollected / totalInvoiced * 100).toFixed(2) : 0;
</script>

<svelte:head>
  <title>Fees & Payments - Faith Brilliant Stars School</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold">Fees & Payments</h1>
    <button on:click={openInvoiceModal} class="btn btn-primary">+ Create Invoice</button>
  </div>
  
  <!-- Summary Cards -->
  <div class="grid md:grid-cols-4 gap-4 mb-6">
    <div class="card bg-blue-50">
      <p class="text-sm text-gray-600">Total Invoiced</p>
      <p class="text-2xl font-bold text-blue-600">{formatCurrency(totalInvoiced)}</p>
    </div>
    <div class="card bg-green-50">
      <p class="text-sm text-gray-600">Collected</p>
      <p class="text-2xl font-bold text-green-600">{formatCurrency(totalCollected)}</p>
    </div>
    <div class="card bg-yellow-50">
      <p class="text-sm text-gray-600">Pending</p>
      <p class="text-2xl font-bold text-yellow-600">{formatCurrency(totalPending)}</p>
    </div>
    <div class="card bg-purple-50">
      <p class="text-sm text-gray-600">Collection Rate</p>
      <p class="text-2xl font-bold text-purple-600">{collectionRate}%</p>
    </div>
  </div>
  
  {#if loading}
    <div class="text-center py-12">
      <p class="text-gray-600">Loading invoices...</p>
    </div>
  {:else if invoices.length === 0}
    <div class="card text-center py-12">
      <p class="text-gray-600">No invoices found</p>
    </div>
  {:else}
    <div class="card overflow-x-auto">
      <table class="w-full">
        <thead>
          <tr class="border-b">
            <th class="text-left py-3 px-4">Invoice #</th>
            <th class="text-left py-3 px-4">Student</th>
            <th class="text-left py-3 px-4">Category</th>
            <th class="text-left py-3 px-4">Amount</th>
            <th class="text-left py-3 px-4">Paid</th>
            <th class="text-left py-3 px-4">Balance</th>
            <th class="text-left py-3 px-4">Status</th>
            <th class="text-left py-3 px-4">Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each invoices as invoice}
            <tr class="border-b hover:bg-gray-50">
              <td class="py-3 px-4 font-mono text-sm">{invoice.invoice_number}</td>
              <td class="py-3 px-4">{students.find(s => s.id === invoice.student_id)?.first_name || 'N/A'}</td>
              <td class="py-3 px-4 capitalize">{invoice.category}</td>
              <td class="py-3 px-4">{formatCurrency(invoice.amount)}</td>
              <td class="py-3 px-4">{formatCurrency(invoice.amount_paid)}</td>
              <td class="py-3 px-4">{formatCurrency(invoice.amount - invoice.amount_paid)}</td>
              <td class="py-3 px-4">
                <span class="px-2 py-1 text-xs rounded-full {getStatusColor(invoice.status)}">
                  {invoice.status}
                </span>
              </td>
              <td class="py-3 px-4">
                {#if invoice.status !== 'paid'}
                  <button on:click={() => openPaymentModal(invoice)} class="text-green-600 hover:text-green-800 text-sm mr-2">Pay</button>
                {/if}
                <button on:click={() => deleteInvoice(invoice.id)} class="text-red-600 hover:text-red-800 text-sm">Delete</button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<!-- Invoice Modal -->
{#if showInvoiceModal}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
      <h2 class="text-2xl font-bold mb-4">Create Invoice</h2>
      
      <div class="space-y-4">
        <div>
          <label class="label">Student</label>
          <select bind:value={currentInvoice.student_id} class="input">
            {#each students as student}
              <option value={student.id}>{student.first_name} {student.last_name} ({student.admission_number})</option>
            {/each}
          </select>
        </div>
        
        <div>
          <label class="label">Category</label>
          <select bind:value={currentInvoice.category} class="input">
            <option value="tuition">Tuition</option>
            <option value="lunch">Lunch</option>
            <option value="transport">Transport</option>
            <option value="uniform">Uniform</option>
            <option value="other">Other</option>
          </select>
        </div>
        
        <div>
          <label class="label">Term</label>
          <select bind:value={currentInvoice.term} class="input">
            <option value="term_1">Term 1</option>
            <option value="term_2">Term 2</option>
            <option value="term_3">Term 3</option>
          </select>
        </div>
        
        <div>
          <label class="label">Amount (RWF)</label>
          <input type="number" bind:value={currentInvoice.amount} class="input" required />
        </div>
        
        <div>
          <label class="label">Due Date</label>
          <input type="date" bind:value={currentInvoice.due_date} class="input" required />
        </div>
      </div>
      
      <div class="flex justify-end space-x-2 mt-6">
        <button on:click={() => showInvoiceModal = false} class="btn btn-secondary">Cancel</button>
        <button on:click={createInvoice} class="btn btn-primary">Create</button>
      </div>
    </div>
  </div>
{/if}

<!-- Payment Modal -->
{#if showPaymentModal}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
      <h2 class="text-2xl font-bold mb-4">Record Payment</h2>
      
      <div class="space-y-4">
        <div>
          <label class="label">Amount (RWF)</label>
          <input type="number" bind:value={currentPayment.amount} class="input" required />
        </div>
        
        <div>
          <label class="label">Payment Method</label>
          <select bind:value={currentPayment.method} class="input">
            <option value="cash">Cash</option>
            <option value="bank">Bank Transfer</option>
            <option value="mtn_momo">MTN Mobile Money</option>
            <option value="airtel_money">Airtel Money</option>
          </select>
        </div>
        
        <div>
          <label class="label">Reference/Transaction ID</label>
          <input type="text" bind:value={currentPayment.reference} class="input" placeholder="Optional" />
        </div>
      </div>
      
      <div class="flex justify-end space-x-2 mt-6">
        <button on:click={() => showPaymentModal = false} class="btn btn-secondary">Cancel</button>
        <button on:click={recordPayment} class="btn btn-primary">Record Payment</button>
      </div>
    </div>
  </div>
{/if}
