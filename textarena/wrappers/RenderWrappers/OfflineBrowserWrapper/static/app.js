console.log('Loading base components...');

// Base components
function EndGameOverlay({ endGameState, onClose }) {
    return (
        <div className="end-game-overlay" onClick={(e) => {
            if (e.target.className === 'end-game-overlay') {
                onClose();
            }
        }}>
            <div className="end-game-content">
                <button className="close-button" onClick={onClose}>×</button>
                <h1>Game Over</h1>
                <p className="winner-text">{endGameState.winner_text}</p>
                <p className="reason-text">{endGameState.reason}</p>
            </div>
        </div>
    );
}

const ChatHistory = ({ chatHistory, currentPlayerId }) => {
    const chatContainerRef = React.useRef(null);

    // Scroll to the bottom when chat updates
    React.useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [chatHistory]);

    return (
        <div className="chat-container">
            <h2>Game Chat</h2>
            <div className="chat-messages" ref={chatContainerRef}>
                {chatHistory.map((msg, i) => {
                    const isCurrentPlayer = msg.player_id === currentPlayerId;
                    return (
                        <div
                            key={i}
                            className={`chat-bubble ${isCurrentPlayer ? "right" : "left"}`}
                            style={{ backgroundColor: msg.color }}
                        >
                            <div className="player-name">{msg.player_name}</div>
                            <div className="message-content">{msg.message}</div>
                            <div className="timestamp">{msg.timestamp}</div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};



const BaseGameContainer = ({ children, gameState, renderGameInfo }) => {
    const [showEndGame, setShowEndGame] = React.useState(false);

    React.useEffect(() => {
        if (gameState.end_game_state) {
            setShowEndGame(true);
        }
    }, [gameState.end_game_state]);

    return (
        <div className="page-container">
            <header className="main-header">
                <h1 class="textarena-title">
                    <img src="http://127.0.0.1:8000/static/assets/TextArena-logo0.png" alt="TextArena Logo" />
                </h1>

                <h2 className="game-env-id">
                        {gameState.env_id ? `${gameState.env_id}` : "No Environment ID"}
                </h2>

                <br /> {/* Add this to create a line break */}

                <a href={gameState.github_link}
                   className="github-link" 
                   target="_blank" 
                   rel="noopener noreferrer">
                    <img
                        src="http://127.0.0.1:8000/static/assets/github-mark-white.png"
                        alt="GitHub Logo"
                        className="github-logo"
                    />
                    View on GitHub
                </a>
            </header>

            <div className="game-layout">
                {/* Main children components */}
                <div className="game-main-content">
                    {children}
                </div>

                {/* Game Info Section */}
                <div className="game-info-wrapper">
                    <h2 className="game-info-header">Game Status</h2>
                    <div className="game-info-container">
                        <div className="game-info-content">
                            {renderGameInfo && renderGameInfo(gameState)}
                        </div>
                    </div>
                </div>
            </div>

            {/* End Game Overlay */}
            {gameState.end_game_state && showEndGame && 
                <EndGameOverlay 
                    endGameState={gameState.end_game_state} 
                    onClose={() => setShowEndGame(false)}
                />
            }

            {/* Chat History */}
            {gameState.chat_history && (
                <ChatHistory chatHistory={gameState.chat_history} />
            )}
        </div>
    );
};

console.log('Base components loaded');