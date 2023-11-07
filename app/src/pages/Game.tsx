import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { PrimaryButton } from 'components/Button';

const Game: React.FC = () => {
  const { gameId } = useParams<{ gameId: string }>();
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      let url = `${process.env.REACT_APP_API}/game/${gameId}/prompt`
      console.log(`POSTing to ${url}`)
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setImageUrl(data.image_url);
    } catch (e) {
      setError('Failed to fetch the image.');
      console.error('There was an error!', e);
    }

    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-custom-green flex flex-col items-center justify-center p-4">
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit} className="w-full max-w-md">
        <label htmlFor="imagePrompt" className="block text-lg font-medium text-gray-700 mb-2">
          Image Prompt
        </label>
        <textarea
          id="imagePrompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="textarea textarea-bordered w-full mb-4 h-32 p-2"
          rows={4}
        />
        <PrimaryButton label="Submit" type="submit" disabled={isLoading} />
      </form>
      {isLoading && <p>Loading...</p>}
      {imageUrl && <img src={imageUrl} alt="Generated" className="mt-4" />}
    </div>
  );
};

export default Game;
