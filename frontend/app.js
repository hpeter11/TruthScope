import React, { useState } from 'react';
import { Send, ChevronDown, ChevronUp } from 'lucide-react';

const TruthScope = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Mock response data structure
  const mockResponse = {
    articles: [
      { title: "Climate Change", content: "Climate change is the long-term alteration of temperature and typical weather patterns...", status: "agree" },
      { title: "Global Warming Effects", content: "The effects of global warming include rising sea levels, extreme weather...", status: "unrelated" },
      { title: "Environmental Impact", content: "Human activities have had a significant impact on the environment...", status: "disagree" }
    ],
    summary: "Based on the analyzed sources, there is strong evidence supporting climate change..."
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsLoading(true);
    
    // In a real application, this would be an API call
    setTimeout(() => {
      setMessages([...messages, 
        { type: 'user', content: input },
        { type: 'system', content: mockResponse }
      ]);
      setInput('');
      setIsLoading(false);
    }, 1000);
  };

  const ArticleDropdown = ({ article }) => {
    const [isOpen, setIsOpen] = useState(false);
    
    const getBorderColor = (status) => {
      switch(status) {
        case 'agree': return 'border-green-500';
        case 'disagree': return 'border-red-500';
        case 'unrelated': return 'border-orange-500';
        default: return 'border-gray-300';
      }
    };

    return (
      <div className={`mb-2 border-2 rounded-lg p-3 ${getBorderColor(article.status)}`}>
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
        <div className="flex gap-2 max-w-3xl mx-auto">
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
  );
};

export default TruthScope;