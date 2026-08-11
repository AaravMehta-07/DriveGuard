export default function FieldVerificationPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Field Verification</h1>
        <button className="bg-dgPrimary text-white px-4 py-2 rounded">Generate Tasks</button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded shadow p-4">
          <h2 className="text-xl font-semibold mb-4">Pending Verifications</h2>
          <ul className="space-y-2">
            <li className="p-3 bg-gray-50 rounded border">Task #4021 - Camera disputed at MG Road</li>
            <li className="p-3 bg-gray-50 rounded border">Task #4022 - Speed limit change on NH44</li>
          </ul>
        </div>
        <div className="bg-white rounded shadow p-4">
          <h2 className="text-xl font-semibold mb-4">Recently Submitted</h2>
          <ul className="space-y-2">
            <li className="p-3 bg-green-50 rounded border border-green-200 text-green-800">Task #4010 - Confirmed 60km/h</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
