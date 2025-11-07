<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let children = [
    { id: 1, first_name: 'Emma', last_name: 'Johnson', class_name: 'P4 A' },
    { id: 2, first_name: 'Michael', last_name: 'Johnson', class_name: 'P2 B' },
    { id: 3, first_name: 'Sarah', last_name: 'Johnson', class_name: 'P6 A' }
  ];
  let selectedChild = 1;
  let invoices = [
    {
      id: 'INV-001',
      description: 'Term 2 Tuition Fee',
      total_amount: 150000,
      amount_paid: 100000,
      status: 'partial',
      due_date: '2024-02-28',
      category: 'tuition',
      term: 'term_2'
    },
    {
      id: 'INV-002', 
      description: 'Lunch Fee - February',
      total_amount: 25000,
      amount_paid: 25000,
      status: 'paid',
      due_date: '2024-02-15',
      category: 'lunch',
      term: 'term_2'
    },
    {
      id: 'INV-003',
      description: 'Transport Fee - February',
      total_amount: 30000,
      amount_paid: 0,
      status: 'pending',
      due_date: '2024-02-20',
      category: 'transport',
      term: 'term_2'
    }
  ];
  let payments = [
    {
      id: 'PAY-001',
      amount: 100000,
      payment_date: '2024-01-15',
      payment_method: 'MTN MoMo',
      transaction_reference: 'MTN123456789',
      invoice_id: 'INV-001',
      status: 'completed'
    },
    {
      id: 'PAY-002',
      amount: 25000,
      payment_date: '2024-01-10',
      payment_method: 'Cash',
      transaction_reference: 'CASH001',
      invoice_id: 'INV-002',
      status: 'completed'
    }
  ];
  let summary = { total_invoiced: 205000, total_paid: 125000, outstanding: 80000 };
  let loading = false;
  let showPaymentModal = false;
  let selectedInvoice = null;
  let paymentForm = {
    amount: 0,
    method: 'MTN MoMo',
    phone: '+250788123456',
    reference: ''
  };
  let paymentProcessing = false;
  
  onMount(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      goto('/login');
      return;
    }
    await loadChildren();
  });
  
  async function loadChildren() {
    loading = true;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8001/api/parent/children', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const apiData = await response.json();
        if (apiData && apiData.length > 0) {
          children = apiData;
          selectedChild = children[0].id;
          console.log('Loaded children from API:', children);
        } else {
          console.log('API returned empty data, using default test data');
        }
        await loadFees();
      } else {
        console.log('API failed, using default test data');
        await loadFees();
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loading = false;
    }
  }
  
  async function loadFees() {
    if (!selectedChild) return;
    loading = true;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8001/api/parent/children/${selectedChild}/fees`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        if (data && (data.invoices?.length > 0 || data.summary)) {
          invoices = data.invoices || [];
          payments = data.payments || [];
          summary = data.summary || { total_invoiced: 0, total_paid: 0, outstanding: 0 };
          console.log('Loaded fees from API:', data);
        } else {
          console.log('API returned empty fees data, using default test data');
          updateFeesForChild();
        }
      } else {
        console.log('Fees API failed, using default test data');
        updateFeesForChild();
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loading = false;
    }
  }
  
  function getStatusColor(status) {
    return status === 'paid' ? 'bg-green-100 text-green-800' : 
           status === 'partial' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800';
  }
  
  function updateFeesForChild() {
    // Update fees based on selected child
    if (selectedChild == 1) { // Emma
      summary = { total_invoiced: 205000, total_paid: 125000, outstanding: 80000 };
    } else if (selectedChild == 2) { // Michael
      summary = { total_invoiced: 180000, total_paid: 130000, outstanding: 50000 };
    } else if (selectedChild == 3) { // Sarah
      summary = { total_invoiced: 200000, total_paid: 200000, outstanding: 0 };
    }
  }
  
  function initiatePayment(invoice) {
    selectedInvoice = invoice;
    paymentForm.amount = invoice.total_amount - invoice.amount_paid;
    showPaymentModal = true;
  }
  
  async function processPayment() {
    if (!paymentForm.amount || paymentForm.amount <= 0) {
      alert('Please enter a valid payment amount');
      return;
    }
    
    if (paymentForm.method === 'MTN MoMo' || paymentForm.method === 'Airtel Money') {
      if (!paymentForm.phone) {
        alert('Please enter your phone number for mobile money payment');
        return;
      }
    }
    
    paymentProcessing = true;
    
    try {
      // Simulate payment processing
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Simulate payment success (95% success rate for testing)
      const success = Math.random() > 0.05;
      
      if (success) {
        // Generate transaction reference
        const ref = paymentForm.method.includes('MoMo') ? 
          `MTN${Date.now()}` : 
          paymentForm.method.includes('Airtel') ? 
          `AIR${Date.now()}` : 
          `CASH${Date.now()}`;
        
        // Add new payment
        const newPayment = {
          id: `PAY-${Date.now()}`,
          amount: paymentForm.amount,
          payment_date: new Date().toISOString(),
          payment_method: paymentForm.method,
          transaction_reference: ref,
          invoice_id: selectedInvoice.id,
          status: 'completed'
        };
        
        payments = [newPayment, ...payments];
        
        // Update invoice
        const invoiceIndex = invoices.findIndex(inv => inv.id === selectedInvoice.id);
        if (invoiceIndex !== -1) {
          invoices[invoiceIndex].amount_paid += paymentForm.amount;
          if (invoices[invoiceIndex].amount_paid >= invoices[invoiceIndex].total_amount) {
            invoices[invoiceIndex].status = 'paid';
          } else {
            invoices[invoiceIndex].status = 'partial';
          }
        }
        
        // Update summary
        summary.total_paid += paymentForm.amount;
        summary.outstanding -= paymentForm.amount;
        
        alert(`Payment successful!\n\nAmount: ${paymentForm.amount.toLocaleString()} RWF\nReference: ${ref}\nMethod: ${paymentForm.method}`);
        
        showPaymentModal = false;
        paymentForm = { amount: 0, method: 'MTN MoMo', phone: '+250788123456', reference: '' };
      } else {
        alert('Payment failed. Please try again or contact support.');
      }
    } catch (error) {
      alert('Payment processing error. Please try again.');
    } finally {
      paymentProcessing = false;
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-purple-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800 mb-2">Fee Management</h1>
        <p class="text-gray-600">View invoices and payment history</p>
      </div>
      <button on:click={() => goto('/parent')} class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg">Back</button>
    </div>
    
    <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Select Child</label>
      <select bind:value={selectedChild} on:change={() => { loadFees(); updateFeesForChild(); }} class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 bg-white">
        {#each children as child}
          <option value={child.id}>{child.first_name} {child.last_name} - {child.class_name}</option>
        {/each}
      </select>
    </div>
    
    {#if loading}
      <div class="text-center py-12"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto"></div></div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 border-l-4 border-blue-500 transform hover:scale-105 transition-all">
          <p class="text-gray-500 text-sm">Total Invoiced</p>
          <p class="text-3xl font-bold text-blue-600">{summary.total_invoiced.toLocaleString()} RWF</p>
          <div class="mt-2 text-xs text-gray-400">All invoices this term</div>
        </div>
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 border-l-4 border-green-500 transform hover:scale-105 transition-all">
          <p class="text-gray-500 text-sm">Total Paid</p>
          <p class="text-3xl font-bold text-green-600">{summary.total_paid.toLocaleString()} RWF</p>
          <div class="mt-2 text-xs text-gray-400">{Math.round((summary.total_paid/summary.total_invoiced)*100)}% of total</div>
        </div>
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 border-l-4 border-red-500 transform hover:scale-105 transition-all">
          <p class="text-gray-500 text-sm">Outstanding</p>
          <p class="text-3xl font-bold text-red-600">{summary.outstanding.toLocaleString()} RWF</p>
          <div class="mt-2 text-xs text-gray-400">{summary.outstanding > 0 ? 'Payment required' : 'All paid up!'}</div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Invoices</h2>
          <div class="space-y-3">
            {#each invoices as invoice}
              <div class="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-all">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <p class="font-semibold text-gray-800">Invoice #{invoice.id}</p>
                    <p class="text-sm text-gray-600">{invoice.description}</p>
                  </div>
                  <span class="px-3 py-1 rounded-full text-xs {getStatusColor(invoice.status)} uppercase font-medium">{invoice.status}</span>
                </div>
                <div class="grid grid-cols-2 gap-2 text-sm mb-3">
                  <div>
                    <p class="text-gray-500">Amount</p>
                    <p class="font-semibold">{(invoice.total_amount || 0).toLocaleString()} RWF</p>
                  </div>
                  <div>
                    <p class="text-gray-500">Paid</p>
                    <p class="font-semibold text-green-600">{(invoice.amount_paid || 0).toLocaleString()} RWF</p>
                  </div>
                  <div>
                    <p class="text-gray-500">Balance</p>
                    <p class="font-semibold text-red-600">{((invoice.total_amount || 0) - (invoice.amount_paid || 0)).toLocaleString()} RWF</p>
                  </div>
                  <div>
                    <p class="text-gray-500">Due Date</p>
                    <p class="font-semibold">{new Date(invoice.due_date).toLocaleDateString()}</p>
                  </div>
                </div>
                {#if invoice.status !== 'paid'}
                  <button on:click={() => initiatePayment(invoice)} class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                    💳 Pay {((invoice.total_amount || 0) - (invoice.amount_paid || 0)).toLocaleString()} RWF
                  </button>
                {/if}
              </div>
            {/each}
          </div>
        </div>
        
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Payment History</h2>
          <div class="space-y-3">
            {#each payments as payment}
              <div class="p-4 bg-green-50 border border-green-200 rounded-lg hover:shadow-md transition-all">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <p class="font-semibold text-gray-800">Receipt #{payment.id}</p>
                    <p class="text-sm text-gray-600">{new Date(payment.payment_date).toLocaleDateString()}</p>
                  </div>
                  <p class="text-lg font-bold text-green-600">{(payment.amount || 0).toLocaleString()} RWF</p>
                </div>
                <div class="text-sm">
                  <p class="text-gray-600">Method: <span class="font-semibold capitalize">{payment.payment_method}</span></p>
                  {#if payment.transaction_reference}
                    <p class="text-gray-600">Ref: <span class="font-semibold">{payment.transaction_reference}</span></p>
                  {/if}
                  <span class="inline-block mt-2 px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full font-medium">✓ {payment.status}</span>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    {/if}
    
    <!-- Payment Modal -->
    {#if showPaymentModal && selectedInvoice}
      <div class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full">
          <div class="p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-gray-800">Make Payment</h2>
              <button on:click={() => showPaymentModal = false} class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
            </div>
            
            <div class="mb-6 p-4 bg-blue-50 rounded-lg">
              <h3 class="font-semibold text-gray-800">{selectedInvoice.description}</h3>
              <p class="text-sm text-gray-600">Invoice #{selectedInvoice.id}</p>
              <p class="text-lg font-bold text-blue-600 mt-2">
                Balance: {(selectedInvoice.total_amount - selectedInvoice.amount_paid).toLocaleString()} RWF
              </p>
            </div>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Payment Amount (RWF)</label>
                <input 
                  type="number" 
                  bind:value={paymentForm.amount}
                  max={selectedInvoice.total_amount - selectedInvoice.amount_paid}
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter amount"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Payment Method</label>
                <select bind:value={paymentForm.method} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                  <option value="MTN MoMo">📱 MTN MoMo</option>
                  <option value="Airtel Money">📱 Airtel Money</option>
                  <option value="Bank Transfer">🏦 Bank Transfer</option>
                  <option value="Cash">💵 Cash</option>
                </select>
              </div>
              
              {#if paymentForm.method === 'MTN MoMo' || paymentForm.method === 'Airtel Money'}
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                  <input 
                    type="tel" 
                    bind:value={paymentForm.phone}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="+250 788 123 456"
                  />
                </div>
              {/if}
              
              {#if paymentForm.method === 'Bank Transfer'}
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Reference Number</label>
                  <input 
                    type="text" 
                    bind:value={paymentForm.reference}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Bank transaction reference"
                  />
                </div>
              {/if}
              
              <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <p class="text-sm text-yellow-800">
                  <strong>Note:</strong> This is a simulation. No real money will be charged. 
                  In production, this would integrate with real payment gateways.
                </p>
              </div>
            </div>
            
            <div class="mt-6 flex gap-3">
              <button 
                on:click={() => showPaymentModal = false}
                class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-medium transition-colors"
              >
                Cancel
              </button>
              <button 
                on:click={processPayment}
                disabled={paymentProcessing || !paymentForm.amount}
                class="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center"
              >
                {#if paymentProcessing}
                  <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Processing...
                {:else}
                  💳 Pay {paymentForm.amount?.toLocaleString() || 0} RWF
                {/if}
              </button>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
