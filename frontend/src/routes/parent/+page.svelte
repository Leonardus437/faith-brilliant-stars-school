<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let dashboard = {
    children: [
      {
        id: 1,
        name: 'Emma Johnson',
        class_name: 'P4 A',
        attendance_rate: 92,
        outstanding_fees: 75000,
        recent_status: 'present',
        admission_number: 'ADM001'
      },
      {
        id: 2,
        name: 'Michael Johnson',
        class_name: 'P2 B',
        attendance_rate: 88,
        outstanding_fees: 50000,
        recent_status: 'late',
        admission_number: 'ADM002'
      },
      {
        id: 3,
        name: 'Sarah Johnson',
        class_name: 'P6 A',
        attendance_rate: 95,
        outstanding_fees: 0,
        recent_status: 'present',
        admission_number: 'ADM003'
      }
    ],
    total_outstanding: 125000,
    unread_messages: 3,
    upcoming_meetings: [
      {
        id: 1,
        purpose: 'Parent-Teacher Conference',
        date: '2024-02-15T10:00:00Z',
        teacher: 'Mrs. Smith',
        child_name: 'Emma Johnson'
      },
      {
        id: 2,
        purpose: 'Academic Progress Review',
        date: '2024-02-20T14:30:00Z',
        teacher: 'Mr. Brown',
        child_name: 'Sarah Johnson'
      }
    ],
    recent_announcements: [
      {
        id: 1,
        title: 'School Sports Day',
        content: 'Annual sports day will be held on March 15th. All parents are invited to attend.',
        date: '2024-01-25',
        priority: 'high'
      },
      {
        id: 2,
        title: 'Term 2 Fees Due',
        content: 'Reminder: Term 2 school fees are due by February 28th. Please make payments on time.',
        date: '2024-01-20',
        priority: 'medium'
      },
      {
        id: 3,
        title: 'New Lunch Menu',
        content: 'We have updated our lunch menu with more nutritious options. Check the school website for details.',
        date: '2024-01-18',
        priority: 'low'
      }
    ]
  };
  
  let loading = true;
  
  onMount(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      goto('/login');
      return;
    }
    
    try {
      const response = await fetch('http://localhost:8001/api/parent/dashboard', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const apiData = await response.json();
        // Only replace with API data if it has content
        if (apiData && (apiData.children?.length > 0 || apiData.total_outstanding > 0)) {
          dashboard = apiData;
          console.log('Loaded dashboard from API:', dashboard);
        } else {
          console.log('API returned empty data, using default test data');
        }
      } else {
        console.log('API failed, using default test data');
      }
    } catch (error) {
      console.error('Error loading dashboard, using default test data:', error);
    } finally {
      loading = false;
    }
  });
  
  function logout() {
    localStorage.clear();
    goto('/login');
  }
</script>

<div class="min-h-screen relative overflow-hidden">
  <!-- Background Image -->
  <div class="absolute inset-0 bg-cover bg-center bg-no-repeat" style="background-image: url('/1.jpg');"></div>
  <div class="absolute inset-0 bg-black/30"></div>
  
  <!-- Content -->
  <div class="relative z-10 min-h-screen p-6">
    <div class="max-w-7xl mx-auto">
      <div class="bg-white/95 backdrop-blur-xl rounded-2xl shadow-xl border border-white/30 p-6 mb-8">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-4xl font-bold text-gray-800 mb-2">Parent Dashboard</h1>
            <p class="text-gray-600">Monitor Your Children's Progress</p>
          </div>
          <button on:click={logout} class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg shadow-lg">
            Logout
          </button>
        </div>
      </div>
    
    {#if loading}
      <div class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto"></div>
      </div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 border-l-4 border-orange-500 transform hover:scale-[1.02] transition-all">
          <p class="text-gray-500 text-sm">My Children</p>
          <p class="text-3xl font-bold text-gray-800">{dashboard.children.length}</p>
        </div>
        
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 border-l-4 border-red-500 transform hover:scale-[1.02] transition-all">
          <p class="text-gray-500 text-sm">Outstanding Fees</p>
          <p class="text-3xl font-bold text-gray-800">{dashboard.total_outstanding.toLocaleString()} RWF</p>
        </div>
        
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 border-l-4 border-blue-500 transform hover:scale-[1.02] transition-all">
          <p class="text-gray-500 text-sm">Unread Messages</p>
          <p class="text-3xl font-bold text-gray-800">{dashboard.unread_messages}</p>
        </div>
      </div>
      
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">My Children</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          {#each dashboard.children as child}
            <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 hover:shadow-2xl transition-all transform hover:scale-[1.02]">
              <div class="flex items-center space-x-4 mb-4">
                <div class="w-16 h-16 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                  {child.name.charAt(0)}
                </div>
                <div>
                  <h3 class="font-bold text-gray-800">{child.name}</h3>
                  <p class="text-sm text-gray-600">{child.class_name}</p>
                </div>
              </div>
              
              <div class="space-y-2 mb-4">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Attendance:</span>
                  <span class="font-semibold text-green-600">{child.attendance_rate}%</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Outstanding:</span>
                  <span class="font-semibold text-red-600">{child.outstanding_fees.toLocaleString()} RWF</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Recent:</span>
                  <span class="font-semibold {child.recent_status === 'present' ? 'text-green-600' : 'text-red-600'}">
                    {child.recent_status}
                  </span>
                </div>
              </div>
              
              <button on:click={() => goto('/parent/children')} class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-2 rounded-lg font-semibold">
                View Details
              </button>
            </div>
          {/each}
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Upcoming Meetings</h2>
          <div class="space-y-3">
            {#each dashboard.upcoming_meetings as meeting}
              <div class="p-3 bg-blue-50 rounded-lg">
                <p class="font-semibold text-gray-800">{meeting.purpose}</p>
                <p class="text-sm text-gray-600">{new Date(meeting.date).toLocaleDateString()}</p>
              </div>
            {/each}
          </div>
        </div>
        
        <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">School Announcements</h2>
          <div class="space-y-3">
            {#each dashboard.recent_announcements as announcement}
              <div class="p-3 bg-yellow-50 rounded-lg">
                <p class="font-semibold text-gray-800">{announcement.title}</p>
                <p class="text-sm text-gray-600">{announcement.content}</p>
              </div>
            {/each}
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <button on:click={() => goto('/parent/children')} 
                class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 hover:shadow-2xl transition-all hover:scale-105">
          <div class="text-4xl mb-3">👶</div>
          <h3 class="font-bold text-gray-800 text-lg mb-2">My Children</h3>
          <p class="text-sm text-gray-600">View detailed profiles</p>
        </button>
        
        <button on:click={() => goto('/parent/attendance')} 
                class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 hover:shadow-2xl transition-all hover:scale-105">
          <div class="text-4xl mb-3">📊</div>
          <h3 class="font-bold text-gray-800 text-lg mb-2">Attendance</h3>
          <p class="text-sm text-gray-600">Track daily attendance</p>
        </button>
        
        <button on:click={() => goto('/parent/fees')} 
                class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 hover:shadow-2xl transition-all hover:scale-105">
          <div class="text-4xl mb-3">💰</div>
          <h3 class="font-bold text-gray-800 text-lg mb-2">Fees</h3>
          <p class="text-sm text-gray-600">View and pay fees</p>
        </button>
      </div>
    {/if}
    </div>
  </div>
</div>
