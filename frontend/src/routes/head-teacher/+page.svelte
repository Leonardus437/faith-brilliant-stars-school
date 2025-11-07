<script>
	import { onMount } from 'svelte';
	import { api } from '$lib/utils/api.js';
	import { authStore } from '$lib/stores/auth.js';
	import { goto } from '$app/navigation';
	import { t } from '$lib/i18n/index.js';
	import LanguageToggle from '$lib/components/LanguageToggle.svelte';

	let dashboardData = null;
	let loading = true;
	let currentUser = null;

	authStore.subscribe(value => {
		currentUser = value.user;
	});

	onMount(async () => {
		authStore.init();
		if (!currentUser || currentUser.role !== 'head_teacher') {
			goto('/login');
			return;
		}
		await loadDashboard();
	});

	async function loadDashboard() {
		try {
			const response = await api.get('/api/admin/dashboard');
			dashboardData = response.data;
			loading = false;
		} catch (error) {
			console.error('Failed to load dashboard:', error);
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>{$t('headTeacher')} - {$t('schoolName')}</title>
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
						<div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-lg">
							FBS
						</div>
						<div>
							<h1 class="text-2xl font-bold text-gray-900">{$t('headTeacherDashboard')}</h1>
							<p class="text-sm text-gray-600">{$t('schoolName')}</p>
						</div>
					</div>
					<div class="flex items-center space-x-3">
						<LanguageToggle />
						<div class="text-right">
							<p class="text-sm font-medium text-gray-700">{currentUser?.full_name || $t('headTeacher')}</p>
							<p class="text-xs text-gray-500">{$t('schoolAdministrator')}</p>
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
				<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
			</div>
		{:else if dashboardData}
			<!-- Overview Cards -->
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
				<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-5 hover:shadow-2xl transition-all transform hover:scale-[1.02]">
					<div class="flex items-center justify-between mb-3">
						<div class="p-2.5 rounded-lg bg-blue-50">
							<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
							</svg>
						</div>
					</div>
					<p class="text-sm font-medium text-gray-600 mb-1">{$t('totalStudents')}</p>
					<p class="text-2xl font-bold text-gray-900">{dashboardData.overview.total_students}</p>
					<p class="text-xs text-gray-500 mt-1">{$t('enrolled')}</p>
				</div>

				<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-5 hover:shadow-2xl transition-all transform hover:scale-[1.02]">
					<div class="flex items-center justify-between mb-3">
						<div class="p-2.5 rounded-lg bg-green-50">
							<svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
							</svg>
						</div>
					</div>
					<p class="text-sm font-medium text-gray-600 mb-1">{$t('totalTeachers')}</p>
					<p class="text-2xl font-bold text-gray-900">{dashboardData.overview.total_teachers}</p>
					<p class="text-xs text-gray-500 mt-1">{$t('staffMembers')}</p>
				</div>

				<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-5 hover:shadow-2xl transition-all transform hover:scale-[1.02]">
					<div class="flex items-center justify-between mb-3">
						<div class="p-2.5 rounded-lg bg-purple-50">
							<svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
							</svg>
						</div>
					</div>
					<p class="text-sm font-medium text-gray-600 mb-1">{$t('totalRevenue')}</p>
					<p class="text-2xl font-bold text-gray-900">{dashboardData.overview.total_revenue.toLocaleString()}</p>
					<p class="text-xs text-gray-500 mt-1">RWF</p>
				</div>

				<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-5 hover:shadow-2xl transition-all transform hover:scale-[1.02]">
					<div class="flex items-center justify-between mb-3">
						<div class="p-2.5 rounded-lg bg-amber-50">
							<svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
							</svg>
						</div>
					</div>
					<p class="text-sm font-medium text-gray-600 mb-1">{$t('attendanceRate')}</p>
					<p class="text-2xl font-bold text-gray-900">{dashboardData.overview.attendance_rate}%</p>
					<p class="text-xs text-gray-500 mt-1">{$t('average')}</p>
				</div>
			</div>

			<!-- Quick Actions -->
			<div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 mb-6">
				<h3 class="text-lg font-semibold text-gray-900 mb-4">{$t('quickActions')}</h3>
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
					<button on:click={() => goto('/admin/students')} class="group flex items-center space-x-3 p-4 rounded-lg border-2 border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all transform hover:scale-[1.02]">
						<div class="p-2 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors">
							<svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
							</svg>
						</div>
						<div class="text-left">
							<p class="font-semibold text-gray-900">{$t('addStudent')}</p>
							<p class="text-xs text-gray-500">{$t('enrollNewStudent')}</p>
						</div>
					</button>

					<button on:click={() => goto('/admin/teachers')} class="group flex items-center space-x-3 p-4 rounded-lg border-2 border-gray-200 hover:border-green-500 hover:bg-green-50 transition-all transform hover:scale-[1.02]">
						<div class="p-2 bg-green-100 rounded-lg group-hover:bg-green-200 transition-colors">
							<svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
							</svg>
						</div>
						<div class="text-left">
							<p class="font-semibold text-gray-900">{$t('addTeacher')}</p>
							<p class="text-xs text-gray-500">{$t('hireNewStaff')}</p>
						</div>
					</button>

					<button on:click={() => goto('/admin/classes')} class="group flex items-center space-x-3 p-4 rounded-lg border-2 border-gray-200 hover:border-purple-500 hover:bg-purple-50 transition-all transform hover:scale-[1.02]">
						<div class="p-2 bg-purple-100 rounded-lg group-hover:bg-purple-200 transition-colors">
							<svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
							</svg>
						</div>
						<div class="text-left">
							<p class="font-semibold text-gray-900">{$t('manageClasses')}</p>
							<p class="text-xs text-gray-500">{$t('viewAllClasses')}</p>
						</div>
					</button>

					<button on:click={() => goto('/head-teacher/finances')} class="group flex items-center space-x-3 p-4 rounded-lg border-2 border-gray-200 hover:border-amber-500 hover:bg-amber-50 transition-all transform hover:scale-[1.02]">
						<div class="p-2 bg-amber-100 rounded-lg group-hover:bg-amber-200 transition-colors">
							<svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
							</svg>
						</div>
						<div class="text-left">
							<p class="font-semibold text-gray-900">{$t('viewFinances')}</p>
							<p class="text-xs text-gray-500">{$t('financialReports')}</p>
						</div>
					</button>
				</div>
			</div>
		{/if}
		</div>
	</div>
</div>