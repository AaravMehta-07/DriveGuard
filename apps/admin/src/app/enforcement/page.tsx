import AdminMap from '@/components/map/AdminMap';

export default function EnforcementMapPage() {
  return (
    <div className="h-full flex flex-col">
      <h1 className="text-2xl font-bold mb-4">Enforcement Map</h1>
      <div className="flex-1 bg-gray-200 rounded overflow-hidden shadow relative">
        <AdminMap />
      </div>
    </div>
  );
}
