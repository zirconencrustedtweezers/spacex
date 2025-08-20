<template>
  <section class="section">
    <div class="container">
      <div class="has-text-centered mb-6">
        <h1 class="title is-2">
          SpaceX Rockets 🚀
        </h1>
        <p class="subtitle">
          Explore the powerful fleet of SpaceX rockets
        </p>
      </div>

      <div v-if="loading" class="has-text-centered py-6">
        <div class="loader"></div>
        <p class="has-text-grey mt-4">Loading rockets...</p>
      </div>

      <div v-else-if="error" class="notification is-danger">
        <p>{{ error }}</p>
        <button @click="fetchRockets" class="button is-primary mt-3">
          Try Again
        </button>
      </div>

      <div v-else class="rockets-container">
        <div v-if="rockets.length === 0" class="has-text-centered py-6">
          <i class="fas fa-database has-text-grey is-size-1 mb-4"></i>
          <p class="title is-4 has-text-grey">No rockets loaded yet</p>
          <div class="box has-background-light">
            <p class="has-text-grey mb-3">
              To load SpaceX rockets data into the database, run:
            </p>
            <code class="has-background-light has-text-dark p-3 is-block">
              python3 scripts/seed_rockets.py
            </code>
            <p class="has-text-grey mt-3 is-size-7">
              Make sure Docker containers are running first
            </p>
          </div>
        </div>
        
        <div v-else class="rockets-grid">
          <div 
            v-for="rocket in rockets" 
            :key="rocket.id"
            class="rocket-card"
          >
            <div class="card">
              <div class="card-content">
                <div class="rocket-header">
                  <div class="rocket-icon">
                    <i class="fas fa-rocket has-text-primary is-size-1"></i>
                  </div>
                  
                  <div class="rocket-info">
                    <h3 class="title is-4 mb-2">{{ rocket.name }}</h3>
                    <p class="subtitle is-6 has-text-grey mb-3">{{ rocket.type }}</p>
                    
                    <div class="rocket-details">
                      <div class="field is-grouped is-grouped-multiline mb-3">
                        <div class="control" v-if="rocket.weight">
                          <div class="tags has-addons">
                            <span class="tag is-light">Weight</span>
                            <span class="tag is-info">{{ formatWeight(rocket.weight) }}</span>
                          </div>
                        </div>
                      </div>
                      
                      <div class="content" v-if="rocket.description">
                        <p class="rocket-description">
                          {{ rocket.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="has-text-centered mt-6" v-if="rockets.length > 0">
          <p class="has-text-grey is-size-7">
            Showing {{ rockets.length }} rocket{{ rockets.length !== 1 ? 's' : '' }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Rockets',
  data() {
    return {
      rockets: [],
      loading: true,
      error: null
    }
  },
  
  methods: {
    async fetchRockets() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/rockets')
        this.rockets = response.data.rockets || []
      } catch (err) {
        this.error = 'Failed to load rockets. Please try again later.'
        console.error('Error fetching rockets:', err)
      } finally {
        this.loading = false
      }
    },
    
    formatWeight(weight) {
      if (!weight) return 'Unknown'
      if (weight >= 1000) {
        return `${(weight / 1000).toFixed(1)}k kg`
      }
      return `${weight.toLocaleString()} kg`
    }
  },
  
  async mounted() {
    await this.fetchRockets()
  }
}
</script>

<style scoped>
.rockets-container {
  max-width: 1200px;
  margin: 0 auto;
}

.rockets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
  padding: 0 1rem;
}

.rocket-card {
  height: fit-content;
}

.rocket-card .card {
  height: 100%;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 12px;
}

.rocket-card .card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.rocket-header {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.rocket-icon {
  flex-shrink: 0;
  text-align: center;
  width: 80px;
}

.rocket-info {
  flex: 1;
  min-width: 0;
}

.rocket-description {
  line-height: 1.6;
  color: #4a4a4a;
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

@media (max-width: 768px) {
  .rockets-grid {
    grid-template-columns: 1fr;
    padding: 0;
  }
  
  .rocket-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .rocket-icon {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .rockets-grid {
    gap: 1rem;
  }
  
  .card-content {
    padding: 1rem;
  }
}
</style>
