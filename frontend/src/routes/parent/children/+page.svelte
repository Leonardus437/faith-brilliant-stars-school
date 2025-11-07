<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let children = [
    {
      id: 1,
      first_name: 'Emma',
      last_name: 'Johnson',
      class_name: 'P4 A',
      admission_number: 'ADM001',
      gender: 'female',
      date_of_birth: '2015-03-15',
      attendance_rate: 92,
      outstanding_fees: 75000,
      recent_status: 'present',
      teacher_name: 'Mrs. Smith',
      parent_phone: '+250788123456',
      emergency_contact: 'John Johnson - +250788654321'
    },
    {
      id: 2,
      first_name: 'Michael',
      last_name: 'Johnson',
      class_name: 'P2 B',
      admission_number: 'ADM002',
      gender: 'male',
      date_of_birth: '2017-07-22',
      attendance_rate: 88,
      outstanding_fees: 50000,
      recent_status: 'late',
      teacher_name: 'Mr. Brown',
      parent_phone: '+250788123456',
      emergency_contact: 'John Johnson - +250788654321'
    },
    {
      id: 3,
      first_name: 'Sarah',
      last_name: 'Johnson',
      class_name: 'P6 A',
      admission_number: 'ADM003',
      gender: 'female',
      date_of_birth: '2013-11-08',
      attendance_rate: 95,
      outstanding_fees: 0,
      recent_status: 'present',
      teacher_name: 'Ms. Davis',
      parent_phone: '+250788123456',
      emergency_contact: 'John Johnson - +250788654321'
    }
  ];
  let loading = false;
  let selectedChild = null;
  let showDetails = false;
  
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
          console.log('Loaded children from API:', children);
        } else {
          console.log('API returned empty data, using default test data');
        }
      } else {
        console.log('API failed, using default test data');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loading = false;
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-purple-50 p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800 mb-2">My Children</h1>
        <p class="text-gray-600">View detailed information about your children</p>
      </div>
      <button on:click={() => goto('/parent')} class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg">Back</button>
    </div>
    
    {#if loading}
      <div class="text-center py-12"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto"></div></div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each children as child}
          <div class="bg-white rounded-xl shadow-lg p-6">
            <div class="flex items-center space-x-4 mb-6">
              <div class="w-20 h-20 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
                {child.first_name?.charAt(0)}{child.last_name?.charAt(0)}
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-800">{child.first_name} {child.last_name}</h3>
                <p class="text-sm text-gray-600">{child.class_name}</p>
                <p class="text-xs text-gray-500">#{child.admission_number}</p>
              </div>
            </div>
            
            <div class="space-y-3">
              <div class="grid grid-cols-2 gap-3">
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-xs text-gray-500">Gender</p>
                  <p class="font-semibold text-gray-800 capitalize">{child.gender}</p>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-xs text-gray-500">Age</p>
                  <p class="font-semibold text-gray-800">{new Date().getFullYear() - new Date(child.date_of_birth).getFullYear()} years</p>
                </div>
              </div>
              <div class="p-3 bg-blue-50 rounded-lg">
                <p class="text-xs text-gray-500">Class Teacher</p>
                <p class="font-semibold text-blue-600">{child.teacher_name}</p>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div class="p-3 bg-green-50 rounded-lg">
                  <p class="text-xs text-gray-500">Attendance</p>
                  <p class="font-semibold text-green-600">{child.attendance_rate || 0}%</p>
                </div>
                <div class="p-3 bg-{child.outstanding_fees > 0 ? 'red' : 'green'}-50 rounded-lg">
                  <p class="text-xs text-gray-500">Fees Status</p>
                  <p class="font-semibold text-{child.outstanding_fees > 0 ? 'red' : 'green'}-600">
                    {child.outstanding_fees > 0 ? `${child.outstanding_fees.toLocaleString()} RWF` : 'Paid'}
                  </p>
                </div>
              </div>
            </div>
            
            <div class="mt-6 space-y-2">
              <div class="flex gap-2">
                <button on:click={() => goto(`/parent/attendance?child=${child.id}`)} class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium">📊 Attendance</button>
                <button on:click={() => goto(`/parent/fees?child=${child.id}`)} class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg text-sm font-medium">💰 Fees</button>
              </div>
              <button on:click={() => { selectedChild = child; showDetails = true; }} class="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 rounded-lg text-sm font-medium">👁️ View Details</button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
    
    <!-- Child Details Modal -->
    {#if showDetails && selectedChild}
      <div class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div class="p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-gray-800">Student Details</h2>
              <button on:click={() => showDetails = false} class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
            </div>
            
            <div class="flex items-center space-x-4 mb-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl">
              <div class="w-20 h-20 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
                {selectedChild.first_name?.charAt(0)}{selectedChild.last_name?.charAt(0)}
              </div>
              <div>
                <h3 class="text-2xl font-bold text-gray-800">{selectedChild.first_name} {selectedChild.last_name}</h3>
                <p class="text-lg text-gray-600">{selectedChild.class_name}</p>
                <p class="text-sm text-gray-500">Admission: {selectedChild.admission_number}</p>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-4">
                <h4 class="font-bold text-gray-800 text-lg">Personal Information</h4>
                <div class="space-y-3">
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Full Name</p>
                    <p class="font-semibold text-gray-800">{selectedChild.first_name} {selectedChild.last_name}</p>
                  </div>
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Date of Birth</p>
                    <p class="font-semibold text-gray-800">{new Date(selectedChild.date_of_birth).toLocaleDateString()}</p>
                  </div>
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Gender</p>
                    <p class="font-semibold text-gray-800 capitalize">{selectedChild.gender}</p>
                  </div>
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Age</p>
                    <p class="font-semibold text-gray-800">{new Date().getFullYear() - new Date(selectedChild.date_of_birth).getFullYear()} years old</p>
                  </div>
                </div>
              </div>
              
              <div class="space-y-4">
                <h4 class="font-bold text-gray-800 text-lg">Academic Information</h4>
                <div class="space-y-3">
                  <div class="p-3 bg-blue-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Class</p>
                    <p class="font-semibold text-blue-600">{selectedChild.class_name}</p>
                  </div>
                  <div class="p-3 bg-blue-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Class Teacher</p>
                    <p class="font-semibold text-blue-600">{selectedChild.teacher_name}</p>
                  </div>
                  <div class="p-3 bg-green-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Attendance Rate</p>
                    <p class="font-semibold text-green-600">{selectedChild.attendance_rate}%</p>
                  </div>
                  <div class="p-3 bg-{selectedChild.outstanding_fees > 0 ? 'red' : 'green'}-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Fee Status</p>
                    <p class="font-semibold text-{selectedChild.outstanding_fees > 0 ? 'red' : 'green'}-600">
                      {selectedChild.outstanding_fees > 0 ? `${selectedChild.outstanding_fees.toLocaleString()} RWF Outstanding` : 'All Fees Paid'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="mt-6 pt-6 border-t border-gray-200">
              <h4 class="font-bold text-gray-800 text-lg mb-4">Contact Information</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Parent Phone</p>
                  <p class="font-semibold text-gray-800">{selectedChild.parent_phone}</p>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Emergency Contact</p>
                  <p class="font-semibold text-gray-800">{selectedChild.emergency_contact}</p>
                </div>
              </div>
            </div>
            
            <div class="mt-6 flex gap-3">
              <button on:click={() => { showDetails = false; goto(`/parent/attendance?child=${selectedChild.id}`); }} class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium">
                📊 View Attendance
              </button>
              <button on:click={() => { showDetails = false; goto(`/parent/fees?child=${selectedChild.id}`); }} class="flex-1 bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-medium">
                💰 View Fees
              </button>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
