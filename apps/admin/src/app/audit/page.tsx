import AuditDiff from '@/components/AuditDiff';

export default function AuditLogPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Audit Log</h1>
      
      <div className="bg-white rounded shadow p-4 mb-4">
        <input type="text" placeholder="Search logs..." className="w-full p-2 border rounded" />
      </div>

      <div className="bg-white rounded shadow overflow-hidden">
        <div className="p-4 border-b">
          <h3 className="font-semibold">Update Speed Limit (ID: req_8x92)</h3>
          <p className="text-sm text-gray-500">By Admin User at 2026-08-11 10:14:00</p>
          <div className="mt-4">
            <AuditDiff 
              before={{ speedLimit: 40, status: 'active' }} 
              after={{ speedLimit: 60, status: 'active' }} 
            />
          </div>
        </div>
      </div>
    </div>
  );
}
