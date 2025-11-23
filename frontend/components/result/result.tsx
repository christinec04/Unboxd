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
import { ExternalLinkIcon } from "lucide-react"
import Image from "next/image"
import { Movie } from "@/app/types"
import Link from "next/link"

interface ResultProps {
  movies: Movie[];
}

export function Result({ movies }: ResultProps) {
  const username = useSearchParams().get("username");
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

      {/* Movies */}
      <section className="py-24 relative overflow-hidden">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
          
          <ItemGroup className="flex flex-row flex-wrap gap-6 justify-center">
            {movies.map((movie) => (
              <Item key={movie.name} variant="outline" className="w-50 bg-accent">
                <ItemHeader className="aspect-[2/3] rounded-sm overflow-hidden">
                  <Image
                    src={movie.posterURL}
                    alt={movie.name}
                    width={230}
                    height={345}
                    className="h-full w-full object-cover"
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

                  <ItemActions>
                    <Link href={movie.letterboxdURL} target="_blank" rel="noopener noreferrer">
                      <ExternalLinkIcon className="size-4" />
                    </Link>
                  </ItemActions>
                </ItemFooter>
              </Item>
            ))}
          </ItemGroup>
        </div>
      </section>
    </>
  );
}