import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [cpuData, setCpuData] = useState([]);
  const [validatorStatus, setValidatorStatus] = useState('online');

  useEffect(() => {
    // Simulate real-time CPU data
    const interval = setInterval(() => {
      setCpuData(prev => [...prev.slice(-50), {
        timestamp: Date.now(),
        cpu: Math.random() * 100,
        memory: Math.random() * 100
      }]);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>NeuroSei Validator Dashboard</h1>
        <div className="status-indicator">
          Status: <span className={`status ${validatorStatus}`}>{validatorStatus}</span>
        </div>
      </header>
      
      <main>
        <div className="metrics-grid">
          <div className="metric-card">
            <h3>CPU Usage</h3>
            <div className="chart">
              {cpuData.map((point, i) => (
                <div 
                  key={i}
                  className="bar"
                  style={{ height: `${point.cpu}%` }}
                />
              ))}
            </div>
          </div>
          
          <div className="metric-card">
            <h3>Memory Usage</h3>
            <div className="chart">
              {cpuData.map((point, i) => (
                <div 
                  key={i}
                  className="bar"
                  style={{ height: `${point.memory}%` }}
                />
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App; 