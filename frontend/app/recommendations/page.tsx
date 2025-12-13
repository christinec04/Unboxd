"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import api from "@/app/api";
import { NavBar } from "@/components/nav-bar";
import { useRouter } from "next/navigation";
import { Loading } from "@/components/loading";
import { Result } from "@/components/result";
import { Error } from "@/components/error";
import { Status } from "@/app/api/types.gen";

export default function RecommendationsPage() {
  type Undefinable<Status> = Status | undefined;

  const searchParams = useSearchParams();
  const [username, setUsername] = useState(searchParams.get("username"));
  const [movies, setMovies] = useState([]);
  const router = useRouter();
  const [status, setStatus] = useState<Status>(Status.STARTING);

  const failed: Undefinable<Status>[] = [Status.FAILED_INVALID_USERNAME, 
    Status.FAILED_NO_RATINGS_AND_REVIEWS_TO_SCRAPE_FOR_THE_USER,
    Status.FAILED_ERROR_WHILE_SCRAPING,
    Status.FAILED_NO_DATA_AVAILABLE_ABOUT_THE_USER_RATED_AND_REVIEWS_MOVIES,
    Status.FAILED_NO_TRENDING_MOVIES_NOT_ALREADY_REVIEWED_ARE_AVAILABLE_FOR_RECOMMENDATION];
  
  const onLoad = async () => {
    if (!username) { return; }

    try {
      await api.post('/usernames/', { username: username });
      const intervalId = setInterval(() => getStatus(intervalId), 2000);
    } 
    catch (error) {
      // error handle
    }
  };

  const getStatus = async (intervalId: NodeJS.Timeout) => {
    try {
      const response = await api.get('/status/', { params: { username } });
      const newStatus = response.data;
      setStatus(newStatus);

      if (newStatus == Status.FINISHED) {
        console.log("Finished");
        clearInterval(intervalId);
        fetchMovies();
      }

      if (failed.includes(newStatus)){
        clearInterval(intervalId);
      } 
    } 
    catch (error) {
      clearInterval(intervalId);
    }
  };

  const fetchMovies = async () => {
    try {
      const res = await api.get(`/movies/?username=${username}`);
      setMovies(res.data);
      console.log(res.data)
    }
    catch(error) {

    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
     router.push(`/recommendations?username=${username}`);
  };

  // On page load
  useEffect(() => {
    onLoad();
  }, [username]);


  return (
    <div className="min-h-screen w-full bg-background flex flex-col">
      <NavBar username={username} setUsername={setUsername} handleSubmit={handleSubmit} />

      {status == Status.FINISHED && <Result movies={movies} />}
      {failed.includes(status) && <Error message={status}/>}
      {status != Status.FINISHED && !failed.includes(status) && <Loading status={status}/>} {/* loading doesn't work atm */}
    
    </div>
  );
}
