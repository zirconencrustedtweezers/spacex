<template>
  <section class="hero is-primary is-fullheight">
    <div class="hero-body">
      <div class="container has-text-centered">
        <div class="columns is-centered">
          <div class="column is-half">
            <div class="box">
              <h1 class="title">
                BiometrIQ SpaceX App 🚀
              </h1>
              
              <div v-if="loading" class="content">
                <div class="loader"></div>
                <p class="has-text-grey">Loading...</p>
              </div>
              
              <div v-else-if="error" class="content">
                <p class="has-text-danger">{{ error }}</p>
                <button @click="fetchUser" class="button is-primary">
                  Try Again
                </button>
              </div>
              
              <div v-else class="content">
                <h2 class="title is-2">
                  Hello {{ user.firstName }} {{ user.lastName }}! 👋
                </h2>
                <p class="subtitle">
                  Welcome to the SpaceX exploration app
                </p>
                <button @click="fetchUser" class="button is-light">
                  Refresh
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      user: null,
      loading: true,
      error: null
    }
  },
  
  methods: {
    async fetchUser() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/user')
        this.user = response.data
      } catch (err) {
        this.error = 'Failed to fetch user data'
        console.error('Error:', err)
      } finally {
        this.loading = false
      }
    }
  },
  
  mounted() {
    this.fetchUser()
  }
}
</script>

<style scoped>
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
</style>
