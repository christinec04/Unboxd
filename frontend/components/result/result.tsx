import { useSearchParams } from "next/dist/client/components/navigation";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Item,
  ItemActions,
  ItemContent,
  ItemDescription,
  ItemFooter,
  ItemGroup,
  ItemHeader,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { ExternalLinkIcon } from "lucide-react"
import Image from "next/image"
import { Movie } from "@/app/types"
import Link from "next/link"
import { Play, CirclePlay } from "lucide-react"
import { useState } from "react"
import YouTube, { YouTubeProps } from "react-youtube";

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
        <section className="py-24 relative overflow-hidden">
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
          
          <ItemGroup className="flex flex-row flex-wrap gap-6 justify-center">
            {movies.map((movie) => (
              <Item key={movie.name} variant="outline" className="w-50 bg-accent">
                <ItemHeader className="group aspect-[2/3] rounded-sm overflow-hidden relative">
                    <div className="w-full h-full absolute inset-0 cursor-pointer 
                      z-10 flex items-center justify-center bg-black/30 opacity-0 group-hover:opacity-100">
                        <Play className="h-[20px] w-[20px] text-white                      group-hover:translate-y-0 transform translate-y-full transition-all duration-300"/>
                    </div>
                    <Image
                      src={movie.posterURL}
                      alt={movie.name}
                      width={230}
                      height={345}
                      className="h-full w-full object-cover rounded-sm"
                    />
                </ItemHeader>

                <ItemContent>
                  <ItemTitle className="line-clamp-1">
                    {movie.name} -{" "}
                    <span className="text-muted-foreground">{movie.year}</span>
                  </ItemTitle>
                  <ItemDescription>{movie.description}</ItemDescription>
                </ItemContent>

                <ItemFooter>
                  <div className="flex flex-wrap gap-2">
                    {movie.genre.map((g) => ( <Badge key={g}>{g}</Badge> ))}
                  </div>

                  <Tooltip>
                    <TooltipTrigger asChild>
                      <ItemActions>
                        <Link href={movie.letterboxdURL} target="_blank" rel="noopener noreferrer">
                          <ExternalLinkIcon className="size-4" />
                        </Link>
                      </ItemActions>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>View on Letterboxd</p>
                    </TooltipContent>
                  </Tooltip>
                </ItemFooter>
              </Item>
            ))}
          </ItemGroup>
        </div>
      </section>
    </>
  );
}