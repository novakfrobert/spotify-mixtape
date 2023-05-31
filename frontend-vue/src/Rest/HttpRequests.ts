import axios from "axios";
import Track from "../Models/Track";

class HttpRequests {

    private http: any


    constructor() {
        this.http = axios.create({
            baseURL: "http://www.localhost:5000/",
            headers: {
              "Content-type": "application/json"
            }
          })
    }

    Login(): Promise<any> {
        const endpoint = "login";
        return this.http.get(endpoint);
    }
    
    GetMyTracks(): Promise<any> {
      const endpoint = "model/fromspotify/tracks/me";
      return this.http.get(endpoint);
    }

    SaveMyTracks(): Promise<any> {
      const endpoint = "model/tracks/me/save";
      return this.http.get(endpoint);
    }


    GetTracksByUser(spotifyId: string): Promise<any> {
      const endpoint = `model/fromdb/tracks/${spotifyId}/`;
      return this.http.get(endpoint);
    }


    CreatePlaylist(tracks: Track[], name: string, spotifyId: string): Promise<any> {
      const endpoint = `${spotifyId}/playlists/create`;
      const payload = { name: name, tracks: tracks }
      return this.http.post(endpoint, payload);
    }


    SearchUsers(query: string): Promise<any> {
      let endpoint = "model/get/users";

      if(query !== ""){
        endpoint = endpoint + "/?query=" + query
      }

      return this.http.get(endpoint);
    }


    GetMyUserInfo(): Promise<any> {
      const endpoint = "model/me";
      return this.http.get(endpoint);
    }
}

export default new HttpRequests();
