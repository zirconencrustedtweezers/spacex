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
        
        <!-- Crew Filter Toggle -->
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

      <!-- Loading State -->
      <div v-if="loading" class="has-text-centered py-6">
        <div class="loader"></div>
        <p class="has-text-grey mt-4">Loading launches...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="notification is-danger">
        <p>{{ error }}</p>
        <button @click="fetchLaunches" class="button is-primary mt-3">
          Try Again
        </button>
      </div>

      <!-- Launches with Navigation -->
      <div v-else class="launches-container">
        <!-- Navigation Container -->
        <div class="navigation-container" v-if="launches.length > 0">
          <!-- Left Arrow -->
          <button 
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="nav-arrow nav-arrow-left"
            :class="{ 'is-disabled': currentPage === 1 }"
          >
            <i class="fas fa-chevron-left"></i>
          </button>

          <!-- Launches List -->
          <div class="launches-list">
            <div 
              v-for="launch in launches" 
              :key="launch.flight_number"
              class="launch-card-horizontal"
            >
              <div class="card">
                <div class="card-content">
                  <div class="columns is-vcentered">
                    <!-- Mission Patch -->
                    <div class="column is-narrow">
                      <figure class="image is-96x96" v-if="launch.links.mission_patch_small">
                        <img 
                          :src="launch.links.mission_patch_small" 
                          :alt="launch.mission_name + ' mission patch'"
                          class="is-rounded"
                        >
                      </figure>
                      <div v-else class="image is-96x96 has-background-light is-flex is-align-items-center is-justify-content-center">
                        <i class="fas fa-rocket has-text-grey"></i>
                      </div>
                    </div>

                    <!-- Launch Info -->
                    <div class="column">
                      <div class="columns is-mobile">
                        <div class="column">
                          <h3 class="title is-5 mb-2">{{ launch.mission_name }}</h3>
                          <p class="subtitle is-6 has-text-grey mb-3">
                            Flight #{{ launch.flight_number }} • {{ launch.launch_year }}
                          </p>
                          
                          <div class="tags">
                            <span class="tag is-light">{{ launch.rocket.rocket_name }}</span>
                            <span 
                              v-if="launch.upcoming" 
                              class="tag is-info"
                            >
                              Upcoming
                            </span>
                            <span 
                              v-else-if="launch.launch_success === true" 
                              class="tag is-success"
                            >
                              Success
                            </span>
                            <span 
                              v-else-if="launch.launch_success === false" 
                              class="tag is-danger"
                            >
                              Failed
                            </span>
                            <span 
                              v-else 
                              class="tag is-warning"
                            >
                              Unknown
                            </span>
                          </div>
                        </div>

                        <div class="column is-narrow">
                          <div class="has-text-right">
                            <p class="has-text-weight-semibold">{{ launch.launch_site.site_name }}</p>
                            <p class="has-text-grey is-size-7">{{ formatDate(launch.launch_date_local) }}</p>
                            
                            <!-- Action Buttons -->
                            <div class="buttons is-right mt-3">
                              <button 
                                v-if="launch.crew && launch.crew.length > 0"
                                @click="viewCrew(launch)"
                                class="button is-small is-primary is-outlined"
                              >
                                <span class="icon is-small">
                                  <i class="fas fa-users"></i>
                                </span>
                                <span>Crew</span>
                              </button>
                              
                              <a 
                                v-if="launch.links.video_link" 
                                :href="launch.links.video_link" 
                                target="_blank"
                                class="button is-small is-danger is-outlined"
                              >
                                <span class="icon is-small">
                                  <i class="fas fa-play"></i>
                                </span>
                                <span>Video</span>
                              </a>
                              
                              <a 
                                v-if="launch.links.wikipedia" 
                                :href="launch.links.wikipedia" 
                                target="_blank"
                                class="button is-small is-info is-outlined"
                              >
                                <span class="icon is-small">
                                  <i class="fab fa-wikipedia-w"></i>
                                </span>
                                <span>Wiki</span>
                              </a>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Details -->
                      <div v-if="launch.details" class="content">
                        <p class="has-text-grey is-size-7">
                          {{ truncateText(launch.details, 150) }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Arrow -->
          <button 
            @click="goToPage(currentPage + 1)"
            :disabled="!hasMore"
            class="nav-arrow nav-arrow-right"
            :class="{ 'is-disabled': !hasMore }"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>

        <!-- Empty State -->
        <div v-else class="has-text-centered py-6">
          <p class="title is-4 has-text-grey">No launches found</p>
          <p class="subtitle has-text-grey">Try going back to an earlier page</p>
        </div>

        <!-- Page Indicator -->
        <div class="has-text-centered mt-4" v-if="launches.length > 0">
          <p class="has-text-grey is-size-7">
            Page {{ currentPage }}
            <span v-if="hasMore">• {{ launches.length }} results</span>
            <span v-else>• Last page</span>
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Launches',
  data() {
    return {
      launches: [],
      loading: true,
      error: null,
      currentPage: 1,
      hasMore: false,
      showCrewOnly: true
    }
  },
  
  methods: {
    async fetchLaunches() {
      this.loading = true
      this.error = null
      
      try {
        let url = `/api/launches?page=${this.currentPage}`
        if (this.showCrewOnly) {
          url += '&withCrew=true'
        }
        
        const response = await axios.get(url)
        this.launches = response.data.launches
        this.hasMore = response.data.has_more
      } catch (err) {
        this.error = 'Failed to fetch launches data'
        console.error('Error:', err)
      } finally {
        this.loading = false
      }
    },

    goToPage(page) {
      if (page >= 1 && (page <= this.currentPage + 1 || this.hasMore)) {
        this.currentPage = page
        this.fetchLaunches()
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    truncateText(text, maxLength) {
      if (text.length <= maxLength) return text
      return text.substr(0, maxLength) + '...'
    },

    viewCrew(launch) {
      console.log('View crew for launch:', launch.mission_name, '(Flight #' + launch.flight_number + ')')
      // TODO: Navigate to crew details page
      // This will be implemented later
    },

    toggleCrewFilter() {
      // Reset to page 1 when toggling filter
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
.navigation-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.launches-list {
  flex: 1;
  min-width: 0;
}

.launch-card-horizontal {
  margin-bottom: 1rem;
}

.launch-card-horizontal:last-child {
  margin-bottom: 0;
}

.launch-card-horizontal .card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid #e1e1e1;
}

.launch-card-horizontal .card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.nav-arrow {
  background: #ffffff;
  border: 2px solid #dbdbdb;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #4a4a4a;
  font-size: 1.2rem;
}

.nav-arrow:hover:not(.is-disabled) {
  border-color: #3273dc;
  color: #3273dc;
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(50, 115, 220, 0.2);
}

.nav-arrow.is-disabled {
  background: #f5f5f5;
  border-color: #e1e1e1;
  color: #b5b5b5;
  cursor: not-allowed;
}

.nav-arrow-left {
  flex-shrink: 0;
}

.nav-arrow-right {
  flex-shrink: 0;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.image.is-96x96 {
  width: 96px;
  height: 96px;
}

.tags {
  gap: 0.25rem;
}

.buttons.is-right {
  justify-content: flex-end;
}

.buttons.is-right .button {
  margin-bottom: 0;
}

.button.is-small {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}

@media screen and (max-width: 768px) {
  .navigation-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-arrow {
    align-self: center;
  }
  
  .nav-arrow-left,
  .nav-arrow-right {
    width: 100%;
    max-width: 200px;
    border-radius: 6px;
    height: 40px;
  }
  
  .launches-list {
    width: 100%;
  }

  .buttons.is-right {
    justify-content: center;
    margin-top: 1rem;
  }
  
  .buttons.is-right .button {
    font-size: 0.7rem;
  }
}
</style>
