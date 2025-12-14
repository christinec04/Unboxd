"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import api from "@/app/api";
import { NavBar } from "@/components/nav-bar";
import { useRouter } from "next/navigation";
import { Result } from "@/components/result";
import { StatusIndicator } from "@/components/status-indicator";
import { Status } from "@/app/api/types.gen";

type ExtendedStatus = Status | "ERROR";

export default function RecommendationsPage() {
  const searchParams = useSearchParams();
  const [username, setUsername] = useState(searchParams.get("username"));
  const [movies, setMovies] = useState([]);
  const router = useRouter();
  const [status, setStatus] = useState<ExtendedStatus>(Status.STARTING);
  
  const onLoad = async () => {
    if (!username) { return; }

    try {
      await api.post('/usernames/', { username: username });
      const intervalId = setInterval(() => getStatus(intervalId), 2000);
    } 
    catch (error) {
      console.log(error);
      setStatus("ERROR");
    }
  };

  const getStatus = async (intervalId: NodeJS.Timeout) => {
    try {
      const response = await api.get('/status/', { params: { username } });
      const newStatus = response.data;
      setStatus(newStatus);
      console.log(newStatus);
      
      if (newStatus == Status.FINISHED) {
        console.log("Finished");
        clearInterval(intervalId);
        fetchMovies();
      }
    } 
    catch (error) {
      clearInterval(intervalId);
      setStatus("ERROR");
      console.log(error);
    }
  };

  const fetchMovies = async () => {
    try {
      const res = await api.get(`/movies/?username=${username}`);
      setMovies(res.data);
      console.log(res.data)
    }
    catch(error) {
      setStatus("ERROR");
      console.log(error);
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

      {status === Status.FINISHED && <Result movies={movies} />}
      {status !== Status.FINISHED && <StatusIndicator status={status}/>}
    
    </div>
  );
}
