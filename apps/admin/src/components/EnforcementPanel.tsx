export default function EnforcementPanel() {
  return (
    <div className="w-80 bg-white border-l shadow-lg h-full p-4 overflow-y-auto">
      <h2 className="text-xl font-bold mb-4">Edit Point</h2>
      <form className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Type</label>
          <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border">
            <option>Speed Camera</option>
            <option>Red Light Camera</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Status</label>
          <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border">
            <option>Verified</option>
            <option>Needs Review</option>
          </select>
        </div>
        <button type="button" className="w-full bg-dgPrimary text-white py-2 rounded">
          Save Changes
        </button>
      </form>
    </div>
  );
}
