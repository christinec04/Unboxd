import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import {
  Item,
  ItemActions,
  ItemContent,
  ItemDescription,
  ItemFooter,
  ItemHeader,
  ItemTitle,
} from "@/components/ui/item"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { ExternalLinkIcon } from "lucide-react"
import Image from "next/image"
import { Movie } from "@/app/api/types.gen"
import Link from "next/link"
import { Play, CirclePlay } from "lucide-react"

interface MovieCardProps extends Movie {
  setTrailer: (movie: Movie) => void;
}

export function MovieCard({ setTrailer, ...movie }: MovieCardProps) {
    return (
        <>
            <Item key={movie.name} variant="outline" className="bg-accent">
                {/* Image */}
                <ItemHeader className="group aspect-[2/3] rounded-sm overflow-hidden relative">
                    {/* Hover Overlay */}
                    <div className="w-full h-full absolute inset-0 cursor-pointer 
                      z-10 flex items-center justify-center bg-black/30 opacity-0 group-hover:opacity-100"
                        onClick={() => setTrailer(movie)}>
                        <Play className="h-[20px] w-[20px] text-white                      group-hover:translate-y-0 transform translate-y-full transition-all duration-300" />
                    </div>
                    {/* Movie Poster */}
                    <Image
                        src={movie.posterURL}
                        alt={movie.name}
                        width={1000}
                        height={1500}
                        className="h-full w-full object-cover rounded-sm"
                    />
                </ItemHeader>

                {/* Movie Info */}
                <ItemContent>
                    <ItemTitle className="line-clamp-1">
                        {movie.name} -{" "}
                        <span className="text-muted-foreground">{movie.year}</span>
                    </ItemTitle>
                    <ItemDescription>{movie.description}</ItemDescription>
                </ItemContent>

                {/* Movie Footer */}
                <ItemFooter>
                    {/* Genres */}
                    <div className="flex flex-wrap gap-2">
                        {movie.genre.map((g) => (<Badge key={g}>{g}</Badge>))}
                    </div>

                    {/* Letterboxd Link */}
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
        </>
    );
}