import React, { useState, useEffect } from 'react';

export default function StatusBar() {
  const [stats, setStats] = useState({
    deviceCount: 0,
    threatCount: 0,
    responseTime: '0ms',
    systemStatus: 'Active'
  });

  useEffect(() => {
    const updateStats = () => {
      setStats({
        deviceCount: Math.floor(Math.random() * 100) + 50,
        threatCount: Math.floor(Math.random() * 10),
        responseTime: Math.floor(Math.random() * 50) + 10 + 'ms',
        systemStatus: 'Active'
      });
    };

    updateStats();
    const interval = setInterval(updateStats, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 mb-8 flex flex-wrap justify-around gap-6">
      <div className="text-center text-white">
        <span className="block text-2xl font-bold">{stats.deviceCount}</span>
        <span className="text-sm opacity-80">Devices Monitored</span>
      </div>
      <div className="text-center text-white">
        <span className="block text-2xl font-bold">{stats.threatCount}</span>
        <span className="text-sm opacity-80">Threats Detected</span>
      </div>
      <div className="text-center text-white">
        <span className="block text-2xl font-bold">{stats.responseTime}</span>
        <span className="text-sm opacity-80">Avg Response Time</span>
      </div>
      <div className="text-center text-white">
        <span className="block text-2xl font-bold">{stats.systemStatus}</span>
        <span className="text-sm opacity-80">System Status</span>
      </div>
    </div>
  );
}
