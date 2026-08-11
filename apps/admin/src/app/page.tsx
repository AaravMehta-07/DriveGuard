import CoverageCard from '@/components/CoverageCard';

export default function DashboardHome() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <CoverageCard title="System Health" value="Optimal" description="All services running normally" />
        <CoverageCard title="Review Queue" value="142" description="Items pending review" />
        <CoverageCard title="Data Coverage" value="84%" description="Overall mapped area" />
        <CoverageCard title="Recent Activity" value="2,401" description="Updates in last 24h" />
      </div>

      <div className="bg-white rounded shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
        <div className="flex gap-4">
          <button className="bg-dgPrimary text-white px-4 py-2 rounded">Go to Review Queue</button>
          <button className="bg-dgSecondary text-white px-4 py-2 rounded">View Active Map</button>
        </div>
      </div>
    </div>
  );
}
