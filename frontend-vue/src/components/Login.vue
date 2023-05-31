<template>
  <div class="background">
    <div class="logo"><img class="logo" alt="Vue logo" src="./../assets/mixtape.png"></div>
    
    <div class="title">Spotify </div>
    <div class="title">Mix Tapes</div>
    <q-btn v-on:click="login" class="login-button" label="Login" />

  </div>

</template>

<script lang="ts">
import { defineComponent } from 'vue'
import querystring from 'querystring';
//import HttpRequests from '../Rest/HttpRequests';

export default defineComponent({

    components: {
    },

    props: {
    },

    data() {
      return {
        AuthURL: 'https://accounts.spotify.com/authorize' as string,

        ClientID: 'redacted' as string,

        RedirectURL: 'http://localhost:5000/callback' as string,

        Scope: 'user-read-private user-read-email playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative user-library-read',

        State: '' as string,
      }
    },

    computed: {

      LoginPage: function(): string {
        // your application requests authorization
        const url = 'https://accounts.spotify.com/authorize?' +
          querystring.stringify({
            response_type: 'code',
            client_id: this.ClientID,
            scope: this.Scope,
            redirect_uri: this.RedirectURL,
            state: this.State
          });

        return url;
      }

    },




    mounted: function() {
      this.State = this.generateRandomString(16);
    }, 


    methods: {

      login() {
        window.location.href = this.LoginPage;
      },

      generateRandomString(length: number) : string {
        var text = '';
        var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

        for (var i = 0; i < length; i++) {
          text += possible.charAt(Math.floor(Math.random() * possible.length));
        }
        return text;
      },

    }

  })
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.background {
  background-color:#1DB954;
  background-size: cover; 
  min-height:99vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;

}

.logo {
  width: 45vw;
  max-width: 200px;
  height: auto;
  align-self: center;
}

.title {
  color: #191414;
  font-size: max(8vw, 50px);
  font-weight: 800;
  font-family: sans-serif;
}

.login-button {
  color: #1DB954;
  background-color:#191414;
  font-size: max(2.8vw, 25px);
  
}


</style>
