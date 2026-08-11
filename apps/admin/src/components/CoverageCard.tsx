export default function CoverageCard({ title, value, description }: { title: string, value: string, description: string }) {
  return (
    <div className="bg-white p-6 rounded shadow border-l-4 border-dgPrimary">
      <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider">{title}</h3>
      <div className="mt-2 text-3xl font-bold text-gray-900">{value}</div>
      <p className="mt-1 text-sm text-gray-600">{description}</p>
    </div>
  );
}
