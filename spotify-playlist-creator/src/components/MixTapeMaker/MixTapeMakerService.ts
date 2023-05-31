import HttpRequests from "../../Rest/HttpRequests";
import Track from "../../Models/Track";
import User from "../../Models/User";

class MixTapeMakerService {

    async GetMyTracks(): Promise<Array<Track>> {

        return await HttpRequests.GetMyTracks().then((res: any) => {
        
          const new_tracks: Array<Track> = [];
          res.data.forEach(track => {
            
            const artists = track.artists.map(artist => artist.name).join()
            const new_track: Track = {name: track.name as string, artists: artists as string, uri: track.uri as string};
            new_tracks.push(new_track);
          });
          return new_tracks;
        });
    }

    async SaveMyTracks(): Promise<Array<Track>> {

      return await HttpRequests.SaveMyTracks().then((res: any) => {
      
        const new_tracks: Array<Track> = [];

        return new_tracks;
      });
  }


    async GetTracksByUser(spotifyId: string): Promise<Array<Track>> {

      return await HttpRequests.GetTracksByUser(spotifyId).then((res: any) => {
      
        const new_tracks: Array<Track> = [];
        res.data.forEach(track => {
          
          const artists = track.artists.map(artist => artist.name).join()
          const new_track: Track = {name: track.name as string, artists: artists as string, uri: track.uri as string};
          new_tracks.push(new_track);
        });
        return new_tracks;
      });
  }


    async SearchUsers(query: string): Promise<User[]> {

        return await HttpRequests.SearchUsers(query).then((res: any) => {
            return res.data
        });
    }


    async GetMyUserInfo(): Promise<User> {
      return await HttpRequests.GetMyUserInfo().then((res: any) => {
        const user: User = {
          name: res.data.name,
          spotify_id: res.data.spotify_id,
          nickname: res.data.nickname,
          is_saved: res.data.is_saved
        }

        return user
      });
    }


    async CreatePlaylist(tracks: Track[], name: string, spotifyId: string): Promise<any> {
      return await HttpRequests.CreatePlaylist(tracks, name, spotifyId);
    }



}

export default new MixTapeMakerService();