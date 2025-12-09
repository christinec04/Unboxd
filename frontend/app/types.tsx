export interface Movie {
    movieId: string;
    name: string;
    year: number;
    genre: string[];
    posterURL: string;
    letterboxdURL: string;
    description: string;
    trailerID: string;
    similarityScore: number;
}
