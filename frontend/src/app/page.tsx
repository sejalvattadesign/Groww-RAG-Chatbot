'use client';

import React, { useState, useEffect, useRef } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  query?: string;
  source_url?: string | null;
  last_updated?: string | null;
  isSafe?: boolean;
}

export default function GrowwLandingPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const suggestions = [
    "Expense ratio of HDFC Mid Cap",
    "Exit load details for HDFC Focused Fund",
    "Minimum SIP amount for Large Cap",
    "ELSS lock-in period",
    "Riskometer classification of ELSS",
    "Benchmark index for HDFC Equity Fund",
    "Process to download statements"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (queryOverride?: string) => {
    const userQuery = queryOverride || input.trim();
    if (!userQuery || isLoading) return;

    setMessages((prev) => [...prev, { role: 'user', content: userQuery, query: userQuery }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userQuery }),
      });

      if (!response.ok) throw new Error('Backend unreachable');

      const data = await response.json();
      setMessages((prev) => [...prev, { 
        role: 'assistant', 
        content: data.answer,
        query: userQuery,
        source_url: data.source_url,
        last_updated: data.last_updated,
        isSafe: data.is_safe 
      }]);
    } catch (error) {
      setMessages((prev) => [...prev, { 
        role: 'assistant', 
        content: "I'm sorry, the backend server is currently unreachable.",
        query: userQuery,
        isSafe: false
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="main-container">
      {/* Groww Navbar */}
      <nav className="navbar">
        <div className="logo" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ width: '32px', height: '32px', background: 'linear-gradient(135deg, #00d09c, #00b386)', borderRadius: '50%' }}></div>
          <span style={{ fontSize: '24px', fontWeight: 'bold', color: '#44475b' }}>Groww</span>
        </div>
        <div className="nav-links">
          <a href="#">Stocks</a>
          <a href="#">F&O</a>
          <a href="#">Mutual Funds</a>
          <a href="#">More</a>
          <div style={{ position: 'relative', marginLeft: '20px' }}>
            <input type="text" placeholder="Search Groww..." style={{ padding: '8px 40px', borderRadius: '20px', border: '1px solid #ebedf2', width: '250px' }} />
          </div>
          <a href="#" className="login-btn">Login/Sign up</a>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="hero-section">
        <h2>Build wealth,<br />SIP by SIP.</h2>
        <p>Invest in Direct Mutual Funds.</p>
        <button className="get-started-btn">Get started</button>

        <div style={{ marginTop: '80px', position: 'relative', display: 'flex', justifyContent: 'center' }}>
           <div style={{ width: '800px', height: '450px', background: '#f4f7fb', borderRadius: '20px', border: '1px solid #ebedf2', overflow: 'hidden', boxShadow: '0 20px 40px rgba(0,0,0,0.05)' }}>
             <div style={{ padding: '20px', background: 'white', borderBottom: '1px solid #ebedf2', display: 'flex', gap: '10px' }}>
                <div style={{ width: '12px', height: '12px', background: '#ff5f56', borderRadius: '50%' }}></div>
                <div style={{ width: '12px', height: '12px', background: '#ffbd2e', borderRadius: '50%' }}></div>
                <div style={{ width: '12px', height: '12px', background: '#27c93f', borderRadius: '50%' }}></div>
             </div>
             <div style={{ padding: '40px', textAlign: 'left' }}>
                <div style={{ width: '200px', height: '20px', background: '#ebedf2', marginBottom: '20px' }}></div>
                <div style={{ width: '400px', height: '40px', background: '#00d09c', marginBottom: '40px', opacity: 0.2 }}></div>
                <div style={{ display: 'flex', gap: '20px' }}>
                   <div style={{ flex: 1, height: '150px', background: '#ebedf2', borderRadius: '10px' }}></div>
                   <div style={{ flex: 1, height: '150px', background: '#ebedf2', borderRadius: '10px' }}></div>
                   <div style={{ flex: 1, height: '150px', background: '#ebedf2', borderRadius: '10px' }}></div>
                </div>
             </div>
           </div>
        </div>
      </main>

      {/* Chat Widget Container */}
      {isChatOpen && (
        <div className="chat-widget">
          <div className="chat-header">
            <h1>Mutual Fund FAQ</h1>
            <p>Facts-only. No investment advice.</p>
            <div className="close-btn" onClick={() => setIsChatOpen(false)}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </div>
          </div>

          <div className="messages-container">
            {messages.length === 0 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <p style={{ fontSize: '13px', color: '#7c7e8c', fontWeight: '500' }}>SUGGESTED QUERIES</p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {suggestions.map((s, idx) => (
                    <button 
                      key={idx} 
                      onClick={() => handleSend(s)}
                      style={{ padding: '8px 16px', borderRadius: '20px', border: '1px solid #00d09c', color: '#00d09c', background: 'white', fontSize: '12px', fontWeight: '500', cursor: 'pointer' }}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((m, i) => (
              <div key={i} className="message-pair">
                {m.role === 'user' ? (
                  <div className="user-query" style={{ color: '#00d09c', fontWeight: '600' }}>{m.content}</div>
                ) : (
                  <>
                    <div className="assistant-answer">{m.content}</div>
                    {(m.source_url || m.last_updated) && (
                      <div className="metadata-container">
                        {m.source_url && (
                          <a href={m.source_url} target="_blank" rel="noreferrer" className="view-source">
                            View source →
                          </a>
                        )}
                        {m.last_updated && (
                          <div className="last-updated">Last updated from sources: {m.last_updated}</div>
                        )}
                      </div>
                    )}
                  </>
                )}
                {i < messages.length - 1 && <div className="divider" />}
              </div>
            ))}
            {isLoading && (
              <div className="assistant-answer" style={{ color: '#7c7e8c' }}>Verifying factual data...</div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-area">
            <div className="input-container">
              <input
                type="text"
                className="input-field"
                placeholder="Search for mutual fund facts"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              />
              <div className="search-icon" onClick={handleSend}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Reopen Button */}
      {!isChatOpen && (
        <div 
          onClick={() => setIsChatOpen(true)}
          style={{ position: 'fixed', bottom: '30px', right: '30px', background: '#00d09c', width: '60px', height: '60px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', boxShadow: '0 8px 24px rgba(0,208,156,0.3)' }}
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        </div>
      )}
    </div>
  );
}
