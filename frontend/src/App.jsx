import React, { useState } from 'react';
import RangeSlider from './components/RangeSlider';
import StatusBar from './components/StatusBar';

export default function App() {
  const [formData, setFormData] = useState({
    device_id: 'D493',
    device_type: 'mri',
    department: 'ICU',
    criticality_level: 3,
    firmware_version: 'v3.2',
    cpu_usage_percent: 40,
    memory_usage_percent: 50,
    disk_write_mb_per_min: 50,
    disk_read_mb_per_min: 80,
    process_spawn_count: 10,
    file_rename_count: 5,
    new_file_creation_count: 10,
    file_entropy_avg: 5.5,
    encrypted_extension_ratio: 0.0,
    outbound_traffic_mb: 20,
    inbound_traffic_mb: 40,
    unique_external_ips: 1,
    dns_request_count: 10,
    unusual_port_flag: 0,
    privilege_escalation_flag: 0,
    configuration_change_flag: 0,
    antivirus_alert_flag: 0,
    failed_auth_attempts: 0
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleInputChange = (name, value) => {
    const numValue = name.includes('flag') || name.includes('level') || name.includes('percent') || name.includes('count') || name.includes('ratio') || name.includes('entropy') || name.includes('mb') ? 
      parseFloat(value) : value;
    
    setFormData(prev => ({
      ...prev,
      [name]: numValue
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      const analysisResult = await response.json();
      setResult(analysisResult);
      
      // Show success message
      console.log('Analysis result:', analysisResult);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatValue = (value, name) => {
    if (name.includes('flag')) {
      return value === 1 ? 'Yes' : 'No';
    } else if (name.includes('percent')) {
      return value + '%';
    } else if (name === 'encrypted_extension_ratio') {
      return parseFloat(value).toFixed(2);
    } else if (name === 'file_entropy_avg') {
      return parseFloat(value).toFixed(1);
    }
    return value;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 p-5">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center text-white mb-8 animate-fade-in-down">
          <h1 className="text-4xl font-bold mb-3 flex items-center justify-center gap-3">
            <i className="fas fa-shield-alt"></i>
            Cognitive SOC Framework
          </h1>
          <p className="text-xl opacity-90">
            AI-Powered Healthcare IoT Security Operations Center
          </p>
        </header>

        <StatusBar />

        {/* Main Form Container */}
        <div className="bg-white/95 backdrop-blur-lg rounded-3xl p-8 shadow-2xl animate-fade-in-up">
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8 mb-8">
              
              {/* Device Context Section */}
              <div className="bg-health-gray p-6 rounded-xl border-l-4 border-health-blue hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <h3 className="text-health-blue text-xl font-semibold mb-5 flex items-center gap-3">
                  <i className="fas fa-microchip text-lg"></i>
                  Device Context
                </h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Device ID
                    </label>
                    <input
                      type="text"
                      value={formData.device_id}
                      onChange={(e) => handleInputChange('device_id', e.target.value)}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-health-blue focus:ring-3 focus:ring-health-blue/20 transition-all duration-300"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Device Type
                    </label>
                    <select
                      value={formData.device_type}
                      onChange={(e) => handleInputChange('device_type', e.target.value)}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-health-blue focus:ring-3 focus:ring-health-blue/20 transition-all duration-300"
                      required
                    >
                      <option value="mri">MRI Scanner</option>
                      <option value="ct">CT Scanner</option>
                      <option value="ultrasound">Ultrasound Machine</option>
                      <option value="ventilator">Ventilator</option>
                      <option value="infusion_pump">Infusion Pump</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Department
                    </label>
                    <select
                      value={formData.department}
                      onChange={(e) => handleInputChange('department', e.target.value)}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-health-blue focus:ring-3 focus:ring-health-blue/20 transition-all duration-300"
                      required
                    >
                      <option value="ICU">Intensive Care Unit</option>
                      <option value="ER">Emergency Room</option>
                      <option value="Radiology">Radiology</option>
                      <option value="Surgery">Surgery</option>
                      <option value="Pediatrics">Pediatrics</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Firmware Version
                    </label>
                    <select
                      value={formData.firmware_version}
                      onChange={(e) => handleInputChange('firmware_version', e.target.value)}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-health-blue focus:ring-3 focus:ring-health-blue/20 transition-all duration-300"
                      required
                    >
                      <option value="v3.2">v3.2 (Latest)</option>
                      <option value="v3.1">v3.1</option>
                      <option value="v3.0">v3.0</option>
                      <option value="v2.0">v2.0</option>
                    </select>
                  </div>

                  <RangeSlider
                    label="Criticality Level"
                    name="criticality_level"
                    min={1}
                    max={5}
                    value={formData.criticality_level}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              {/* System Metrics Section */}
              <div className="bg-health-gray p-6 rounded-xl border-l-4 border-health-blue hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <h3 className="text-health-blue text-xl font-semibold mb-5 flex items-center gap-3">
                  <i className="fas fa-tachometer-alt text-lg"></i>
                  System Metrics
                </h3>
                
                <div className="space-y-4">
                  <RangeSlider
                    label="CPU Usage %"
                    name="cpu_usage_percent"
                    min={0}
                    max={100}
                    value={formData.cpu_usage_percent}
                    onChange={handleInputChange}
                    unit="%"
                  />

                  <RangeSlider
                    label="Memory Usage %"
                    name="memory_usage_percent"
                    min={0}
                    max={100}
                    value={formData.memory_usage_percent}
                    onChange={handleInputChange}
                    unit="%"
                  />

                  <RangeSlider
                    label="Disk Write MB/min"
                    name="disk_write_mb_per_min"
                    min={0}
                    max={1500}
                    value={formData.disk_write_mb_per_min}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="Disk Read MB/min"
                    name="disk_read_mb_per_min"
                    min={0}
                    max={300}
                    value={formData.disk_read_mb_per_min}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="Process Spawn Count"
                    name="process_spawn_count"
                    min={0}
                    max={100}
                    value={formData.process_spawn_count}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              {/* File System Metrics Section */}
              <div className="bg-health-gray p-6 rounded-xl border-l-4 border-health-blue hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <h3 className="text-health-blue text-xl font-semibold mb-5 flex items-center gap-3">
                  <i className="fas fa-file-alt text-lg"></i>
                  File System Metrics
                </h3>
                
                <div className="space-y-4">
                  <RangeSlider
                    label="File Rename Count"
                    name="file_rename_count"
                    min={0}
                    max={2000}
                    value={formData.file_rename_count}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="New File Creation Count"
                    name="new_file_creation_count"
                    min={0}
                    max={1000}
                    value={formData.new_file_creation_count}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="File Entropy Avg"
                    name="file_entropy_avg"
                    min={0}
                    max={8}
                    step={0.1}
                    value={formData.file_entropy_avg}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="Encrypted Extension Ratio"
                    name="encrypted_extension_ratio"
                    min={0}
                    max={1}
                    step={0.01}
                    value={formData.encrypted_extension_ratio}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              {/* Network Metrics Section */}
              <div className="bg-health-gray p-6 rounded-xl border-l-4 border-health-blue hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <h3 className="text-health-blue text-xl font-semibold mb-5 flex items-center gap-3">
                  <i className="fas fa-network-wired text-lg"></i>
                  Network Metrics
                </h3>
                
                <div className="space-y-4">
                  <RangeSlider
                    label="Outbound Traffic MB"
                    name="outbound_traffic_mb"
                    min={0}
                    max={1000}
                    value={formData.outbound_traffic_mb}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="Inbound Traffic MB"
                    name="inbound_traffic_mb"
                    min={0}
                    max={200}
                    value={formData.inbound_traffic_mb}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="Unique External IPs"
                    name="unique_external_ips"
                    min={0}
                    max={50}
                    value={formData.unique_external_ips}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="DNS Request Count"
                    name="dns_request_count"
                    min={0}
                    max={200}
                    value={formData.dns_request_count}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="Unusual Port Activity"
                    name="unusual_port_flag"
                    min={0}
                    max={1}
                    value={formData.unusual_port_flag}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              {/* Security Signals Section */}
              <div className="bg-health-gray p-6 rounded-xl border-l-4 border-health-blue hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <h3 className="text-health-blue text-xl font-semibold mb-5 flex items-center gap-3">
                  <i className="fas fa-shield-alt text-lg"></i>
                  Security Signals
                </h3>
                
                <div className="space-y-4">
                  <RangeSlider
                    label="Privilege Escalation"
                    name="privilege_escalation_flag"
                    min={0}
                    max={1}
                    value={formData.privilege_escalation_flag}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="Configuration Change"
                    name="configuration_change_flag"
                    min={0}
                    max={1}
                    value={formData.configuration_change_flag}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="Antivirus Alert"
                    name="antivirus_alert_flag"
                    min={0}
                    max={1}
                    value={formData.antivirus_alert_flag}
                    onChange={handleInputChange}
                  />

                  <RangeSlider
                    label="Failed Auth Attempts"
                    name="failed_auth_attempts"
                    min={0}
                    max={20}
                    value={formData.failed_auth_attempts}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

            </div>

            {/* Submit Button */}
            <div className="text-center mt-8">
              <button
                type="submit"
                disabled={loading}
                className="bg-gradient-to-r from-health-blue to-health-dark text-white px-12 py-4 text-lg font-semibold rounded-full hover:shadow-xl hover:-translate-y-1 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <i className="fas fa-spinner fa-spin mr-3"></i>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <i className="fas fa-search mr-3"></i>
                    Analyze Device Security
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Loading State */}
          {loading && (
            <div className="text-center mt-6">
              <div className="inline-block animate-spin rounded-full h-10 w-10 border-4 border-gray-200 border-t-health-blue"></div>
              <p className="mt-3 text-gray-600">Analyzing device security...</p>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="mt-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
              <p className="text-red-700 font-medium">Error: {error}</p>
            </div>
          )}

          {/* Success State */}
          {result && (
            <div className="mt-6 bg-green-50 border-l-4 border-green-500 p-4 rounded-lg">
              <h3 className="text-green-700 font-semibold mb-2">Analysis Complete!</h3>
              <div className="text-green-600">
                <p><strong>Anomaly Probability:</strong> {result.detection?.anomaly_probability?.toFixed(4) || 'N/A'}</p>
                <p><strong>Decision:</strong> {result.detection?.decision || 'N/A'}</p>
                <p><strong>Uncertainty Score:</strong> {result.detection?.uncertainty_score?.toFixed(4) || 'N/A'}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
