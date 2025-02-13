// src/TruthScope.jsx
import React, { useState } from 'react';
import { Send, ChevronDown, ChevronUp } from 'lucide-react';

const TruthScope = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsLoading(true);
    // Add the user query to messages
    setMessages((prev) => [...prev, { type: 'user', content: input }]);

    try {
      // Call the backend API (adjust the URL if necessary)
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input }),
      });
      if (!response.ok) {
        throw new Error("Failed to fetch results");
      }
      const data = await response.json();
      setMessages((prev) => [...prev, { type: 'system', content: data }]);
    } catch (err) {
      console.error(err);
      alert("Error: " + err.message);
    } finally {
      setInput('');
      setIsLoading(false);
    }
  };

  const ArticleDropdown = ({ article }) => {
    const [isOpen, setIsOpen] = useState(false);
  
    // Define the mapping first
    const borderColorClasses = {
      red: "border-red-500",
      green: "border-green-500",
      orange: "border-orange-500",
      gray: "border-gray-500", // if needed
    };
  
    // Normalize the color and get the corresponding class
    const normalizedColor = article.color.toLowerCase();
    const borderClass = borderColorClasses[normalizedColor] || "border-black";
  
    return (
      <div className={`mb-2 border-2 rounded-lg p-3 ${borderClass}`}>
        <div 
          className="flex justify-between items-center cursor-pointer"
          onClick={() => setIsOpen(!isOpen)}
        >
          <h3 className="font-medium">{article.title}</h3>
          {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </div>
        {isOpen && (
          <div className="mt-2 text-gray-600">
            {article.content}
          </div>
        )}
      </div>
    );
  };
  
  

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Centered container with a max width */}
      <div className="max-w-3xl mx-auto w-full">
        {/* Header */}
        <div className="text-center py-6 bg-white shadow-sm">
          <h1 className="text-3xl font-bold text-gray-800">TruthScope</h1>
          <p className="text-gray-600 mt-2">Ask me a question!</p>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-auto p-4">
          {messages.map((message, index) => (
            <div key={index} className="mb-4">
              {message.type === 'user' ? (
                <div className="bg-blue-100 p-3 rounded-lg max-w-3xl ml-auto">
                  {message.content}
                </div>
              ) : (
                <div className="max-w-3xl">
                  {message.content.articles.map((article, i) => (
                    <ArticleDropdown key={i} article={article} />
                  ))}
                  <div className="bg-gray-100 p-3 rounded-lg mt-4">
                    {message.content.summary}
                  </div>
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-center">
              <div className="animate-pulse text-gray-500">Analyzing...</div>
            </div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="p-4 bg-white border-t">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your question..."
              className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 disabled:bg-blue-300 transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TruthScope;
