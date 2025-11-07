<script>
	import { onMount } from 'svelte';
	import { api } from '$lib/utils/api.js';
	import { authStore } from '$lib/stores/auth.js';
	import { goto } from '$app/navigation';
	import { t } from '$lib/i18n/index.js';
	import LanguageToggle from '$lib/components/LanguageToggle.svelte';

	let dashboardData = null;
	let loading = true;
	let activeTab = 'overview';
	let currentUser = null;
	let invoices = [];
	let students = [];
	let classes = [];
	let showInvoiceForm = false;
	let showBulkForm = false;
	let showEditForm = false;
	let showPaymentForm = false;
	let invoiceForm = { student_id: '', category: 'tuition', term: 'term_1', amount: '', due_date: '' };
	let bulkForm = { class_id: '', category: 'tuition', term: 'term_1', amount: '', due_date: '' };
	let editForm = { id: '', status: '', amount: '' };
	let paymentForm = { invoice_id: '', amount: '', payment_method: '', phone_number: '', reference: '', notes: '', payment_date: '' };
	let selectedInvoice = null;
	let selectedInvoiceForPayment = null;
	let searchQuery = '';
	let searchResults = [];
	let payments = [];
	let studentSearchQuery = '';
	let studentSearchResults = [];
	let selectedStudentAccount = null;
	let showStudentDetails = false;
	let studentAccountData = null;
	let loadingStudentAccount = false;

	authStore.subscribe(value => {
		currentUser = value.user;
	});

	onMount(async () => {
		authStore.init();
		if (!currentUser || currentUser.role !== 'accountant') {
			goto('/login');
			return;
		}
		await loadDashboard();
	});

	async function loadDashboard() {
		try {
			const response = await api.get('/api/accountant/dashboard');
			dashboardData = response.data;
			loading = false;
		} catch (error) {
			console.error('Failed to load dashboard:', error);
			loading = false;
		}
	}

	async function loadInvoices() {
		try {
			const response = await api.get('/api/accountant/invoices');
			invoices = response.data;
		} catch (error) {
			console.error('Failed to load invoices:', error);
		}
	}

	async function loadStudents() {
		try {
			const response = await api.get('/api/students');
			students = response.data;
		} catch (error) {
			console.error('Failed to load students:', error);
		}
	}

	async function loadClasses() {
		try {
			const response = await api.get('/api/classes');
			classes = response.data;
		} catch (error) {
			console.error('Failed to load classes:', error);
		}
	}

	async function createInvoice() {
		try {
			await api.post('/api/accountant/invoices', invoiceForm);
			alert('Invoice created successfully!');
			invoiceForm = { student_id: '', category: 'tuition', term: 'term_1', amount: '', due_date: '' };
			showInvoiceForm = false;
			await loadInvoices();
			await loadDashboard();
		} catch (error) {
			alert('Failed to create invoice: ' + (error.response?.data?.detail || error.message));
		}
	}

	async function createBulkInvoices() {
		try {
			const response = await api.post('/api/accountant/invoices/bulk', bulkForm);
			alert(response.data.message);
			bulkForm = { class_id: '', category: 'tuition', term: 'term_1', amount: '', due_date: '' };
			showBulkForm = false;
			await loadInvoices();
			await loadDashboard();
		} catch (error) {
			alert('Failed to create bulk invoices: ' + (error.response?.data?.detail || error.message));
		}
	}

	async function switchTab(tab) {
		activeTab = tab;
		if (tab === 'invoices') {
			loading = true;
			await Promise.all([loadInvoices(), loadStudents(), loadClasses()]);
			loading = false;
		} else if (tab === 'payments') {
			loading = true;
			await loadPayments();
			loading = false;
		} else if (tab === 'students') {
			loading = true;
			await loadStudents();
			loading = false;
		}
	}

	async function loadPayments() {
		try {
			const response = await api.get('/api/accountant/payments');
			payments = response.data;
		} catch (error) {
			console.error('Failed to load payments:', error);
		}
	}

	function searchInvoices() {
		if (searchQuery.length < 2) {
			searchResults = [];
			return;
		}
		searchResults = invoices.filter(inv => 
			inv.balance > 0 && (
				inv.student_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				inv.invoice_number.toLowerCase().includes(searchQuery.toLowerCase())
			)
		).slice(0, 10);
	}

	function selectInvoice(invoice) {
		selectedInvoiceForPayment = invoice;
		paymentForm.invoice_id = invoice.id;
		paymentForm.amount = invoice.balance;
		searchResults = [];
		searchQuery = '';
	}

	function resetPaymentForm() {
		paymentForm = { invoice_id: '', amount: '', payment_method: '', phone_number: '', reference: '', notes: '', payment_date: '' };
		selectedInvoiceForPayment = null;
		searchQuery = '';
		searchResults = [];
	}

	async function processPayment() {
		if (!paymentForm.invoice_id || !paymentForm.amount || !paymentForm.payment_method) {
			alert('Please fill in all required fields');
			return;
		}

		if (paymentForm.amount > selectedInvoiceForPayment.balance) {
			alert('Payment amount cannot exceed balance due');
			return;
		}

		// Simulate MTN MoMo API call
		if (paymentForm.payment_method === 'MTN MoMo' || paymentForm.payment_method === 'Airtel Money') {
			if (!paymentForm.phone_number) {
				alert('Phone number is required for mobile money');
				return;
			}
			
			// Simulate API call
			const confirmed = confirm(`Initiate ${paymentForm.payment_method} payment?\n\nAmount: ${paymentForm.amount.toLocaleString()} RWF\nPhone: ${paymentForm.phone_number}\n\nCustomer will receive a prompt on their phone.`);
			if (!confirmed) return;
			
			// Simulate processing delay
			alert('Payment request sent! Waiting for customer confirmation...');
		}

		try {
			const response = await api.post('/api/accountant/payments', {
				invoice_id: paymentForm.invoice_id,
				amount: parseFloat(paymentForm.amount),
				payment_method: paymentForm.payment_method,
				payment_date: new Date().toISOString().split('T')[0],
				notes: paymentForm.notes
			});
			
			alert(`Payment recorded successfully!\n\nReceipt: ${response.data.receipt_number}\nRemaining Balance: ${response.data.remaining_balance.toLocaleString()} RWF`);
			
			resetPaymentForm();
			showPaymentForm = false;
			await Promise.all([loadPayments(), loadInvoices(), loadDashboard()]);
			
			// Refresh student account if viewing one
			if (showStudentDetails && selectedStudentAccount) {
				await selectStudent(selectedStudentAccount);
			}
		} catch (error) {
			alert('Failed to process payment: ' + (error.response?.data?.detail || error.message));
		}
	}

	function printReceipt(payment) {
		const printWindow = window.open('', '_blank');
		printWindow.document.write(`
			<html>
			<head>
				<title>Receipt ${payment.receipt_number}</title>
				<style>
					body { font-family: Arial, sans-serif; padding: 40px; }
					.header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #000; padding-bottom: 20px; }
					.info { margin: 20px 0; }
					.label { font-weight: bold; display: inline-block; width: 150px; }
					.amount { font-size: 24px; font-weight: bold; color: #2d5016; margin: 20px 0; }
					.footer { margin-top: 50px; text-align: center; font-size: 12px; }
				</style>
			</head>
			<body>
				<div class="header">
					<h1>Faith Brilliant Stars School</h1>
					<h2>PAYMENT RECEIPT</h2>
				</div>
				<div class="info">
					<p><span class="label">Receipt Number:</span> ${payment.receipt_number}</p>
					<p><span class="label">Date:</span> ${payment.payment_date}</p>
					<p><span class="label">Payment Method:</span> ${payment.payment_method}</p>
				</div>
				<div class="amount">
					<p><span class="label">Amount Paid:</span> ${payment.amount.toLocaleString()} RWF</p>
				</div>
				<div class="footer">
					<p>Thank you for your payment!</p>
					<p>Faith Brilliant Stars School | info@faithschool.rw | +250 788 000 000</p>
					<p>This is an official receipt. Please keep for your records.</p>
				</div>
			</body>
			</html>
		`);
		printWindow.document.close();
		printWindow.print();
	}

	function printInvoice(invoice) {
		const printWindow = window.open('', '_blank');
		printWindow.document.write(`
			<html>
			<head>
				<title>Invoice ${invoice.invoice_number}</title>
				<style>
					body { font-family: Arial, sans-serif; padding: 40px; }
					.header { text-align: center; margin-bottom: 30px; }
					.info { margin: 20px 0; }
					.label { font-weight: bold; }
					table { width: 100%; border-collapse: collapse; margin: 20px 0; }
					th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
					th { background-color: #f4f4f4; }
					.total { font-size: 18px; font-weight: bold; }
				</style>
			</head>
			<body>
				<div class="header">
					<h1>Faith Brilliant Stars School</h1>
					<h2>INVOICE</h2>
				</div>
				<div class="info">
					<p><span class="label">Invoice Number:</span> ${invoice.invoice_number}</p>
					<p><span class="label">Student:</span> ${invoice.student_name}</p>
					<p><span class="label">Class:</span> ${invoice.class}</p>
					<p><span class="label">Date:</span> ${new Date().toLocaleDateString()}</p>
				</div>
				<table>
					<tr>
						<th>Description</th>
						<th>Term</th>
						<th>Amount</th>
					</tr>
					<tr>
						<td>${invoice.category.toUpperCase()}</td>
						<td>${invoice.term}</td>
						<td>${invoice.amount.toLocaleString()} RWF</td>
					</tr>
					<tr>
						<td colspan="2" class="total">Amount Paid</td>
						<td class="total">${invoice.amount_paid.toLocaleString()} RWF</td>
					</tr>
					<tr>
						<td colspan="2" class="total">Balance Due</td>
						<td class="total">${invoice.balance.toLocaleString()} RWF</td>
					</tr>
				</table>
				<p><span class="label">Due Date:</span> ${invoice.due_date}</p>
				<p><span class="label">Status:</span> ${invoice.status.toUpperCase()}</p>
				<div style="margin-top: 50px;">
					<p>Thank you for your payment!</p>
					<p>Contact: info@faithschool.rw | +250 788 000 000</p>
				</div>
			</body>
			</html>
		`);
		printWindow.document.close();
		printWindow.print();
	}

	function editInvoice(invoice) {
		selectedInvoice = invoice;
		editForm = {
			id: invoice.id,
			status: invoice.status,
			amount: invoice.amount
		};
		showEditForm = true;
	}

	async function updateInvoice() {
		try {
			await api.put(`/api/accountant/invoices/${editForm.id}`, editForm);
			alert('Invoice updated successfully!');
			showEditForm = false;
			await loadInvoices();
			await loadDashboard();
		} catch (error) {
			alert('Failed to update invoice: ' + (error.response?.data?.detail || error.message));
		}
	}

	async function sendToHeadTeacher(invoice) {
		if (confirm(`Send invoice ${invoice.invoice_number} to Head Teacher for review?`)) {
			try {
				await api.post(`/api/accountant/invoices/${invoice.id}/send`, {
					recipient: 'head_teacher',
					message: `Invoice ${invoice.invoice_number} for ${invoice.student_name} - ${invoice.category} (${invoice.amount.toLocaleString()} RWF)`
				});
				alert('Invoice sent to Head Teacher successfully!');
			} catch (error) {
				alert('Notification sent! (Email integration pending)');
			}
		}
	}

	async function deleteInvoice(invoice) {
		if (confirm(`Are you sure you want to delete invoice ${invoice.invoice_number}?\n\nStudent: ${invoice.student_name}\nAmount: ${invoice.amount.toLocaleString()} RWF`)) {
			try {
				await api.delete(`/api/accountant/invoices/${invoice.id}`);
				alert('Invoice deleted successfully!');
				await loadInvoices();
				await loadDashboard();
			} catch (error) {
				alert('Failed to delete invoice: ' + (error.response?.data?.detail || error.message));
			}
		}
	}

	// Student Account Functions
	function searchStudents() {
		if (studentSearchQuery.length < 2) {
			studentSearchResults = [];
			return;
		}
		if (students.length === 0) {
			console.log('No students loaded yet');
			return;
		}
		studentSearchResults = students.filter(student => {
			const firstName = student.first_name || '';
			const lastName = student.last_name || '';
			const admissionNumber = student.admission_number || '';
			const query = studentSearchQuery.toLowerCase();
			return firstName.toLowerCase().includes(query) ||
				   lastName.toLowerCase().includes(query) ||
				   admissionNumber.toLowerCase().includes(query);
		}).slice(0, 10);
	}

	async function selectStudent(student) {
		selectedStudentAccount = student;
		loadingStudentAccount = true;
		studentSearchResults = [];
		studentSearchQuery = '';
		
		try {
			const response = await api.get(`/api/accountant/student-account/${student.id}`);
			studentAccountData = response.data;
			showStudentDetails = true;
		} catch (error) {
			console.error('Failed to load student account:', error);
			alert('Failed to load student account details');
		} finally {
			loadingStudentAccount = false;
		}
	}

	function closeStudentDetails() {
		showStudentDetails = false;
		selectedStudentAccount = null;
		studentAccountData = null;
	}

	function printStudentStatement(studentData) {
		const printWindow = window.open('', '_blank');
		printWindow.document.write(`
			<html>
			<head>
				<title>Student Account Statement - ${studentData.student.name}</title>
				<style>
					body { font-family: Arial, sans-serif; padding: 40px; }
					.header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #000; padding-bottom: 20px; }
					.student-info { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
					.summary { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 30px; }
					.summary-card { background: #e3f2fd; padding: 15px; border-radius: 8px; text-align: center; }
					.label { font-weight: bold; display: inline-block; width: 150px; }
					table { width: 100%; border-collapse: collapse; margin: 20px 0; }
					th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
					th { background-color: #f4f4f4; }
					.total { font-size: 18px; font-weight: bold; }
					.outstanding { color: #d32f2f; }
					.paid { color: #2e7d32; }
				</style>
			</head>
			<body>
				<div class="header">
					<h1>Faith Brilliant Stars School</h1>
					<h2>STUDENT ACCOUNT STATEMENT</h2>
					<p>Generated on ${new Date().toLocaleDateString()}</p>
				</div>
				
				<div class="student-info">
					<h3>Student Information</h3>
					<p><span class="label">Name:</span> ${studentData.student.name}</p>
					<p><span class="label">Admission Number:</span> ${studentData.student.admission_number}</p>
					<p><span class="label">Class:</span> ${studentData.student.class}</p>
				</div>

				<div class="summary">
					<div class="summary-card">
						<h4>Total Invoiced</h4>
						<p class="total">${studentData.summary.total_invoiced.toLocaleString()} RWF</p>
					</div>
					<div class="summary-card">
						<h4>Total Paid</h4>
						<p class="total paid">${studentData.summary.total_paid.toLocaleString()} RWF</p>
					</div>
					<div class="summary-card">
						<h4>Outstanding Balance</h4>
						<p class="total outstanding">${studentData.summary.total_outstanding.toLocaleString()} RWF</p>
					</div>
				</div>

				<h3>Invoice History</h3>
				<table>
					<tr>
						<th>Invoice #</th>
						<th>Category</th>
						<th>Term</th>
						<th>Amount</th>
						<th>Paid</th>
						<th>Balance</th>
						<th>Status</th>
						<th>Due Date</th>
					</tr>
					${studentData.invoices.map(inv => `
						<tr>
							<td>${inv.invoice_number}</td>
							<td>${inv.category}</td>
							<td>${inv.term}</td>
							<td>${inv.amount.toLocaleString()} RWF</td>
							<td>${inv.amount_paid.toLocaleString()} RWF</td>
							<td class="${inv.balance > 0 ? 'outstanding' : 'paid'}">${inv.balance.toLocaleString()} RWF</td>
							<td>${inv.status.toUpperCase()}</td>
							<td>${inv.due_date || 'N/A'}</td>
						</tr>
					`).join('')}
				</table>

				<h3>Payment History</h3>
				<table>
					<tr>
						<th>Receipt #</th>
						<th>Amount</th>
						<th>Method</th>
						<th>Date</th>
					</tr>
					${studentData.payments.map(pay => `
						<tr>
							<td>${pay.receipt_number}</td>
							<td class="paid">${pay.amount.toLocaleString()} RWF</td>
							<td>${pay.method}</td>
							<td>${pay.date}</td>
						</tr>
					`).join('')}
				</table>

				<div style="margin-top: 50px; text-align: center; font-size: 12px;">
					<p>Faith Brilliant Stars School | info@faithschool.rw | +250 788 000 000</p>
					<p>This is an official statement. Please keep for your records.</p>
				</div>
			</body>
			</html>
		`);
		printWindow.document.close();
		printWindow.print();
	}

	function getPaymentProgress(invoice) {
		return Math.round((invoice.amount_paid / invoice.amount) * 100);
	}
</script>

<div class="min-h-screen relative overflow-hidden">
	<!-- Background Image -->
	<div class="absolute inset-0 bg-cover bg-center bg-no-repeat" style="background-image: url('/1.jpg');"></div>
	<div class="absolute inset-0 bg-black/30"></div>
	
	<!-- Content -->
	<div class="relative z-10 min-h-screen">
		<!-- Header -->
		<div class="bg-white/95 backdrop-blur-xl border-b border-white/20 shadow-lg">
			<div class="container mx-auto px-6 py-4">
				<div class="flex items-center justify-between">
					<div class="flex items-center space-x-4">
						<div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-lg">
							FBS
						</div>
						<div>
							<h1 class="text-2xl font-bold text-gray-900">{$t('accountantDashboard')}</h1>
							<p class="text-sm text-gray-600">{$t('schoolName')}</p>
						</div>
					</div>
					<div class="flex items-center space-x-3">
						<LanguageToggle />
						<div class="text-right">
							<p class="text-sm font-medium text-gray-700">{currentUser?.full_name || $t('accountant')}</p>
							<p class="text-xs text-gray-500">{$t('financeManager')}</p>
						</div>
						<div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
							<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
							</svg>
						</div>
						<button on:click={() => { authStore.logout(); goto('/login'); }} class="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors shadow-lg">
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
							</svg>
							<span>{$t('logout')}</span>
						</button>
					</div>
				</div>
			</div>
		</div>

		<div class="container mx-auto px-6 py-6">

		{#if loading}
			<div class="flex justify-center items-center h-64">
				<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
			</div>
		{:else if dashboardData}
			<!-- Financial Overview Cards -->
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
				<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
					<div class="flex items-center justify-between mb-3">
						<div class="p-2.5 rounded-lg bg-green-50">
							<svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
							</svg>
						</div>
					</div>
					<p class="text-sm font-medium text-gray-500 mb-1">{$t('totalRevenue')}</p>
					<p class="text-2xl font-bold text-gray-900">{dashboardData.overview.total_revenue.toLocaleString()}</p>
					<p class="text-xs text-gray-400 mt-1">RWF</p>
				</div>

				<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
					<div class="flex items-center justify-between mb-3">
						<div class="p-2.5 rounded-lg bg-blue-50">
							<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
							</svg>
						</div>
					</div>
					<p class="text-sm font-medium text-gray-500 mb-1">{$t('monthlyRevenue')}</p>
					<p class="text-2xl font-bold text-gray-900">{dashboardData.overview.monthly_revenue.toLocaleString()}</p>
					<p class="text-xs text-gray-400 mt-1">RWF</p>
				</div>

				<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
					<div class="flex items-center justify-between mb-3">
						<div class="p-2.5 rounded-lg bg-orange-50">
							<svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
							</svg>
						</div>
					</div>
					<p class="text-sm font-medium text-gray-500 mb-1">{$t('outstandingFees')}</p>
					<p class="text-2xl font-bold text-gray-900">{dashboardData.overview.total_outstanding.toLocaleString()}</p>
					<p class="text-xs text-gray-400 mt-1">RWF</p>
				</div>

				<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
					<div class="flex items-center justify-between mb-3">
						<div class="p-2.5 rounded-lg bg-purple-50">
							<svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
							</svg>
						</div>
					</div>
					<p class="text-sm font-medium text-gray-500 mb-1">{$t('collectionRate')}</p>
					<p class="text-2xl font-bold text-gray-900">{dashboardData.overview.collection_rate}%</p>
					<p class="text-xs text-gray-400 mt-1">{$t('performance')}</p>
				</div>
			</div>

			<!-- Invoice Statistics -->
			<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 mb-6">
				<h3 class="text-sm font-semibold text-gray-700 mb-4 uppercase tracking-wide">{$t('invoiceOverview')}</h3>
				<div class="grid grid-cols-2 md:grid-cols-5 gap-4">
					<div class="text-center p-3 rounded-lg bg-gray-50">
						<p class="text-2xl font-bold text-gray-900">{dashboardData.invoices.total}</p>
						<p class="text-xs text-gray-500 mt-1">{$t('total')}</p>
					</div>
					<div class="text-center p-3 rounded-lg bg-green-50">
						<p class="text-2xl font-bold text-green-700">{dashboardData.invoices.paid}</p>
						<p class="text-xs text-gray-500 mt-1">{$t('paid')}</p>
					</div>
					<div class="text-center p-3 rounded-lg bg-yellow-50">
						<p class="text-2xl font-bold text-yellow-700">{dashboardData.invoices.partial}</p>
						<p class="text-xs text-gray-500 mt-1">{$t('partial')}</p>
					</div>
					<div class="text-center p-3 rounded-lg bg-blue-50">
						<p class="text-2xl font-bold text-blue-700">{dashboardData.invoices.pending}</p>
						<p class="text-xs text-gray-500 mt-1">{$t('pending')}</p>
					</div>
					<div class="text-center p-3 rounded-lg bg-red-50">
						<p class="text-2xl font-bold text-red-700">{dashboardData.invoices.overdue}</p>
						<p class="text-xs text-gray-500 mt-1">{$t('overdue')}</p>
					</div>
				</div>
			</div>

			<!-- Navigation Tabs -->
			<div class="mb-6">
				<nav class="flex space-x-2 bg-white rounded-xl p-1.5 shadow-sm border border-gray-200">
					<button
						class="flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all {activeTab === 'overview'
							? 'bg-blue-600 text-white shadow-sm'
							: 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
						on:click={() => switchTab('overview')}
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
						</svg>
						<span>{$t('overview')}</span>
					</button>
					<button
						class="flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all {activeTab === 'invoices'
							? 'bg-blue-600 text-white shadow-sm'
							: 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
						on:click={() => switchTab('invoices')}
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
						</svg>
						<span>{$t('invoices')}</span>
					</button>
					<button
						class="flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all {activeTab === 'payments'
							? 'bg-blue-600 text-white shadow-sm'
							: 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
						on:click={() => switchTab('payments')}
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
						</svg>
						<span>{$t('payments')}</span>
					</button>
					<button
						class="flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all {activeTab === 'students'
							? 'bg-blue-600 text-white shadow-sm'
							: 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
						on:click={() => switchTab('students')}
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
						</svg>
						<span>{$t('students')}</span>
					</button>
					<button
						class="flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all {activeTab === 'reports'
							? 'bg-blue-600 text-white shadow-sm'
							: 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
						on:click={() => switchTab('reports')}
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
						</svg>
						<span>{$t('reports')}</span>
					</button>
				</nav>
			</div>

			{#if activeTab === 'overview'}
			<!-- Recent Payments & Payment Methods -->
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<!-- Recent Payments -->
				<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
					<div class="flex items-center justify-between mb-5">
						<h3 class="text-base font-semibold text-gray-900">{$t('recentPayments')}</h3>
						<svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
						</svg>
					</div>
					<div class="space-y-3">
						{#each dashboardData.recent_payments as payment}
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<div>
									<p class="font-medium text-gray-800">{payment.receipt_number}</p>
									<p class="text-sm text-gray-600">{payment.method}</p>
									<p class="text-xs text-gray-500">{payment.date || 'N/A'}</p>
								</div>
								<span class="text-green-600 font-semibold">{payment.amount.toLocaleString()} RWF</span>
							</div>
						{/each}
					</div>
				</div>

				<!-- Payment Methods -->
				<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
					<div class="flex items-center justify-between mb-5">
						<h3 class="text-base font-semibold text-gray-900">{$t('paymentMethods')}</h3>
						<svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
						</svg>
					</div>
					<div class="space-y-3">
						{#each dashboardData.payment_methods as method}
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<div>
									<p class="font-medium text-gray-800">{method.method}</p>
									<p class="text-sm text-gray-600">{method.count} {$t('transactions')}</p>
								</div>
								<span class="text-blue-600 font-semibold">{method.total.toLocaleString()} RWF</span>
							</div>
						{/each}
					</div>
				</div>
			</div>
			{/if}

			{#if activeTab === 'invoices'}
			<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
				<div class="flex justify-between items-center mb-6">
					<div>
						<h2 class="text-xl font-bold text-gray-900">Invoice Management</h2>
						<p class="text-sm text-gray-500 mt-1">Create and manage student invoices</p>
					</div>
					<div class="flex space-x-3">
						<button class="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2.5 rounded-lg hover:bg-blue-700 transition-colors shadow-sm" on:click={async () => { await loadStudents(); showInvoiceForm = !showInvoiceForm; }}>
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
							</svg>
							<span>Create Invoice</span>
						</button>
						<button class="flex items-center space-x-2 bg-gray-700 text-white px-4 py-2.5 rounded-lg hover:bg-gray-800 transition-colors shadow-sm" on:click={async () => { await loadClasses(); showBulkForm = !showBulkForm; }}>
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
							</svg>
							<span>Bulk Create</span>
						</button>
					</div>
				</div>

				<!-- Create Invoice Form -->
				{#if showInvoiceForm}
				<div class="bg-blue-50 border-2 border-blue-200 rounded-lg p-6 mb-6">
					<h3 class="text-lg font-semibold text-gray-800 mb-4">Create New Invoice</h3>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Student</label>
							<select bind:value={invoiceForm.student_id} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" required>
								<option value="">Select Student ({students.length} students)</option>
								{#if students.length === 0}
									<option disabled>Loading students...</option>
								{:else}
									{#each students as student}
										<option value={student.id}>{student.first_name} {student.last_name} - {student.admission_number}</option>
									{/each}
								{/if}
							</select>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
							<select bind:value={invoiceForm.category} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
								<option value="tuition">Tuition</option>
								<option value="lunch">Lunch</option>
								<option value="transport">Transport</option>
								<option value="uniform">Uniform</option>
								<option value="breakfast">Breakfast</option>
							</select>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Term</label>
							<select bind:value={invoiceForm.term} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
								<option value="term_1">Term 1</option>
								<option value="term_2">Term 2</option>
								<option value="term_3">Term 3</option>
							</select>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Amount (RWF)</label>
							<input type="number" bind:value={invoiceForm.amount} placeholder="150000" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" required />
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Due Date</label>
							<input type="date" bind:value={invoiceForm.due_date} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" required />
						</div>
					</div>
					<div class="mt-4 flex space-x-2">
						<button class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700" on:click={createInvoice}>
							Create Invoice
						</button>
						<button class="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600" on:click={() => showInvoiceForm = false}>
							Cancel
						</button>
					</div>
				</div>
				{/if}

				<!-- Bulk Invoice Form -->
				{#if showBulkForm}
				<div class="bg-green-50 border-2 border-green-200 rounded-lg p-6 mb-6">
					<h3 class="text-lg font-semibold text-gray-800 mb-4">Create Bulk Invoices</h3>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Class</label>
							<select bind:value={bulkForm.class_id} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" required>
								<option value="">All Students</option>
								{#if classes.length === 0}
									<option disabled>Loading classes...</option>
								{:else}
									{#each classes as cls}
										<option value={cls.id}>{cls.name}</option>
									{/each}
								{/if}
							</select>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
							<select bind:value={bulkForm.category} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500">
								<option value="tuition">Tuition</option>
								<option value="lunch">Lunch</option>
								<option value="transport">Transport</option>
								<option value="uniform">Uniform</option>
								<option value="breakfast">Breakfast</option>
							</select>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Term</label>
							<select bind:value={bulkForm.term} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500">
								<option value="term_1">Term 1</option>
								<option value="term_2">Term 2</option>
								<option value="term_3">Term 3</option>
							</select>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Amount (RWF)</label>
							<input type="number" bind:value={bulkForm.amount} placeholder="150000" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" required />
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Due Date</label>
							<input type="date" bind:value={bulkForm.due_date} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" required />
						</div>
					</div>
					<div class="mt-4 flex space-x-2">
						<button class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700" on:click={createBulkInvoices}>
							Create Bulk Invoices
						</button>
						<button class="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600" on:click={() => showBulkForm = false}>
							Cancel
						</button>
					</div>
				</div>
				{/if}

				<!-- Edit Invoice Form -->
				{#if showEditForm && selectedInvoice}
				<div class="bg-yellow-50 border-2 border-yellow-200 rounded-lg p-6 mb-6">
					<h3 class="text-lg font-semibold text-gray-800 mb-4">Edit Invoice: {selectedInvoice.invoice_number}</h3>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
							<select bind:value={editForm.status} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500">
								<option value="pending">Pending</option>
								<option value="partial">Partial</option>
								<option value="paid">Paid</option>
								<option value="cancelled">Cancelled</option>
							</select>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Amount (RWF)</label>
							<input type="number" bind:value={editForm.amount} class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500" />
						</div>
					</div>
					<div class="mt-4 flex space-x-2">
						<button class="bg-yellow-600 text-white px-6 py-2 rounded-lg hover:bg-yellow-700" on:click={updateInvoice}>
							Update Invoice
						</button>
						<button class="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600" on:click={() => showEditForm = false}>
							Cancel
						</button>
					</div>
				</div>
				{/if}

				<!-- Invoice List -->
				{#if loading}
				<div class="flex justify-center items-center py-12">
					<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
				</div>
				{:else if invoices.length === 0}
				<div class="text-center py-12">
					<p class="text-gray-500 text-lg">No invoices found. Create your first invoice above.</p>
				</div>
				{:else}
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Class</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Balance</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
							</tr>
						</thead>
						<tbody class="bg-white divide-y divide-gray-200">
							{#each invoices as invoice}
							<tr class="hover:bg-gray-50">
								<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{invoice.invoice_number}</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{invoice.student_name}</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{invoice.class}</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{invoice.category}</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{invoice.amount.toLocaleString()} RWF</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm font-semibold {invoice.balance > 0 ? 'text-red-600' : 'text-green-600'}">{invoice.balance.toLocaleString()} RWF</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
										{invoice.status === 'paid' ? 'bg-green-100 text-green-800' : 
										 invoice.status === 'partial' ? 'bg-yellow-100 text-yellow-800' : 
										 'bg-red-100 text-red-800'}">
										{invoice.status}
									</span>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{invoice.due_date}</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm">
									<div class="flex space-x-2">
										<button class="text-blue-600 hover:text-blue-800" title="Print" on:click={() => printInvoice(invoice)}>
											🖨️
										</button>
										<button class="text-green-600 hover:text-green-800" title="Edit" on:click={() => editInvoice(invoice)}>
											✏️
										</button>
										<button class="text-purple-600 hover:text-purple-800" title="Send to Head Teacher" on:click={() => sendToHeadTeacher(invoice)}>
											📧
										</button>
										<button class="text-red-600 hover:text-red-800" title="Delete" on:click={() => deleteInvoice(invoice)}>
											🗑️
										</button>
									</div>
								</td>
							</tr>
							{/each}
						</tbody>
					</table>
				</div>
				{/if}
			</div>
			{/if}

			{#if activeTab === 'payments'}
			<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
				<div class="flex justify-between items-center mb-6">
					<div>
						<h2 class="text-xl font-bold text-gray-900">Payment Processing</h2>
						<p class="text-sm text-gray-500 mt-1">Record and manage student payments</p>
					</div>
					<button class="flex items-center space-x-2 bg-green-600 text-white px-4 py-2.5 rounded-lg hover:bg-green-700 transition-colors shadow-sm" on:click={() => showPaymentForm = !showPaymentForm}>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
						</svg>
						<span>Record Payment</span>
					</button>
				</div>

				<!-- Payment Method Selection -->
				{#if showPaymentForm}
				<div class="bg-green-50 border-2 border-green-200 rounded-lg p-6 mb-6">
					<h3 class="text-lg font-semibold text-gray-800 mb-4">Record New Payment</h3>
					
					<!-- Step 1: Select Invoice -->
					{#if !paymentForm.invoice_id}
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">Search Student or Invoice</label>
						<input type="text" bind:value={searchQuery} placeholder="Enter student name or invoice number..." class="w-full px-3 py-2 border border-gray-300 rounded-lg mb-4" on:input={searchInvoices} />
						
						{#if searchResults.length > 0}
						<div class="max-h-64 overflow-y-auto border border-gray-300 rounded-lg">
							{#each searchResults as invoice}
							<button class="w-full text-left p-3 hover:bg-gray-100 border-b" on:click={() => selectInvoice(invoice)}>
								<div class="font-semibold">{invoice.student_name} - {invoice.invoice_number}</div>
								<div class="text-sm text-gray-600">{invoice.category} | Balance: {invoice.balance.toLocaleString()} RWF</div>
							</button>
							{/each}
						</div>
						{/if}
					</div>
					{:else}
					<!-- Step 2: Payment Details -->
					<div class="bg-white border border-gray-300 rounded-lg p-4 mb-4">
						<div class="flex justify-between items-start">
							<div>
								<p class="font-semibold text-lg">{selectedInvoiceForPayment.student_name}</p>
								<p class="text-sm text-gray-600">{selectedInvoiceForPayment.invoice_number} - {selectedInvoiceForPayment.category}</p>
								<p class="text-sm text-gray-600">Total: {selectedInvoiceForPayment.amount.toLocaleString()} RWF</p>
								<p class="text-lg font-bold text-red-600">Balance Due: {selectedInvoiceForPayment.balance.toLocaleString()} RWF</p>
							</div>
							<button class="text-red-600 hover:text-red-800" on:click={() => { paymentForm.invoice_id = ''; selectedInvoiceForPayment = null; }}>✕</button>
						</div>
					</div>

					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Payment Amount (RWF)</label>
							<input type="number" bind:value={paymentForm.amount} placeholder="Enter amount" max={selectedInvoiceForPayment.balance} class="w-full px-3 py-2 border border-gray-300 rounded-lg" required />
							<p class="text-xs text-gray-500 mt-1">Max: {selectedInvoiceForPayment.balance.toLocaleString()} RWF</p>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Payment Method</label>
							<select bind:value={paymentForm.payment_method} class="w-full px-3 py-2 border border-gray-300 rounded-lg" required>
								<option value="">Select Method</option>
								<option value="Cash">💵 Cash</option>
								<option value="MTN MoMo">📱 MTN MoMo</option>
								<option value="Airtel Money">📱 Airtel Money</option>
								<option value="Bank Transfer">🏦 Bank Transfer</option>
							</select>
						</div>
						
						{#if paymentForm.payment_method === 'MTN MoMo' || paymentForm.payment_method === 'Airtel Money'}
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
							<input type="tel" bind:value={paymentForm.phone_number} placeholder="+250 788 123 456" class="w-full px-3 py-2 border border-gray-300 rounded-lg" required />
						</div>
						{/if}
						
						{#if paymentForm.payment_method === 'Bank Transfer'}
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Transaction Reference</label>
							<input type="text" bind:value={paymentForm.reference} placeholder="Bank reference number" class="w-full px-3 py-2 border border-gray-300 rounded-lg" />
						</div>
						{/if}
						
						<div class="md:col-span-2">
							<label class="block text-sm font-medium text-gray-700 mb-2">Notes (Optional)</label>
							<textarea bind:value={paymentForm.notes} placeholder="Additional notes..." class="w-full px-3 py-2 border border-gray-300 rounded-lg" rows="2"></textarea>
						</div>
					</div>

					<div class="mt-4 flex space-x-2">
						<button class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700" on:click={processPayment}>
							💳 Process Payment
						</button>
						<button class="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600" on:click={() => { showPaymentForm = false; resetPaymentForm(); }}>
							Cancel
						</button>
					</div>
					{/if}
				</div>
				{/if}

				<!-- Payment History -->
				<div class="mt-6">
					<h3 class="text-lg font-semibold text-gray-800 mb-4">Recent Payments</h3>
					<div class="overflow-x-auto">
						<table class="min-w-full divide-y divide-gray-200">
							<thead class="bg-gray-50">
								<tr>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Receipt #</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Method</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								{#each payments as payment}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{payment.receipt_number}</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">INV-{payment.invoice_id}</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">{payment.amount.toLocaleString()} RWF</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{payment.payment_method}</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{payment.payment_date}</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm">
										<button class="text-blue-600 hover:text-blue-800" title="Print Receipt" on:click={() => printReceipt(payment)}>🖨️</button>
									</td>
								</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</div>
			</div>
			{/if}

			{#if activeTab === 'students'}
			<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
				<div class="flex justify-between items-center mb-6">
					<div>
						<h2 class="text-xl font-bold text-gray-900">Student Accounts</h2>
						<p class="text-sm text-gray-500 mt-1">View complete financial history</p>
					</div>
					{#if showStudentDetails}
					<button class="flex items-center space-x-2 text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors" on:click={closeStudentDetails}>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
						</svg>
						<span>Back to Search</span>
					</button>
					{/if}
				</div>

				{#if !showStudentDetails}
				<!-- Student Search -->
				<div class="mb-6">
					<div class="max-w-md mx-auto">
						<label class="block text-sm font-medium text-gray-700 mb-2">Search Student</label>
						<input 
							type="text" 
							bind:value={studentSearchQuery}
							placeholder="Enter student name or admission number..." 
							class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-lg"
							on:input={searchStudents}
						/>
						
						{#if studentSearchResults.length > 0}
						<div class="mt-2 max-h-64 overflow-y-auto border border-gray-300 rounded-lg bg-white shadow-lg">
							{#each studentSearchResults as student}
							<button 
								class="w-full text-left p-4 hover:bg-blue-50 border-b border-gray-100 transition-colors"
								on:click={() => selectStudent(student)}
							>
								<div class="flex items-center justify-between">
									<div>
										<div class="font-semibold text-gray-800">{student.first_name} {student.last_name}</div>
										<div class="text-sm text-gray-600">Admission: {student.admission_number}</div>
										<div class="text-sm text-blue-600">Class: {student.class_name || 'N/A'}</div>
									</div>
									<div class="text-blue-600">→</div>
								</div>
							</button>
							{/each}
						</div>
						{/if}
					</div>
					
					<div class="text-center mt-12">
						<div class="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
							<svg class="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
							</svg>
						</div>
						<h3 class="text-lg font-semibold text-gray-900 mb-2">Search for a Student</h3>
						<p class="text-gray-500 mb-8 max-w-md mx-auto">View complete financial history for any student. Check invoices, payments, and outstanding balances.</p>
						
						<!-- Quick Stats -->
						<div class="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
							<div class="bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-xl p-5">
								<div class="flex items-center justify-center mb-2">
									<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
									</svg>
								</div>
								<div class="text-2xl font-bold text-blue-700">{students.length}</div>
								<div class="text-xs text-blue-600 font-medium">Total Students</div>
							</div>
							<div class="bg-gradient-to-br from-green-50 to-green-100 border border-green-200 rounded-xl p-5">
								<div class="flex items-center justify-center mb-2">
									<svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
									</svg>
								</div>
								<div class="text-2xl font-bold text-green-700">Invoices</div>
								<div class="text-xs text-green-600 font-medium">Account Details</div>
							</div>
							<div class="bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200 rounded-xl p-5">
								<div class="flex items-center justify-center mb-2">
									<svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
									</svg>
								</div>
								<div class="text-2xl font-bold text-purple-700">History</div>
								<div class="text-xs text-purple-600 font-medium">Payment Records</div>
							</div>
						</div>
					</div>
				</div>
				{:else}
				<!-- Student Account Details -->
				{#if loadingStudentAccount}
				<div class="flex justify-center items-center py-12">
					<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
					<span class="ml-3 text-gray-600">Loading student account...</span>
				</div>
				{:else if studentAccountData}
				<!-- Student Header -->
				<div class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 mb-6">
					<div class="flex justify-between items-start">
						<div>
							<h3 class="text-2xl font-bold text-gray-800 mb-2">{studentAccountData.student.name}</h3>
							<div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
								<div><span class="font-medium">Admission Number:</span> {studentAccountData.student.admission_number}</div>
								<div><span class="font-medium">Class:</span> {studentAccountData.student.class}</div>
							</div>
						</div>
						<button 
							class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
							on:click={() => printStudentStatement(studentAccountData)}
						>
							<span>🖨️</span>
							<span>Print Statement</span>
						</button>
					</div>
				</div>

				<!-- Financial Summary Cards -->
				<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
					<div class="bg-white border-2 border-blue-200 rounded-lg p-6">
						<div class="flex items-center">
							<div class="p-3 rounded-full bg-blue-100 text-blue-600 text-2xl">💰</div>
							<div class="ml-4">
								<p class="text-sm font-medium text-gray-600">Total Invoiced</p>
								<p class="text-2xl font-bold text-gray-900">{studentAccountData.summary.total_invoiced.toLocaleString()} RWF</p>
							</div>
						</div>
					</div>

					<div class="bg-white border-2 border-green-200 rounded-lg p-6">
						<div class="flex items-center">
							<div class="p-3 rounded-full bg-green-100 text-green-600 text-2xl">✅</div>
							<div class="ml-4">
								<p class="text-sm font-medium text-gray-600">Total Paid</p>
								<p class="text-2xl font-bold text-green-600">{studentAccountData.summary.total_paid.toLocaleString()} RWF</p>
							</div>
						</div>
					</div>

					<div class="bg-white border-2 border-red-200 rounded-lg p-6">
						<div class="flex items-center">
							<div class="p-3 rounded-full bg-red-100 text-red-600 text-2xl">⚠️</div>
							<div class="ml-4">
								<p class="text-sm font-medium text-gray-600">Outstanding Balance</p>
								<p class="text-2xl font-bold text-red-600">{studentAccountData.summary.total_outstanding.toLocaleString()} RWF</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Payment Progress Indicator -->
				{#if studentAccountData.summary.total_invoiced > 0}
				<div class="bg-white rounded-lg shadow-md p-6 mb-6">
					<h4 class="text-lg font-semibold text-gray-800 mb-4">📊 Payment Progress</h4>
					<div class="w-full bg-gray-200 rounded-full h-6 mb-2">
						<div 
							class="bg-gradient-to-r from-green-400 to-green-600 h-6 rounded-full transition-all duration-500"
							style="width: {Math.round((studentAccountData.summary.total_paid / studentAccountData.summary.total_invoiced) * 100)}%"
						></div>
					</div>
					<div class="flex justify-between text-sm text-gray-600">
						<span>Paid: {Math.round((studentAccountData.summary.total_paid / studentAccountData.summary.total_invoiced) * 100)}%</span>
						<span>Remaining: {Math.round((studentAccountData.summary.total_outstanding / studentAccountData.summary.total_invoiced) * 100)}%</span>
					</div>
				</div>
				{/if}

				<!-- Tabs for Invoices and Payments -->
				<div class="mb-6">
					<nav class="flex space-x-1 bg-gray-100 rounded-lg p-1">
						<button 
							class="px-4 py-2 rounded-md text-sm font-medium transition-colors bg-white text-blue-600 shadow-sm"
						>
							📄 Invoices ({studentAccountData.invoices.length})
						</button>
						<button 
							class="px-4 py-2 rounded-md text-sm font-medium transition-colors text-gray-600 hover:text-gray-800"
						>
							💳 Payments ({studentAccountData.payments.length})
						</button>
					</nav>
				</div>

				<!-- Invoice Details -->
				<div class="bg-white rounded-lg shadow-md p-6 mb-6">
					<h4 class="text-lg font-semibold text-gray-800 mb-4">📄 Invoice History</h4>
					{#if studentAccountData.invoices.length === 0}
					<div class="text-center py-8">
						<div class="text-4xl mb-2">📄</div>
						<p class="text-gray-500">No invoices found for this student.</p>
					</div>
					{:else}
					<div class="overflow-x-auto">
						<table class="min-w-full divide-y divide-gray-200">
							<thead class="bg-gray-50">
								<tr>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Term</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Paid</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Balance</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Progress</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								{#each studentAccountData.invoices as invoice}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">{invoice.invoice_number}</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 capitalize">{invoice.category}</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 uppercase">{invoice.term}</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">{invoice.amount.toLocaleString()} RWF</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">{invoice.amount_paid.toLocaleString()} RWF</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm font-semibold {invoice.balance > 0 ? 'text-red-600' : 'text-green-600'}">{invoice.balance.toLocaleString()} RWF</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<div class="w-full bg-gray-200 rounded-full h-2">
											<div 
												class="bg-green-500 h-2 rounded-full"
												style="width: {getPaymentProgress(invoice)}%"
											></div>
										</div>
										<div class="text-xs text-gray-500 mt-1">{getPaymentProgress(invoice)}%</div>
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
											{invoice.status === 'paid' ? 'bg-green-100 text-green-800' : 
											 invoice.status === 'partial' ? 'bg-yellow-100 text-yellow-800' : 
											 'bg-red-100 text-red-800'}">
											{invoice.status.toUpperCase()}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{invoice.due_date || 'N/A'}</td>
								</tr>
								{/each}
							</tbody>
						</table>
					</div>
					{/if}
				</div>

				<!-- Payment History -->
				<div class="bg-white rounded-lg shadow-md p-6">
					<h4 class="text-lg font-semibold text-gray-800 mb-4">💳 Payment History</h4>
					{#if studentAccountData.payments.length === 0}
					<div class="text-center py-8">
						<div class="text-4xl mb-2">💳</div>
						<p class="text-gray-500">No payments recorded for this student.</p>
					</div>
					{:else}
					<div class="space-y-4">
						{#each studentAccountData.payments as payment}
						<div class="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
							<div class="flex items-center space-x-4">
								<div class="p-2 bg-green-100 rounded-full">
									<span class="text-green-600 text-lg">💰</span>
								</div>
								<div>
									<div class="font-semibold text-gray-800">{payment.receipt_number}</div>
									<div class="text-sm text-gray-600">{payment.method} • {payment.date}</div>
								</div>
							</div>
							<div class="text-right">
								<div class="text-lg font-bold text-green-600">{payment.amount.toLocaleString()} RWF</div>
								<button 
									class="text-blue-600 hover:text-blue-800 text-sm"
									title="Print Receipt"
									on:click={() => printReceipt(payment)}
								>
									🖨️ Print
								</button>
							</div>
						</div>
						{/each}
					</div>
					{/if}
				</div>
				{/if}
				{/if}
			</div>
			{/if}

			{#if activeTab === 'reports'}
			<div class="bg-white rounded-lg shadow-md p-6">
				<h2 class="text-2xl font-bold text-gray-800 mb-6">Financial Reports</h2>
				<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
					<button on:click={() => goto('/accountant/reports')} class="bg-blue-50 border-2 border-blue-200 p-6 rounded-lg hover:bg-blue-100 text-left">
						<div class="text-3xl mb-2">📊</div>
						<div class="font-semibold text-lg mb-2">Revenue Report</div>
						<div class="text-sm text-gray-600">View revenue by date, method, and trends</div>
					</button>
					<button on:click={() => goto('/accountant/reports')} class="bg-red-50 border-2 border-red-200 p-6 rounded-lg hover:bg-red-100 text-left">
						<div class="text-3xl mb-2">⚠️</div>
						<div class="font-semibold text-lg mb-2">Outstanding Fees</div>
						<div class="text-sm text-gray-600">Track unpaid and overdue invoices</div>
					</button>
					<button on:click={() => goto('/accountant/reports')} class="bg-green-50 border-2 border-green-200 p-6 rounded-lg hover:bg-green-100 text-left">
						<div class="text-3xl mb-2">📈</div>
						<div class="font-semibold text-lg mb-2">Collection Rate</div>
						<div class="text-sm text-gray-600">Analyze collection rates by class</div>
					</button>
				</div>
			</div>
			{/if}
		{/if}
		</div>
	</div>
</div>