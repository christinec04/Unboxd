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

export enum Status {
    STARTING = "starting",
    SCRAPING_REVIEWS = "scraping reviews",
    PREPROCESSING_DATA = "preprocessing data",
    FINDING_RECOMMENDATION = "finding recommendations",
    FINISHED = "finished",
    FAILED = "failed",
}
