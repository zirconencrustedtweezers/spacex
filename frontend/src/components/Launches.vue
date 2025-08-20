<template>
  <section class="section">
    <div class="container">
      <div class="has-text-centered mb-6">
        <h1 class="title is-2">
          SpaceX Launches 🚀
        </h1>
        <p class="subtitle">
          Explore the history of SpaceX missions
        </p>
        
        
        <div class="field is-grouped is-grouped-centered mt-4">
          <div class="control">
            <label class="checkbox">
              <input 
                type="checkbox" 
                v-model="showCrewOnly"
                @change="toggleCrewFilter"
              >
              <span class="ml-2">Show launches with crew only</span>
            </label>
          </div>
        </div>
      </div>

      
      <div v-if="loading" class="has-text-centered py-6">
        <div class="loader"></div>
        <p class="has-text-grey mt-4">Loading launches...</p>
      </div>

      
      <div v-else-if="error" class="notification is-danger">
        <p>{{ error }}</p>
        <button @click="fetchLaunches" class="button is-primary mt-3">
          Try Again
        </button>
      </div>

      
      <div v-else class="launches-container">
        
        <div class="navigation-container" v-if="launches.length > 0">
          
          <button 
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="nav-arrow nav-arrow-left"
            :class="{ 'is-disabled': currentPage === 1 }"
          >
            <i class="fas fa-chevron-left"></i>
          </button>
          
          
          <div class="launches-grid">
            <LaunchCard
              v-for="launch in launches" 
              :key="launch.flight_number"
              :launch="launch"
              :is-expanded="isLaunchExpanded(launch)"
              @toggle-crew="viewCrew"
            />
          </div>
          
          
          <button 
            @click="goToPage(currentPage + 1)"
            :disabled="!hasMore"
            class="nav-arrow nav-arrow-right"
            :class="{ 'is-disabled': !hasMore }"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
        
        
        <div class="has-text-centered mt-4" v-if="launches.length > 0">
          <p class="has-text-grey is-size-7">
            Page {{ currentPage }} • {{ launches.length }} launches
            <span v-if="hasMore"> • More available</span>
          </p>
        </div>
        
        
        <div v-if="launches.length === 0" class="has-text-centered py-6">
          <i class="fas fa-search has-text-grey is-size-1 mb-4"></i>
          <p class="title is-4 has-text-grey">No launches found</p>
          <p class="has-text-grey">Try adjusting your filters or check back later.</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import LaunchCard from './LaunchCard.vue'

export default {
  name: 'Launches',
  components: {
    LaunchCard
  },
  inject: ['crewMap', 'getCrewMember'],
  data() {
    return {
      launches: [],
      loading: true,
      error: null,
      currentPage: 1,
      hasMore: false,
      showCrewOnly: true,
      expandedLaunches: new Set()
    }
  },
  methods: {
    async fetchLaunches() {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          page: this.currentPage
        }
        
        if (this.showCrewOnly) {
          params.withCrew = true
        }
        
        const response = await axios.get('/api/launches', { params })
        
        this.launches = response.data.launches
        this.hasMore = response.data.has_more
        this.loading = false
        
      } catch (error) {
        this.error = 'Failed to load launches. Please try again.'
        this.loading = false
        console.error('Error fetching launches:', error)
      }
    },
    
    async goToPage(page) {
      if (page < 1) return
      this.currentPage = page
      await this.fetchLaunches()
    },

    viewCrew(launch) {
      const launchId = launch.flight_number
      if (this.expandedLaunches.has(launchId)) {
        this.expandedLaunches.delete(launchId)
      } else {
        this.expandedLaunches.add(launchId)
      }
      this.$forceUpdate()
    },

    isLaunchExpanded(launch) {
      return this.expandedLaunches.has(launch.flight_number)
    },

    toggleCrewFilter() {
      this.currentPage = 1
      this.fetchLaunches()
    }
  },
  mounted() {
    this.fetchLaunches()
  }
}
</script>

<style scoped>
.section {
  padding: 2rem 1.5rem;
}

.launches-container {
  position: relative;
}

.navigation-container {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  min-height: 400px;
}

.launches-grid {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.nav-arrow {
  position: sticky;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: white;
  border: 2px solid #dbdbdb;
  color: #4a4a4a;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
  flex-shrink: 0;
}

.nav-arrow:hover:not(.is-disabled) {
  background: #3273dc;
  color: white;
  border-color: #3273dc;
  transform: translateY(-50%) scale(1.1);
}

.nav-arrow.is-disabled {
  opacity: 0.3;
  cursor: not-allowed;
  background: #f5f5f5;
}

.nav-arrow-left {
  margin-right: auto;
}

.nav-arrow-right {
  margin-left: auto;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3273dc;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .navigation-container {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .nav-arrow {
    position: static;
    transform: none;
    margin: 0;
  }
  
  .nav-arrow-left,
  .nav-arrow-right {
    margin: 0;
  }
  
  .section {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .navigation-container {
    gap: 0.75rem;
  }
  
  .nav-arrow {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}
</style>