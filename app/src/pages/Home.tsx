import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  const [gameCode, setGameCode] = useState<string>('');

  return (
    <div className="min-h-screen bg-custom-blue flex items-center justify-center">
      <div className="text-center">
        <input
          className="text-black mb-4 p-2"
          type="text"
          value={gameCode}
          onChange={(e) => setGameCode(e.target.value)}
        />
        <Link to={`/game/${gameCode}`}>
          <button className="bg-custom-pink text-white font-bold py-2 px-4 rounded">
            Submit
          </button>
        </Link>
      </div>
    </div>
  );
};

export default Home;
