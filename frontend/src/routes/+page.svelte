<script>
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { t } from '$lib/i18n/index.js';
  import LanguageToggle from '$lib/components/LanguageToggle.svelte';
  
  let currentImageIndex = 0;
  let isVisible = false;
  
  const images = [
    { src: '/1.jpg', title: 'Modern Learning Environment' },
    { src: '/2.jpg', title: 'Interactive Classrooms' },
    { src: '/3.jpg', title: 'Dedicated Teachers' },
    { src: '/4.jpg', title: 'Student Activities' },
    { src: '/5.jpg', title: 'School Community' },
    { src: '/6.jpg', title: 'Excellence in Education' }
  ];
  
  onMount(() => {
    isVisible = true;
    
    // Auto-rotate images
    const interval = setInterval(() => {
      currentImageIndex = (currentImageIndex + 1) % images.length;
    }, 4000);
    
    return () => clearInterval(interval);
  });
  
  function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % images.length;
  }
  
  function prevImage() {
    currentImageIndex = currentImageIndex === 0 ? images.length - 1 : currentImageIndex - 1;
  }
</script>

<svelte:head>
  <title>Faith Brilliant Stars School - Excellence in Education</title>
</svelte:head>

<div class="min-h-screen bg-white dark:bg-gray-900 transition-colors">
  <!-- Navigation -->
  <nav class="fixed top-0 w-full bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 z-50 transition-all duration-300">
    <div class="container mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-3">
          <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl flex items-center justify-center text-white font-bold text-xl">
            FBS
          </div>
          <div>
            <h1 class="text-xl font-bold text-gray-900 dark:text-white">{$t('schoolName')}</h1>
            <p class="text-xs text-gray-600 dark:text-gray-400">{$t('schoolTagline')}</p>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <LanguageToggle />
          <button on:click={() => goto('/login')} class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg font-semibold shadow-lg transform hover:scale-105 transition-all duration-200">
            {$t('login')} →
          </button>
        </div>
      </div>
    </div>
  </nav>

  <!-- Hero Section with Image Carousel -->
  <section class="relative min-h-screen flex items-center overflow-hidden pt-20">
    <!-- Background Image Carousel -->
    <div class="absolute inset-0">
      {#each images as image, index}
        <div class="absolute inset-0 transition-opacity duration-1000 {index === currentImageIndex ? 'opacity-100' : 'opacity-0'}">
          <img src={image.src} alt={image.title} class="w-full h-full object-cover" />
          <div class="absolute inset-0 bg-gradient-to-r from-black/70 via-black/50 to-black/30"></div>
        </div>
      {/each}
    </div>
    
    <!-- Hero Content -->
    <div class="relative container mx-auto px-6 py-20 z-10">
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <div class="text-white {isVisible ? 'animate-fade-in-up' : 'opacity-0'}">
          <h2 class="text-6xl lg:text-7xl font-bold mb-6 leading-tight">
            {$t('nurturingBrilliant')} <span class="text-blue-400">{$t('brilliant')}</span> <br>{$t('mindsForTomorrow')}
          </h2>
          <p class="text-xl lg:text-2xl mb-8 text-gray-200">
            {$t('modernSystem')}
          </p>
          <div class="flex flex-col sm:flex-row gap-4">
            <button on:click={() => goto('/login')} class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-semibold text-lg shadow-2xl transform hover:scale-105 transition-all duration-200">
              {$t('getStartedToday')}
            </button>
          </div>
        </div>
        
        <!-- Image Navigation -->
        <div class="relative {isVisible ? 'animate-fade-in-right' : 'opacity-0'}">
          <div class="bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20">
            <div class="relative h-80 rounded-2xl overflow-hidden">
              <img src={images[currentImageIndex].src} alt={images[currentImageIndex].title} class="w-full h-full object-cover" />
              
              <!-- Navigation Arrows -->
              <button on:click={prevImage} class="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-all">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                </svg>
              </button>
              <button on:click={nextImage} class="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-all">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </button>
              
              <!-- Image Title -->
              <div class="absolute bottom-4 left-4 right-4 bg-black/50 backdrop-blur-sm text-white p-3 rounded-lg">
                <h3 class="font-semibold">{images[currentImageIndex].title}</h3>
              </div>
            </div>
            
            <!-- Dots Indicator -->
            <div class="flex justify-center mt-6 space-x-2">
              {#each images as _, index}
                <button on:click={() => currentImageIndex = index} class="w-3 h-3 rounded-full transition-all {index === currentImageIndex ? 'bg-blue-400' : 'bg-white/50 hover:bg-white/70'}">
                </button>
              {/each}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="py-20 bg-gray-50">
    <div class="container mx-auto px-6">
      <div class="text-center mb-16">
        <h2 class="text-5xl font-bold text-gray-900 dark:text-white mb-4">{$t('comprehensiveManagement')}</h2>
        <p class="text-xl text-gray-600 dark:text-gray-400">{$t('everythingInOne')}</p>
      </div>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div class="group bg-white dark:bg-gray-800 rounded-3xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-4 transition-all duration-300">
          <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900/40 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-blue-600 transition-colors">
            <svg class="w-8 h-8 text-blue-600 dark:text-blue-400 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold mb-3 text-gray-900 dark:text-white">{$t('forTeachers')}</h3>
          <p class="text-gray-600 dark:text-gray-400">{$t('teacherDescription')}</p>
        </div>
        
        <div class="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-4 transition-all duration-300">
          <div class="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-green-600 transition-colors">
            <svg class="w-8 h-8 text-green-600 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold mb-3 text-gray-900">For Parents</h3>
          <p class="text-gray-600">Monitor children's attendance, view fees, and stay connected with teachers</p>
        </div>
        
        <div class="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-4 transition-all duration-300">
          <div class="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-purple-600 transition-colors">
            <svg class="w-8 h-8 text-purple-600 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold mb-3 text-gray-900">For Accountants</h3>
          <p class="text-gray-600">Manage fees, track payments, and generate comprehensive financial reports</p>
        </div>
        
        <div class="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-4 transition-all duration-300">
          <div class="w-16 h-16 bg-orange-100 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-orange-600 transition-colors">
            <svg class="w-8 h-8 text-orange-600 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold mb-3 text-gray-900">For Administrators</h3>
          <p class="text-gray-600">Full system control, analytics, and comprehensive oversight tools</p>
        </div>
      </div>
    </div>
  </section>

  <!-- School Gallery Section -->
  <section class="py-20 bg-white">
    <div class="container mx-auto px-6">
      <div class="text-center mb-16">
        <h2 class="text-5xl font-bold text-gray-900 mb-4">Our School Environment</h2>
        <p class="text-xl text-gray-600">Take a look at our modern facilities and vibrant community</p>
      </div>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each images as image, index}
          <div class="group relative overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-105">
            <img src={image.src} alt={image.title} class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-500" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <div class="absolute bottom-4 left-4 right-4 text-white">
                <h3 class="font-semibold text-lg">{image.title}</h3>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- Stats Section -->
  <section class="py-20 bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 relative overflow-hidden">
    <div class="absolute inset-0 bg-black/20"></div>
    <div class="container mx-auto px-6 relative z-10">
      <div class="grid md:grid-cols-4 gap-8 text-white text-center">
        <div class="transform hover:scale-110 transition-transform duration-300">
          <div class="text-6xl font-bold mb-2 bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">60+</div>
          <div class="text-xl opacity-90">Active Students</div>
        </div>
        <div class="transform hover:scale-110 transition-transform duration-300">
          <div class="text-6xl font-bold mb-2 bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">6</div>
          <div class="text-xl opacity-90">Classes</div>
        </div>
        <div class="transform hover:scale-110 transition-transform duration-300">
          <div class="text-6xl font-bold mb-2 bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">4</div>
          <div class="text-xl opacity-90">User Roles</div>
        </div>
        <div class="transform hover:scale-110 transition-transform duration-300">
          <div class="text-6xl font-bold mb-2 bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">100%</div>
          <div class="text-xl opacity-90">Digital Platform</div>
        </div>
      </div>
    </div>
  </section>

 

  <!-- Footer -->
  <footer class="bg-gray-900 text-white py-16">
    <div class="container mx-auto px-6">
      <div class="grid md:grid-cols-4 gap-8 mb-8">
        <div class="col-span-2">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl flex items-center justify-center text-white font-bold text-xl">
              FBS
            </div>
            <div>
              <h3 class="text-2xl font-bold">Faith Brilliant Stars School</h3>
              <p class="text-gray-400">Excellence in Education</p>
            </div>
          </div>
          <p class="text-gray-400 mb-4">Empowering the next generation through innovative education and technology.</p>
          <p class="text-gray-400">Kigali, Rwanda</p>
        </div>
        
        <div>
          <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
          <ul class="space-y-2 text-gray-400">
            <li><a href="#" class="hover:text-white transition-colors">About Us</a></li>
            <li><a href="#" class="hover:text-white transition-colors">Admissions</a></li>
            <li><a href="#" class="hover:text-white transition-colors">Programs</a></li>
            <li><a href="#" class="hover:text-white transition-colors">Contact</a></li>
          </ul>
        </div>
        
        <div>
          <h4 class="text-lg font-semibold mb-4">System Access</h4>
          <ul class="space-y-2 text-gray-400">
            <li><a href="/login" class="hover:text-white transition-colors">Teacher Portal</a></li>
            <li><a href="/login" class="hover:text-white transition-colors">Parent Portal</a></li>
            <li><a href="/login" class="hover:text-white transition-colors">Admin Panel</a></li>
            <li><a href="/login" class="hover:text-white transition-colors">Accountant Access</a></li>
          </ul>
        </div>
      </div>
      
      <div class="border-t border-gray-800 pt-8 text-center">
        <p class="text-gray-500">© 2025 Faith Brilliant Stars School. All rights reserved.</p>
      </div>
    </div>
  </footer>
</div>

<style>
  @keyframes fade-in-up {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes fade-in-right {
    from {
      opacity: 0;
      transform: translateX(30px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
  
  .animate-fade-in-up {
    animation: fade-in-up 1s ease-out;
  }
  
  .animate-fade-in-right {
    animation: fade-in-right 1s ease-out 0.3s both;
  }
</style>