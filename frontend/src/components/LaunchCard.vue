<template>
  <div class="launch-card-horizontal">
    <div class="card">
      <div class="card-content">
        <div class="launch-header">
          <div class="launch-image">
            <figure class="image is-96x96" v-if="launch.links.mission_patch">
              <img 
                :src="launch.links.mission_patch" 
                :alt="`${launch.mission_name} mission patch`"
                class="is-rounded"
              >
            </figure>
            <div v-else class="image is-96x96 has-background-light is-flex is-align-items-center is-justify-content-center is-rounded">
              <i class="fas fa-rocket has-text-grey is-size-2"></i>
            </div>
          </div>
          
          <div class="launch-info">
            <h3 class="title is-5 mb-2">{{ launch.mission_name }}</h3>
            <p class="subtitle is-6 has-text-grey mb-3">
              Flight #{{ launch.flight_number }} • {{ launch.launch_year }}
            </p>
            
            <div class="tags mb-3">
              <span class="tag is-info is-light">{{ launch.rocket.rocket_name }}</span>
              <span 
                class="tag"
                :class="{
                  'is-success': launch.launch_success === true,
                  'is-danger': launch.launch_success === false,
                  'is-warning': launch.upcoming
                }"
              >
                {{ launch.upcoming ? 'Upcoming' : (launch.launch_success ? 'Success' : 'Failed') }}
              </span>
            </div>
            
            <div class="launch-details">
              <p class="has-text-weight-semibold is-size-7 mb-1">
                <i class="fas fa-map-marker-alt mr-1"></i>
                {{ launch.launch_site.site_name }}
              </p>
              <p class="has-text-grey is-size-7 mb-2">
                <i class="fas fa-calendar mr-1"></i>
                {{ formatDate(launch.launch_date_utc) }}
              </p>
              <p class="launch-description is-size-7" v-if="launch.details">
                {{ truncateText(launch.details, 120) }}
              </p>
            </div>
          </div>
          
          <div class="launch-actions">
            <button 
              v-if="launch.crew && launch.crew.length > 0"
              class="button is-small is-outlined is-primary"
              @click="toggleCrew"
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
              class="button is-small is-outlined is-danger"
            >
              <span class="icon is-small">
                <i class="fab fa-youtube"></i>
              </span>
              <span>Video</span>
            </a>
            
            <a 
              v-if="launch.links.wikipedia"
              :href="launch.links.wikipedia" 
              target="_blank"
              class="button is-small is-outlined is-link"
            >
              <span class="icon is-small">
                <i class="fab fa-wikipedia-w"></i>
              </span>
              <span>Wiki</span>
            </a>
          </div>
        </div>
      </div>
      
      <div 
        v-if="isExpanded && launch.crew && launch.crew.length > 0"
        class="crew-expansion"
      >
        <div class="crew-divider"></div>
        <div class="crew-list">
          <div 
            v-for="crewMember in crewMembers" 
            :key="crewMember.id"
            class="crew-member"
          >
            <div class="crew-avatar">
              <figure class="image is-48x48" v-if="crewMember.image">
                <img 
                  :src="crewMember.image" 
                  :alt="crewMember.name"
                  class="is-rounded"
                >
              </figure>
              <div v-else class="image is-48x48 has-background-light is-flex is-align-items-center is-justify-content-center is-rounded">
                <i class="fas fa-user has-text-grey"></i>
              </div>
            </div>
            <div class="crew-info">
              <p class="crew-name has-text-weight-semibold">{{ crewMember.name }}</p>
              <p class="crew-details has-text-grey is-size-7">
                {{ crewMember.agency }} • {{ crewMember.status }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LaunchCard',
  inject: ['getCrewMember'],
  props: {
    launch: {
      type: Object,
      required: true
    },
    isExpanded: {
      type: Boolean,
      default: false
    }
  },
  emits: ['toggle-crew'],
  computed: {
    crewMembers() {
      if (!this.launch.crew || this.launch.crew.length === 0) return []
      
      return this.launch.crew.map(({ crew: crewId }) => {
        return this.getCrewMember(crewId)
      }).filter(member => member !== null)
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'TBD'
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
    
    toggleCrew() {
      this.$emit('toggle-crew', this.launch)
    }
  }
}
</script>

<style scoped>
.launch-card-horizontal {
  margin-bottom: 1rem;
}

.launch-card-horizontal .card {
  transition: transform 0.2s ease, box-shadow 0.2s ease, max-height 0.3s ease;
  overflow: hidden;
}

.launch-card-horizontal .card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.card-content {
  padding: 1.5rem;
}

.launch-header {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.launch-image {
  flex-shrink: 0;
}

.launch-image .image {
  width: 96px !important;
  height: 96px !important;
}

.launch-info {
  flex: 1;
  min-width: 0;
}

.launch-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex-shrink: 0;
  align-self: flex-start;
}

.crew-expansion {
  padding: 0 1.5rem 1.5rem 1.5rem;
  animation: slideDown 0.3s ease-out;
}

.crew-divider {
  height: 1px;
  background: linear-gradient(to right, #dbdbdb, transparent);
  margin-bottom: 1rem;
}

.crew-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.crew-member {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
}

.crew-avatar {
  flex-shrink: 0;
}

.crew-avatar .image {
  width: 48px !important;
  height: 48px !important;
}

.crew-info {
  flex: 1;
}

.crew-name {
  margin-bottom: 0.25rem;
  line-height: 1.2;
}

.crew-details {
  margin-bottom: 0;
  line-height: 1.2;
}

@keyframes slideDown {
  from {
    max-height: 0;
    opacity: 0;
    padding-bottom: 0;
  }
  to {
    max-height: 500px;
    opacity: 1;
    padding-bottom: 1.5rem;
  }
}

@media (max-width: 768px) {
  .launch-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .launch-actions {
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .card-content {
    padding: 1rem;
  }
  
  .crew-expansion {
    padding: 0 1rem 1rem 1rem;
  }
}

@media (max-width: 480px) {
  .launch-header {
    gap: 0.75rem;
  }
  
  .launch-image .image {
    width: 80px !important;
    height: 80px !important;
  }
  
  .launch-actions .button {
    font-size: 0.75rem;
  }
}
</style>
