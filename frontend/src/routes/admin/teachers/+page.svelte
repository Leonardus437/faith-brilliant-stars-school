<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores/auth.js';
  
  let teachers = [
    {
      id: 1,
      first_name: 'Sarah',
      last_name: 'Smith',
      employee_id: 'EMP001',
      subject: 'Mathematics',
      class_assigned: 'P4 A',
      phone: '+250788123456',
      email: 'sarah.smith@faithschool.rw',
      salary: 150000,
      status: 'active'
    },
    {
      id: 2,
      first_name: 'John',
      last_name: 'Brown',
      employee_id: 'EMP002',
      subject: 'English',
      class_assigned: 'P2 B',
      phone: '+250788654321',
      email: 'john.brown@faithschool.rw',
      salary: 140000,
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
  
  let subjects = ['Mathematics', 'English', 'Science', 'Social Studies', 'Kinyarwanda'];
  
  let showAddForm = false;
  let loading = false;
  let searchQuery = '';
  let currentUser = null;
  
  let teacherForm = {
    first_name: '',
    last_name: '',
    employee_id: '',
    subject: '',
    class_id: '',
    phone: '',
    email: '',
    salary: ''
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
    teacherForm = {
      first_name: '',
      last_name: '',
      employee_id: `EMP${String(teachers.length + 1).padStart(3, '0')}`,
      subject: '',
      class_id: '',
      phone: '',
      email: '',
      salary: ''
    };
    showAddForm = true;
  }
  
  async function saveTeacher() {
    if (!teacherForm.first_name || !teacherForm.last_name) {
      alert('Please fill in required fields');
      return;
    }
    
    const newTeacher = {
      ...teacherForm,
      id: teachers.length + 1,
      class_assigned: classes.find(c => c.id == teacherForm.class_id)?.name || '',
      status: 'active'
    };
    
    teachers = [...teachers, newTeacher];
    alert('Teacher added successfully!');
    showAddForm = false;
  }
  
  $: filteredTeachers = teachers.filter(teacher => 
    teacher.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    teacher.last_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    teacher.subject.toLowerCase().includes(searchQuery.toLowerCase())
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
              <h1 class="text-2xl font-bold text-gray-900">Teacher Management</h1>
              <p class="text-sm text-gray-600">Manage teaching staff</p>
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
            placeholder="Search teachers..."
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white"
          />
          <button
            on:click={openAddForm}
            class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium shadow-lg transition-colors"
          >
            + Add Teacher
          </button>
        </div>
      </div>

      <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 overflow-hidden">
        <table class="min-w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Teacher</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Employee ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Subject</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Class</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contact</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            {#each filteredTeachers as teacher}
              <tr class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <div class="flex items-center">
                    <div class="w-10 h-10 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                      {teacher.first_name.charAt(0)}{teacher.last_name.charAt(0)}
                    </div>
                    <div class="ml-3">
                      <div class="text-sm font-medium text-gray-900">{teacher.first_name} {teacher.last_name}</div>
                      <div class="text-sm text-gray-500">{teacher.email}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-sm text-gray-900">{teacher.employee_id}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{teacher.subject}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{teacher.class_assigned}</td>
                <td class="px-6 py-4 text-sm text-gray-900">{teacher.phone}</td>
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
              <h2 class="text-2xl font-bold text-gray-800">Add New Teacher</h2>
              <button on:click={() => showAddForm = false} class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
            </div>
            
            <form on:submit|preventDefault={saveTeacher} class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">First Name *</label>
                  <input
                    type="text"
                    bind:value={teacherForm.first_name}
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Last Name *</label>
                  <input
                    type="text"
                    bind:value={teacherForm.last_name}
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Employee ID</label>
                  <input
                    type="text"
                    bind:value={teacherForm.employee_id}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Subject</label>
                  <select
                    bind:value={teacherForm.subject}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  >
                    <option value="">Select Subject</option>
                    {#each subjects as subject}
                      <option value={subject}>{subject}</option>
                    {/each}
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Class</label>
                  <select
                    bind:value={teacherForm.class_id}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  >
                    <option value="">Select Class</option>
                    {#each classes as cls}
                      <option value={cls.id}>{cls.name}</option>
                    {/each}
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                  <input
                    type="tel"
                    bind:value={teacherForm.phone}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                  <input
                    type="email"
                    bind:value={teacherForm.email}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Salary (RWF)</label>
                  <input
                    type="number"
                    bind:value={teacherForm.salary}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
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
                  class="flex-1 bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-medium transition-colors"
                >
                  Add Teacher
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>