<template>
  <div id="app">
    <Launches />
  </div>
</template>

<script>
import Launches from './components/Launches.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    Launches
  },
  data() {
    return {
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
    }
  },
  
  async created() {
    await this.fetchCrewData()
  }
}
</script>
