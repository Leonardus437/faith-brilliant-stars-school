<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores/auth.js';
  
  let classes = [
    {
      id: 1,
      name: 'P1 A',
      level: 'Primary 1',
      capacity: 30,
      current_students: 25,
      teacher_name: 'Mrs. Johnson',
      teacher_id: 1,
      room_number: 'Room 101',
      schedule: 'Monday - Friday, 8:00 AM - 3:00 PM',
      subjects: ['Mathematics', 'English', 'Science', 'Social Studies'],
      status: 'active'
    },
    {
      id: 2,
      name: 'P2 A',
      level: 'Primary 2',
      capacity: 30,
      current_students: 28,
      teacher_name: 'Mr. Brown',
      teacher_id: 2,
      room_number: 'Room 102',
      schedule: 'Monday - Friday, 8:00 AM - 3:00 PM',
      subjects: ['Mathematics', 'English', 'Science', 'Social Studies'],
      status: 'active'
    },
    {
      id: 3,
      name: 'P3 A',
      level: 'Primary 3',
      capacity: 30,
      current_students: 26,
      teacher_name: 'Ms. Davis',
      teacher_id: 3,
      room_number: 'Room 103',
      schedule: 'Monday - Friday, 8:00 AM - 3:00 PM',
      subjects: ['Mathematics', 'English', 'Science', 'Social Studies', 'Kinyarwanda'],
      status: 'active'
    },
    {
      id: 4,
      name: 'P4 A',
      level: 'Primary 4',
      capacity: 30,
      current_students: 24,
      teacher_name: 'Mrs. Wilson',
      teacher_id: 4,
      room_number: 'Room 104',
      schedule: 'Monday - Friday, 8:00 AM - 3:00 PM',
      subjects: ['Mathematics', 'English', 'Science', 'Social Studies', 'Kinyarwanda'],
      status: 'active'
    },
    {
      id: 5,
      name: 'P5 A',
      level: 'Primary 5',
      capacity: 30,
      current_students: 22,
      teacher_name: 'Mr. Anderson',
      teacher_id: 5,
      room_number: 'Room 105',
      schedule: 'Monday - Friday, 8:00 AM - 3:00 PM',
      subjects: ['Mathematics', 'English', 'Science', 'Social Studies', 'Kinyarwanda', 'French'],
      status: 'active'
    },
    {
      id: 6,
      name: 'P6 A',
      level: 'Primary 6',
      capacity: 30,
      current_students: 20,
      teacher_name: 'Mrs. Taylor',
      teacher_id: 6,
      room_number: 'Room 106',
      schedule: 'Monday - Friday, 8:00 AM - 3:00 PM',
      subjects: ['Mathematics', 'English', 'Science', 'Social Studies', 'Kinyarwanda', 'French'],
      status: 'active'
    }
  ];
  
  let teachers = [
    { id: 1, name: 'Mrs. Johnson' },
    { id: 2, name: 'Mr. Brown' },
    { id: 3, name: 'Ms. Davis' },
    { id: 4, name: 'Mrs. Wilson' },
    { id: 5, name: 'Mr. Anderson' },
    { id: 6, name: 'Mrs. Taylor' }
  ];
  
  let showAddForm = false;
  let showDetailsModal = false;
  let selectedClass = null;
  let loading = false;
  let searchQuery = '';
  let currentUser = null;
  
  let classForm = {
    name: '',
    level: '',
    capacity: 30,
    teacher_id: '',
    room_number: '',
    subjects: []
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
    classForm = {
      name: '',
      level: '',
      capacity: 30,
      teacher_id: '',
      room_number: '',
      subjects: []
    };
    showAddForm = true;
  }
  
  function viewClassDetails(cls) {
    selectedClass = cls;
    showDetailsModal = true;
  }
  
  async function saveClass() {
    if (!classForm.name || !classForm.level) {
      alert('Please fill in required fields');
      return;
    }
    
    const newClass = {
      ...classForm,
      id: classes.length + 1,
      current_students: 0,
      teacher_name: teachers.find(t => t.id == classForm.teacher_id)?.name || '',
      schedule: 'Monday - Friday, 8:00 AM - 3:00 PM',
      status: 'active'
    };
    
    classes = [...classes, newClass];
    alert('Class created successfully!');
    showAddForm = false;
  }
  
  function getCapacityColor(current, capacity) {
    const percentage = (current / capacity) * 100;
    if (percentage >= 90) return 'text-red-600';
    if (percentage >= 75) return 'text-yellow-600';
    return 'text-green-600';
  }
  
  $: filteredClasses = classes.filter(cls => 
    cls.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    cls.level.toLowerCase().includes(searchQuery.toLowerCase()) ||
    cls.teacher_name.toLowerCase().includes(searchQuery.toLowerCase())
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
              <h1 class="text-2xl font-bold text-gray-900">Class Management</h1>
              <p class="text-sm text-gray-600">Manage classes and assignments</p>
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
            placeholder="Search classes..."
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white"
          />
          <button
            on:click={openAddForm}
            class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium shadow-lg transition-colors"
          >
            + Add Class
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each filteredClasses as cls}
          <div class="bg-white/95 backdrop-blur-xl rounded-xl shadow-xl border border-white/30 p-6 hover:shadow-2xl transition-all transform hover:scale-[1.02]">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="text-xl font-bold text-gray-900">{cls.name}</h3>
                <p class="text-sm text-gray-600">{cls.level}</p>
              </div>
              <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                {cls.status}
              </span>
            </div>
            
            <div class="space-y-3 mb-4">
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">Teacher:</span>
                <span class="text-sm font-medium text-gray-900">{cls.teacher_name}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">Room:</span>
                <span class="text-sm font-medium text-gray-900">{cls.room_number}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">Students:</span>
                <span class="text-sm font-medium {getCapacityColor(cls.current_students, cls.capacity)}">
                  {cls.current_students}/{cls.capacity}
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                  style="width: {(cls.current_students / cls.capacity) * 100}%"
                ></div>
              </div>
            </div>
            
            <div class="flex gap-2">
              <button 
                on:click={() => viewClassDetails(cls)}
                class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors"
              >
                View Details
              </button>
              <button 
                on:click={() => goto(`/admin/students?class=${cls.id}`)}
                class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg text-sm font-medium transition-colors"
              >
                View Students
              </button>
            </div>
          </div>
        {/each}
      </div>
    </div>

    {#if showAddForm}
      <div class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full">
          <div class="p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-gray-800">Add New Class</h2>
              <button on:click={() => showAddForm = false} class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
            </div>
            
            <form on:submit|preventDefault={saveClass} class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Class Name *</label>
                  <input
                    type="text"
                    bind:value={classForm.name}
                    required
                    placeholder="e.g., P1 B"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Level *</label>
                  <select
                    bind:value={classForm.level}
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="">Select Level</option>
                    <option value="Primary 1">Primary 1</option>
                    <option value="Primary 2">Primary 2</option>
                    <option value="Primary 3">Primary 3</option>
                    <option value="Primary 4">Primary 4</option>
                    <option value="Primary 5">Primary 5</option>
                    <option value="Primary 6">Primary 6</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Capacity</label>
                  <input
                    type="number"
                    bind:value={classForm.capacity}
                    min="1"
                    max="50"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Assigned Teacher</label>
                  <select
                    bind:value={classForm.teacher_id}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="">Select Teacher</option>
                    {#each teachers as teacher}
                      <option value={teacher.id}>{teacher.name}</option>
                    {/each}
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Room Number</label>
                  <input
                    type="text"
                    bind:value={classForm.room_number}
                    placeholder="e.g., Room 107"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
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
                  class="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-lg font-medium transition-colors"
                >
                  Add Class
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    {/if}

    {#if showDetailsModal && selectedClass}
      <div class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
          <div class="p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-gray-800">Class Details - {selectedClass.name}</h2>
              <button on:click={() => showDetailsModal = false} class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-4">
                <h3 class="text-lg font-semibold text-gray-800">Basic Information</h3>
                <div class="space-y-3">
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Class Name</p>
                    <p class="font-semibold text-gray-800">{selectedClass.name}</p>
                  </div>
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Level</p>
                    <p class="font-semibold text-gray-800">{selectedClass.level}</p>
                  </div>
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Room</p>
                    <p class="font-semibold text-gray-800">{selectedClass.room_number}</p>
                  </div>
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Schedule</p>
                    <p class="font-semibold text-gray-800">{selectedClass.schedule}</p>
                  </div>
                </div>
              </div>
              
              <div class="space-y-4">
                <h3 class="text-lg font-semibold text-gray-800">Class Statistics</h3>
                <div class="space-y-3">
                  <div class="p-3 bg-blue-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Class Teacher</p>
                    <p class="font-semibold text-blue-600">{selectedClass.teacher_name}</p>
                  </div>
                  <div class="p-3 bg-green-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Current Students</p>
                    <p class="font-semibold text-green-600">{selectedClass.current_students} / {selectedClass.capacity}</p>
                    <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div 
                        class="bg-green-600 h-2 rounded-full transition-all duration-300" 
                        style="width: {(selectedClass.current_students / selectedClass.capacity) * 100}%"
                      ></div>
                    </div>
                  </div>
                  <div class="p-3 bg-purple-50 rounded-lg">
                    <p class="text-xs text-gray-500 uppercase tracking-wide">Available Spots</p>
                    <p class="font-semibold text-purple-600">{selectedClass.capacity - selectedClass.current_students}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="mt-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-3">Subjects Taught</h3>
              <div class="flex flex-wrap gap-2">
                {#each selectedClass.subjects as subject}
                  <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                    {subject}
                  </span>
                {/each}
              </div>
            </div>
            
            <div class="mt-6 flex gap-3">
              <button 
                on:click={() => { showDetailsModal = false; goto(`/admin/students?class=${selectedClass.id}`); }}
                class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium"
              >
                👥 View Students
              </button>
              <button 
                on:click={() => { showDetailsModal = false; goto(`/attendance?class=${selectedClass.id}`); }}
                class="flex-1 bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-medium"
              >
                📊 Take Attendance
              </button>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>