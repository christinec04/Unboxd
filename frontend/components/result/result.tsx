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

export function Result() {
  const username = useSearchParams().get("username");
  const dummyData = [{name:"Barbie", 
    year:"2023", 
    genre:["Comedy", "Fantasy"],
    description:"Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.", 
    posterURL:"https://a.ltrbxd.com/resized/film-poster/2/7/7/0/6/4/277064-barbie-0-230-0-345-crop.jpg?v=1b83dc7a71"},
  
    {name:"Oppenheimer", 
    year:"2023", 
    genre:["Drama", "History"],
    description:"The story of J. Robert Oppenheimer's role in the development of the atomic bomb during World War II.", 
    posterURL:"https://a.ltrbxd.com/resized/film-poster/7/8/4/3/2/8/784328-oppenheimer-0-230-0-345-crop.jpg?v=e3c6e7a32c"},
  ];

  return (
    <>
      {/* Profile */}
      <section className="py-24 relative overflow-hidden">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative 
        flex justify-center items-center gap-8">
          {/* If we can get Letterboxd profile pic, display it here */}
          <Avatar>
            <AvatarImage src={`https://letterboxd.com/${username}/#avatar-large`} />
            <AvatarFallback></AvatarFallback>
          </Avatar>

            <h1>{username}</h1>
          </div>
      </section>


      {/* Trailer */}

      {/* Movies */}
      <section className="py-24 relative overflow-hidden">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
          
          <ItemGroup className="flex flex-row flex-wrap gap-6 justify-center">
            {dummyData.map((movie) => (
              <Item key={movie.name} variant="outline" className="w-50">
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
                    <ExternalLinkIcon className="size-4" />
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