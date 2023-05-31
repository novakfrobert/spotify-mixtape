<template>
  <div class="background">
    
    <div class="header">
      <div class="title">Spotify Mix Tapes</div>
    </div>
    <q-select class="user-selection"
              outlined
              clearable
              multiple
              v-model="selectedUsers"
              :options="userOptions"
              :option-value="'name'"
              :option-label="'name'"
              map-options
              use-chips
              stack-label
              use-input
              filled
              label-color="grey"
              label="Add Users"
              behavior="menu"
              :key="selectedUsers"
              @filter="filterFn"
              @add="userAdded"
              @remove="userRemoved"
              :input-style="{ color: 'white' }"
            >
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
      </q-select>

    <!-- <div class="table-controls">
      <q-btn v-on:click="GetMyTracks" class="table-control" label="Get My Tracks" />
      <q-btn v-on:click="GetMyTracks" class="table-control" label="Save My Tracks" />
      <q-btn v-on:click="GetMyTracks" class="table-control" label="Create Mix Tape" />
    </div> -->
    <div v-if="tracks !== undefined">
      <q-table class="track-table"
        title="Tracks"
        :rows="tracks"
        :columns="columns"
        row-key="name"
        dark
        color="green"
        virtual-scroll
        :rows-per-page-options="[0]"
      />
    </div>
    <q-btn v-on:click="mixtapeDialog = true" class="mixtape-button" label="Create Mixtape" />



    <q-dialog v-model="saveDialog" persistent transition-show="scale" transition-hide="scale">
      <q-card class="save-dialog" >
        <q-card-section>
          <div class="text-h6">Save Tracks?</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          If you save your tracks, other people will be able to create playlists based on what you like. 
          <br/>
          <br/>
          No personal data will be stored.
        </q-card-section>

        <q-card-actions align="right" class="save-dialog">
          <q-btn v-on:click="saveMyTracks" flat label="OK" v-close-popup />
          <q-btn v-on:click="getMyTracks" flat label="No Thanks" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>



    <q-dialog v-model="mixtapeDialog" persistent transition-show="scale" transition-hide="scale">
      <q-card class="mixtape-dialog" >
        <q-card-section>
          <div class="text-h6">Create Mix Tape?</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          This will create a playlist on your spotify account with all the songs shown
        </q-card-section>

        <q-card-actions align="right" class="save-dialog">
          <q-btn v-on:click="createPlaylist" flat label="OK" v-close-popup />
          <q-btn flat label="No Thanks" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>


  </div>

</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Track from "../../Models/Track";
import User from "../../Models/User";
import MixTapeMakerService from "./MixTapeMakerService";
import { Loading, QSpinnerFacebook  } from 'quasar'


export default defineComponent({



    components: {
    },

    props: {
    },

    data() {
      return {


        saveDialog: false as boolean,

        mixtapeDialog: false as boolean,

        columns: [ 
          { 
            name: 'name', align: 'left', label: 'Track', field: 'name', sortable: true,  classes: '',
            style: 'max-width:20vw; width: 20vw; overflow: hidden;',
            headerStyle: 'max-width:20vw; width: 20vw; overflow: hidden;'
          },
          { 
            name: 'artists', align: 'center', label: 'Artists', field: 'artists', sortable: true,  
            style: 'max-width:20vw; width: 20vw; overflow: hidden;',
            headerStyle: 'max-width:20vw; width: 20vw; overflow: hidden;'
          },
        ],


        selectedUsers: [] as User[],

        userOptions: [] as User[],

        cachedUsers: [] as User[],

        tracksByUser: {} as any,

        searchAheadTimeout: null as any,

        tracks: [] as Array<Track>,

        user : {} as User,


      }
    },

    computed: {

   
     
    },

    watch: {

      

    },


    created: function() {

    },

    mounted: function() {
      

      MixTapeMakerService.GetMyUserInfo().then(user => {
        console.log(user);

        this.user = user;

        if (!user.is_saved){
          this.saveDialog = true;
        }
        else{
          this.userAdded({value: user});
        }

      });
    }, 


    methods: {

      createPlaylist() {
        const users = this.selectedUsers.map((u: User) => u.name).join(', ')
        const name = "Mixtape for " + users;
        MixTapeMakerService.CreatePlaylist(this.tracks, name, this.user.spotify_id);
      },

      getMyTracks() {
        MixTapeMakerService.GetMyTracks().then(res => {
          console.log(res);
          const spotifyId = this.user.spotify_id;
          this.tracksByUser[spotifyId] = res;
          this.userAdded({value: this.user});
        });
      },


      saveMyTracks() {
        Loading.show({ 
          spinner: QSpinnerFacebook,
          spinnerColor: 'green',
          spinnerSize: 140,
          backgroundColor: 'black',
          message: 'Saving your tracks. Hang on...',
          messageColor: 'green'
        });
        MixTapeMakerService.SaveMyTracks().then(() => {
          this.userAdded({value: this.user});
          Loading.hide();
        });
      },

      refreshTable() {
        let trackHashOld: any = {};
        let trackHashNew: any = {};

        this.selectedUsers.forEach((user, index) => {


          const spotifyId = user.spotify_id;

          if (spotifyId in this.tracksByUser) {

            trackHashOld = trackHashNew;
            trackHashNew = {};

            let userTracks = this.tracksByUser[spotifyId] as Track[];

            userTracks.forEach(track => {

              const name = track.name;
              if (name in trackHashOld || index === 0){
                trackHashNew[name] = track;
              }
            });

          }

        });

        this.tracks = Object.values(trackHashNew);
      },


      userAdded(obj: any) {
        const spotifyId = obj.value.spotify_id;

        if(!this.selectedUsers.some(u => u.spotify_id === spotifyId)){
          this.selectedUsers.push(obj.value);
        }

        if(!this.cachedUsers.some(u => u.spotify_id === spotifyId)){
          this.cachedUsers.push(obj.value);
        }

        if (!(spotifyId in this.tracksByUser)) {
          MixTapeMakerService.GetTracksByUser(spotifyId).then(res => {
            this.tracksByUser[spotifyId] = res;
            this.refreshTable();
          })
        }
        else{
          this.refreshTable();
        }
      },


      userRemoved(obj: any) {
        const user: User = obj.value;
        this.selectedUsers = this.selectedUsers.filter(u => u.spotify_id != user.spotify_id);
        this.refreshTable();
      },

        /**
       * Does the searching for our input box
       * Wait 1 second before searching so that we give the user time to stop typing
       */
      filterFn(val: string, update: any, abort: any) {

        // if the user has typed less than 2 letters, dont do anything
        if (val.length < 2) {
          abort();
          return
        }

        // If we've initiated a search, kill it and start a new one
        if(this.searchAheadTimeout !== null){
          clearTimeout(this.searchAheadTimeout);
        }

        // perform a search in 1 second
        this.searchAheadTimeout = setTimeout(() => {
          // performs search
          MixTapeMakerService.SearchUsers(val)
            .then((res: User[]) => {
              const filtedCacheUsers = this.cachedUsers.filter(u => u.name.toLowerCase().startsWith(val.toLowerCase()));

              let merged = filtedCacheUsers.concat(res);
              let options: User[] = []
              let userHash: any = {}

              merged.forEach(user => {
                const name = user.name;
                if (!(name in userHash)){
                  userHash[name] = true;
                  options.push(user);
                }

              });

              // actually update our list of options to the user
              update(() => {
                  this.userOptions = options
              });

            });
          }, 100);

      }

   

    }

  })
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.background {
  background-color:#191414;
  background-size: cover; 
  min-height:99vh;
  display: flex;
  justify-content: center;
  flex-direction: column;
}


.track-table {
  min-width: 50vw;
  height: 50vh;
  margin-left: 5vw;
  margin-right: 5vw;
  margin-top: 2vw;
  margin-bottom: 3vw;
}

.header {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  justify-self: flex-start;
}

.logo {
  width: 45vw;
  max-width: 50px;
  height: auto;
  align-self: center;
}

.title {
  color: #1DB954;
  font-size: max(min(8vw, 7vh), 30px);
  font-weight: 800;
  font-family: sans-serif;
  margin-bottom: 5vw;
}

.table-control {
  color: #191414;
  background-color:#1DB954;
  font-size: max(1.4vw, 10px);
}

.table-controls {
    display: flex;
    justify-content: space-around;
}

.user-selection {
  border-color: white;
  background-color: #332e2e;
  margin-left: 5vw;
  margin-right: 5vw;
}

.save-dialog {
  color: #292929;
  background-color:#c9c9c9;
}

.mixtape-dialog {
  color: #292929;
  background-color:#c9c9c9;
}

.mixtape-button {
  color: #191414;
  background-color:#1DB954;
  font-size: min(3.3vw, 20px);
  align-self:flex-start;
  font-family: sans-serif;
  font-weight: 700;
  margin-left: 5vw;
  
}


</style>
