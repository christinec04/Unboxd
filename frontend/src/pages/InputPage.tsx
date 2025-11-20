import { useState } from "react";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group"
import { Spinner } from "@/components/ui/spinner"
import { TypeAnimation } from 'react-type-animation';
import api from '../api';

export function Input() {
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [disabled, setDisabled] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!username) { return}

    setLoading(true);
    setDisabled(true);

    try { // Need to check if username exists
      await api.post('/scrapeReviews', { username: username });
      console.log("Finished scraping successfully!");
    } 
    catch (error) {
      console.error("Error sending username to backend", error);
    }
  };

  return (
    <div className="@container flex flex-col h-screen justify-center items-center">
      <div className="w-full max-w-md">
        <TypeAnimation
          sequence={[
            'Movie Recommendation System',
            () => {
              console.log('Sequence completed');
            },
          ]}
          wrapper="span"
          style={{ fontSize: '2em', display: 'inline-block' }}
        />

        <form onSubmit={handleSubmit}>
          <InputGroup>
            <InputGroupInput id="username"
            type="text"
            placeholder="Enter your Letterboxd username"
            value={username}                
            onChange={(e) => setUsername(e.target.value)} 
            disabled={disabled}
            autoComplete="off"/>

            <InputGroupAddon align="inline-end">
              {loading && <Spinner />} 
            </InputGroupAddon>
          </InputGroup>
        </form>

        </div>
    </div>
  )
}
