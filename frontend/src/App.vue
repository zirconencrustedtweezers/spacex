<template>
  <div id="app">
    <nav class="navbar is-primary" role="navigation">
      <div class="navbar-brand">
        <div class="navbar-item">
          <h1 class="title is-4 has-text-white">
            🚀 SpaceX Explorer
          </h1>
        </div>
      </div>
    </nav>
    
    <div class="tabs is-centered is-boxed">
      <ul>
        <li :class="{ 'is-active': activeTab === 'launches' }">
          <a @click="setActiveTab('launches')">
            <span class="icon is-small">
              <i class="fas fa-rocket"></i>
            </span>
            <span>Launches</span>
          </a>
        </li>
        <li :class="{ 'is-active': activeTab === 'rockets' }">
          <a @click="setActiveTab('rockets')">
            <span class="icon is-small">
              <i class="fas fa-space-shuttle"></i>
            </span>
            <span>Rockets</span>
          </a>
        </li>
      </ul>
    </div>
    
    <div class="tab-content">
      <Launches v-if="activeTab === 'launches'" />
      <Rockets v-else-if="activeTab === 'rockets'" />
    </div>
  </div>
</template>

<script>
import Launches from './components/Launches.vue'
import Rockets from './components/Rockets.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    Launches,
    Rockets
  },
  data() {
    return {
      activeTab: 'launches',
      crewMap: new Map(),
      crewLoading: true,
      crewError: null
    }
  },
  
  provide() {
    return {
      crewMap: this.crewMap,
      getCrewMember: this.getCrewMember
    }
  },
  
  methods: {
    async fetchCrewData() {
      try {
        const response = await axios.get('/api/crew')
        const crewData = response.data.crew
        
        crewData.forEach(crewMember => {
          this.crewMap.set(crewMember.id, crewMember)
        })
        
        this.crewLoading = false
        
      } catch (error) {
        this.crewError = 'Failed to load crew data'
        this.crewLoading = false
        console.error('Error fetching crew data:', error)
      }
    },
    
    getCrewMember(crewId) {
      return this.crewMap.get(crewId) || null
    },
    
    setActiveTab(tab) {
      this.activeTab = tab
    }
  },
  
  async created() {
    await this.fetchCrewData()
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #ffffff !important;
  color: #363636 !important;
}

#app {
  min-height: 100vh;
  background: #f8f9fa !important;
  color: #363636 !important;
}

html {
  background: #ffffff !important;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tabs {
  background: white;
  margin: 0;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tabs ul {
  border-bottom: none !important;
}

.tabs {
  border-bottom: none !important;
}

.tabs li a {
  border: none;
  border-radius: 0;
  padding: 1rem 1.5rem;
  transition: all 0.3s ease;
}

.tabs li:hover a {
  background-color: #f5f5f5;
  border-color: transparent;
}

.tabs li.is-active a {
  background-color: #3273dc !important;
  color: white !important;
  border-color: #3273dc !important;
}

.tabs li.is-active a:hover {
  background-color: #2366d1 !important;
  color: white !important;
}

.tab-content {
  background: #ffffff !important;
  color: #363636 !important;
  min-height: calc(100vh - 140px);
}

p, h1, h2, h3, h4, h5, h6, span:not(.icon), div:not(.button):not(.tag) {
  color: #363636 !important;
}

.section {
  background: #ffffff !important;
}

.container {
  background: #ffffff !important;
}



@media (max-width: 768px) {
  .tabs ul {
    flex-direction: row;
    justify-content: center;
  }
  
  .tabs li a {
    padding: 0.75rem 1rem;
  }
  
  .tabs li a span:last-child {
    display: none;
  }
}
</style>
