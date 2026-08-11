'use client';
import { useEffect, useRef } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

export default function AdminMap() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (map.current || !mapContainer.current) return;
    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: 'https://demotiles.maplibre.org/style.json', // Placeholder style
      center: [78.9629, 20.5937], // Center of India
      zoom: 4,
    });
    
    map.current.addControl(new maplibregl.NavigationControl(), 'top-right');
  }, []);

  return (
    <div className="absolute inset-0 w-full h-full">
      <div ref={mapContainer} className="w-full h-full" />
      <div className="absolute top-4 left-4 bg-white p-4 rounded shadow-md z-10 w-64">
        <h3 className="font-semibold mb-2">Filters</h3>
        <label className="flex items-center space-x-2 text-sm">
          <input type="checkbox" defaultChecked />
          <span>Verified Cameras</span>
        </label>
        <label className="flex items-center space-x-2 text-sm mt-2">
          <input type="checkbox" defaultChecked />
          <span>Needs Review</span>
        </label>
      </div>
    </div>
  );
}
