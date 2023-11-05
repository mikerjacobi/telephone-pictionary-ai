import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { PrimaryButton, SecondaryButton } from 'components/Button';

const Game: React.FC = () => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(prompt);
  };

  return (
    <div className="min-h-screen bg-custom-green flex flex-col items-center justify-center p-4">
      <form onSubmit={handleSubmit} className="w-full max-w-md p-6">
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
        <PrimaryButton label="Submit" onClick={handleSubmit} />
      </form>
    </div>
  );
};


export default Game;
