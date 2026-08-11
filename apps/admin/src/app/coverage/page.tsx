'use client';
import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, CartesianGrid, Legend } from 'recharts';
import CoverageCard from '@/components/CoverageCard';
import { api } from '@/lib/api';
import { CoverageMetrics } from '@/lib/types';

const COLORS = ['#10B981', '#F59E0B', '#EF4444'];

export default function CoveragePage() {
  const [metrics, setMetrics] = useState<CoverageMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getCoverageMetrics()
      .then(setMetrics)
      .catch(() => {
        // Fallback to mock data
        setMetrics({
          roadNetworkPercent: 88,
          speedLimitPercent: 76,
          signalPercent: 92,
          cameraCounts: { verified: 12450, probable: 3120, needsReview: 840 },
          tempOrdersStats: { active: 145, expired: 3020 }
        });
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading || !metrics) {
    return <div className="p-8 dark:text-white">Loading coverage metrics...</div>;
  }

  const cameraData = [
    { name: 'Verified', value: metrics.cameraCounts.verified },
    { name: 'Probable', value: metrics.cameraCounts.probable },
    { name: 'Reported', value: metrics.cameraCounts.needsReview },
  ];

  const timelineData = [
    { month: 'Jan', active: 40, expired: 120 },
    { month: 'Feb', active: 65, expired: 150 },
    { month: 'Mar', active: 80, expired: 200 },
    { month: 'Apr', active: 110, expired: 250 },
    { month: 'May', active: 145, expired: 310 },
  ];

  return (
    <div className="space-y-6 dark:bg-gray-900 dark:text-white p-6 rounded-lg min-h-full">
      <h1 className="text-2xl font-bold">Data Coverage Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <CoverageCard title="Road Network" value={`${metrics.roadNetworkPercent}%`} description="Major cities mapped" />
        <CoverageCard title="Speed Limits" value={`${metrics.speedLimitPercent}%`} description="Coverage of known roads" />
        <CoverageCard title="Traffic Signals" value={`${metrics.signalPercent}%`} description="Verified signal locations" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <div className="bg-white dark:bg-gray-800 rounded shadow p-6 border dark:border-gray-700">
          <h2 className="text-xl font-semibold mb-4">Camera Counts by Status</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={cameraData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                  {cameraData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded shadow p-6 border dark:border-gray-700">
          <h2 className="text-xl font-semibold mb-4">Temporary Restrictions Timeline</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="month" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <RechartsTooltip contentStyle={{ backgroundColor: '#1F2937', border: 'none', color: '#fff' }} />
                <Legend />
                <Line type="monotone" dataKey="active" stroke="#F59E0B" strokeWidth={2} />
                <Line type="monotone" dataKey="expired" stroke="#6B7280" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
