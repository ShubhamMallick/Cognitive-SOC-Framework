import React from 'react';

export default function RangeSlider({ 
  label, 
  name, 
  min, 
  max, 
  step, 
  value, 
  onChange,
  unit = '' 
}) {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      <div className="flex items-center gap-4">
        <input
          type="range"
          name={name}
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(name, e.target.value)}
          className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(to right, #007BFF 0%, #007BFF ${((value - min) / (max - min)) * 100}%, #e5e7eb ${((value - min) / (max - min)) * 100}%, #e5e7eb 100%)`
          }}
        />
        <span className="min-w-[60px] text-center font-bold text-health-blue bg-health-light px-3 py-1 rounded">
          {value}{unit}
        </span>
      </div>
    </div>
  );
}
