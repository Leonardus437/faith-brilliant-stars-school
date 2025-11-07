<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores/auth.js';
  
  let students = [
    {
      id: 1,
      first_name: 'Emma',
      last_name: 'Johnson',
      admission_number: 'ADM001',
      class_name: 'P4 A',
      gender: 'female',
      date_of_birth: '2015-03-15',
      parent_name: 'John Johnson',
      parent_phone: '+250788123456',
      address: 'Kigali, Rwanda',
      enrollment_date: '2023-01-15',
      status: 'active'
    },
    {
      id: 2,
      first_name: 'Michael',
      last_name: 'Smith',
      admission_number: 'ADM002',
      class_name: 'P2 B',
      gender: 'male',
      date_of_birth: '2017-07-22',
      parent_name: 'Sarah Smith',
      parent_phone: '+250788654321',
      address: 'Kigali, Rwanda',
      enrollment_date: '2023-01-20',
      status: 'active'
    }
  ];
  
  let classes = [
    { id: 1, name: 'P1 A' },
    { id: 2, name: 'P2 A' },
    { id: 3, name: 'P3 A' },
    { id: 4, name: 'P4 A' },
    { id: 5, name: 'P5 A' },
    { id: 6, name: 'P6 A' }
  ];
  
  let showAddForm = false;
  let loading = false;
  let searchQuery = '';
  let currentUser = null;
  
  let studentForm = {
    first_name: '',
    last_name: '',
    admission_number: '',
    class_id: '',
    gender: 'male',
    date_of_birth: '',
    parent_name: '',
    parent_phone: '',
    address: ''
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
  });
  
  function openAddForm() {
    studentForm = {
      first_name: '',
      last_name: '',
      admission_number: `ADM${String(students.length + 1).padStart(3, '0')}`,
      class_id: '',
      gender: 'male',
      date_of_birth: '',
      parent_name: '',
      parent_phone: '',
      address: ''
    };
    showAddForm = true;
  }
  
  async function saveStudent() {
    if (!studentForm.first_name || !studentForm.last_name) {
      alert('Please fill in required fields');
      return;
    }
    
    const newStudent = {
      ...studentForm,
      id: students.length + 1,
      class_name: classes.find(c => c.id == studentForm.class_id)?.name || '',
      status: 'active',
      enrollment_date: new Date().toISOString().split('T')[0]
    };
    
    students = [...students, newStudent];
    alert('Student added successfully!');
    showAddForm = false;
  }
  
  $: filteredStudents = students.filter(student => 
    student.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    student.last_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    student.admission_number.toLowerCase().includes(searchQuery.toLowerCase())
  );
</script>

<div class="min-h-screen relative overflow-hidden">
  <div class="absolute inset-0 bg-cover bg-center bg-no-repeat" style="background-image: url('/1.jpg');"></div>
  <div class="absolute inset-0 bg-black/30"></div>
  
  <div class="relative z-10 min-h-screen">
    <div class="bg-white/95 backdrop-blur-xl border-b border-white/20 shadow-lg">
      <div class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-lg">
              FBS
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Student Management</h1>
              <p class="text-sm text-gray-600">Manage student enrollment</p>
            </div>
          </div>
          <button on:click={() => goto('/head-teacher')} class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors shadow-lg">
            ← Back
          </button>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-6 py-6">
      <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 mb-6">
        <div class="flex justify-between items-center gap-4">
          <input
            type="text"
            bind:value={searchQuery}
            placeholder="Search students..."
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white"
          />
          <button
            on:click={openAddForm}
            class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium shadow-lg transition-colors"
          >
            + Add Student
          </button>
        </div>
      </div>

      <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 overflow-hidden">
        <table class="min-w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Admission #</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Class</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Parent</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phone</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            {#each filteredStudents as student}
              <tr class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <div class="flex items-center">
                    <div class="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                      {student.first_name.charAt(0)}{student.last_name.charAt(0)}
                    </div>
                    <div class="ml-3">
                      <div class="text-sm font-medium text-gray-900">{student.first_name} {student.last_name}</div>
                      <div class="text-sm text-gray-500">{student.gender}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-sm text-gray-900">{student.admission_number}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{student.class_name}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{student.parent_name}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{student.parent_phone}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>

    {#if showAddForm}
      <div class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full">
          <div class="p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-gray-800">Add New Student</h2>
              <button on:click={() => showAddForm = false} class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
            </div>
            
            <form on:submit|preventDefault={saveStudent} class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">First Name *</label>
                  <input
                    type="text"
                    bind:value={studentForm.first_name}
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Last Name *</label>
                  <input
                    type="text"
                    bind:value={studentForm.last_name}
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Admission Number</label>
                  <input
                    type="text"
                    bind:value={studentForm.admission_number}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Class</label>
                  <select
                    bind:value={studentForm.class_id}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Select Class</option>
                    {#each classes as cls}
                      <option value={cls.id}>{cls.name}</option>
                    {/each}
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                  <select
                    bind:value={studentForm.gender}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Date of Birth</label>
                  <input
                    type="date"
                    bind:value={studentForm.date_of_birth}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Parent Name</label>
                  <input
                    type="text"
                    bind:value={studentForm.parent_name}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Parent Phone</label>
                  <input
                    type="tel"
                    bind:value={studentForm.parent_phone}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Address</label>
                <textarea
                  bind:value={studentForm.address}
                  rows="2"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>
              
              <div class="flex gap-3 pt-4">
                <button
                  type="button"
                  on:click={() => showAddForm = false}
                  class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-medium transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors"
                >
                  Add Student
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>