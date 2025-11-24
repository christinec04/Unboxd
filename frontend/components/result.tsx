import { useSearchParams } from "next/dist/client/components/navigation";
import {ItemGroup} from "@/components/ui/item"
import { Movie } from "@/app/types"
import { useState } from "react"
import YouTube, { YouTubeProps } from "react-youtube";
import { MovieCard } from "./movie-card";

interface ResultProps {
  movies: Movie[];
}

export function Result({ movies }: ResultProps) {
  const username = useSearchParams().get("username");
  const [trailer, setTrailer] = useState<Movie | null>(null);
  const onPlayerReady: YouTubeProps['onReady'] = (event) => {
    // access to player in all event handlers via event.target
    event.target.pauseVideo();
  }

  const opts: YouTubeProps['opts'] = {
    height: '390',
    width: '640',
    playerVars: {
      // https://developers.google.com/youtube/player_parameters
      autoplay: 1,
    },
  };

  return (
    <>
      {/* Profile */}
      <section className="py-24 relative overflow-hidden bg-accent">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative flex justify-center items-center gap-8 ">
          {/* If we can get Letterboxd profile pic, display it here */}
          {/* <Avatar>
            <AvatarImage src={`https://letterboxd.com/${username}/#avatar-large`} />
            <AvatarFallback></AvatarFallback>
          </Avatar> */}

            <h3 className="scroll-m-20 text-2xl font-semibold tracking-tight text-center">
              {username}&apos;s movie recommendations
            </h3>
          </div>
      </section>


      {/* Trailer */}
      {trailer && 
      (
        <section className="py-24 relative overflow-hidden border-b-1">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative flex flex-col justify-center items-center gap-8">
             <h4 className="scroll-m-20 text-xl font-semibold tracking-tight text-center">
              Now Playing: {trailer.name}
            </h4>
            <YouTube videoId={trailer.trailerID} opts={opts} onReady={onPlayerReady} />
          </div>
        </section>
      )}

      {/* Movies */}
      <section className="py-24 relative overflow-hidden">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
          <ItemGroup className="grid gap-4 grid-cols-[repeat(auto-fill,minmax(200px,1fr))]">
            {movies.map((movie) => (
              <MovieCard key={movie.name} {...movie} setTrailer={setTrailer} />
            ))}
          </ItemGroup>
        </div>
      </section>
    </>
  );
}