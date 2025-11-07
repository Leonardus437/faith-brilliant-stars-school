<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth.js';
	import { t } from '$lib/i18n/index.js';

	let currentUser = null;
	let loading = true;
	let selectedPeriod = 'current_term';
	let selectedReport = 'overview';

	// Sample financial data
	let financialData = {
		overview: {
			total_revenue: 45750000,
			total_collected: 38250000,
			outstanding_fees: 7500000,
			collection_rate: 83.6,
			monthly_growth: 12.5
		},
		revenue_breakdown: [
			{ category: 'Tuition Fees', amount: 35000000, percentage: 76.5 },
			{ category: 'Registration Fees', amount: 4500000, percentage: 9.8 },
			{ category: 'Uniform Sales', amount: 3250000, percentage: 7.1 },
			{ category: 'Transport Fees', amount: 2000000, percentage: 4.4 },
			{ category: 'Other Fees', amount: 1000000, percentage: 2.2 }
		],
		monthly_trends: [
			{ month: 'Jan', revenue: 3800000, collected: 3200000 },
			{ month: 'Feb', revenue: 3900000, collected: 3400000 },
			{ month: 'Mar', revenue: 4100000, collected: 3650000 },
			{ month: 'Apr', revenue: 4200000, collected: 3800000 },
			{ month: 'May', revenue: 4300000, collected: 3900000 },
			{ month: 'Jun', revenue: 4450000, collected: 4100000 }
		],
		class_performance: [
			{ class: 'P1 A', students: 15, total_fees: 4500000, collected: 4200000, rate: 93.3 },
			{ class: 'P2 A', students: 12, total_fees: 3600000, collected: 3240000, rate: 90.0 },
			{ class: 'P3 A', students: 10, total_fees: 3000000, collected: 2550000, rate: 85.0 },
			{ class: 'P4 A', students: 8, total_fees: 2400000, collected: 1920000, rate: 80.0 },
			{ class: 'P5 A', students: 9, total_fees: 2700000, collected: 2025000, rate: 75.0 },
			{ class: 'P6 A', students: 6, total_fees: 1800000, collected: 1350000, rate: 75.0 }
		],
		payment_methods: [
			{ method: 'MTN MoMo', amount: 18500000, percentage: 48.4 },
			{ method: 'Cash', amount: 12200000, percentage: 31.9 },
			{ method: 'Bank Transfer', amount: 5100000, percentage: 13.3 },
			{ method: 'Airtel Money', amount: 2450000, percentage: 6.4 }
		]
	};

	authStore.subscribe(value => {
		currentUser = value.user;
	});

	onMount(async () => {
		authStore.init();
		if (!currentUser || currentUser.role !== 'head_teacher') {
			goto('/login');
			return;
		}
		loading = false;
	});

	function formatCurrency(amount) {
		return new Intl.NumberFormat('rw-RW', {
			style: 'currency',
			currency: 'RWF',
			minimumFractionDigits: 0
		}).format(amount);
	}

	function exportReport() {
		alert('Report export functionality would be implemented here');
	}
</script>

<svelte:head>
	<title>Financial Reports - {$t('schoolName')}</title>
</svelte:head>

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
						<button on:click={() => goto('/head-teacher')} class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
							<svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
							</svg>
						</button>
						<div>
							<h1 class="text-2xl font-bold text-gray-900">Financial Reports</h1>
							<p class="text-sm text-gray-600">Comprehensive financial analytics and insights</p>
						</div>
					</div>
					<div class="flex items-center space-x-3">
						<select bind:value={selectedPeriod} class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
							<option value="current_term">Current Term</option>
							<option value="last_term">Last Term</option>
							<option value="current_year">Current Year</option>
							<option value="last_year">Last Year</option>
						</select>
						<button on:click={exportReport} class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
							Export Report
						</button>
					</div>
				</div>
			</div>
		</div>

		<div class="container mx-auto px-6 py-6">
			{#if loading}
				<div class="flex justify-center items-center h-64">
					<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
				</div>
			{:else}
				<!-- Report Navigation -->
				<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 mb-6">
					<div class="flex space-x-4 overflow-x-auto">
						<button on:click={() => selectedReport = 'overview'} class="px-4 py-2 rounded-lg font-medium transition-colors {selectedReport === 'overview' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}">
							Overview
						</button>
						<button on:click={() => selectedReport = 'revenue'} class="px-4 py-2 rounded-lg font-medium transition-colors {selectedReport === 'revenue' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}">
							Revenue Analysis
						</button>
						<button on:click={() => selectedReport = 'collections'} class="px-4 py-2 rounded-lg font-medium transition-colors {selectedReport === 'collections' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}">
							Collections
						</button>
						<button on:click={() => selectedReport = 'trends'} class="px-4 py-2 rounded-lg font-medium transition-colors {selectedReport === 'trends' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}">
							Trends
						</button>
					</div>
				</div>

				{#if selectedReport === 'overview'}
					<!-- Financial Overview -->
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
						<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
							<div class="flex items-center justify-between mb-4">
								<div class="p-3 bg-green-100 rounded-lg">
									<svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
									</svg>
								</div>
								<span class="text-xs text-green-600 bg-green-100 px-2 py-1 rounded-full">+{financialData.overview.monthly_growth}%</span>
							</div>
							<h3 class="text-sm font-medium text-gray-600 mb-1">Total Revenue</h3>
							<p class="text-2xl font-bold text-gray-900">{formatCurrency(financialData.overview.total_revenue)}</p>
						</div>

						<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
							<div class="flex items-center justify-between mb-4">
								<div class="p-3 bg-blue-100 rounded-lg">
									<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
									</svg>
								</div>
							</div>
							<h3 class="text-sm font-medium text-gray-600 mb-1">Amount Collected</h3>
							<p class="text-2xl font-bold text-gray-900">{formatCurrency(financialData.overview.total_collected)}</p>
						</div>

						<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
							<div class="flex items-center justify-between mb-4">
								<div class="p-3 bg-red-100 rounded-lg">
									<svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z"/>
									</svg>
								</div>
							</div>
							<h3 class="text-sm font-medium text-gray-600 mb-1">Outstanding Fees</h3>
							<p class="text-2xl font-bold text-gray-900">{formatCurrency(financialData.overview.outstanding_fees)}</p>
						</div>

						<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
							<div class="flex items-center justify-between mb-4">
								<div class="p-3 bg-purple-100 rounded-lg">
									<svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
									</svg>
								</div>
							</div>
							<h3 class="text-sm font-medium text-gray-600 mb-1">Collection Rate</h3>
							<p class="text-2xl font-bold text-gray-900">{financialData.overview.collection_rate}%</p>
						</div>
					</div>

					<!-- Class Performance -->
					<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
						<h3 class="text-lg font-semibold text-gray-900 mb-4">Fee Collection by Class</h3>
						<div class="overflow-x-auto">
							<table class="w-full">
								<thead>
									<tr class="border-b border-gray-200">
										<th class="text-left py-3 px-4 font-medium text-gray-600">Class</th>
										<th class="text-left py-3 px-4 font-medium text-gray-600">Students</th>
										<th class="text-left py-3 px-4 font-medium text-gray-600">Total Fees</th>
										<th class="text-left py-3 px-4 font-medium text-gray-600">Collected</th>
										<th class="text-left py-3 px-4 font-medium text-gray-600">Rate</th>
									</tr>
								</thead>
								<tbody>
									{#each financialData.class_performance as classData}
										<tr class="border-b border-gray-100 hover:bg-gray-50">
											<td class="py-3 px-4 font-medium">{classData.class}</td>
											<td class="py-3 px-4">{classData.students}</td>
											<td class="py-3 px-4">{formatCurrency(classData.total_fees)}</td>
											<td class="py-3 px-4">{formatCurrency(classData.collected)}</td>
											<td class="py-3 px-4">
												<span class="px-2 py-1 rounded-full text-xs font-medium {classData.rate >= 90 ? 'bg-green-100 text-green-800' : classData.rate >= 80 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}">
													{classData.rate}%
												</span>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				{/if}

				{#if selectedReport === 'revenue'}
					<!-- Revenue Breakdown -->
					<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
						<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
							<h3 class="text-lg font-semibold text-gray-900 mb-4">Revenue by Category</h3>
							<div class="space-y-4">
								{#each financialData.revenue_breakdown as category}
									<div>
										<div class="flex justify-between items-center mb-2">
											<span class="text-sm font-medium text-gray-700">{category.category}</span>
											<span class="text-sm text-gray-600">{category.percentage}%</span>
										</div>
										<div class="w-full bg-gray-200 rounded-full h-2">
											<div class="bg-blue-600 h-2 rounded-full" style="width: {category.percentage}%"></div>
										</div>
										<div class="text-right mt-1">
											<span class="text-sm font-semibold text-gray-900">{formatCurrency(category.amount)}</span>
										</div>
									</div>
								{/each}
							</div>
						</div>

						<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
							<h3 class="text-lg font-semibold text-gray-900 mb-4">Payment Methods</h3>
							<div class="space-y-4">
								{#each financialData.payment_methods as method}
									<div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
										<div>
											<p class="font-medium text-gray-900">{method.method}</p>
											<p class="text-sm text-gray-600">{method.percentage}% of total</p>
										</div>
										<div class="text-right">
											<p class="font-semibold text-gray-900">{formatCurrency(method.amount)}</p>
										</div>
									</div>
								{/each}
							</div>
						</div>
					</div>
				{/if}

				{#if selectedReport === 'trends'}
					<!-- Monthly Trends -->
					<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
						<h3 class="text-lg font-semibold text-gray-900 mb-4">Monthly Revenue Trends</h3>
						<div class="overflow-x-auto">
							<table class="w-full">
								<thead>
									<tr class="border-b border-gray-200">
										<th class="text-left py-3 px-4 font-medium text-gray-600">Month</th>
										<th class="text-left py-3 px-4 font-medium text-gray-600">Expected Revenue</th>
										<th class="text-left py-3 px-4 font-medium text-gray-600">Collected</th>
										<th class="text-left py-3 px-4 font-medium text-gray-600">Collection Rate</th>
									</tr>
								</thead>
								<tbody>
									{#each financialData.monthly_trends as month}
										<tr class="border-b border-gray-100 hover:bg-gray-50">
											<td class="py-3 px-4 font-medium">{month.month}</td>
											<td class="py-3 px-4">{formatCurrency(month.revenue)}</td>
											<td class="py-3 px-4">{formatCurrency(month.collected)}</td>
											<td class="py-3 px-4">
												<span class="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
													{((month.collected / month.revenue) * 100).toFixed(1)}%
												</span>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				{/if}
			{/if}
		</div>
	</div>
</div>