export default function IngestionPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Ingestion Status</h1>
        <button className="bg-dgPrimary text-white px-4 py-2 rounded">Trigger Sync</button>
      </div>

      <div className="bg-white rounded shadow overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-100 border-b">
              <th className="p-4">Source</th>
              <th className="p-4">Status</th>
              <th className="p-4">Success Rate</th>
              <th className="p-4">Unprocessed</th>
              <th className="p-4">Last Run</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b">
              <td className="p-4">Delhi Traffic Police API</td>
              <td className="p-4"><span className="text-green-600 font-medium">Success</span></td>
              <td className="p-4">99.9%</td>
              <td className="p-4">0</td>
              <td className="p-4">10 mins ago</td>
            </tr>
            <tr className="border-b">
              <td className="p-4">Mumbai BMC Data</td>
              <td className="p-4"><span className="text-yellow-600 font-medium">Running</span></td>
              <td className="p-4">95.2%</td>
              <td className="p-4">1,240</td>
              <td className="p-4">In Progress</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
