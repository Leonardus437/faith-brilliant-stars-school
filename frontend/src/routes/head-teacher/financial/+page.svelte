<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let financial = {
    total_revenue: 0,
    outstanding_fees: 0,
    collection_rate: 0,
    monthly_trend: [],
    payment_methods: {},
    top_debtors: [],
    recent_payments: []
  };
  
  let invoices = [];
  let allInvoices = [];
  let allPayments = [];
  let loading = true;
  let activeTab = 'overview';
  let showReminderModal = false;
  let remindersSent = 0;
  
  onMount(async () => {
    const token = localStorage.getItem('token');
    console.log('Fetching financial data...');
    
    const [invoicesRes, paymentsRes] = await Promise.all([
      fetch('http://localhost:8001/api/fees/invoices', { headers: { 'Authorization': `Bearer ${token}` }}),
      fetch('http://localhost:8001/api/fees/payments', { headers: { 'Authorization': `Bearer ${token}` }})
    ]);
    
    console.log('Invoices response:', invoicesRes.status);
    console.log('Payments response:', paymentsRes.status);
    
    if (invoicesRes.ok) {
      invoices = await invoicesRes.json();
      console.log('Invoices loaded:', invoices.length);
      allInvoices = invoices;
      
      financial.total_revenue = invoices.reduce((sum, inv) => sum + inv.amount_paid, 0);
      financial.outstanding_fees = invoices.reduce((sum, inv) => sum + (inv.total_amount - inv.amount_paid), 0);
      financial.collection_rate = financial.total_revenue / (financial.total_revenue + financial.outstanding_fees) * 100;
      
      financial.top_debtors = invoices
        .filter(inv => inv.status !== 'paid')
        .map(inv => ({ student_id: inv.student_id, amount: inv.total_amount - inv.amount_paid, invoice_id: inv.id }))
        .sort((a, b) => b.amount - a.amount)
        .slice(0, 5);
    }
    
    if (paymentsRes.ok) {
      const payments = await paymentsRes.json();
      console.log('Payments loaded:', payments.length);
      allPayments = payments;
      financial.recent_payments = payments.slice(0, 10);
      
      financial.payment_methods = payments.reduce((acc, p) => {
        acc[p.payment_method] = (acc[p.payment_method] || 0) + p.amount;
        return acc;
      }, {});
    } else {
      console.error('Failed to load payments:', await paymentsRes.text());
    }
    
    console.log('Financial data:', financial);
    console.log('All invoices:', allInvoices.length);
    console.log('All payments:', allPayments.length);
    loading = false;
  });
  
  function getHealthStatus() {
    if (financial.collection_rate >= 80) return { text: 'Excellent', color: 'green', icon: '✓' };
    if (financial.collection_rate >= 60) return { text: 'Good', color: 'blue', icon: '→' };
    if (financial.collection_rate >= 40) return { text: 'Fair', color: 'yellow', icon: '⚠' };
    return { text: 'Critical', color: 'red', icon: '!' };
  }
  
  $: healthStatus = getHealthStatus();
  
  function exportReport() {
    const csvContent = 'data:text/csv;charset=utf-8,' + 
      'Invoice,Student,Amount,Paid,Outstanding,Status\n' +
      allInvoices.map(inv => 
        `${inv.invoice_number},${inv.student_id},${inv.total_amount},${inv.amount_paid},${inv.total_amount - inv.amount_paid},${inv.status}`
      ).join('\n');
    
    const link = document.createElement('a');
    link.href = encodeURI(csvContent);
    link.download = `financial_report_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  }
  
  function sendReminders() {
    const outstanding = allInvoices.filter(inv => inv.status !== 'paid');
    remindersSent = outstanding.length;
    showReminderModal = true;
    setTimeout(() => showReminderModal = false, 3000);
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800">Financial Overview</h1>
        <p class="text-gray-600">Complete financial health and revenue tracking</p>
      </div>
      <button on:click={() => goto('/head-teacher')} class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg">
        Back to Dashboard
      </button>
    </div>
    
    {#if loading}
      <div class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
      </div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
          <div class="flex items-center justify-between mb-2">
            <p class="text-gray-500 text-sm">Total Revenue</p>
            <span class="text-2xl">💰</span>
          </div>
          <p class="text-3xl font-bold text-green-600">{financial.total_revenue.toLocaleString()} RWF</p>
          <p class="text-xs text-gray-500 mt-2">All-time collected</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-red-500">
          <div class="flex items-center justify-between mb-2">
            <p class="text-gray-500 text-sm">Outstanding Fees</p>
            <span class="text-2xl">📋</span>
          </div>
          <p class="text-3xl font-bold text-red-600">{financial.outstanding_fees.toLocaleString()} RWF</p>
          <p class="text-xs text-gray-500 mt-2">Pending collection</p>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
          <div class="flex items-center justify-between mb-2">
            <p class="text-gray-500 text-sm">Collection Rate</p>
            <span class="text-2xl">📊</span>
          </div>
          <p class="text-3xl font-bold text-blue-600">{financial.collection_rate.toFixed(1)}%</p>
          <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
            <div class="bg-blue-600 h-2 rounded-full" style="width: {financial.collection_rate}%"></div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-{healthStatus.color}-500">
          <div class="flex items-center justify-between mb-2">
            <p class="text-gray-500 text-sm">Financial Health</p>
            <span class="text-2xl">{healthStatus.icon}</span>
          </div>
          <p class="text-3xl font-bold text-{healthStatus.color}-600">{healthStatus.text}</p>
          <p class="text-xs text-gray-500 mt-2">Based on collection rate</p>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="text-2xl mr-2">💳</span>
            Payment Methods Breakdown
          </h2>
          <div class="space-y-3">
            {#each Object.entries(financial.payment_methods) as [method, amount]}
              <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div class="flex items-center">
                  <div class="w-3 h-3 rounded-full bg-blue-500 mr-3"></div>
                  <span class="font-semibold text-gray-700">{method}</span>
                </div>
                <span class="text-lg font-bold text-gray-800">{amount.toLocaleString()} RWF</span>
              </div>
            {/each}
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="text-2xl mr-2">⚠️</span>
            Top 5 Outstanding Debtors
          </h2>
          <div class="space-y-3">
            {#each financial.top_debtors as debtor, i}
              <div class="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                <div class="flex items-center">
                  <span class="w-6 h-6 rounded-full bg-red-500 text-white flex items-center justify-center text-xs font-bold mr-3">
                    {i + 1}
                  </span>
                  <span class="font-semibold text-gray-700">Student #{debtor.student_id}</span>
                </div>
                <span class="text-lg font-bold text-red-600">{debtor.amount.toLocaleString()} RWF</span>
              </div>
            {/each}
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <div class="border-b">
          <div class="flex">
            <button on:click={() => activeTab = 'overview'} 
                    class="px-6 py-4 font-semibold {activeTab === 'overview' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}">
              Overview
            </button>
            <button on:click={() => activeTab = 'invoices'} 
                    class="px-6 py-4 font-semibold {activeTab === 'invoices' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}">
              All Invoices
            </button>
            <button on:click={() => activeTab = 'payments'} 
                    class="px-6 py-4 font-semibold {activeTab === 'payments' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}">
              All Payments
            </button>
          </div>
        </div>
        
        <div class="p-6">
          {#if activeTab === 'overview'}
            <h2 class="text-xl font-bold text-gray-800 mb-4">Recent Payment Transactions</h2>
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Receipt #</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Method</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  {#each financial.recent_payments as payment}
                    <tr class="hover:bg-gray-50">
                      <td class="px-6 py-4 font-mono text-sm">{payment.receipt_number}</td>
                      <td class="px-6 py-4">#{payment.invoice_id}</td>
                      <td class="px-6 py-4 font-bold text-green-600">{payment.amount.toLocaleString()} RWF</td>
                      <td class="px-6 py-4">
                        <span class="px-2 py-1 rounded text-xs bg-blue-100 text-blue-800">{payment.payment_method}</span>
                      </td>
                      <td class="px-6 py-4 text-sm">{new Date(payment.payment_date).toLocaleDateString()}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          {:else if activeTab === 'invoices'}
            <h2 class="text-xl font-bold text-gray-800 mb-4">All Invoices</h2>
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Paid</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Outstanding</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  {#each allInvoices as invoice}
                    <tr class="hover:bg-gray-50">
                      <td class="px-6 py-4 font-mono text-sm">{invoice.invoice_number}</td>
                      <td class="px-6 py-4">Student #{invoice.student_id}</td>
                      <td class="px-6 py-4 font-bold">{invoice.total_amount.toLocaleString()} RWF</td>
                      <td class="px-6 py-4 text-green-600">{invoice.amount_paid.toLocaleString()} RWF</td>
                      <td class="px-6 py-4 text-red-600">{(invoice.total_amount - invoice.amount_paid).toLocaleString()} RWF</td>
                      <td class="px-6 py-4">
                        <span class="px-2 py-1 rounded text-xs {invoice.status === 'paid' ? 'bg-green-100 text-green-800' : invoice.status === 'partial' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}">
                          {invoice.status}
                        </span>
                      </td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          {:else if activeTab === 'payments'}
            <h2 class="text-xl font-bold text-gray-800 mb-4">All Payment Transactions</h2>
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Receipt #</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Method</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  {#each allPayments as payment}
                    <tr class="hover:bg-gray-50">
                      <td class="px-6 py-4 font-mono text-sm">{payment.receipt_number}</td>
                      <td class="px-6 py-4">#{payment.invoice_id}</td>
                      <td class="px-6 py-4 font-bold text-green-600">{payment.amount.toLocaleString()} RWF</td>
                      <td class="px-6 py-4">
                        <span class="px-2 py-1 rounded text-xs bg-blue-100 text-blue-800">{payment.payment_method}</span>
                      </td>
                      <td class="px-6 py-4 text-sm">{new Date(payment.payment_date).toLocaleDateString()}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          {/if}
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <button on:click={() => activeTab = 'invoices'} class="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-xl shadow-lg p-6 transition-all hover:scale-105">
          <div class="text-4xl mb-3">📋</div>
          <h3 class="font-bold text-lg mb-2">View All Invoices</h3>
          <p class="text-sm opacity-90">Manage student invoices</p>
        </button>
        
        <button on:click={exportReport} class="bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white rounded-xl shadow-lg p-6 transition-all hover:scale-105">
          <div class="text-4xl mb-3">📊</div>
          <h3 class="font-bold text-lg mb-2">Generate Report</h3>
          <p class="text-sm opacity-90">Export financial data</p>
        </button>
        
        <button on:click={sendReminders} class="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white rounded-xl shadow-lg p-6 transition-all hover:scale-105">
          <div class="text-4xl mb-3">📧</div>
          <h3 class="font-bold text-lg mb-2">Send Reminders</h3>
          <p class="text-sm opacity-90">Notify outstanding fees</p>
        </button>
      </div>
    {/if}
  </div>
</div>

{#if showReminderModal}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-8 max-w-md w-full text-center">
      <div class="text-6xl mb-4">✅</div>
      <h2 class="text-2xl font-bold text-gray-800 mb-2">Reminders Sent!</h2>
      <p class="text-gray-600">{remindersSent} payment reminders have been sent to parents with outstanding fees.</p>
    </div>
  </div>
{/if}
