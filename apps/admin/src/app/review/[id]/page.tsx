import ReviewForm from '@/components/ReviewForm';

export default function ReviewDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Review Item: {params.id}</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Location Context</h2>
          <div className="bg-gray-200 h-64 rounded flex items-center justify-center text-gray-500 mb-4">
            Map Placeholder
          </div>
          <h3 className="font-semibold mb-2">Evidence & Comparison</h3>
          <p className="text-sm text-gray-600">Proposed value: 60 km/h</p>
          <p className="text-sm text-gray-600">Existing value: 40 km/h</p>
        </div>
        
        <div className="bg-white rounded shadow p-6">
          <ReviewForm itemId={params.id} />
        </div>
      </div>
    </div>
  );
}
